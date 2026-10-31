"""Function registry and common helpers for the show logic."""

from mc import T, snbt, q, argb, item_components, item_arg, item_nbt, Raw, b, s_, f_, d
from layout import *  # noqa

NS = "rufu"
F = {}          # function name (without namespace) -> list of commands
EXTRA = {}      # other data files: path -> content (str)


def fn(name, *cmds):
    lst = F.setdefault(name, [])
    _add(lst, cmds)
    return f"{NS}:{name}"


def _add(lst, cmds):
    for c in cmds:
        if c is None:
            continue
        if isinstance(c, (list, tuple)):
            _add(lst, c)
        else:
            lst.append(c)


def call(name):
    return f"function {NS}:{name}"


_anon = [0]


def sub(prefix, *cmds):
    """Create an anonymous helper function and return a 'function ...' command."""
    _anon[0] += 1
    name = f"{prefix}/_{_anon[0]}"
    fn(name, *cmds)
    return call(name)


def run_block(cond, cmds, prefix="z"):
    """execute <cond> run <cmd or helper function>"""
    cmds = [c for c in _flat(cmds)]
    if len(cmds) == 1:
        return f"execute {cond} run {cmds[0]}"
    return f"execute {cond} run {sub(prefix, *cmds)}"


def _flat(x):
    out = []
    _add(out, [x])
    return out


# ---------------------------------------------------------------- scoreboard
def sset(name, v, obj="rufu"):
    return f"scoreboard players set {name} {obj} {v}"


def sadd(name, v, obj="rufu"):
    if v >= 0:
        return f"scoreboard players add {name} {obj} {v}"
    return f"scoreboard players remove {name} {obj} {-v}"


def rnd(name, lo, hi, obj="rufu"):
    return f"execute store result score {name} {obj} run random value {lo}..{hi}"


def ifs(name, rng, obj="rufu"):
    return f"if score {name} {obj} matches {rng}"


# ---------------------------------------------------------------- text helpers
P = "@a[tag=rufu_p]"          # participants
HERO = "@a[tag=rufu_hero,limit=1]"
GM = "@a[tag=rufu_gm]"
ALL = "@a"

SPEAKERS = {
    "heroine": dict(name="ヒロイン", color="light_purple", sound="entity.allay.ambient_without_item", pitch=1.25,
                    bg=argb(225, 255, 236, 246), fg="#7a1f5c"),
    "leon": dict(name="レオン", color="aqua", sound="entity.villager.trade", pitch=0.85,
                 bg=argb(225, 225, 245, 255), fg="#16425b"),
    "priest": dict(name="神父", color="gold", sound="entity.villager.ambient", pitch=0.6,
                   bg=argb(225, 255, 248, 225), fg="#5b4316"),
    "sakura": dict(name="さくら", color="#ff8fc8", sound="entity.allay.ambient_with_item", pitch=1.5,
                   bg=argb(225, 255, 230, 242), fg="#8a2353"),
    "mio": dict(name="みお", color="#7fb8ff", sound="entity.allay.ambient_with_item", pitch=1.35,
                bg=argb(225, 228, 240, 255), fg="#1f3f7a"),
    "hinata": dict(name="ひなた", color="#ffd34d", sound="entity.allay.ambient_with_item", pitch=1.6,
                   bg=argb(225, 255, 249, 225), fg="#7a5a00"),
    "q": dict(name="？？？", color="gold", sound="entity.allay.ambient_without_item", pitch=1.1,
              bg=argb(225, 255, 236, 246), fg="#7a1f5c"),
    "hero": dict(name="主人公", color="green", sound=None, pitch=1.0, bg=0, fg="white"),
    "all3": dict(name="3人", color="#ffb3d9", sound="entity.allay.ambient_with_item", pitch=1.45,
                 bg=argb(225, 255, 236, 246), fg="#7a1f5c"),
}


