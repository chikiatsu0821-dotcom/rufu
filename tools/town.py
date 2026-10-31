"""Procedural builder for the old European town.

Everything is drawn into an in-memory voxel map, then compressed into
`fill ... strict` commands.  Coordinates come from layout.py.
"""

import math
import random

from layout import *  # noqa

R = random.Random(20261031)

DIRS = {"n": (0, -1), "s": (0, 1), "w": (-1, 0), "e": (1, 0)}
OPP = {"n": "s", "s": "n", "e": "w", "w": "e"}
FACE = {"n": "north", "s": "south", "e": "east", "w": "west"}

NONSOLID_HINTS = (
    "stairs", "slab", "fence", "pane", "bars", "_wall", "door", "trapdoor", "torch",
    "lantern", "sign", "button", "carpet", "rail", "ladder", "water", "lava", "air",
    "chain", "bell", "potted", "flower_pot", "campfire", "sapling", "short_grass",
    "fern", "vine", "bed", "banner", "candle", "wheat", "sugar_cane", "head", "skull",
    "pressure_plate", "scaffolding", "lily_pad", "petals", "wildflowers", "bush",
    "dandelion", "poppy", "cornflower", "allium", "daisy", "tulip", "bluet", "lilac",
    "rose", "peony", "sunflower", "light", "end_rod", "cake", "dirt_path", "farmland",
    "leaf_litter", "moss_carpet", "grindstone", "lectern", "anvil", "composter",
    "cauldron", "hopper", "shelf",
)
PANE_LIKE = ("glass_pane", "iron_bars")


def bid(state):
    return state.split("[", 1)[0].split("{", 1)[0]


def is_fence(i):
    return i.endswith("_fence") and "gate" not in i


def is_wall(i):
    return i.endswith("_wall") and not any(k in i for k in ("sign", "torch", "banner", "head", "skull", "fan"))


def is_pane(i):
    return i.endswith("glass_pane") or i == "iron_bars"


def is_solid(i):
    if i in ("air",):
        return False
    if any(h in i for h in NONSOLID_HINTS):
        # some exceptions that are full blocks
        if i in ("hay_block", "light_gray_wool", "lightning_rod"):
            return i == "hay_block"
        return False
    if i.endswith("_leaves"):
        return True
    return True


class World:
    def __init__(self):
        self.b = {}
        self.bents = []        # (x,y,z,state,nbt)
        self.late = []         # setblocks executed normally after everything (fluids)

    # ------------------------------------------------------------ primitives
    @staticmethod
    def default(y):
        if y > G:
            return "air"
        if y == G:
            return "grass_block"
        if y >= G - 3:
            return "dirt"
        if y >= BASE_Y0:
            return "stone"
        return None

    def get(self, x, y, z):
        v = self.b.get((x, y, z))
        if v is None:
            return self.default(y) or "air"
        return v

    def set(self, x, y, z, s):
        self.b[(x, y, z)] = s

    def box(self, x0, y0, z0, x1, y1, z1, s):
        if x0 > x1: x0, x1 = x1, x0
        if y0 > y1: y0, y1 = y1, y0
        if z0 > z1: z0, z1 = z1, z0
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                for z in range(z0, z1 + 1):
                    self.b[(x, y, z)] = s

    def hollow(self, x0, y0, z0, x1, y1, z1, s, inside="air"):
        self.box(x0, y0, z0, x1, y1, z1, s)
        if x1 - x0 >= 2 and z1 - z0 >= 2 and y1 - y0 >= 2 and inside is not None:
            self.box(x0 + 1, y0 + 1, z0 + 1, x1 - 1, y1 - 1, z1 - 1, inside)

    def walls(self, x0, y0, z0, x1, y1, z1, s):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.set(x, y, z0, s)
                self.set(x, y, z1, s)
            for z in range(z0, z1 + 1):
                self.set(x0, y, z, s)
                self.set(x1, y, z, s)

    def clear(self, x0, y0, z0, x1, y1, z1):
        self.box(x0, y0, z0, x1, y1, z1, "air")

    def bent(self, x, y, z, state, nbt):
        self.set(x, y, z, state)
        self.bents.append((x, y, z, state, nbt))

    def ground(self, x0, z0, x1, z1, s, y=G):
        self.box(x0, y, z0, x1, y, z1, s)

    def disc(self, cx, cz, r, y, s, r_in=-1):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            for z in range(int(cz - r - 1), int(cz + r + 2)):
                dd = math.hypot(x - cx, z - cz)
                if r_in < dd <= r:
                    self.set(x, y, z, s)

    # ------------------------------------------------------------ post process
    def connect(self):
        """Compute fence / pane / wall connections from neighbours."""
        for (x, y, z), s in list(self.b.items()):
            i = bid(s)
            fam = None
            if is_fence(i):
                fam = "fence"
            elif is_pane(i):
                fam = "pane"
            elif is_wall(i):
                fam = "wall"
            if not fam:
                continue
            props = {}
            for dname, (dx, dz) in DIRS.items():
                n = bid(self.get(x + dx, y, z + dz))
                ok = False
                if fam == "fence":
                    ok = is_fence(n) and (("nether" in n) == ("nether" in i)) or n.endswith("fence_gate") or is_solid(n)
                elif fam == "pane":
                    ok = is_pane(n) or is_wall(n) or is_solid(n)
                else:
                    ok = is_wall(n) or is_pane(n) or n.endswith("fence_gate") or is_solid(n)
                if fam == "wall":
                    above = bid(self.get(x, y + 1, z))
                    props[FACE[dname]] = ("tall" if is_solid(above) or is_wall(above) else "low") if ok else "none"
                else:
                    props[FACE[dname]] = "true" if ok else "false"
            if fam == "wall":
                straight = (props["north"] != "none" and props["south"] != "none" and props["east"] == "none" and props["west"] == "none") or \
                           (props["east"] != "none" and props["west"] != "none" and props["north"] == "none" and props["south"] == "none")
                above = bid(self.get(x, y + 1, z))
                props["up"] = "false" if straight and not (above not in ("air",)) else "true"
            extra = ""
            if "[" in s:
                old = s[s.index("[") + 1:s.index("]")]
                kv = dict(p.split("=") for p in old.split(",") if p)
                kv.update(props)
                props = kv
            self.b[(x, y, z)] = i + "[" + ",".join(f"{k}={v}" for k, v in props.items()) + "]"

    # ------------------------------------------------------------ export
    def to_commands(self):
        """Greedy-mesh the voxel map into fill commands."""
        by_state = {}
        for (x, y, z), s in self.b.items():
            dflt = self.default(y)
            if dflt is not None and s == dflt:
                continue
            if dflt is None and s == "air":
                continue
            by_state.setdefault(s, set()).add((x, y, z))
        cmds = []
        order = sorted(by_state.keys(), key=lambda s: (_layer_rank(s), s))
        for s in order:
            pts = by_state[s]
            layers = {}
            for (x, y, z) in pts:
                layers.setdefault(y, set()).add((x, z))
            rects_by_y = {}
            for y, cells in layers.items():
                rects_by_y[y] = _greedy(cells)
            # vertical merge
            open_boxes = {}
            boxes = []
            for y in sorted(rects_by_y):
                nxt = {}
                for r in rects_by_y[y]:
                    if r in open_boxes and open_boxes[r][1] == y - 1:
                        y0, _ = open_boxes[r]
                        nxt[r] = (y0, y)
                    else:
                        nxt[r] = (y, y)
                for r, (y0, y1) in open_boxes.items():
                    if r not in nxt or nxt[r][0] != y0:
                        boxes.append((r, y0, y1))
                open_boxes = nxt
            for r, (y0, y1) in open_boxes.items():
                boxes.append((r, y0, y1))
            for (x0, z0, x1, z1), y0, y1 in boxes:
                for bx in _split(x0, y0, z0, x1, y1, z1):
                    if bx[0] == bx[3] and bx[1] == bx[4] and bx[2] == bx[5]:
                        cmds.append(f"setblock {bx[0]} {bx[1]} {bx[2]} {s} strict")
                    else:
                        cmds.append("fill %d %d %d %d %d %d %s strict" % (*bx, s))
        for (x, y, z, state, nbt) in self.bents:
            cmds.append(f"setblock {x} {y} {z} {state}{nbt} strict")
        return cmds


def _layer_rank(s):
    i = bid(s)
    if i == "air":
        return 0
    if i in ("water", "lava"):
        return 3
    if not is_solid(i):
        return 2
    return 1


def _greedy(cells):
    cells = set(cells)
    rects = []
    while cells:
        x, z = min(cells)
        x1 = x
        while (x1 + 1, z) in cells:
            x1 += 1
        z1 = z
        while all((xx, z1 + 1) in cells for xx in range(x, x1 + 1)):
            z1 += 1
        for xx in range(x, x1 + 1):
            for zz in range(z, z1 + 1):
                cells.discard((xx, zz))
        rects.append((x, z, x1, z1))
    return rects


def _split(x0, y0, z0, x1, y1, z1, limit=32768):
    vol = (x1 - x0 + 1) * (y1 - y0 + 1) * (z1 - z0 + 1)
    if vol <= limit:
        return [(x0, y0, z0, x1, y1, z1)]
    # split along the longest axis
    dx, dy, dz = x1 - x0, y1 - y0, z1 - z0
    if dx >= dy and dx >= dz:
        m = (x0 + x1) // 2
        return _split(x0, y0, z0, m, y1, z1) + _split(m + 1, y0, z0, x1, y1, z1)
    if dz >= dy:
        m = (z0 + z1) // 2
        return _split(x0, y0, z0, x1, y1, m) + _split(x0, y0, m + 1, x1, y1, z1)
    m = (y0 + y1) // 2
    return _split(x0, y0, z0, x1, m, z1) + _split(x0, m + 1, z0, x1, y1, z1)


# ====================================================================== pieces

STYLES = [
    dict(base="stone_bricks", frame="dark_oak_log", beam="stripped_dark_oak_log", infill="calcite",
         roof="deepslate_tile_stairs", ridge="deepslate_tiles", rslab="deepslate_tile_slab", door="dark_oak_door", shutter="dark_oak_trapdoor"),
    dict(base="cobblestone", frame="spruce_log", beam="stripped_spruce_log", infill="white_terracotta",
         roof="brick_stairs", ridge="bricks", rslab="brick_slab", door="spruce_door", shutter="spruce_trapdoor"),
    dict(base="polished_andesite", frame="stripped_spruce_log", beam="spruce_log", infill="yellow_terracotta",
         roof="dark_oak_stairs", ridge="dark_oak_planks", rslab="dark_oak_slab", door="oak_door", shutter="spruce_trapdoor"),
    dict(base="stone_bricks", frame="oak_log", beam="stripped_oak_log", infill="smooth_sandstone",
         roof="spruce_stairs", ridge="spruce_planks", rslab="spruce_slab", door="spruce_door", shutter="oak_trapdoor"),
    dict(base="deepslate_bricks", frame="mangrove_log", beam="stripped_mangrove_log", infill="pink_terracotta",
         roof="mud_brick_stairs", ridge="mud_bricks", rslab="mud_brick_slab", door="mangrove_door", shutter="mangrove_trapdoor"),
    dict(base="bricks", frame="dark_oak_log", beam="stripped_dark_oak_log", infill="white_concrete",
         roof="nether_brick_stairs", ridge="nether_bricks", rslab="nether_brick_slab", door="dark_oak_door", shutter="dark_oak_trapdoor"),
    dict(base="mossy_stone_bricks", frame="spruce_log", beam="stripped_spruce_log", infill="light_gray_terracotta",
         roof="waxed_oxidized_cut_copper_stairs", ridge="waxed_oxidized_cut_copper", rslab="waxed_oxidized_cut_copper_slab", door="spruce_door", shutter="spruce_trapdoor"),
    dict(base="polished_tuff", frame="cherry_log", beam="stripped_cherry_log", infill="calcite",
         roof="granite_stairs", ridge="polished_granite", rslab="granite_slab", door="cherry_door", shutter="cherry_trapdoor"),
]

