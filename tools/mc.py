"""Small helpers for writing Minecraft (Java 26.3) commands from Python.

Text components are written in SNBT form (the format commands use since 1.21.5).
"""

import json


def q(s):
    """Quote a Python string as an SNBT string literal."""
    return json.dumps(s, ensure_ascii=False)


def snbt(v):
    """Convert a Python value to SNBT.

    dict -> compound, list -> list, str -> quoted string, bool -> true/false,
    int -> int, float -> float with 'f' suffix unless it is a Raw.
    """
    if isinstance(v, Raw):
        return v.s
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return repr(v) + "f"
    if isinstance(v, str):
        return q(v)
    if isinstance(v, (list, tuple)):
        return "[" + ",".join(snbt(x) for x in v) + "]"
    if isinstance(v, dict):
        parts = []
        for k, x in v.items():
            key = k if _plain_key(k) else q(k)
            parts.append(f"{key}:{snbt(x)}")
        return "{" + ",".join(parts) + "}"
    raise TypeError(type(v))


def _plain_key(k):
    return all(c.isalnum() or c in "_-.+" for c in k) and k != ""


class Raw:
    """Pre-formatted SNBT fragment."""

    def __init__(self, s):
        self.s = s

    def __repr__(self):
        return f"Raw({self.s!r})"


def d(x):
    """double literal"""
    return Raw(f"{x}d")


def b(x):
    return Raw(f"{int(x)}b")


def s_(x):
    return Raw(f"{int(x)}s")


def f_(x):
    return Raw(f"{x}f")


def L(x):
    return Raw(f"{int(x)}L")


def ia(*xs):
    return Raw("[I;" + ",".join(str(int(x)) for x in xs) + "]")


# ---------------------------------------------------------------- text

def T(text="", color=None, bold=None, italic=None, underlined=None,
      obfuscated=None, shadow_color=None, font=None, extra=None, **kw):
    """Build a text component dict."""
    c = {"text": text}
    if color is not None:
        c["color"] = color
    if bold is not None:
        c["bold"] = bool(bold)
    if italic is not None:
        c["italic"] = bool(italic)
    if underlined is not None:
        c["underlined"] = bool(underlined)
    if obfuscated is not None:
        c["obfuscated"] = bool(obfuscated)
    if font is not None:
        c["font"] = font
    if extra:
        c["extra"] = list(extra)
    c.update(kw)
    return c


def click_cmd(comp, command, hover=None):
    comp = dict(comp)
    comp["click_event"] = {"action": "run_command", "command": command}
    if hover is not None:
        comp["hover_event"] = {"action": "show_text", "value": hover}
    return comp


def tc(*parts):
    """Join text parts into a component SNBT string. Strings become plain text."""
    out = []
    for p in parts:
        if isinstance(p, str):
            out.append({"text": p})
        else:
            out.append(p)
    if len(out) == 1:
        return snbt(out[0])
    return snbt({"text": "", "extra": out})


def argb(a, r, g, bl):
    v = (a << 24) | (r << 16) | (g << 8) | bl
    if v >= 1 << 31:
        v -= 1 << 32
    return v


def rgb(r, g, bl):
    return (r << 16) | (g << 8) | bl


# ---------------------------------------------------------------- items

def item_components(name=None, lore=None, data=None, model=None, glint=None,
                    unbreakable=False, can_break=None, can_place_on=None,
                    extra=None, name_color="white"):
    comps = {}
    if name is not None:
        if isinstance(name, str):
            name = T(name, color=name_color, italic=False)
        comps["custom_name"] = name
    if lore:
        ll = []
        for x in lore:
            if isinstance(x, str):
                x = T(x, color="gray", italic=False)
            ll.append(x)
        comps["lore"] = ll
    if data is not None:
        comps["custom_data"] = data
    if model is not None:
        comps["item_model"] = model
    if glint is not None:
        comps["enchantment_glint_override"] = bool(glint)
    if unbreakable:
        comps["unbreakable"] = {}
    if can_break is not None:
        comps["can_break"] = {"blocks": can_break}
    if can_place_on is not None:
        comps["can_place_on"] = {"blocks": can_place_on}
    if extra:
        comps.update(extra)
    return comps


def item_arg(item_id, comps=None):
    """Item stack argument for /give: id[comp=value,...]"""
    if not comps:
        return item_id
    inner = ",".join(f"{k}={snbt(v)}" for k, v in comps.items())
    return f"{item_id}[{inner}]"


def item_nbt(item_id, count=1, comps=None, slot=None):
    dct = {"id": item_id, "count": count}
    if comps:
        dct["components"] = comps
    if slot is not None:
        dct = {"Slot": b(slot), **dct}
    return dct