def tellraw(target, *parts):
    comps = []
    for p in parts:
        comps.append(T(p) if isinstance(p, str) else p)
    if len(comps) == 1:
        return f"tellraw {target} {snbt(comps[0])}"
    return f"tellraw {target} {snbt({'text': '', 'extra': comps})}"


def title(target, main, sub_=None, times=(5, 50, 12)):
    out = [f"title {target} times {times[0]} {times[1]} {times[2]}"]
    if sub_ is not None:
        out.append(f"title {target} subtitle {snbt(sub_ if not isinstance(sub_, str) else T(sub_))}")
    out.append(f"title {target} title {snbt(main if not isinstance(main, str) else T(main))}")
    return out


def actionbar(target, comp):
    return f"title {target} actionbar {snbt(comp if not isinstance(comp, str) else T(comp))}"


def sound(snd, target="@a", pos="~ ~ ~", vol=1, pitch=1, src="master"):
    return f"playsound minecraft:{snd} {src} {target} {pos} {vol} {pitch}"


def gsound(snd, vol=1, pitch=1):
    """Global sound for everyone at their own position."""
    return f"execute as @a at @s run playsound minecraft:{snd} master @s ~ ~ ~ {vol} {pitch}"


NB = "@e[type=marker,tag=rufu_namebox,limit=1]"


def speaker_label(who, suffix=""):
    sp = SPEAKERS[who]
    if who == "heroine":
        return [{"selector": NB, "color": sp["color"], "bold": True}, T(suffix, color=sp["color"], bold=True)]
    return [T(sp["name"] + suffix, color=sp["color"], bold=True)]


def say(who, text, dur=90, big=False, sub_title=True, chat=True, pitch=None):
    """NPC line: speech bubble + subtitle + chat log + voice."""
    sp = SPEAKERS[who]
    out = []
    comp_line = T(text, color=sp["fg"] if sp["bg"] else "white")
    if sp["bg"]:
        out.append(f"execute as @e[type=text_display,tag=rufu_bub_{who}] run data merge entity @s "
                   f"{{text:{snbt(comp_line)},background:{sp['bg']}}}")
        out.append(f"scoreboard players set @e[type=text_display,tag=rufu_bub_{who}] rufu.bt {dur}")
    if chat:
        out.append(tellraw("@a", *speaker_label(who), T("「" + text + "」", color="white")))
    if sub_title:
        out.append("title @a times 3 %d 8" % max(20, dur - 10))
        out.append(f"title @a subtitle {snbt(T('', extra=speaker_label(who, '：') + [T('「' + text + '」', color='white')]))}")
        out.append(f"title @a title {snbt(T(text, color=sp['color'], bold=True)) if big else snbt(T(''))}")
    if sp["sound"]:
        out.append(f"execute as @e[tag=rufu_npc_{who}] at @s run playsound minecraft:{sp['sound']} voice @a ~ ~ ~ 1.4 {pitch or sp['pitch']}")
    return out


def narr(text, color="white", sub_title=True):
    out = [tellraw("@a", T("▶ ", color="gray"), T(text, color=color))]
    if sub_title:
        out += ["title @a times 3 60 10", f"title @a subtitle {snbt(T(text, color=color))}", f"title @a title {snbt(T(''))}"]
    return out


def love(delta, reason):
    """Change love gauge (clamped) and tell everyone."""
    out = []
    if delta >= 0:
        out.append(f"scoreboard players add #love rufu {delta}")
        out.append("execute if score #love rufu matches 101.. run scoreboard players set #love rufu 100")
        out.append(tellraw("@a", T(f"♥ 好感度 +{delta} ", color="light_purple", bold=True), T(reason, color="gray")))
        out.append(gsound("block.note_block.chime", 0.8, 1.6))
    else:
        out.append(f"scoreboard players remove #love rufu {-delta}")
        out.append("execute if score #love rufu matches ..-1 run scoreboard players set #love rufu 0")
        out.append(tellraw("@a", T(f"💔 好感度 {delta} ", color="red", bold=True), T(reason, color="gray")))
        out.append(gsound("entity.villager.no", 0.9, 1.2))
    out.append(call("hud/love"))
    return out