FLOWERS = ["poppy", "dandelion", "cornflower", "allium", "oxeye_daisy", "pink_tulip", "azure_bluet",
           "red_tulip", "white_tulip", "orange_tulip", "lily_of_the_valley"]
POTTED = ["potted_poppy", "potted_dandelion", "potted_red_tulip", "potted_azure_bluet", "potted_allium",
          "potted_pink_tulip", "potted_cornflower", "potted_fern", "potted_azalea_bush", "potted_flowering_azalea_bush"]


def axis_log(log, axis):
    return f"{log}[axis={axis}]"


def stairs(mat, facing, half="bottom", shape="straight"):
    return f"{mat}[facing={facing},half={half},shape={shape}]"


def door(w, x, y, z, mat, facing, hinge="left"):
    w.set(x, y, z, f"{mat}[facing={facing},half=lower,hinge={hinge},open=false]")
    w.set(x, y + 1, z, f"{mat}[facing={facing},half=upper,hinge={hinge},open=false]")


def gable_roof(w, x0, z0, x1, z1, yb, ridge_axis, st, infill=None, overhang=1, frame=None):
    """Roof whose first stair row sits at y=yb."""
    roof, ridge, rslab = st["roof"], st["ridge"], st["rslab"]
    infill = infill or st["infill"]
    if ridge_axis == "z":
        a0, a1, b0, b1 = x0, x1, z0, z1
    else:
        a0, a1, b0, b1 = z0, z1, x0, x1
    i = 0
    top = yb
    while True:
        lo = a0 - overhang + i
        hi = a1 + overhang - i
        y = yb + i
        if lo > hi:
            break
        for bb in range(b0 - overhang, b1 + overhang + 1):
            if lo == hi:
                p = (lo, y, bb) if ridge_axis == "z" else (bb, y, lo)
                w.set(*p, ridge)
            else:
                if ridge_axis == "z":
                    w.set(lo, y, bb, stairs(roof, "east"))
                    w.set(hi, y, bb, stairs(roof, "west"))
                else:
                    w.set(bb, y, lo, stairs(roof, "south"))
                    w.set(bb, y, hi, stairs(roof, "north"))
        # gable infill and attic air
        for aa in range(lo + 1, hi):
            for bb in (b0, b1):
                p = (aa, y, bb) if ridge_axis == "z" else (bb, y, aa)
                if aa >= a0 and aa <= a1:
                    mid = (a0 + a1) / 2
                    if frame and abs(aa - mid) < 0.6:
                        w.set(*p, axis_log(frame, "y"))
                    else:
                        w.set(*p, infill)
            for bb in range(b0 + 1, b1):
                p = (aa, y, bb) if ridge_axis == "z" else (bb, y, aa)
                if a0 <= aa <= a1:
                    w.set(*p, "air")
        top = y
        if lo == hi:
            break
        if lo + 1 == hi:
            # even width: cap with slabs
            for bb in range(b0 - overhang, b1 + overhang + 1):
                for aa in (lo, hi):
                    p = (aa, y + 1, bb) if ridge_axis == "z" else (bb, y + 1, aa)
                    w.set(*p, f"{rslab}[type=bottom]")
            top = y + 1
            break
        i += 1
    return top


def window(w, x, y, z, side, st, tall=2, shutters=True, box=False):
    """window in a wall at (x,z) facing `side`"""
    for k in range(tall):
        w.set(x, y + k, z, "glass_pane")
    if shutters:
        dx, dz = DIRS[side]
        # shutters on both sides of the window, outside the wall
        if side in "ns":
            for sx in (-1, 1):
                for k in range(tall):
                    w.set(x + sx, y + k, z + dz, f"{st['shutter']}[facing={FACE[side]},half=bottom,open=true]")
        else:
            for sz in (-1, 1):
                for k in range(tall):
                    w.set(x + dx, y + k, z + sz, f"{st['shutter']}[facing={FACE[side]},half=bottom,open=true]")
    if box:
        dx, dz = DIRS[side]
        w.set(x + dx, y - 1, z + dz, f"{st['shutter']}[facing={FACE[side]},half=top,open=false]")
        w.set(x + dx, y, z + dz, R.choice(POTTED))


