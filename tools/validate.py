"""Static validator for the generated datapack (Minecraft Java 26.3).

Parses every command against the official brigadier command tree
(mcdata/commands_data.json from misode/mcmeta 26.3-summary) and checks
block / item / entity / particle / sound ids, block states, selectors,
SNBT syntax, text components and function references.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "mcdata")
TREE = json.load(open(os.path.join(D, "commands_data.json")))
REG = json.load(open(os.path.join(D, "registries_data.json")))
BLOCKS = json.load(open(os.path.join(D, "blocks_data.json")))

PACK = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "datapack", "rufu_kekkon")

ITEMS = set(REG["item"])
ENTITIES = set(REG["entity_type"])
PARTICLES = set(REG["particle_type"])
SOUNDS = set(REG["sound_event"])
EFFECTS = set(REG["mob_effect"])
ATTRS = set(REG["attribute"])
COMPONENTS = set(REG["data_component_type"])
BLOCK_TAGS = set(REG.get("tag/block", []))
ITEM_TAGS = set(REG.get("tag/item", []))
ENTITY_TAGS = set(REG.get("tag/entity_type", []))
COLORS = {"black", "dark_blue", "dark_green", "dark_aqua", "dark_red", "dark_purple", "gold", "gray", "dark_gray", "blue",
          "green", "aqua", "red", "light_purple", "yellow", "white", "reset"}
TEXT_KEYS = {"text", "color", "bold", "italic", "underlined", "strikethrough", "obfuscated", "extra", "score", "selector",
             "storage", "nbt", "interpret", "click_event", "hover_event", "translate", "with", "keybind", "font",
             "insertion", "shadow_color", "separator", "entity", "block", "type", "fallback", "plain", "object", "sprite",
             "atlas", "player", "hat"}

errors = []
warnings = []
functions = set()
objectives = set()
predicates = set()


def strip_ns(i):
    return i[10:] if i.startswith("minecraft:") else i


class PErr(Exception):
    pass


# ====================================================================== SNBT
WORD = re.compile(r"[0-9A-Za-z_\-.+]+")
NUM = re.compile(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?[bBsSlLfFdD]?$")


def skip_ws(s, i):
    while i < len(s) and s[i] in " \t":
        i += 1
    return i


def snbt(s, i):
    """parse SNBT value at s[i]; returns (value, end)"""
    i = skip_ws(s, i)
    if i >= len(s):
        raise PErr("unexpected end in SNBT")
    c = s[i]
    if c == "{":
        i += 1
        out = {}
        i = skip_ws(s, i)
        if i < len(s) and s[i] == "}":
            return out, i + 1
        while True:
            i = skip_ws(s, i)
            if s[i] in "\"'":
                k, i = qstr(s, i)
            else:
                m = WORD.match(s, i)
                if not m:
                    raise PErr(f"bad compound key at {s[i:i + 20]!r}")
                k = m.group(0)
                i = m.end()
            i = skip_ws(s, i)
            if i >= len(s) or s[i] != ":":
                raise PErr(f"expected ':' after key {k!r}")
            v, i = snbt(s, i + 1)
            out[k] = v
            i = skip_ws(s, i)
            if i < len(s) and s[i] == ",":
                i += 1
                continue
            if i < len(s) and s[i] == "}":
                return out, i + 1
            raise PErr(f"expected , or }} near {s[i:i + 20]!r}")
    if c == "[":
        i += 1
        if s[i:i + 2] in ("I;", "B;", "L;"):
            i += 2
        out = []
        i = skip_ws(s, i)
        if i < len(s) and s[i] == "]":
            return out, i + 1
        while True:
            v, i = snbt(s, i)
            out.append(v)
            i = skip_ws(s, i)
            if i < len(s) and s[i] == ",":
                i += 1
                continue
            if i < len(s) and s[i] == "]":
                return out, i + 1
            raise PErr(f"expected , or ] near {s[i:i + 20]!r}")
    if c in "\"'":
        return qstr(s, i)
    m = re.compile(r"[0-9A-Za-z_\-.+]+").match(s, i)
    if not m:
        raise PErr(f"bad SNBT value at {s[i:i + 20]!r}")
    w = m.group(0)
    if w in ("true", "false"):
        return w == "true", m.end()
    if NUM.match(w):
        return Num(w), m.end()
    return w, m.end()


class Num(str):
    pass


def qstr(s, i):
    qc = s[i]
    i += 1
    out = []
    while i < len(s):
        c = s[i]
        if c == "\\":
            out.append(s[i + 1])
            i += 2
            continue
        if c == qc:
            return "".join(out), i + 1
        out.append(c)
        i += 1
    raise PErr("unterminated string")


# ====================================================================== text components
def check_text(v, where):
    if isinstance(v, str):
        return
    if isinstance(v, list):
        for x in v:
            check_text(x, where)
        return
    if isinstance(v, (bool, Num)):
        return
    if not isinstance(v, dict):
        raise PErr(f"bad text component in {where}")
    for k in v:
        if k not in TEXT_KEYS:
            raise PErr(f"unknown text component key {k!r} in {where}")
    if "clickEvent" in v or "hoverEvent" in v:
        raise PErr("old style clickEvent/hoverEvent")
    if "color" in v:
        col = v["color"]
        if not (col in COLORS or re.fullmatch(r"#[0-9a-fA-F]{6}", col)):
            raise PErr(f"bad color {col!r}")
    if "extra" in v:
        check_text(v["extra"], where)
    if "click_event" in v:
        ce = v["click_event"]
        if ce.get("action") == "run_command" and "command" not in ce:
            raise PErr("click_event run_command needs 'command'")
        if ce.get("action") == "run_command":
            cmd = ce["command"]
            if cmd.startswith("/"):
                cmd = cmd[1:]
            if "$(" not in cmd:
                check_command(cmd, where + " (click_event)")
    if "hover_event" in v:
        he = v["hover_event"]
        if he.get("action") == "show_text":
            if "value" not in he:
                raise PErr("hover_event show_text needs 'value'")
            check_text(he["value"], where)
    if "score" in v:
        sc = v["score"]
        if "name" not in sc or "objective" not in sc:
            raise PErr("score component needs name+objective")


# ====================================================================== argument parsers
def read_until_space(s, i):
    j = i
    depth = 0
    q = None
    while j < len(s):
        c = s[j]
        if q:
            if c == "\\":
                j += 2
                continue
            if c == q:
                q = None
        elif c in "\"'":
            q = c
        elif c in "[{(":
            depth += 1
        elif c in "]})":
            depth -= 1
        elif c == " " and depth <= 0:
            break
        j += 1
    return s[i:j], j


def p_number(s, i, props, kind):
    tok, j = read_until_space(s, i)
    pat = r"[-+]?\d+" if kind in ("integer", "long") else r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?"
    if not re.fullmatch(pat, tok):
        raise PErr(f"expected {kind}, got {tok!r}")
    v = float(tok)
    if "min" in props and v < props["min"]:
        raise PErr(f"{tok} below min {props['min']}")
    if "max" in props and v > props["max"]:
        raise PErr(f"{tok} above max {props['max']}")
    return j


def coord(tok, integer):
    if tok.startswith("^") or tok.startswith("~"):
        rest = tok[1:]
        if rest and not re.fullmatch(r"[-+]?(?:\d+\.?\d*|\.\d+)", rest):
            raise PErr(f"bad relative coord {tok!r}")
        return tok[0]
    if integer:
        if not re.fullmatch(r"[-+]?\d+", tok):
            raise PErr(f"block position must be integer: {tok!r}")
    elif not re.fullmatch(r"[-+]?(?:\d+\.?\d*|\.\d+)", tok):
        raise PErr(f"bad coord {tok!r}")
    return "a"


def p_coords(s, i, n, integer=False, allow_local=True):
    kinds = []
    for k in range(n):
        if k:
            if i >= len(s) or s[i] != " ":
                raise PErr("expected more coordinates")
            i += 1
        tok, i = read_until_space(s, i)
        kinds.append(coord(tok, integer))
    if "^" in kinds and any(k != "^" for k in kinds):
        raise PErr("cannot mix local and world coordinates")
    if "^" in kinds and not allow_local:
        raise PErr("local coordinates not allowed")
    return i


def parse_id(s, i):
    m = re.compile(r"#?[a-z0-9_\-.]+(?::[a-z0-9_\-./]+)?").match(s, i)
    if not m:
        raise PErr(f"expected id at {s[i:i + 20]!r}")
    return m.group(0), m.end()


def p_block(s, i, predicate=False):
    bid_, i = parse_id(s, i)
    if bid_.startswith("#"):
        if not predicate:
            raise PErr("block tag not allowed here")
        if strip_ns(bid_[1:]) not in BLOCK_TAGS:
            raise PErr(f"unknown block tag {bid_}")
        b = None
    else:
        b = strip_ns(bid_)
        if b not in BLOCKS:
            raise PErr(f"unknown block {bid_}")
    if i < len(s) and s[i] == "[":
        j = s.index("]", i)
        body = s[i + 1:j]
        if b:
            props = BLOCKS[b][0]
            for kv in filter(None, body.split(",")):
                k, _, v = kv.partition("=")
                k, v = k.strip(), v.strip()
                if k not in props:
                    raise PErr(f"block {b} has no property {k!r}")
                if v not in props[k]:
                    raise PErr(f"block {b} property {k} has no value {v!r}")
        i = j + 1
    if i < len(s) and s[i] == "{":
        _, i = snbt(s, i)
    return i


def p_item(s, i, predicate=False):
    if predicate and s[i] == "*":
        i += 1
    else:
        iid, i = parse_id(s, i)
        if iid.startswith("#"):
            if not predicate:
                raise PErr("item tag not allowed here")
            if strip_ns(iid[1:]) not in ITEM_TAGS:
                raise PErr(f"unknown item tag {iid}")
        elif strip_ns(iid) not in ITEMS:
            raise PErr(f"unknown item {iid}")
    if i < len(s) and s[i] == "[":
        i += 1
        while True:
            i = skip_ws(s, i)
            if s[i] == "]":
                i += 1
                break
            neg = False
            if s[i] == "!":
                neg = True
                i += 1
            cid, i = parse_id(s, i)
            if strip_ns(cid) not in COMPONENTS and not predicate:
                raise PErr(f"unknown item component {cid}")
            if predicate and strip_ns(cid) not in COMPONENTS and strip_ns(cid) not in ("count", "damage", "enchantments", "custom_data", "stored_enchantments", "potion_contents", "jukebox_playable", "trim", "writable_book_content", "written_book_content", "fireworks", "firework_explosion", "bundle_contents", "container", "attribute_modifiers", "villager/variant"):
                raise PErr(f"unknown item predicate {cid}")
            i = skip_ws(s, i)
            if s[i] in "=~":
                v, i = snbt(s, i + 1)
                if strip_ns(cid) == "custom_name" or strip_ns(cid) == "item_name":
                    check_text(v, "item name")
                if strip_ns(cid) == "lore":
                    check_text(v, "lore")
            i = skip_ws(s, i)
            if s[i] in ",|":
                i += 1
                continue
            if s[i] == "]":
                i += 1
                break
            raise PErr(f"bad item components near {s[i:i + 20]!r}")
    if i < len(s) and s[i] == "{":
        raise PErr("item NBT braces are not allowed (use components)")
    return i


SEL_KEYS = {"x", "y", "z", "dx", "dy", "dz", "distance", "scores", "tag", "team", "limit", "sort", "level", "gamemode",
            "name", "x_rotation", "y_rotation", "type", "nbt", "advancements", "predicate"}


def p_selector(s, i, props):
    if s[i] != "@":
        tok, j = read_until_space(s, i)
        if not tok or len(tok) > 40:
            raise PErr(f"bad entity/player name {tok!r}")
        return j
    kind = s[i + 1]
    if kind not in "aeprsn":
        raise PErr(f"bad selector @{kind}")
    i += 2
    args = {}
    if i < len(s) and s[i] == "[":
        i += 1
        while True:
            i = skip_ws(s, i)
            if s[i] == "]":
                i += 1
                break
            m = WORD.match(s, i)
            if not m:
                raise PErr(f"bad selector key at {s[i:i + 20]!r}")
            k = m.group(0)
            if k not in SEL_KEYS:
                raise PErr(f"unknown selector argument {k!r}")
            i = m.end()
            if s[i] != "=":
                raise PErr("expected = in selector")
            i += 1
            neg = s[i] == "!"
            if neg:
                i += 1
            if k in ("scores", "advancements"):
                depth = 0
                j = i
                while True:
                    if s[j] == "{":
                        depth += 1
                    elif s[j] == "}":
                        depth -= 1
                        if depth == 0:
                            break
                    j += 1
                val = s[i:j + 1]
                for part in filter(None, val[1:-1].split(",")):
                    obj, _, rng = part.partition("=")
                    objectives_used.add(obj)
                    if not re.fullmatch(r"-?\d*(\.\.)?-?\d*", rng) or rng in ("", ".."):
                        raise PErr(f"bad score range {rng!r}")
                i = j + 1
            elif k == "nbt":
                _, i = snbt(s, i)
            else:
                m = re.compile(r"[^,\]]*").match(s, i)
                val = m.group(0)
                i = m.end()
                if k == "type":
                    t = val
                    if t.startswith("#"):
                        if strip_ns(t[1:]) not in ENTITY_TAGS:
                            raise PErr(f"unknown entity tag {t}")
                    elif strip_ns(t) not in ENTITIES:
                        raise PErr(f"unknown entity type {t}")
                if k in ("x", "y", "z", "dx", "dy", "dz"):
                    float(val)
                if k == "limit":
                    int(val)
                if k == "sort" and val not in ("nearest", "furthest", "random", "arbitrary"):
                    raise PErr(f"bad sort {val}")
                if k == "gamemode" and val not in ("survival", "creative", "adventure", "spectator"):
                    raise PErr(f"bad gamemode {val}")
                if k == "predicate":
                    predicates_used.add(val)
                if k in ("distance", "level", "x_rotation", "y_rotation"):
                    if not re.fullmatch(r"-?[\d.]*(\.\.)?-?[\d.]*", val):
                        raise PErr(f"bad range {val}")
                args.setdefault(k, []).append((neg, val))
            i = skip_ws(s, i)
            if s[i] == ",":
                i += 1
                continue
            if s[i] == "]":
                i += 1
                break
            raise PErr(f"bad selector near {s[i:i + 20]!r}")
    single = props.get("amount") == "single"
    players = props.get("type") == "players"
    if single and kind in "ae":
        lim = args.get("limit")
        if not lim or lim[0][1] != "1":
            raise PErr("selector must be limited to one entity (limit=1)")
    if players and kind in "en":
        t = args.get("type")
        if not t or strip_ns(t[0][1]) != "player":
            raise PErr("only players allowed here")
    return i


def p_component(s, i):
    v, j = snbt(s, i)
    check_text(v, "component")
    return j


ARG = {}


def parse_arg(parser, props, s, i):
    if parser in ("brigadier:integer", "brigadier:long"):
        return p_number(s, i, props, "integer")
    if parser in ("brigadier:float", "brigadier:double"):
        return p_number(s, i, props, "float")
    if parser == "brigadier:bool":
        tok, j = read_until_space(s, i)
        if tok not in ("true", "false"):
            raise PErr("expected bool")
        return j
    if parser == "brigadier:string":
        t = props.get("type")
        if t == "greedy":
            return len(s)
        if t == "phrase" and s[i] in "\"'":
            _, j = qstr(s, i)
            return j
        m = WORD.match(s, i)
        if not m:
            raise PErr("expected word")
        return m.end()
    if parser == "minecraft:entity":
        return p_selector(s, i, props)
    if parser == "minecraft:game_profile":
        return p_selector(s, i, {"type": "players"})
    if parser == "minecraft:score_holder":
        if s[i] == "*":
            return i + 1
        if s[i] == "@":
            return p_selector(s, i, {"amount": props.get("amount")})
        tok, j = read_until_space(s, i)
        return j
    if parser == "minecraft:block_pos":
        return p_coords(s, i, 3, integer=True)
    if parser == "minecraft:vec3":
        return p_coords(s, i, 3)
    if parser == "minecraft:vec2":
        return p_coords(s, i, 2, allow_local=False)
    if parser == "minecraft:column_pos":
        return p_coords(s, i, 2, integer=True, allow_local=False)
    if parser == "minecraft:rotation":
        return p_coords(s, i, 2, allow_local=False)
    if parser == "minecraft:block_state":
        return p_block(s, i)
    if parser == "minecraft:block_predicate":
        return p_block(s, i, predicate=True)
    if parser == "minecraft:item_stack":
        return p_item(s, i)
    if parser == "minecraft:item_predicate":
        return p_item(s, i, predicate=True)
    if parser == "minecraft:nbt_compound_tag":
        if s[i] != "{":
            raise PErr("expected compound")
        _, j = snbt(s, i)
        return j
    if parser == "minecraft:nbt_tag":
        _, j = snbt(s, i)
        return j
    if parser == "minecraft:nbt_path":
        tok, j = read_until_space(s, i)
        if not tok:
            raise PErr("empty nbt path")
        return j
    if parser == "minecraft:component":
        return p_component(s, i)
    if parser in ("minecraft:resource_location", "minecraft:resource_key", "minecraft:dimension",
                  "minecraft:loot_table", "minecraft:loot_predicate", "minecraft:loot_modifier", "minecraft:uuid",
                  "minecraft:resource_selector"):
        tok, j = read_until_space(s, i)
        if not re.fullmatch(r"[a-z0-9_\-.]+(:[a-z0-9_\-./]+)?", tok) and parser != "minecraft:uuid":
            raise PErr(f"bad resource location {tok!r}")
        return j
    if parser in ("minecraft:resource", "minecraft:resource_or_tag", "minecraft:resource_or_tag_key"):
        tok, j = read_until_space(s, i)
        reg = props.get("registry", "").replace("minecraft:", "")
        if reg in REG and not tok.startswith("#") and strip_ns(tok) not in REG[reg]:
            raise PErr(f"unknown {reg} {tok!r}")
        return j
    if parser == "minecraft:function":
        tok, j = read_until_space(s, i)
        functions_used.add(tok)
        return j
    if parser == "minecraft:time":
        tok, j = read_until_space(s, i)
        if not re.fullmatch(r"-?\d+(\.\d+)?[dst]?", tok):
            raise PErr(f"bad time {tok!r}")
        if props.get("min", -1 << 40) > float(re.sub(r"[dst]$", "", tok)):
            raise PErr(f"time below min: {tok}")
        return j
    if parser == "minecraft:objective":
        tok, j = read_until_space(s, i)
        objectives_used.add(tok)
        return j
    if parser == "minecraft:objective_criteria":
        tok, j = read_until_space(s, i)
        return j
    if parser == "minecraft:operation":
        tok, j = read_until_space(s, i)
        if tok not in ("=", "+=", "-=", "*=", "/=", "%=", "<", ">", "><"):
            raise PErr("bad operation")
        return j
    if parser in ("minecraft:color", "minecraft:team_color"):
        tok, j = read_until_space(s, i)
        if tok not in COLORS:
            raise PErr("bad color")
        return j
    if parser == "minecraft:swizzle":
        tok, j = read_until_space(s, i)
        if not re.fullmatch(r"[xyz]{1,3}", tok):
            raise PErr("bad swizzle")
        return j
    if parser == "minecraft:entity_anchor":
        tok, j = read_until_space(s, i)
        if tok not in ("eyes", "feet"):
            raise PErr("bad anchor")
        return j
    if parser in ("minecraft:int_range", "minecraft:float_range"):
        tok, j = read_until_space(s, i)
        if not re.fullmatch(r"-?[\d.]*(\.\.)?-?[\d.]*", tok) or tok in ("", ".."):
            raise PErr(f"bad range {tok!r}")
        return j
    if parser == "minecraft:gamemode":
        tok, j = read_until_space(s, i)
        if tok not in ("survival", "creative", "adventure", "spectator"):
            raise PErr("bad gamemode")
        return j
    if parser == "minecraft:message":
        return len(s)
    if parser == "minecraft:scoreboard_slot":
        tok, j = read_until_space(s, i)
        if not re.fullmatch(r"list|sidebar|below_name|sidebar\.team\.\w+", tok):
            raise PErr("bad scoreboard slot")
        return j
    if parser == "minecraft:particle":
        pid, j = parse_id(s, i)
        if strip_ns(pid) not in PARTICLES:
            raise PErr(f"unknown particle {pid}")
        if j < len(s) and s[j] == "{":
            _, j = snbt(s, j)
        return j
    if parser == "minecraft:team":
        tok, j = read_until_space(s, i)
        return j
    if parser == "minecraft:dialog":
        if s[i] == "{":
            _, j = snbt(s, i)
            return j
        tok, j = read_until_space(s, i)
        return j
    if parser in ("minecraft:style",):
        _, j = snbt(s, i)
        return j
    if parser in ("minecraft:item_slot", "minecraft:heightmap", "minecraft:template_mirror", "minecraft:template_rotation",
                  "minecraft:hex_color", "minecraft:swing_animation"):
        tok, j = read_until_space(s, i)
        return j
    if parser == "minecraft:slot_source":
        raise PErr("slot_source arguments are avoided in this pack (format uncertain)")
    raise PErr(f"unsupported parser {parser}")


def node_at(path):
    n = TREE
    for p in path:
        n = n["children"][p]
    return n


def parse_from(node, s, i, depth=0):
    """Try to parse s[i:] starting after `node`. Returns True or raises PErr with best message."""
    if i >= len(s):
        if node.get("executable"):
            return True
        raise PErr("incomplete command")
    if s[i] != " ":
        raise PErr(f"expected space at {s[i:i + 15]!r}")
    i += 1
    children = node.get("children", {})
    if "redirect" in node:
        children = node_at(node["redirect"]).get("children", {})
    elif not children and node.get("type") == "literal":
        children = TREE["children"]  # 'run' -> root
    last_err = None
    # literals first
    for name, ch in children.items():
        if ch["type"] == "literal":
            if s.startswith(name, i) and (i + len(name) == len(s) or s[i + len(name)] == " "):
                try:
                    return parse_from(ch, s, i + len(name), depth + 1)
                except PErr as e:
                    last_err = e
    for name, ch in children.items():
        if ch["type"] == "argument":
            try:
                j = parse_arg(ch["parser"], ch.get("properties", {}), s, i)
            except PErr as e:
                last_err = last_err or PErr(f"<{name}>: {e}")
                if not str(last_err).startswith("<"):
                    pass
                last_err = PErr(f"<{name}>: {e}")
                continue
            except (ValueError, IndexError) as e:
                last_err = PErr(f"<{name}>: {e}")
                continue
            try:
                return parse_from(ch, s, j, depth + 1)
            except PErr as e:
                last_err = e
    raise last_err or PErr(f"unknown command/literal at {s[i:i + 25]!r}")


def check_command(cmd, where):
    root_name, _, _ = cmd.partition(" ")
    if root_name not in TREE["children"]:
        raise PErr(f"unknown command {root_name!r}")
    node = TREE["children"][root_name]
    parse_from(node, cmd, len(root_name))
    # extra semantic checks
    m = re.match(r"playsound (\S+)", cmd)
    if m and strip_ns(m.group(1)) not in SOUNDS:
        raise PErr(f"unknown sound {m.group(1)}")
    for m in re.finditer(r"playsound (minecraft:[a-z0-9_.]+)", cmd):
        if strip_ns(m.group(1)) not in SOUNDS:
            raise PErr(f"unknown sound {m.group(1)}")
    m = re.match(r"(?:summon|execute .* run summon) (minecraft:[a-z_]+)", cmd)
    for m in re.finditer(r"summon (minecraft:[a-z_]+) (\S+ \S+ \S+) (\{.*)$", cmd):
        nbt, _ = snbt(m.group(3), 0)
        check_entity_nbt(nbt, where)
    for m in re.finditer(r"effect give \S+ (minecraft:[a-z_]+)", cmd):
        if strip_ns(m.group(1)) not in EFFECTS:
            raise PErr(f"unknown effect {m.group(1)}")


def check_entity_nbt(nbt, where):
    if not isinstance(nbt, dict):
        return
    for k in ("CustomName", "text"):
        if k in nbt:
            check_text(nbt[k], where + " " + k)
    for p in nbt.get("Passengers", []):
        if "id" not in p:
            raise PErr("passenger without id")
        if strip_ns(p["id"]) not in ENTITIES:
            raise PErr(f"unknown passenger {p['id']}")
        check_entity_nbt(p, where)
    for k in ("Item", "FireworksItem"):
        if k in nbt:
            check_itemstack(nbt[k])
    if "equipment" in nbt:
        for slot, it in nbt["equipment"].items():
            if slot not in ("mainhand", "offhand", "head", "chest", "legs", "feet", "body", "saddle"):
                raise PErr(f"bad equipment slot {slot}")
            check_itemstack(it)
    if "BlockState" in nbt:
        bs = nbt["BlockState"]
        if isinstance(bs, str):
            if strip_ns(bs) not in BLOCKS:
                raise PErr(f"unknown block {bs}")
        elif isinstance(bs, dict) and "Name" in bs:
            raise PErr("26.3 falling_block BlockState uses id/properties, not Name")
    if "attributes" in nbt:
        for a in nbt["attributes"]:
            if strip_ns(a["id"]) not in ATTRS:
                raise PErr(f"unknown attribute {a['id']}")
    if "variant" in nbt and "Type" not in nbt:
        pass


def check_itemstack(it):
    if not isinstance(it, dict):
        return
    if "id" not in it:
        raise PErr("item stack without id")
    if strip_ns(it["id"]) not in ITEMS:
        raise PErr(f"unknown item {it['id']}")
    if "Count" in it:
        raise PErr("old 'Count' in item stack")
    for c in it.get("components", {}):
        if strip_ns(c) not in COMPONENTS:
            raise PErr(f"unknown component {c}")


functions_used = set()
objectives_used = set()
predicates_used = set()


def main():
    fdir = os.path.join(PACK, "data")
    defined = set()
    lines_total = 0
    for root, _, files in os.walk(fdir):
        for f in files:
            if f.endswith(".mcfunction"):
                rel = os.path.relpath(os.path.join(root, f), fdir).replace(os.sep, "/")
                ns, _, rest = rel.partition("/function/")
                defined.add(f"{ns}:{rest[:-len('.mcfunction')]}")
            if f.endswith(".json") and "/predicate" in root.replace(os.sep, "/"):
                rel = os.path.relpath(os.path.join(root, f), fdir).replace(os.sep, "/")
                ns, _, rest = rel.partition("/predicate/")
                predicates.add(f"{ns}:{rest[:-5]}")
    declared_obj = set()
    for root, _, files in os.walk(fdir):
        for f in sorted(files):
            if not f.endswith(".mcfunction"):
                continue
            path = os.path.join(root, f)
            rel = os.path.relpath(path, fdir)
            for ln, line in enumerate(open(path, encoding="utf-8"), 1):
                line = line.rstrip("\n")
                if not line.strip() or line.startswith("#"):
                    continue
                lines_total += 1
                cmd = line
                if cmd.startswith("$"):
                    cmd = cmd[1:]
                    cmd = cmd.replace("$(id)", "3").replace("$(r)", "1").replace("$(n)", "5").replace("$(a)", "45.0").replace("$(role)", "GM")
                    if "$(" in cmd:
                        errors.append(f"{rel}:{ln}: unknown macro var in {cmd[:80]}")
                        continue
                m = re.match(r"scoreboard objectives add (\S+)", cmd)
                if m:
                    declared_obj.add(m.group(1))
                try:
                    check_command(cmd, f"{rel}:{ln}")
                except PErr as e:
                    errors.append(f"{rel}:{ln}: {e}\n      {cmd[:220]}")
                except Exception as e:  # parser bug
                    errors.append(f"{rel}:{ln}: INTERNAL {type(e).__name__}: {e}\n      {cmd[:220]}")
    for fu in sorted(functions_used):
        if fu.startswith("#"):
            continue
        if fu not in defined and "$(" not in fu:
            errors.append(f"missing function {fu}")
    for o in sorted(objectives_used - declared_obj):
        errors.append(f"objective used but never created: {o}")
    for p in sorted(predicates_used):
        if p not in predicates:
            errors.append(f"missing predicate {p}")
    # predicate json sanity
    for p in predicates:
        ns, name = p.split(":")
        j = json.load(open(os.path.join(fdir, ns, "predicate", name + ".json")))
        if "condition" in j or "type" not in j:
            errors.append(f"predicate {p}: 26.3 needs 'type' (not 'condition')")
            continue
        if "minecraft:equipment" not in j["predicate"]:
            errors.append(f"predicate {p}: 26.3 entity predicate needs 'minecraft:equipment' key")
            continue
        it = j["predicate"]["minecraft:equipment"]["mainhand"]["items"]
        for x in (it if isinstance(it, list) else [it]):
            if x.startswith("#"):
                if strip_ns(x[1:]) not in ITEM_TAGS:
                    errors.append(f"predicate {p}: unknown tag {x}")
            elif strip_ns(x) not in ITEMS:
                errors.append(f"predicate {p}: unknown item {x}")
    print(f"checked {lines_total} commands in {len(defined)} functions")
    for e in errors[:200]:
        print("ERROR", e)
    print(f"{len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