def particles_heart(sel, n=8):
    return f"execute at {sel} run particle minecraft:heart ~ ~2.2 ~ 0.5 0.4 0.5 0 {n} force"


# ---------------------------------------------------------------- items
def ring_item():
    return item_components(
        name=T("💍 婚約指輪", color="gold", italic=False, bold=True),
        lore=["ヒロインに渡すための指輪。", "キツネの大好物ではない。"],
        data={"rufu_ring": b(1), "rufu_m": b(1)}, glint=True)


def returned_ring_item():
    return item_components(
        name=T("💍 返品された指輪", color="gray", italic=False),
        lore=["返品理由：元彼が来たため", "※返金はありません"],
        data={"rufu_ring_returned": b(1)}, glint=False)


REMOTES = {
    "next": dict(model="minecraft:lime_dye", name="▶ 次へ", color="green",
                 lore=["右クリック：次の段階へ進む"]),
    "again": dict(model="minecraft:yellow_dye", name="↻ もう一回", color="yellow",
                  lore=["右クリック：今の段階をもう一度"]),
    "redo": dict(model="minecraft:red_dye", name="⟲ やり直し", color="red",
                 lore=["右クリック：今のミッションを最初から", "（トラブル用・リトライ回数は増えない）"]),
}


def remote_item(kind):
    r = REMOTES[kind]
    return item_components(
        name=T(r["name"], color=r["color"], bold=True, italic=False),
        lore=r["lore"] + ["るふ専用リモコン"],
        data={"rufu_remote": kind}, model=r["model"], glint=True, unbreakable=True)


def give(target, item, comps=None, count=1):
    return f"give {target} {item_arg('minecraft:' + item, comps)} {count}"


def item_entity(x, y, z, item, comps=None, count=1, tags=("rufu_item",), extra=None):
    nbt = {"Item": item_nbt("minecraft:" + item, count, comps), "Tags": list(tags), "PickupDelay": s_(0)}
    if extra:
        nbt.update(extra)
    return f"summon minecraft:item {x} {y} {z} {snbt(nbt)}"


# ---------------------------------------------------------------- NPCs
SKINS = {
    "heroine": ("entity/player/slim/alex", "slim"),
    "leon": ("entity/player/wide/kai", "wide"),
    "priest": ("entity/player/wide/steve", "wide"),
    "sakura": ("entity/player/slim/sunny", "slim"),
    "mio": ("entity/player/slim/noor", "slim"),
    "hinata": ("entity/player/slim/efe", "slim"),
}


def leather(slot_item, color):
    return {"id": f"minecraft:{slot_item}", "count": 1, "components": {"dyed_color": color}}


OUTFITS = {
    "casual": {"chest": leather("leather_chestplate", 0xF4A6C8)},
    "wedding": {"chest": leather("leather_chestplate", 0xFFFFFF), "legs": leather("leather_leggings", 0xFFFFFF),
                "feet": leather("leather_boots", 0xFFFFFF), "mainhand": {"id": "minecraft:pink_tulip", "count": 1}},
    "leon": {"chest": leather("leather_chestplate", 0x1E2A44), "legs": leather("leather_leggings", 0x2B2B2B),
             "feet": leather("leather_boots", 0x3B2A1A)},
    "leon_fly": {"chest": {"id": "minecraft:elytra", "count": 1}, "legs": leather("leather_leggings", 0x2B2B2B),
                 "feet": leather("leather_boots", 0x3B2A1A)},
    "priest": {"chest": leather("leather_chestplate", 0x1A1A1A), "legs": leather("leather_leggings", 0x1A1A1A),
               "feet": leather("leather_boots", 0x1A1A1A), "mainhand": {"id": "minecraft:book", "count": 1}},
    "none": {},
}