def house(w, x0, z0, x1, z1, floors=2, door_side="s", st=None, ridge=None, chimney=True,
          shop=False, light=True, flower_boxes=True, door_pos=None, roof_extra=0):
    st = st or R.choice(STYLES)
    wd, dp = x1 - x0 + 1, z1 - z0 + 1
    if ridge is None:
        ridge = "z" if wd <= dp else "x"
        if R.random() < 0.3:
            ridge = "x" if ridge == "z" else "z"
    yt = G + 4 * floors
    # foundation + floor
    w.box(x0, G, z0, x1, G, z1, "spruce_planks")
    w.walls(x0, G, z0, x1, G, z1, st["base"])
    # clear interior
    w.box(x0 + 1, G + 1, z0 + 1, x1 - 1, yt, z1 - 1, "air")
    for fl in range(floors):
        yb = G + 1 + 4 * fl
        wallmat = st["base"] if fl == 0 else st["infill"]
        for y in range(yb, yb + 4):
            top_row = (y == yb + 3)
            for x in range(x0, x1 + 1):
                for z in (z0, z1):
                    if top_row:
                        w.set(x, y, z, axis_log(st["beam"], "x"))
                    elif fl > 0 and (x - x0) % 4 == 0:
                        w.set(x, y, z, axis_log(st["frame"], "y"))
                    else:
                        w.set(x, y, z, wallmat)
            for z in range(z0, z1 + 1):
                for x in (x0, x1):
                    if top_row:
                        w.set(x, y, z, axis_log(st["beam"], "z"))
                    elif fl > 0 and (z - z0) % 4 == 0:
                        w.set(x, y, z, axis_log(st["frame"], "y"))
                    else:
                        w.set(x, y, z, wallmat)
        for x in (x0, x1):
            for z in (z0, z1):
                for y in range(yb, yb + 4):
                    w.set(x, y, z, axis_log(st["frame"], "y"))
        # floor above
        if fl < floors - 1:
            w.box(x0 + 1, yb + 3, z0 + 1, x1 - 1, yb + 3, z1 - 1, "spruce_planks")
        if light:
            w.set((x0 + x1) // 2, yb + 2, (z0 + z1) // 2, "light[level=11]")
        # windows
        wy = yb + 1
        for side in "nsew":
            if side in "ns":
                z = z0 if side == "n" else z1
                rng = range(x0 + 2, x1 - 1)
                for x in rng:
                    if (x - x0) % 4 == 2 or (shop and fl == 0 and (x - x0) % 4 in (1, 2, 3)):
                        window(w, x, wy, z, side, st, shutters=not (shop and fl == 0) and R.random() < 0.7,
                               box=(fl > 0 and flower_boxes and R.random() < 0.5))
            else:
                x = x0 if side == "w" else x1
                for z in range(z0 + 2, z1 - 1):
                    if (z - z0) % 4 == 2:
                        window(w, x, wy, z, side, st, shutters=R.random() < 0.6,
                               box=(fl > 0 and flower_boxes and R.random() < 0.4))
    # door
    if door_side:
        if door_pos is None:
            if door_side in "ns":
                dx = (x0 + x1) // 2
                dz = z0 if door_side == "n" else z1
            else:
                dz = (z0 + z1) // 2
                dx = x0 if door_side == "w" else x1
        else:
            dx, dz = door_pos
        door(w, dx, G + 1, dz, st["door"], FACE[door_side])
        ox, oz = DIRS[door_side]
        w.set(dx + ox, G + 3, dz + oz, "lantern[hanging=false]") if False else None
        # lantern beside the door on the wall
        if door_side in "ns":
            w.set(dx + 1, G + 3, dz + oz, f"{st['shutter']}[facing={FACE[door_side]},half=top,open=false]")
            w.set(dx + 1, G + 4, dz + oz, "lantern")
        else:
            w.set(dx + ox, G + 3, dz + 1, f"{st['shutter']}[facing={FACE[door_side]},half=top,open=false]")
            w.set(dx + ox, G + 4, dz + 1, "lantern")
        # step in front
        w.set(dx + ox, G, dz + oz, st["base"] if st["base"] not in ("mossy_stone_bricks",) else "stone_bricks")
    top = gable_roof(w, x0, z0, x1, z1, yt + 1 + roof_extra, ridge, st, frame=st["frame"])
    if roof_extra:
        w.walls(x0, yt + 1, z0, x1, yt + roof_extra, z1, st["infill"])
    if chimney and R.random() < 0.75:
        cx = x0 + 2 if R.random() < 0.5 else x1 - 2
        cz = z0 + 2 if R.random() < 0.5 else z1 - 2
        for y in range(yt + 1, top + 3):
            w.set(cx, y, cz, "bricks")
        w.set(cx, top + 3, cz, "campfire[lit=true,signal_fire=false]") if R.random() < 0.4 else w.set(cx, top + 3, cz, "brick_slab[type=bottom]")
    return dict(yt=yt, top=top, st=st, ridge=ridge)


def lamp(w, x, z, y=G + 1, h=3, kind="spruce_fence", top="lantern"):
    for k in range(h):
        w.set(x, y + k, z, kind)
    w.set(x, y + h, z, top)


def tree(w, x, y, z, kind="oak", h=None, r=None):
    leaves = {"oak": "oak_leaves", "birch": "birch_leaves", "cherry": "cherry_leaves",
              "spruce": "spruce_leaves", "azalea": "flowering_azalea_leaves", "dark_oak": "dark_oak_leaves"}[kind]
    log = {"oak": "oak_log", "birch": "birch_log", "cherry": "cherry_log", "spruce": "spruce_log",
           "azalea": "oak_log", "dark_oak": "dark_oak_log"}[kind]
    h = h or R.randint(4, 6)
    r = r or R.choice([2, 2, 3])
    for k in range(h):
        w.set(x, y + k, z, axis_log(log, "y"))
    cy = y + h - 1
    if kind == "spruce":
        for k in range(h + 2):
            rr = max(0, int((h + 2 - k) / 2.2))
            for dx in range(-rr, rr + 1):
                for dz in range(-rr, rr + 1):
                    if abs(dx) + abs(dz) <= rr + 0.5 and w.get(x + dx, y + 2 + k, z + dz) == "air":
                        w.set(x + dx, y + 2 + k, z + dz, f"{leaves}[persistent=true]")
        w.set(x, y + h + 3, z, f"{leaves}[persistent=true]")
        return
    for dx in range(-r, r + 1):
        for dy in range(-1, r + 1):
            for dz in range(-r, r + 1):
                dd = math.sqrt(dx * dx + (dy * 1.3) ** 2 + dz * dz)
                if dd <= r + 0.3 and R.random() > 0.08:
                    p = (x + dx, cy + dy, z + dz)
                    if w.get(*p) == "air":
                        w.set(*p, f"{leaves}[persistent=true]")


def flowers(w, x0, z0, x1, z1, density=0.5, y=G + 1, kinds=None):
    kinds = kinds or FLOWERS
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if R.random() < density and w.get(x, y, z) == "air":
                w.set(x, y, z, R.choice(kinds))


def bench(w, x, z, facing, y=G + 1, mat="spruce"):
    """2-long bench; facing = direction a sitter looks."""
    back = OPP[facing[0]] if len(facing) == 1 else facing
    fs = FACE[OPP[facing]]
    if facing in "ns":
        for dx in (0, 1):
            w.set(x + dx, y, z, f"{mat}_stairs[facing={fs},half=bottom]")
        w.set(x - 1, y, z, f"{mat}_trapdoor[facing=west,half=bottom,open=true]")
        w.set(x + 2, y, z, f"{mat}_trapdoor[facing=east,half=bottom,open=true]")
    else:
        for dz in (0, 1):
            w.set(x, y, z + dz, f"{mat}_stairs[facing={fs},half=bottom]")
        w.set(x, y, z - 1, f"{mat}_trapdoor[facing=north,half=bottom,open=true]")
        w.set(x, y, z + 2, f"{mat}_trapdoor[facing=south,half=bottom,open=true]")


def stall(w, x0, z0, facing, colors=("red_wool", "white_wool")):
    """3x2 market stall, counter on the street side."""
    xs = range(x0, x0 + 3)
    zs = range(z0, z0 + 2)
    for x in xs:
        for z in zs:
            w.set(x, G, z, "spruce_planks")
    corners = [(x0, z0), (x0 + 2, z0), (x0, z0 + 1), (x0 + 2, z0 + 1)]
    for (x, z) in corners:
        for y in range(G + 1, G + 3):
            w.set(x, y, z, "spruce_fence")
    k = 0
    for x in range(x0 - 0, x0 + 3):
        for z in zs:
            w.set(x, G + 3, z, colors[(x - x0) % 2])
    # counter
    goods = ["melon", "pumpkin", "hay_block", "barrel[facing=up]", "composter", "cake", "potted_red_tulip",
             "flower_pot", "beehive[facing=north,honey_level=5]", "carved_pumpkin[facing=south]"]
    cz = z0 if facing == "n" else z0 + 1
    if facing in "ns":
        w.set(x0 + 1, G + 1, cz, "spruce_slab[type=top]")
        w.set(x0 + 1, G + 2, cz, R.choice(["cake", "potted_red_tulip", "potted_dandelion", "candle[candles=3,lit=true]"]))
        w.set(x0, G + 1, cz, "spruce_fence")
        w.set(x0 + 2, G + 1, cz, "spruce_fence")
        bz = z0 + 1 if facing == "n" else z0
        w.set(x0 + 1, G + 1, bz, R.choice(["barrel[facing=up]", "melon", "pumpkin", "hay_block[axis=y]", "composter"]))


def round_tower(w, cx, cz, r, y0, y1, mat="stone_bricks", roof="waxed_oxidized_cut_copper_stairs",
                roofblock="waxed_oxidized_cut_copper", cap="lightning_rod"):
    for y in range(y0, y1 + 1):
        for x in range(cx - r - 1, cx + r + 2):
            for z in range(cz - r - 1, cz + r + 2):
                dd = math.hypot(x - cx, z - cz)
                if dd <= r + 0.3:
                    if dd > r - 1.2:
                        m = mat if R.random() > 0.15 else R.choice(["mossy_stone_bricks", "andesite", "stone_bricks"])
                        w.set(x, y, z, m)
                    else:
                        w.set(x, y, z, "air" if y > G else mat)
    # floor at top & battlements
    w.disc(cx, cz, r, y1, mat)
    for x in range(cx - r - 1, cx + r + 2):
        for z in range(cz - r - 1, cz + r + 2):
            dd = math.hypot(x - cx, z - cz)
            if r - 1.2 < dd <= r + 0.3 and (x + z) % 2 == 0:
                w.set(x, y1 + 1, z, mat)
    # arrow slits
    for y in range(y0 + 3, y1 - 1, 4):
        for ang in range(0, 360, 60):
            x = cx + round((r) * math.cos(math.radians(ang)))
            z = cz + round((r) * math.sin(math.radians(ang)))
            w.set(x, y, z, "air")
            w.set(x, y + 1, z, "air")
    # cone roof
    rr = r - 1
    y = y1 + 2
    while rr >= 0:
        for x in range(cx - rr - 1, cx + rr + 2):
            for z in range(cz - rr - 1, cz + rr + 2):
                dx, dz = x - cx, z - cz
                dd = math.hypot(dx, dz)
                if dd <= rr + 0.3:
                    if dd > rr - 1.0 and rr > 0:
                        if abs(dx) >= abs(dz):
                            f = "west" if dx > 0 else "east"
                        else:
                            f = "north" if dz > 0 else "south"
                        w.set(x, y, z, stairs(roof, f))
                    else:
                        w.set(x, y, z, roofblock)
        rr -= 1 if rr > 2 else 1
        y += 1
    w.set(cx, y, cz, roofblock)
    w.set(cx, y + 1, cz, cap)
    return y + 1


# ====================================================================== the town

def build():
    w = World()
    x0a, z0a, x1a, z1a = AREA

    terrain(w)
    moat_and_walls(w)
    south_outside(w)
    south_district(w)
    old_town(w)
    main_streets(w)
    park(w)
    back_alleys(w)
    church(w)
    hill(w)
    farm(w)
    misc_blocks(w)
    hall(w)
    w.connect()
    return w


def terrain(w):
    x0, z0, x1, z1 = AREA
    # grass speckles / paths outside handled later
    for _ in range(900):
        x = R.randint(x0, x1)
        z = R.randint(z0, z1)
        if w.get(x, G + 1, z) == "air":
            w.set(x, G + 1, z, R.choice(["short_grass", "short_grass", "short_grass", "fern", "dandelion", "poppy"]))


def street(w, x0, z0, x1, z1, mats=("stone_bricks", "andesite", "cobblestone", "polished_andesite", "stone")):
    weights = [5, 2, 2, 2, 1]
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            w.set(x, G, z, R.choices(mats, weights=weights[:len(mats)])[0])
            for y in range(G + 1, G + 8):
                if bid(w.get(x, y, z)) in ("short_grass", "fern", "dandelion", "poppy"):
                    w.set(x, y, z, "air")


def moat_and_walls(w):
    # moat ring
    M = MOAT
    I = OW
    for x in range(RIM["x0"], RIM["x1"] + 1):
        for z in range(RIM["z0"], RIM["z1"] + 1):
            inside_outer = M["x0"] <= x <= M["x1"] and M["z0"] <= z <= M["z1"]
            inside_wall = I["x0"] <= x <= I["x1"] and I["z0"] <= z <= I["z1"]
            if inside_outer and not inside_wall:
                w.set(x, M["y0"] - 1, z, R.choice(["gravel", "gravel", "mud", "clay"]))
                for y in range(M["y0"], M["y1"] + 1):
                    w.set(x, y, z, "water")
                w.set(x, G, z, "air")
                for y in range(G + 1, G + 4):
                    w.set(x, y, z, "air")
            elif not inside_outer:
                # rim
                for y in range(M["y0"] - 1, G):
                    w.set(x, y, z, "stone_bricks")
                w.set(x, G, z, "tuff_bricks")
                for y in range(G + 1, G + 3):
                    w.set(x, y, z, "air")
    # outer wall
    t = I["t"]
    for x in range(I["x0"], I["x1"] + 1):
        for z in range(I["z0"], I["z1"] + 1):
            edge = min(x - I["x0"], I["x1"] - x, z - I["z0"], I["z1"] - z)
            if edge < t:
                for y in range(M["y0"] - 1, I["top"]):
                    m = "stone_bricks"
                    rr = R.random()
                    if rr < 0.12:
                        m = "mossy_stone_bricks"
                    elif rr < 0.18:
                        m = "andesite"
                    elif y <= G and rr < 0.4:
                        m = "mossy_stone_bricks"
                    w.set(x, y, z, m)
                # walkway & battlements
                if edge == 0:
                    if (x + z) % 2 == 0:
                        w.set(x, I["top"], z, "stone_bricks")
                        w.set(x, I["top"] + 1, z, "stone_brick_slab[type=bottom]")
                    else:
                        w.set(x, I["top"], z, "stone_brick_slab[type=bottom]")
                elif edge == t - 1:
                    w.set(x, I["top"], z, "stone_brick_wall")
    # decorative banners/lanterns on the inner face
    for x in range(I["x0"] + 6, I["x1"] - 5, 12):
        w.set(x, G + 6, I["z1"] - t, "lantern[hanging=false]") if False else None
    # corner towers
    for (cx, cz) in [(I["x0"] + 1, I["z0"] + 1), (I["x1"] - 1, I["z0"] + 1), (I["x0"] + 1, I["z1"] - 1), (I["x1"] - 1, I["z1"] - 1)]:
        round_tower(w, cx, cz, 5, M["y0"] - 1, I["top"] + 6)
    # mid towers
    for (cx, cz) in [((I["x0"] + I["x1"]) // 2, I["z0"] + 1), (I["x0"] + 1, (I["z0"] + I["z1"]) // 2),
                     (I["x1"] - 1, (I["z0"] + I["z1"]) // 2)]:
        round_tower(w, cx, cz, 4, M["y0"] - 1, I["top"] + 4)
    # south gate house: two square towers
    g = GATE_S
    for (tx0, tx1) in [(g["x0"] - 7, g["x0"] - 1), (g["x1"] + 1, g["x1"] + 7)]:
        tz0, tz1 = I["z1"] - 4, I["z1"] + 2
        for x in range(tx0, tx1 + 1):
            for z in range(tz0, tz1 + 1):
                for y in range(M["y0"] - 1, I["top"] + 6):
                    border = x in (tx0, tx1) or z in (tz0, tz1)
                    if border or y <= G:
                        w.set(x, y, z, "stone_bricks" if R.random() > 0.12 else "mossy_stone_bricks")
                    else:
                        w.set(x, y, z, "air")
        top = I["top"] + 6
        for x in range(tx0, tx1 + 1):
            for z in range(tz0, tz1 + 1):
                w.set(x, top, z, "stone_bricks")
                if (x in (tx0, tx1) or z in (tz0, tz1)) and (x + z) % 2 == 0:
                    w.set(x, top + 1, z, "stone_bricks")
        # pointed roof
        st = dict(roof="waxed_oxidized_cut_copper_stairs", ridge="waxed_oxidized_cut_copper",
                  rslab="waxed_oxidized_cut_copper_slab", infill="stone_bricks")
        gable_roof(w, tx0 + 1, tz0 + 1, tx1 - 1, tz1 - 1, top + 2, "z", st, overhang=0)
        # banners
        cx = (tx0 + tx1) // 2
        w.set(cx, I["top"] + 1, tz1 + 1, "red_wall_banner[facing=south]")
        w.set(cx, I["top"], tz1 + 1, "air")
        # windows
        for y in (G + 8, G + 13):
            w.set(cx, y, tz1, "iron_bars")
            w.set(cx, y + 1, tz1, "iron_bars")
    # gate opening
    w.box(g["x0"], g["y0"], I["z1"] - 4, g["x1"], g["y1"], I["z1"] + 2, "air")
    w.box(g["x0"], G, I["z1"] - 4, g["x1"], G, I["z1"] + 2, "stone_bricks")
    # arch
    for x in range(g["x0"], g["x1"] + 1):
        for z in range(I["z1"] - 4, I["z1"] + 3):
            w.set(x, g["y1"] + 1, z, "stone_bricks")
    for z in range(I["z1"] - 4, I["z1"] + 3):
        w.set(g["x0"], g["y1"], z, stairs("stone_brick_stairs", "west", "top"))
        w.set(g["x1"], g["y1"], z, stairs("stone_brick_stairs", "east", "top"))
    # portcullis teeth above the opening
    for x in range(g["x0"], g["x1"] + 1):
        w.set(x, g["y1"], I["z1"] - 1, "iron_bars")
    # lanterns at the gate
    w.set(g["x0"] - 1, G + 4, I["z1"] + 3, "lantern") if False else None
    for x in (g["x0"] - 2, g["x1"] + 2):
        w.set(x, G + 4, RIM["z1"], "air")
    # drawbridge deck is handled by the game logic; build the raised state now
    B = BRIDGE
    for x in range(B["x0"], B["x1"] + 1):
        for y in range(G + 1, G + 1 + (B["z1"] - B["z0"] + 1)):
            w.set(x, y, B["z0"], "spruce_planks" if x not in (B["x0"], B["x1"]) else axis_log("stripped_dark_oak_log", "y"))
    # postern (side door into the gate square)
    P = POSTERN
    for z in range(I["z1"] - 2, I["z1"] + 1):
        w.set(P["x"], P["y0"], z, "air")
        w.set(P["x"], P["y1"], z, "air")
    w.set(P["x"], P["y1"] + 1, I["z1"], "stone_brick_stairs[facing=south,half=top]")
    # north gate (closed, decorative)
    for x in range(126, 131):
        for y in range(G + 1, G + 7):
            w.set(x, y, I["z0"], "iron_bars" if (x + y) % 1 == 0 else "air")
    # inside face: lamps every 16 along the south wall
    for x in range(I["x0"] + 8, I["x1"] - 7, 16):
        if abs(x - 128) > 10:
            w.set(x, G + 4, I["z1"] - t, "lantern[hanging=false]")
            w.set(x, G + 3, I["z1"] - t, "stone_brick_slab[type=top]")


def south_outside(w):
    C = CORRIDOR
    I = OW
    # meadow path & corridor walls
    for z in range(C["z0"], C["z1"] + 1):
        for x in (C["x0"] - 1, C["x1"] + 1):
            for y in range(G + 1, G + 3):
                w.set(x, y, z, "mossy_stone_brick_wall" if R.random() < 0.5 else "stone_brick_wall")
            w.set(x, G, z, "stone_bricks")
            if z % 6 == 0:
                w.set(x, G + 3, z, "lantern")
    # pit field: per-cell uniform random surface; under layer stone
    P = PIT
    surf = ["coarse_dirt", "packed_mud", "dirt_path", "gravel", "rooted_dirt"]
    for c in range(P["cols"]):
        for r in range(P["rows"]):
            m = PIT_SURF[c][r]
            for dx in range(3):
                for dz in range(3):
                    x = P["x0"] + 3 * c + dx
                    z = P["z0"] + 3 * r + dz
                    w.set(x, G, z, m)
                    w.set(x, G - 1, z, "stone")
                    w.set(x, G - 2, z, "stone")
                    w.set(x, G + 1, z, "air")
    for x in range(C["x0"], C["x1"] + 1):
        for z in list(range(C["z0"], P["z0"])) + list(range(P["z0"] + 3 * P["rows"], C["z1"] + 1)):
            w.set(x, G, z, R.choice(["grass_block", "grass_block", "coarse_dirt", "dirt_path"]))
            w.set(x, G + 1, z, "air")
    # warning sign posts
    w.bent(128, G + 1, C["z1"] - 1, "oak_sign[rotation=8]",
           '{front_text:{messages:[{text:"↑ 町まで"},{text:"足元注意",color:"red"},{text:""},{text:""}]}}')
    # hero's house (cosy cottage)
    H = HOUSE
    st = dict(STYLES[3])
    house(w, H["x0"], H["z0"], H["x1"], H["z1"], floors=1, door_side="n", st=st, ridge="x", chimney=True,
          flower_boxes=True, roof_extra=1)
    # garden around
    for x in range(H["x0"] - 4, H["x1"] + 5):
        for z in range(H["z0"] - 1, H["z1"] + 4):
            if not (H["x0"] <= x <= H["x1"] and H["z0"] <= z <= H["z1"]):
                if x in (H["x0"] - 4, H["x1"] + 4) or z == H["z1"] + 3:
                    w.set(x, G + 1, z, "oak_fence")
    flowers(w, H["x0"] - 3, H["z1"] + 1, H["x1"] + 3, H["z1"] + 2, 0.6)
    tree(w, H["x0"] - 2, G + 1, H["z1"] + 2, "cherry", h=5, r=3)
    tree(w, H["x1"] + 2, G + 1, H["z1"] + 2, "oak", h=5, r=2)
    # mailbox
    w.set(H["x0"] - 2, G + 1, H["z0"] - 1, "oak_fence")
    w.set(H["x0"] - 2, G + 2, H["z0"] - 1, "barrel[facing=north]")
    # pickaxe pedestal
    px, py, pz = PICK_POS
    w.set(px, py, pz, "polished_andesite")
    w.set(px, py - 1, pz, "polished_andesite")
    # woodshed with barrel
    bx, by, bz = BARREL_POS
    for y in range(G + 1, G + 4):
        w.set(bx - 1, y, bz + 1, "spruce_fence")
        w.set(bx + 1, y, bz + 1, "spruce_fence")
    w.box(bx - 1, G + 4, bz - 1, bx + 1, G + 4, bz + 1, "spruce_slab[type=bottom]")
    w.set(bx, by + 1, bz + 1, "oak_log[axis=x]")
    w.set(bx - 1, by, bz + 1, "oak_log[axis=x]")
    # path from house door through the pit field
    for z in range(PIT["z0"] + 3 * PIT["rows"], H["z0"]):
        for x in range(126, 131):
            w.set(x, G, z, "dirt_path")
    # outside meadows: trees & flowers
    for _ in range(40):
        x = R.choice(list(range(10, 105)) + list(range(152, 246)))
        z = R.randint(217, 252)
        if w.get(x, G + 1, z) in ("air", "short_grass", "fern", "dandelion", "poppy"):
            tree(w, x, G + 1, z, R.choice(["oak", "oak", "birch", "spruce", "cherry"]))
    flowers(w, 10, 216, 110, 254, 0.05)
    flowers(w, 146, 216, 246, 254, 0.05)


def south_district(w):
    I = OW
    t = I["t"]
    # ring road & gate square
    rr = RING_ROAD
    street(w, rr["x0"], rr["z0"], rr["x1"], rr["z1"])
    gs = GATE_SQ
    street(w, gs["x0"], gs["z0"], gs["x1"], gs["z1"], mats=("polished_andesite", "stone_bricks", "andesite"))
    # gate square well
    w.disc(140, 194, 1.5, G + 1, "stone_bricks")
    w.set(140, G + 1, 194, "water")
    for y in (G + 2, G + 3):
        w.set(139, y, 194, "spruce_fence"); w.set(141, y, 194, "spruce_fence")
    w.box(139, G + 4, 193, 141, G + 4, 195, "spruce_slab[type=bottom]")
    lamp(w, 114, 193)
    # rooftop houses
    st_list = [STYLES[1], STYLES[0], STYLES[3]]
    for k, (x0, x1, z0, z1, yt) in enumerate(ROOF_HOUSES):
        st = dict(st_list[k])
        floors = 1
        house(w, x0, z0, x1, z1, floors=floors, door_side=None, st=st, ridge="z", chimney=False,
              roof_extra=(yt - (G + 4)))
    # chimney obstacle on the middle ridge
    (x0, x1, z0, z1, yt) = ROOF_HOUSES[1]
    cz = (z0 + z1) // 2
    ridge_y = yt + 1 + (x1 - x0 + 2) // 2
    for y in range(ridge_y, ridge_y + 3):
        w.set(128, y, cz, "bricks")
        w.set(128, y, cz + 1, "bricks")
    w.set(128, ridge_y + 3, cz, "campfire[lit=true]")
    # alleys
    for (ax0, ax1, az0, az1) in ALLEYS:
        street(w, ax0, az0, ax1, az1, mats=("cobblestone", "mossy_cobblestone", "gravel"))
        for x in range(ax0, ax1 + 1, 5):
            w.set(x, G + 1, az0, R.choice(["barrel[facing=up]", "composter", "hay_block[axis=y]"]))
    # lane east
    lx0, lx1, lz0, lz1 = LANE_E
    street(w, lx0, lz0, lx1, lz1, mats=("cobblestone", "mossy_cobblestone", "stone"))
    # H1 yard with outside stairs (west side)
    street(w, 118, 182, 122, 190, mats=("cobblestone",))
    for k in range(5):
        z = 190 - k
        y = G + 1 + k
        for x in (120, 121):
            w.box(x, G + 1, z, x, y - 1, z, "spruce_planks") if y - 1 >= G + 1 else None
            w.set(x, y, z, "spruce_stairs[facing=north,half=bottom]")
    for z in range(183, 186):
        for x in (120, 121):
            w.box(x, G + 1, z, x, G + 5, z, "spruce_planks")
    for z in range(183, 191):
        w.set(119, G + 6, z, "spruce_fence") if z < 186 else None
    for y in range(G + 1, G + 4):
        for x in range(118, 123):
            w.set(x, y, 181, "cobblestone_wall" if y < G + 3 else "air")
    # crates to make the stairs readable
    w.set(118, G + 1, 190, "barrel[facing=up]")
    w.set(118, G + 1, 189, "barrel[facing=up]")
    # block lane E at the north end
    w.box(134, G + 1, 162, 136, G + 6, 162, "stone_bricks")
    # strip with hay bales
    S = STRIP
    street(w, S["x0"], S["z0"], S["x1"], S["z1"], mats=("cobblestone", "gravel"))
    w.box(124, G + 1, S["z0"], 132, G + 1, S["z1"], "hay_block[axis=y]")
    for y in range(G + 1, G + 8):
        for z in range(S["z0"], S["z1"] + 1):
            w.set(S["x0"] - 1, y, z, "stone_bricks")
            w.set(S["x1"] + 1, y, z, "stone_bricks")
    # solid filler blocks (warehouses) so the roof route is the only short way
    warehouse(w, 107, 151, 120, 162, "e")
    warehouse(w, 107, 163, 117, 180, "w")
    warehouse(w, 107, 181, 117, 190, "w")
    warehouse(w, 134, 151, 149, 161, "e")
    warehouse(w, 137, 163, 149, 190, "e")
    # houses facing NS streets
    rows_along_z(w, 95, 106, 151, 190, "w")
    rows_along_z(w, 150, 161, 151, 190, "e")
    # houses facing the ring road / gate square
    rows_along_x(w, 95, 111, 191, 196, "s", depth=6)
    rows_along_x(w, 145, 161, 191, 196, "s", depth=6)
    # far west south block
    rows_along_x(w, 35, 87, 185, 196, "s", depth=12)
    rows_along_x(w, 35, 87, 162, 173, "n", depth=12)
    garden(w, 35, 174, 87, 184)
    # NS streets
    street(w, NS_W["x0"], NS_W["z0"], NS_W["x1"], NS_W["z1"])
    street(w, NS_E["x0"], NS_E["z0"], NS_E["x1"], NS_E["z1"])
    for z in range(NS_W["z0"] + 4, NS_W["z1"], 10):
        lamp(w, NS_W["x0"], z)
        lamp(w, NS_E["x1"], z)


def warehouse(w, x0, z0, x1, z1, face):
    st = dict(R.choice(STYLES))
    floors = R.choice([2, 3])
    house(w, x0, z0, x1, z1, floors=floors, door_side=None, st=st, chimney=True, light=False)


def rows_along_x(w, x0, x1, z0, z1, face, depth=None):
    """Row of houses along x, doors facing n or s."""
    x = x0
    while x <= x1:
        wd = R.randint(7, 11)
        if x1 - (x + wd - 1) < 7:
            wd = x1 - x + 1
        dp = depth or (z1 - z0 + 1)
        if face == "s":
            hz0, hz1 = z1 - dp + 1, z1
        else:
            hz0, hz1 = z0, z0 + dp - 1
        if wd >= 5:
            house(w, x, hz0, x + wd - 1, hz1, floors=R.choice([2, 2, 3]), door_side=face)
        x += wd


def rows_along_z(w, x0, x1, z0, z1, face, depth=None):
    z = z0
    while z <= z1:
        dp = R.randint(7, 11)
        if z1 - (z + dp - 1) < 7:
            dp = z1 - z + 1
        wd = depth or (x1 - x0 + 1)
        if face == "e":
            hx0, hx1 = x1 - wd + 1, x1
        else:
            hx0, hx1 = x0, x0 + wd - 1
        if dp >= 5:
            house(w, hx0, z, hx1, z + dp - 1, floors=R.choice([2, 2, 3]), door_side=face)
        z += dp


def garden(w, x0, z0, x1, z1):
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            w.set(x, G, z, "grass_block")
    flowers(w, x0, z0, x1, z1, 0.15)
    for x in range(x0 + 3, x1 - 2, 9):
        tree(w, x, G + 1, (z0 + z1) // 2, R.choice(["oak", "birch", "cherry"]), h=4, r=2)
    for x in range(x0, x1 + 1, 7):
        for z in (z0, z1):
            pass


def old_town(w):
    I = IW
    cx, cz = PC
    # ground of the whole inner town
    street(w, I["x0"] + 2, I["z0"] + 2, I["x1"] - 2, I["z1"] - 2,
           mats=("stone_bricks", "polished_andesite", "andesite", "cobblestone", "stone"))
    # plaza pattern
    for x in range(cx - PLAZA_R - 1, cx + PLAZA_R + 2):
        for z in range(cz - PLAZA_R - 1, cz + PLAZA_R + 2):
            dd = math.hypot(x - cx, z - cz)
            if dd <= PLAZA_R + 0.4:
                ring = int(dd)
                ang = math.degrees(math.atan2(z - cz, x - cx)) % 360
                if ring % 4 == 0:
                    m = "polished_diorite"
                elif ring % 4 == 2:
                    m = "chiseled_stone_bricks" if int(ang / 15) % 2 == 0 else "polished_andesite"
                elif int(ang / 22.5) % 2 == 0:
                    m = "stone_bricks"
                else:
                    m = "polished_andesite"
                w.set(x, G, z, m)
    # fountain
    for x in range(cx - 7, cx + 8):
        for z in range(cz - 7, cz + 8):
            dd = math.hypot(x - cx, z - cz)
            if dd <= FOUNTAIN_R + 0.4:
                if dd > FOUNTAIN_R - 0.8:
                    w.set(x, G, z, "stone_bricks")
                    w.set(x, G + 1, z, "smooth_stone_slab[type=bottom]")
                else:
                    w.set(x, G - 1, z, "prismarine_bricks")
                    w.set(x, G, z, "water")
                    w.set(x, G + 1, z, "air")
    for y in range(G, G + 4):
        for (dx, dz) in [(0, 0), (1, 0), (0, 1), (1, 1)]:
            w.set(cx + dx - 1 + 1, y, cz + dz - 1 + 1, "air")
    for y in range(G, G + 4):
        w.set(cx, y, cz, "chiseled_stone_bricks" if y == G + 3 else "stone_brick_wall")
    w.set(cx, G + 4, cz, "quartz_block")
    w.disc(cx, cz, 1.5, G + 2, "smooth_stone_slab[type=top]")
    w.set(cx, G + 2, cz, "stone_brick_wall")
    w.late.append(f"setblock {cx} {G + 5} {cz} water")
    for (dx, dz) in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
        w.late.append(f"setblock {cx + dx} {G + 3} {cz + dz} water")
    # lamp ring and benches around the plaza
    for k in range(12):
        a = math.radians(k * 30 + 15)
        lx = cx + round((PLAZA_R - 2) * math.cos(a))
        lz = cz + round((PLAZA_R - 2) * math.sin(a))
        lamp(w, lx, lz, kind="dark_oak_fence")
    for k in range(4):
        a = math.radians(k * 90 + 45)
        bx = cx + round(9 * math.cos(a))
        bz = cz + round(9 * math.sin(a))
        # flower beds (source of flowers)
        for x in range(bx - 2, bx + 3):
            for z in range(bz - 2, bz + 3):
                if abs(x - bx) + abs(z - bz) <= 3:
                    w.set(x, G, z, "grass_block")
                    w.set(x, G + 1, z, R.choice(FLOWERS))
        for x in range(bx - 3, bx + 4):
            for z in range(bz - 3, bz + 4):
                if abs(x - bx) + abs(z - bz) == 4:
                    w.set(x, G + 1, z, "spruce_trapdoor[facing=north,half=top,open=false]") if False else w.set(x, G, z, "polished_diorite")
    # inner wall
    for x in range(I["x0"], I["x1"] + 1):
        for z in range(I["z0"], I["z1"] + 1):
            edge = min(x - I["x0"], I["x1"] - x, z - I["z0"], I["z1"] - z)
            if edge < 2:
                top = I["top"]
                for y in range(G, top + 1):
                    m = R.choice(["stone_bricks", "stone_bricks", "mossy_stone_bricks", "cobblestone", "mossy_cobblestone", "andesite"])
                    w.set(x, y, z, m)
                if edge == 0 and (x + z) % 2 == 0 and R.random() > 0.2:
                    w.set(x, top + 1, z, R.choice(["stone_bricks", "mossy_stone_bricks"]))
                if R.random() < 0.05:
                    w.set(x, top + 1, z, "moss_block")
    # gates
    for (gx0, gx1, gz0, gz1) in [(I["x0"], I["x0"] + 1, 119, 123), (I["x1"] - 1, I["x1"], 119, 123), (126, 130, I["z0"], I["z0"] + 1)]:
        w.box(gx0, G + 1, gz0, gx1, G + 5, gz1, "air")
        w.box(gx0, G, gz0, gx1, G, gz1, "stone_bricks")
    # crumbled patch: ruined top + cracked bricks you can break
    P = PATCH
    for x in range(P["x0"] - 2, P["x1"] + 3):
        h = I["top"] - (4 - abs(x - 128)) - R.randint(0, 1)
        for z in (P["z0"], P["z1"]):
            for y in range(h + 1, I["top"] + 2):
                w.set(x, y, z, "air")
    w.box(P["x0"], P["y0"], P["z0"], P["x1"], P["y1"], P["z1"], "cracked_stone_bricks")
    # rubble around the patch
    for (x, z) in [(124, 148), (132, 148), (125, 151), (131, 151), (133, 148)]:
        w.set(x, G + 1, z, R.choice(["cobblestone_slab[type=bottom]", "mossy_cobblestone_slab[type=bottom]", "andesite_slab[type=bottom]"]))
    # buildings around the plaza (corners)
    inner_buildings(w)


def inner_buildings(w):
    cx, cz = PC
    # NW / NE / SW / SE quarters; keep 3 wide gaps for streets
    specs = [
        # x0,x1,z0,z1,door
        (99, 110, 95, 104, "s"), (111, 122, 95, 101, "s"),
        (99, 108, 106, 115, "e"),
        (134, 145, 95, 101, "s"), (146, 157, 95, 104, "s"),
        (148, 157, 106, 115, "w"),
        (99, 108, 127, 136, "e"), (99, 110, 138, 147, "n"), (111, 122, 141, 147, "n"),
        (148, 157, 127, 136, "w"), (146, 157, 138, 147, "n"), (134, 145, 141, 147, "n"),
    ]
    for (x0, x1, z0, z1, dside) in specs:
        house(w, x0, z0, x1, z1, floors=R.choice([2, 3, 3]), door_side=dside, shop=True)
    # bakery (east side, big sign)
    bk = (148, 157, 106, 115)
    w.bent(147, G + 3, 110, "oak_wall_sign[facing=west]",
           '{front_text:{messages:[{text:""},{text:"パン屋",color:"gold",bold:true},{text:"Bäckerei"},{text:""}]}}')
    w.set(149, G + 1, 108, "crafting_table")
    w.bent(149, G + 1, 112, "furnace[facing=east]", '{Items:[{Slot:1b,id:"minecraft:coal",count:16}]}')
    w.bent(149, G + 1, 113, "smoker[facing=east]", '{Items:[{Slot:1b,id:"minecraft:coal",count:16}]}')
    # town hall facade decoration on the north block
    w.set(116, G + 6, 101, "bell[attachment=single_wall,facing=south]")


def main_streets(w):
    for S in (MAIN_W, MAIN_E):
        street(w, S["x0"], S["z0"], S["x1"], S["z1"])
    # inner streets from plaza to gates are part of old_town ground
    # stalls along main street west (both edges), leave the middle free
    for x in range(40, 92, 8):
        if 47 <= x <= 52 or 59 <= x <= 66 or 77 <= x <= 82:
            continue
        stall(w, x, MAIN_W["z0"], "s", colors=R.choice([("red_wool", "white_wool"), ("blue_wool", "white_wool"), ("yellow_wool", "white_wool"), ("lime_wool", "white_wool")]))
        stall(w, x + 3, MAIN_W["z1"] - 1, "n", colors=R.choice([("red_wool", "white_wool"), ("pink_wool", "white_wool"), ("orange_wool", "white_wool")]))
    for x in range(38, 95, 9):
        lamp(w, x, MAIN_W["z0"] + 2 if x % 2 else MAIN_W["z1"] - 2, kind="dark_oak_fence")
    for x in range(164, 220, 9):
        lamp(w, x, MAIN_E["z0"], kind="dark_oak_fence")
        lamp(w, x + 4, MAIN_E["z1"], kind="dark_oak_fence")
    # houses north of main street west (facing south)
    rows_along_x(w, 35, 59, 105, 116, "s")
    rows_along_x(w, 65, 95, 105, 116, "s")
    garden(w, 35, 99, 59, 104)
    garden(w, 65, 99, 95, 104)
    # houses south of main street west (facing north) between the lanes
    for (hx0, hx1) in [(35, 48), (52, 61), (65, 78), (82, 87)]:
        rows_along_x(w, hx0, hx1, 126, 134, "n")
    # SW interior between back alleys
    rows_along_x(w, 35, 48, 138, 158, "e") if False else rows_along_z(w, 35, 48, 138, 158, "e")
    rows_along_x(w, 52, 84, 138, 147, "s")
    rows_along_x(w, 52, 84, 149, 158, "n")
    # houses along main street east: north side
    rows_along_x(w, 170, 192, 108, 116, "s", depth=9)
    rows_along_x(w, 199, 220, 108, 116, "s", depth=9)
    # between NS_E and the inner wall: none (street)


def park(w):
    P = PARK
    for x in range(P["x0"], P["x1"] + 1):
        for z in range(P["z0"], P["z1"] + 1):
            w.set(x, G, z, "grass_block")
            w.set(x, G + 1, z, "air")
    # hedge border
    for x in range(P["x0"], P["x1"] + 1):
        for z in (P["z1"],):
            if not (PARK_LANE["x0"] <= x <= PARK_LANE["x1"]) and not (47 <= x <= 52):
                w.set(x, G + 1, z, "oak_leaves[persistent=true]")
                w.set(x, G + 2, z, "oak_leaves[persistent=true]")
    for z in range(P["z0"], P["z1"] + 1):
        w.set(P["x1"], G + 1, z, "oak_leaves[persistent=true]")
        w.set(P["x1"], G + 2, z, "oak_leaves[persistent=true]")
    cx, cz = PARK_C
    # paths: lane in, ring around gazebo, path west
    for z in range(cz, P["z1"] + 1):
        for x in range(PARK_LANE["x0"], PARK_LANE["x1"] + 1):
            w.set(x, G, z, "dirt_path")
    for z in range(cz, P["z1"] + 1):
        for x in range(49, 52):
            w.set(x, G, z, "dirt_path")
    for x in range(49, cx + 1):
        for z in range(cz + 9, cz + 12):
            w.set(x, G, z, "dirt_path")
    w.disc(cx, cz, 9.5, G, "dirt_path", r_in=6.5)
    # gazebo
    w.disc(cx, cz, 5.4, G, "polished_diorite")
    w.disc(cx, cz, 5.4, G + 1, "air")
    for ang in range(0, 360, 45):
        x = cx + round(4.6 * math.cos(math.radians(ang)))
        z = cz + round(4.6 * math.sin(math.radians(ang)))
        for y in range(G + 1, G + 5):
            w.set(x, y, z, "white_concrete" if False else "birch_fence")
    for rr, y in [(5.6, G + 5), (4.4, G + 6), (3.2, G + 7), (2.0, G + 8), (1.0, G + 9)]:
        w.disc(cx, cz, rr, y, "waxed_oxidized_cut_copper" if rr > 1.1 else "waxed_oxidized_copper")
    w.set(cx, G + 10, cz, "lightning_rod")
    w.set(cx, G + 4, cz, "lantern[hanging=true]")
    # pond
    pcx, pcz = 46, 64
    for x in range(pcx - 9, pcx + 10):
        for z in range(pcz - 7, pcz + 8):
            dd = math.hypot((x - pcx) / 1.3, z - pcz)
            if dd <= 6.0:
                w.set(x, G - 1, z, "mud")
                w.set(x, G, z, "water")
                if R.random() < 0.06:
                    w.set(x, G + 1, z, "lily_pad")
            elif dd <= 6.8:
                w.set(x, G, z, R.choice(["mud", "moss_block", "grass_block"]))
                if R.random() < 0.3:
                    w.set(x, G + 1, z, R.choice(["sugar_cane", "short_grass", "fern"])) if False else w.set(x, G + 1, z, R.choice(["short_grass", "fern", "blue_orchid"]))
    # bridge over the pond
    for x in range(pcx - 2, pcx + 3):
        w.set(x, G + 1, pcz, "spruce_slab[type=bottom]")
    # flower beds (lots of flowers for gifts)
    for (fx, fz) in [(76, 62), (80, 86), (54, 88), (40, 82), (72, 56), (86, 70)]:
        for x in range(fx - 3, fx + 4):
            for z in range(fz - 2, fz + 3):
                w.set(x, G, z, "grass_block")
                w.set(x, G + 1, z, R.choice(FLOWERS))
    # trees
    for (tx, tz, k) in [(40, 54, "cherry"), (58, 56, "oak"), (84, 56, "birch"), (88, 92, "cherry"), (38, 94, "oak"),
                        (74, 92, "cherry"), (82, 80, "oak"), (60, 64, "birch"), (68, 88, "oak"), (88, 64, "cherry"),
                        (38, 72, "spruce"), (56, 94, "birch")]:
        tree(w, tx, G + 1, tz, k, h=R.randint(5, 7), r=3)
    # benches around the gazebo ring
    for (bx, bz, f) in [(cx - 1, cz - 10, "s"), (cx - 1, cz + 10, "n"), (cx - 10, cz - 1, "e"), (cx + 10, cz - 1, "w")]:
        bench(w, bx, bz, f)
    for k in range(8):
        a = math.radians(k * 45 + 22)
        lamp(w, cx + round(11 * math.cos(a)), cz + round(11 * math.sin(a)), kind="birch_fence")
    # lane to main street
    street(w, PARK_LANE["x0"], PARK_LANE["z0"], PARK_LANE["x1"], PARK_LANE["z1"], mats=("stone_bricks", "cobblestone", "andesite"))
    for x in range(49, 52):
        for z in range(99, 117):
            w.set(x, G, z, R.choice(["cobblestone", "stone_bricks", "gravel"]))
            for y in range(G + 1, G + 10):
                w.set(x, y, z, "air")


def back_alleys(w):
    for (x0, x1, z0, z1) in BACK_ALLEYS:
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                w.set(x, G, z, R.choice(["cobblestone", "mossy_cobblestone", "gravel", "andesite", "mud"]))
                for y in range(G + 1, G + 14):
                    w.set(x, y, z, "air")
        # junk & cobwebs for atmosphere (only on the edges)
        for k in range(R.randint(3, 6)):
            if x1 - x0 > z1 - z0:
                x = R.randint(x0, x1)
                z = R.choice([z0, z1])
            else:
                z = R.randint(z0, z1)
                x = R.choice([x0, x1])
            w.set(x, G + 1, z, R.choice(["barrel[facing=up]", "composter", "cauldron", "hay_block[axis=y]"]))
    # a couple of dim lights only
    for (x, z) in [(50, 140), (70, 160), (86, 150), (75, 136)]:
        w.set(x, G + 5, z, "lantern[hanging=true]") if False else None


def church(w):
    C = CHURCH
    x0, x1, z0, z1, yt = C["x0"], C["x1"], C["z0"], C["z1"], C["yt"]
    # clear the church yard
    for x in range(98, 167):
        for z in range(51, 90):
            w.set(x, G, z, "grass_block")
    street(w, LANE_N["x0"], LANE_N["z0"], LANE_N["x1"], LANE_N["z1"])
    # nave shell
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            w.set(x, G, z, "polished_andesite")
    for y in range(G + 1, yt + 1):
        for x in range(x0, x1 + 1):
            for z in (z0, z1):
                w.set(x, y, z, "stone_bricks" if R.random() > 0.1 else "mossy_stone_bricks")
        for z in range(z0, z1 + 1):
            for x in (x0, x1):
                w.set(x, y, z, "stone_bricks" if R.random() > 0.1 else "mossy_stone_bricks")
    w.box(x0 + 1, G + 1, z0 + 1, x1 - 1, yt + 12, z1 - 1, "air")
    # buttresses + tall stained windows
    colors = ["pink", "light_blue", "yellow", "magenta", "lime", "orange"]
    for z in range(z0 + 2, z1 - 1, 4):
        for (x, dx) in ((x0, -1), (x1, 1)):
            for y in range(G + 1, yt - 2):
                w.set(x + dx, y, z, "stone_bricks")
            w.set(x + dx, yt - 2, z, stairs("stone_brick_stairs", "east" if dx < 0 else "west"))
            # windows between buttresses
            wz = z + 2
            if wz < z1 - 1:
                col = colors[(wz // 4) % len(colors)]
                for y in range(G + 3, yt - 2):
                    w.set(x, y, wz, f"{col}_stained_glass_pane")
                w.set(x, yt - 2, wz, f"{col}_stained_glass_pane")
    # rose window at the north end
    for x in range(x0 + 4, x1 - 3):
        for y in range(G + 5, yt + 6):
            dd = math.hypot(x - 128, y - (yt + 1))
            if dd <= 4.2:
                w.set(x, y, z0, "pink_stained_glass_pane" if dd > 2.5 else "yellow_stained_glass_pane")
    # roof
    st = dict(roof="deepslate_tile_stairs", ridge="deepslate_tiles", rslab="deepslate_tile_slab", infill="stone_bricks")
    gable_roof(w, x0, z0, x1, z1, yt + 1, "z", st)
    # interior: aisle carpet, pews, altar, chandeliers
    for z in range(z0 + 1, z1 + 1):
        for x in range(127, 130):
            w.set(x, G + 1, z, "red_carpet")
    for z in range(66, z1 - 1, 2):
        for x in list(range(x0 + 1, 126)) + list(range(131, x1)):
            w.set(x, G + 1, z, "dark_oak_stairs[facing=south,half=bottom]")
        w.set(x0 + 1, G + 1, z, "dark_oak_trapdoor[facing=west,half=bottom,open=true]") if False else None
    # altar platform
    w.box(x0 + 1, G + 1, z0 + 1, x1 - 1, G + 1, 64, "polished_diorite")
    for x in range(x0 + 1, x1):
        w.set(x, G + 1, 65, "polished_diorite_stairs[facing=north,half=bottom]")
    for x in range(127, 130):
        w.set(x, G + 1, 65, "polished_diorite_stairs[facing=north,half=bottom]")
    w.box(126, G + 2, 59, 130, G + 2, 59, "quartz_slab[type=top]") if False else None
    w.set(127, G + 2, 59, "quartz_stairs[facing=east,half=top]")
    w.set(128, G + 2, 59, "quartz_slab[type=top]")
    w.set(129, G + 2, 59, "quartz_stairs[facing=west,half=top]")
    w.set(128, G + 3, 59, "candle[candles=3,lit=true]")
    w.set(127, G + 3, 59, "white_candle[candles=2,lit=true]")
    w.set(129, G + 3, 59, "white_candle[candles=2,lit=true]")
    for (x, z) in [(122, 60), (134, 60), (122, 63), (134, 63)]:
        w.set(x, G + 2, z, "potted_white_tulip" if False else "flower_pot")
        w.set(x, G + 2, z, "white_tulip")
        w.set(x, G + 1, z, "moss_block")
    for x in (x0 + 1, x1 - 1):
        for z in (z0 + 1,):
            w.set(x, G + 6, z + 1, "white_wall_banner[facing=south]")
    for (x, z) in [(124, 64), (132, 64), (124, 72), (132, 72), (124, 78), (132, 78)]:
        for y in range(yt - 3, yt + 4):
            w.set(x, y, z, "iron_chain[axis=y]")
        w.set(x, yt - 4, z, "lantern[hanging=true]")
    # skylight above the altar
    for x in range(126, 131):
        for z in range(60, 63):
            pass
    # tower in front
    T_ = TOWER
    ty_top = yt + 12
    for x in range(T_["x0"], T_["x1"] + 1):
        for z in range(T_["z0"], T_["z1"] + 1):
            w.set(x, G, z, "polished_andesite")
            border = x in (T_["x0"], T_["x1"]) or z in (T_["z0"], T_["z1"])
            for y in range(G + 1, ty_top + 1):
                if border:
                    w.set(x, y, z, "stone_bricks" if R.random() > 0.1 else "mossy_stone_bricks")
                else:
                    w.set(x, y, z, "air")
    # tower opens into the nave
    w.box(126, G + 1, T_["z0"] - 1, 130, G + 7, T_["z0"], "air")
    for z in range(T_["z0"] - 1, T_["z1"] + 1):
        for x in range(127, 130):
            w.set(x, G + 1, z, "red_carpet")
    # big door
    D = CHURCH_DOOR
    for x in range(D["x0"], D["x1"] + 1):
        for y in range(G + 1, G + 5):
            w.set(x, y, D["z"], "air")
    w.set(D["x0"] - 1, G + 5, D["z"], "stone_brick_stairs[facing=east,half=top]")
    w.set(D["x1"] + 1, G + 5, D["z"], "stone_brick_stairs[facing=west,half=top]")
    for x in range(D["x0"], D["x1"] + 1):
        w.set(x, G + 5, D["z"], "chiseled_stone_bricks")
    # belfry openings and bell
    for y in range(ty_top - 5, ty_top - 1):
        for (x, z) in [(128, T_["z0"]), (128, T_["z1"]), (T_["x0"], 85), (T_["x1"], 85)]:
            w.set(x, y, z, "air")
    w.set(128, ty_top - 2, 85, "bell[attachment=ceiling,facing=south]")
    w.box(T_["x0"] + 1, ty_top - 1, T_["z0"] + 1, T_["x1"] - 1, ty_top - 1, T_["z1"] - 1, "stone_bricks")
    w.set(128, ty_top - 1, 85, "stone_bricks")
    # clock face
    for x in range(126, 131):
        for y in range(ty_top - 10, ty_top - 7):
            pass
    w.set(128, ty_top - 9, T_["z1"] + 1, "white_wall_banner[facing=south]") if False else None
    # spire
    sx, sz = 128, 85
    r = 5
    y = ty_top + 1
    for x in range(T_["x0"], T_["x1"] + 1):
        for z in range(T_["z0"], T_["z1"] + 1):
            if (x in (T_["x0"], T_["x1"]) or z in (T_["z0"], T_["z1"])) and (x + z) % 2 == 0:
                w.set(x, y, z, "stone_bricks")
    while r >= 0:
        for x in range(sx - r, sx + r + 1):
            for z in range(sz - r, sz + r + 1):
                if max(abs(x - sx), abs(z - sz)) == r:
                    w.set(x, y, z, "waxed_oxidized_cut_copper")
        y += 2 if r > 1 else 3
        r -= 1
    w.set(sx, y, sz, "waxed_oxidized_cut_copper")
    for k in range(3):
        w.set(sx, y + 1 + k, sz, "gold_block" if k == 1 else "end_rod[facing=up]")
    # church garden with flowers, path to the portal and the portal
    for z in range(PORTAL["z"] + 1, LANE_N["z0"]):
        for x in range(150, 154):
            w.set(x, G, z, "dirt_path")
    for x in range(138, 167):
        for z in range(52, 90):
            if w.get(x, G, z) == "grass_block" and w.get(x, G + 1, z) == "air" and not (148 <= x <= 155):
                if R.random() < 0.12:
                    w.set(x, G + 1, z, R.choice(FLOWERS + ["short_grass", "short_grass"]))
    for (tx, tz) in [(142, 56), (162, 58), (144, 80), (162, 84), (110, 56), (104, 70)]:
        tree(w, tx, G + 1, tz, R.choice(["cherry", "oak", "birch"]), h=5, r=2)
    P = PORTAL
    for x in range(P["x0"], P["x1"] + 1):
        for y in range(P["y0"], P["y1"] + 1):
            edge = x in (P["x0"], P["x1"]) or y in (P["y0"], P["y1"])
            if edge:
                w.set(x, y, P["z"], "obsidian")
            else:
                w.set(x, y, P["z"], "nether_portal[axis=x]")
    for x in range(P["x0"] - 1, P["x1"] + 2):
        for z in range(P["z"] - 1, P["z"] + 2):
            w.set(x, G, z, R.choice(["netherrack", "blackstone", "crimson_nylium"]))
    # houses west of the church
    rows_along_x(w, 98, 117, 78, 89, "s")
    rows_along_x(w, 98, 117, 52, 63, "n") if False else None
    house(w, 99, 52, 112, 64, floors=2, door_side="e")


def hill(w):
    hx, hz = HILL_C
    for x in range(hx - HILL_R_BASE - 1, hx + HILL_R_BASE + 2):
        for z in range(hz - HILL_R_BASE - 1, hz + HILL_R_BASE + 2):
            if not (OW["x0"] + 3 <= x <= OW["x1"] - 3 and OW["z0"] + 3 <= z <= OW["z1"] - 3):
                continue
            dd = math.hypot(x - hx, (z - hz) * 1.0)
            if dd <= HILL_R_TOP:
                h = HILL_TOP
            elif dd <= HILL_R_BASE:
                tt = (dd - HILL_R_TOP) / (HILL_R_BASE - HILL_R_TOP)
                h = round(G + (HILL_TOP - G) * (0.5 + 0.5 * math.cos(math.pi * tt)))
            else:
                continue
            if h <= G:
                continue
            for y in range(G, h):
                w.set(x, y, z, "dirt" if y > h - 4 else "stone")
            w.set(x, h, z, "grass_block")
            # decorations on slopes
            if dd > HILL_R_TOP + 0.5 and R.random() < 0.08:
                w.set(x, h + 1, z, R.choice(["short_grass", "fern", "poppy", "dandelion", "cornflower", "bush"]))
            elif dd <= HILL_R_TOP and R.random() < 0.12:
                w.set(x, h + 1, z, R.choice(["short_grass", "short_grass", "wildflowers[flower_amount=4,facing=north]", "pink_petals[flower_amount=3,facing=east]", "dandelion", "poppy"]))
    # ramp with stairs from main street up to the plateau (south side)
    for k in range(HILL_TOP - G):
        y = G + 1 + k
        z = hz + HILL_R_TOP + 1 + (HILL_TOP - G - 1) - k
        for x in range(RAMP["x0"] - 1, RAMP["x1"] + 2):
            edge = x in (RAMP["x0"] - 1, RAMP["x1"] + 1)
            for yy in range(G + 1, y):
                w.set(x, yy, z, "stone_bricks")
            if edge:
                w.set(x, y, z, "stone_bricks")
                w.set(x, y + 1, z, "stone_brick_wall") if k % 3 else w.set(x, y + 1, z, "lantern")
            else:
                w.set(x, y, z, "stone_brick_stairs[facing=north,half=bottom]")
            for yy in range(y + 1 + (1 if edge else 0), y + 5):
                if w.get(x, yy, z) != "air":
                    w.set(x, yy, z, "air")
    for z in range(hz + HILL_R_TOP + HILL_TOP - G, MAIN_E["z0"]):
        for x in range(RAMP["x0"], RAMP["x1"] + 1):
            w.set(x, G, z, "stone_bricks")
            w.set(x, G + 1, z, "air")
    # the legendary poplar
    tx, tz = TREE
    trunk_h = 16
    for y in range(HILL_TOP + 1, HILL_TOP + 1 + trunk_h):
        for (dx, dz) in [(0, 0), (1, 0), (0, 1), (1, 1)]:
            w.set(tx + dx, y, tz + dz, "poplar_log[axis=y]")
    # roots
    for (dx, dz, ax) in [(-1, 0, "x"), (2, 1, "x"), (0, -1, "z"), (1, 2, "z"), (-2, 1, "x"), (3, 0, "x")]:
        w.set(tx + dx, HILL_TOP + 1, tz + dz, f"poplar_log[axis={ax}]")
    # branches
    top = HILL_TOP + trunk_h
    for (dx, dz, ax, n) in [(1, 0, "x", 4), (-1, 0, "x", 4), (0, 1, "z", 4), (0, -1, "z", 4)]:
        for k in range(1, n + 1):
            bx = tx + (1 if dx > 0 else 0) + dx * k
            bz = tz + (1 if dz > 0 else 0) + dz * k
            w.set(bx, top - 4 + k // 2, bz, f"poplar_log[axis={ax}]")
    # canopy: big ellipsoid with yellow / orange / red poplar leaves
    ccx, ccz, ccy = tx + 0.5, tz + 0.5, top + 1
    for x in range(int(ccx) - 10, int(ccx) + 11):
        for z in range(int(ccz) - 10, int(ccz) + 11):
            for y in range(ccy - 8, ccy + 9):
                dd = ((x - ccx) / 8.5) ** 2 + ((z - ccz) / 8.5) ** 2 + ((y - ccy) / 7.0) ** 2
                if dd <= 1.0 and (dd < 0.8 or R.random() > 0.35):
                    if w.get(x, y, z) == "air":
                        rr = R.random()
                        kind = "yellow_poplar_leaves" if rr < 0.6 else ("orange_poplar_leaves" if rr < 0.9 else "red_poplar_leaves")
                        w.set(x, y, z, f"{kind}[persistent=true]")
    # the glowing circle under the tree (shroomlights flush with the ground)
    ccx, cy, ccz = CIRCLE
    for x in range(int(ccx) - 6, int(ccx) + 7):
        for z in range(int(ccz) - 6, int(ccz) + 7):
            dd = math.hypot(x + 0.5 - ccx, z + 0.5 - ccz)
            if CIRCLE_R - 0.6 <= dd <= CIRCLE_R + 0.3:
                w.set(x, HILL_TOP, z, "shroomlight")
                w.set(x, HILL_TOP + 1, z, "air")
    # bench and lanterns on the plateau
    bench(w, hx - 8, hz + 6, "e")
    bench(w, hx + 8, hz + 6, "w")
    for ang in (30, 150, 210, 330):
        lx = hx + round(11 * math.cos(math.radians(ang)))
        lz = hz + round(11 * math.sin(math.radians(ang)))
        lamp(w, lx, lz, y=HILL_TOP + 1, kind="spruce_fence")
    # treasure X marks (chests filled by the game logic)
    for (x, z) in TREASURES:
        w.set(x, HILL_TOP, z, "coarse_dirt")
        w.set(x, HILL_TOP - 1, z, "chest[facing=south]")
        for (dx, dz) in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
            w.set(x + dx, HILL_TOP, z + dz, "coarse_dirt")


def farm(w):
    F = FARM
    for x in range(F["x0"], F["x1"] + 1):
        for z in range(F["z0"], F["z1"] + 1):
            w.set(x, G, z, "grass_block")
    # fence
    for x in range(F["x0"], F["x1"] + 1):
        for z in (F["z0"],):
            if not (176 <= x <= 184):
                w.set(x, G + 1, z, "oak_fence")
    for z in range(F["z0"], F["z1"] + 1):
        if not (140 <= z <= 144):
            w.set(F["x0"], G + 1, z, "oak_fence")
    # farm road
    for x in range(176, 185):
        for z in range(F["z0"], 196):
            if 146 <= z <= 160 and 172 <= x <= 186:
                continue
            w.set(x, G, z, "dirt_path") if not (168 <= z <= 184 and 172 <= x <= 186) else None
    for z in range(140, 145):
        for x in range(F["x0"], 176):
            w.set(x, G, z, "dirt_path")
    for z in range(161, 167):
        for x in range(176, 215):
            w.set(x, G, z, "dirt_path")
    # wheat
    WH = WHEAT
    for x in range(WH["x0"] - 1, WH["x1"] + 2):
        for z in range(WH["z0"] - 1, WH["z1"] + 2):
            edge = x in (WH["x0"] - 1, WH["x1"] + 1) or z in (WH["z0"] - 1, WH["z1"] + 1)
            if edge:
                w.set(x, G, z, "oak_log[axis=x]" if z in (WH["z0"] - 1, WH["z1"] + 1) else "oak_log[axis=z]")
            elif x in WH["water"]:
                w.set(x, G, z, "water")
            else:
                w.set(x, G, z, "farmland[moisture=7]")
                w.set(x, G + 1, z, "wheat[age=7]")
    # sugar cane along a channel
    CN = CANE
    for z in range(CN["z0"], CN["z1"] + 1):
        w.set(CN["x"], G, z, "water")
        for x in (CN["x"] - 1, CN["x"] + 1):
            w.set(x, G, z, "sand")
            for y in range(G + 1, G + 4):
                w.set(x, y, z, "sugar_cane")
    # pens
    for (P, label) in ((COW_PEN, "cow"), (PIG_PEN, "pig")):
        for x in range(P["x0"], P["x1"] + 1):
            for z in range(P["z0"], P["z1"] + 1):
                edge = x in (P["x0"], P["x1"]) or z in (P["z0"], P["z1"])
                w.set(x, G, z, "grass_block" if label == "cow" else R.choice(["mud", "coarse_dirt", "podzol"]))
                if edge:
                    w.set(x, G + 1, z, "spruce_fence")
        gx = P["x0"] + 3
        w.set(gx, G + 1, P["z0"] if label == "cow" else P["z0"], "spruce_fence_gate[facing=north,open=false,in_wall=false]")
        w.set(P["x0"] + 1, G + 1, P["z0"] + 1, "hay_block[axis=y]")
        w.set(P["x1"] - 1, G + 1, P["z1"] - 1, "water_cauldron[level=3]")
    # barn
    B = BARN
    st = dict(base="spruce_planks", frame="stripped_spruce_log", beam="spruce_log", infill="red_terracotta",
              roof="dark_oak_stairs", ridge="dark_oak_planks", rslab="dark_oak_slab", door="spruce_door", shutter="spruce_trapdoor")
    house(w, B["x0"], B["z0"], B["x1"], B["z1"], floors=2, door_side=None, st=st, ridge="z", chimney=False)
    # wide barn door (north)
    for x in range(177, 182):
        for y in range(G + 1, G + 5):
            w.set(x, y, B["z0"], "air")
    for x in range(177, 182):
        w.set(x, G, B["z0"], "spruce_planks")
    # remove first floor ceiling for a high barn inside
    w.box(B["x0"] + 1, G + 4, B["z0"] + 1, B["x1"] - 1, G + 4, B["z1"] - 1, "air")
    # work stations
    w.set(174, G + 1, 170, "crafting_table")
    w.set(175, G + 1, 170, "crafting_table")
    w.set(184, G + 1, 170, "crafting_table")
    for k, z in enumerate((172, 174, 176)):
        w.bent(173, G + 1, z, "furnace[facing=east]", '{Items:[{Slot:1b,id:"minecraft:coal",count:16}]}')
    w.bent(185, G + 1, 172, "chest[facing=west]", "{}")   # refilled by logic
    for (x, z) in [(174, 182), (175, 182), (184, 182), (185, 182), (174, 181), (185, 181)]:
        w.set(x, G + 1, z, "hay_block[axis=y]")
    w.set(179, G + 4, 176, "lantern[hanging=true]")
    w.set(179, G + 5, 176, "iron_chain[axis=y]") if False else None
    w.set(179, G + 8, 176, "light[level=14]")
    w.bent(178, G + 5, B["z0"] - 1, "oak_wall_sign[facing=north]",
           '{front_text:{messages:[{text:""},{text:"農場",color:"dark_green",bold:true},{text:"Bauernhof"},{text:""}]}}')
    # windmill
    mx, mz = 196, 186
    for y in range(G + 1, G + 15):
        r = 4 if y < G + 6 else (3 if y < G + 11 else 2)
        for x in range(mx - r, mx + r + 1):
            for z in range(mz - r, mz + r + 1):
                dd = math.hypot(x - mx, z - mz)
                if dd <= r + 0.3:
                    w.set(x, y, z, ("white_terracotta" if y % 4 else "stripped_birch_log[axis=y]") if dd > r - 0.9 else "air")
    for y in range(G + 1, G + 3):
        w.set(mx, y, mz - 4, "air")
    door(w, mx, G + 1, mz - 4, "spruce_door", "north")
    st = dict(roof="dark_oak_stairs", ridge="dark_oak_planks", rslab="dark_oak_slab", infill="white_terracotta")
    rr = 3
    y = G + 15
    while rr >= 0:
        w.disc(mx, mz, rr, y, "dark_oak_planks")
        y += 1
        rr -= 1
    # static sails in an X on the north face
    hub = (mx, G + 12, mz - 4)
    w.set(*hub, "spruce_planks")
    for k in range(1, 8):
        for (sx, sy) in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
            x = hub[0] + sx * k
            y = hub[1] + sy * k
            if y > G + 1:
                w.set(x, y, hub[2], "spruce_fence")
                if k > 2:
                    w.set(x + (1 if sx > 0 else -1) * 0, y + (1 if sy < 0 else -1), hub[2] - 0, "white_wool") if False else None
    for k in range(3, 8):
        for (sx, sy) in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
            w.set(hub[0] + sx * k, hub[1] + sy * (k - 1), hub[2], "white_wool")
    # farm flowers and a scarecrow
    flowers(w, 190, 130, 218, 142, 0.25)
    w.set(184, G + 1, 153, "oak_fence") if False else None
    for x in range(F["x0"] + 1, 175):
        for z in range(F["z0"] + 1, 139):
            if R.random() < 0.05:
                w.set(x, G + 1, z, R.choice(FLOWERS))


def misc_blocks(w):
    # remove any grass bits standing in water / on non-grass (cleanup)
    for (x, y, z), s in list(w.b.items()):
        i = bid(s)
        if i in ("short_grass", "fern") + tuple(FLOWERS):
            below = bid(w.get(x, y - 1, z))
            if below not in ("grass_block", "dirt", "coarse_dirt", "podzol", "moss_block", "rooted_dirt", "mud"):
                w.set(x, y, z, "air")


HEART = [
    "..XXX...XXX..",
    ".XXXXX.XXXXX.",
    "XXXXXXXXXXXXX",
    "XXXXXXXXXXXXX",
    "XXXXXXXXXXXXX",
    ".XXXXXXXXXXX.",
    "..XXXXXXXXX..",
    "...XXXXXXX...",
    "....XXXXX....",
    ".....XXX.....",
    "......X......",
]


def hall(w):
    H = HALL
    x0, x1, z0, z1, y0, y1 = H["x0"], H["x1"], H["z0"], H["z1"], H["y0"], H["y1"]
    # clear the space (trees from the meadow)
    w.box(x0 - 2, y0 + 1, z0 - 2, x1 + 2, y1 + 8, min(z1 + 1, 255), "air")
    # shell: black walls / ceiling, dark floor
    w.box(x0, y0, z0, x1, y0, z1, "polished_blackstone")
    w.walls(x0, y0 + 1, z0, x1, y1, z1, "black_concrete")
    w.box(x0, y1, z0, x1, y1, z1, "black_concrete")
    w.box(x0 + 1, y0 + 1, z0 + 1, x1 - 1, y1 - 1, z1 - 1, "air")
    # subtle floor pattern
    for x in range(x0 + 1, x1):
        for z in range(z0 + 1, z1):
            if (x + z) % 2 == 0:
                w.set(x, y0, z, "polished_blackstone_bricks")
    # hidden lights in the ceiling
    for x in range(x0 + 3, x1 - 1, 6):
        for z in range(z0 + 3, z1 - 1, 6):
            w.set(x, y1 - 1, z, "light[level=13]")
    # stage
    S = STAGE
    w.box(S["x0"], y0 + 1, S["z0"], S["x1"], y0 + 1, S["z1"], "smooth_quartz")
    for x in range(S["x0"], S["x1"] + 1):
        w.set(x, y0 + 1, S["z1"] + 1, "quartz_stairs[facing=north,half=bottom]")
    for x in range(S["x0"] + 2, S["x1"] - 1):
        w.set(x, y0 + 2, S["z0"] + 2, "pink_carpet")
    # gold pedestal for ???
    qx, qz = 41, 225
    w.set(qx, y0 + 2, qz, "gold_block")
    for (dx, dz) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        w.set(qx + dx, y0 + 2, qz + dz, "gold_block" if False else "smooth_quartz_slab[type=bottom]")
    # small pedestals under the others
    for gx in (23, 28, 36):
        w.set(gx, y0 + 1, 225, "smooth_quartz")
    # spotlights (light blocks) over the stage
    for gx in (23, 28, 32, 36, 41):
        w.set(gx, y1 - 3, 225, "light[level=15]")
    # red carpet with gold lines on both sides
    cx = HALL_CX
    for z in range(S["z1"] + 1, z1):
        w.set(cx - 2, y0, z, "gold_block")
        w.set(cx + 2, y0, z, "gold_block")
        for x in range(cx - 1, cx + 2):
            w.set(x, y0 + 1, z, "red_carpet")
    for z in range(S["z0"] + 3, S["z1"] + 1):
        for x in range(cx - 1, cx + 2):
            w.set(x, y0 + 2, z, "red_carpet")
    # big pink heart on the back wall
    hw = len(HEART[0])
    for r, row in enumerate(HEART):
        for c, ch in enumerate(row):
            if ch == "X":
                x = cx - hw // 2 + c
                y = y1 - 4 - r
                edge = (c == 0 or row[c - 1] != "X" or c == hw - 1 or row[c + 1] != "X" or
                        r == 0 or HEART[r - 1][c] != "X" or r == len(HEART) - 1 or HEART[r + 1][c] != "X")
                w.set(x, y, z0 + 1, "magenta_concrete" if edge else "pink_concrete")
                if not edge and (r + c) % 3 == 0:
                    w.set(x, y, z0 + 2, "light[level=6]")
    # red curtains: proscenium + side drapes
    for x in list(range(x0 + 1, x0 + 6)) + list(range(x1 - 5, x1)):
        for y in range(y0 + 1, y1):
            w.set(x, y, S["z1"] + 2, "red_wool" if (x % 2) else "red_concrete")
    for x in range(x0 + 1, x1):
        for y in range(y1 - 2, y1):
            w.set(x, y, S["z1"] + 2, "red_wool" if (x % 2) else "red_concrete")
        w.set(x, y1 - 3, S["z1"] + 2, "yellow_carpet" if False else "gold_block" if x % 4 == 0 else "red_wool")
    for z in range(S["z1"] + 4, z1, 4):
        for y in range(y0 + 1, y1):
            w.set(x0 + 1, y, z, "red_wool")
            w.set(x1 - 1, y, z, "red_wool")
            w.set(x0 + 1, y, z + 1, "red_concrete")
            w.set(x1 - 1, y, z + 1, "red_concrete")
    # chandeliers
    for (lx, lz) in [(24, 240), (40, 240), (32, 250)]:
        for y in range(y1 - 4, y1):
            w.set(lx, y, lz, "iron_chain[axis=y]")
        w.set(lx, y1 - 5, lz, "lantern[hanging=true]")
    # the anvil for the name tag
    ax, ay, az = HALL_ANVIL
    w.set(ax, ay - 1, az, "gold_block")
    w.set(ax, ay, az, "anvil[facing=north]")
    w.bent(ax, ay, az - 1, "dark_oak_wall_sign[facing=north]" if False else "air", "") if False else None