def npc_spawn(who, x, y, z, yaw=0.0, outfit="casual", name=None, skin=None, tags=(), extra=None, look=True):
    """Kill and (re)spawn a mannequin NPC with a speech bubble riding on it."""
    sp = SPEAKERS.get(who, SPEAKERS["heroine"])
    tex, model = SKINS[skin or who]
    nbt = {
        "profile": {"texture": tex, "model": model},
        "CustomName": T(name or sp["name"], color=sp["color"], bold=True),
        "CustomNameVisible": True,
        "hide_description": True,
        "immovable": True,
        "Invulnerable": True,
        "Silent": True,
        "Rotation": [f_(float(yaw)), f_(0.0)],
        "Tags": ["rufu_npc", f"rufu_npc_{who}", f"rufu_part_{who}"] + (["rufu_look"] if look else []) + list(tags),
        "equipment": OUTFITS[outfit],
        "Passengers": [{
            "id": "minecraft:text_display",
            "Tags": ["rufu_bub", f"rufu_bub_{who}", f"rufu_part_{who}", "rufu_npcpart"],
            "billboard": "center",
            "text": T(""),
            "background": 0,
            "line_width": 180,
            "shadow": False,
            "see_through": False,
            "transformation": {"translation": [f_(0.0), f_(0.9), f_(0.0)], "left_rotation": [f_(0.0), f_(0.0), f_(0.0), f_(1.0)],
                               "right_rotation": [f_(0.0), f_(0.0), f_(0.0), f_(1.0)], "scale": [f_(1.0), f_(1.0), f_(1.0)]},
        }],
    }
    if extra:
        nbt.update(extra)
    out = [f"kill @e[tag=rufu_part_{who}]",
           f"summon minecraft:mannequin {x} {y} {z} {snbt(nbt)}"]
    if who == "heroine":
        out.append(f"data modify entity @e[type=mannequin,tag=rufu_npc_heroine,limit=1] CustomName set from entity {NB} CustomName")
        out.append(f"summon minecraft:interaction {x} {y} {z} "
                   f"{snbt({'Tags': ['rufu_click', 'rufu_hit_heroine', 'rufu_part_heroine'], 'width': f_(0.95), 'height': f_(2.05), 'response': True})}")
    return out


def npc_kill(who):
    return f"kill @e[tag=rufu_part_{who}]"


def npc_tp(who, x, y, z, yaw=None):
    if yaw is None:
        return f"tp @e[type=mannequin,tag=rufu_npc_{who},limit=1] {x} {y} {z}"
    return f"tp @e[type=mannequin,tag=rufu_npc_{who},limit=1] {x} {y} {z} {yaw} 0"


def poof(sel, n=30):
    return [f"execute at {sel} run particle minecraft:poof ~ ~1 ~ 0.4 0.8 0.4 0.02 {n} force",
            f"execute at {sel} run playsound minecraft:entity.illusioner.mirror_move master @a ~ ~ ~ 1 1.2"]


def firework(x, y, z, colors=(0xFF6FB5, 0xFFFFFF), shape="large_ball", life=20, fade=(0xFFD1E8,), twinkle=True):
    fw = {"id": "minecraft:firework_rocket", "count": 1,
          "components": {"fireworks": {"flight_duration": 1, "explosions": [
              {"shape": shape, "colors": Raw("[I;" + ",".join(str(c) for c in colors) + "]"),
               "fade_colors": Raw("[I;" + ",".join(str(c) for c in fade) + "]"),
               "has_trail": True, "has_twinkle": twinkle}]}}}
    return f"summon minecraft:firework_rocket {x} {y} {z} {snbt({'LifeTime': life, 'FireworksItem': fw, 'Tags': ['rufu_fw']})}"


def freeze(sel=P):
    return [f"execute as {sel} run attribute @s minecraft:movement_speed base set 0",
            f"execute as {sel} run attribute @s minecraft:jump_strength base set 0"]


def unfreeze(sel="@a"):
    return [f"execute as {sel} run attribute @s minecraft:movement_speed base reset",
            f"execute as {sel} run attribute @s minecraft:jump_strength base reset"]
