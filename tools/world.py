"""Write a ready-built Minecraft world save (the town only, no datapack).

The save is written in the 1.21.4 chunk/level format (DataVersion 4189);
Minecraft 26.3 upgrades it automatically when the world is opened.
"""

import gzip
import io
import json
import math
import os
import shutil
import struct
import sys
import time
import zlib
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import town  # noqa: E402
from layout import AREA, G, BASE_Y0, M1_START  # noqa: E402
import validate  # noqa: E402  (SNBT parser)

DATA_VERSION = 4189          # 1.21.4
ROOT = os.path.dirname(HERE)
WORLD_NAME = "恋 結婚の試練 の町"


# ====================================================================== NBT writer
class Byte(int): pass
class Short(int): pass
class Int(int): pass
class Long(int): pass
class Float(float): pass
class Double(float): pass
class LongArray(list): pass
class IntArray(list): pass


def _tid(v):
    if isinstance(v, bool) or isinstance(v, Byte): return 1
    if isinstance(v, Short): return 2
    if isinstance(v, Long): return 4
    if isinstance(v, Float): return 5
    if isinstance(v, Double): return 6
    if isinstance(v, LongArray): return 12
    if isinstance(v, IntArray): return 11
    if isinstance(v, int): return 3
    if isinstance(v, float): return 6
    if isinstance(v, str): return 8
    if isinstance(v, list): return 9
    if isinstance(v, dict): return 10
    raise TypeError(type(v))


def _str(s):
    b = s.encode("utf-8")
    return struct.pack(">H", len(b)) + b


def _payload(v):
    t = _tid(v)
    if t == 1: return struct.pack(">b", int(v))
    if t == 2: return struct.pack(">h", v)
    if t == 3: return struct.pack(">i", v)
    if t == 4: return struct.pack(">q", v)
    if t == 5: return struct.pack(">f", v)
    if t == 6: return struct.pack(">d", v)
    if t == 8: return _str(v)
    if t == 12: return struct.pack(">i", len(v)) + b"".join(struct.pack(">q", x) for x in v)
    if t == 11: return struct.pack(">i", len(v)) + b"".join(struct.pack(">i", x) for x in v)
    if t == 9:
        et = _tid(v[0]) if v else 0
        return struct.pack(">bi", et, len(v)) + b"".join(_payload(x) for x in v)
    if t == 10:
        out = []
        for k, x in v.items():
            out.append(struct.pack(">b", _tid(x)) + _str(k) + _payload(x))
        return b"".join(out) + b"\x00"


def nbt_bytes(root, name=""):
    return struct.pack(">b", 10) + _str(name) + _payload(root)


# ====================================================================== SNBT -> typed
def typed(v):
    if isinstance(v, validate.Num):
        s = str(v)
        suf = s[-1].lower()
        if suf == "b": return Byte(int(s[:-1]))
        if suf == "s": return Short(int(s[:-1]))
        if suf == "l": return Long(int(s[:-1]))
        if suf == "f": return Float(float(s[:-1]))
        if suf == "d": return Double(float(s[:-1]))
        return Int(int(s)) if "." not in s and "e" not in s.lower() else Double(float(s))
    if isinstance(v, bool): return Byte(1 if v else 0)
    if isinstance(v, dict): return {k: typed(x) for k, x in v.items()}
    if isinstance(v, list): return [typed(x) for x in v]
    return v


def block_entity(bid, x, y, z, snbt_str):
    nbt = typed(validate.snbt(snbt_str, 0)[0]) if snbt_str.strip() else {}
    if "sign" in bid:
        for side in ("front_text", "back_text"):
            if side in nbt:
                msgs = nbt[side].get("messages", [])
                # 1.21.4 stores sign lines as JSON strings
                nbt[side]["messages"] = [json.dumps(untyped(m), ensure_ascii=False) for m in msgs]
                nbt[side].setdefault("color", "black")
                nbt[side].setdefault("has_glowing_text", Byte(0))
        nbt.setdefault("is_waxed", Byte(1))
    ident = {"chest": "chest", "barrel": "barrel", "furnace": "furnace", "smoker": "smoker"}
    eid = None
    for k, v in ident.items():
        if bid.endswith(k):
            eid = v
    if "sign" in bid:
        eid = "hanging_sign" if "hanging" in bid else "sign"
    if eid is None:
        return None
    nbt.update({"id": f"minecraft:{eid}", "x": Int(x), "y": Int(y), "z": Int(z), "keepPacked": Byte(0)})
    return nbt


def untyped(v):
    if isinstance(v, dict): return {k: untyped(x) for k, x in v.items()}
    if isinstance(v, list): return [untyped(x) for x in v]
    if isinstance(v, (Byte,)): return bool(v)
    return v


# ====================================================================== chunks
def parse_state(s):
    name = s.split("[", 1)[0]
    props = {}
    if "[" in s:
        for kv in s[s.index("[") + 1:s.rindex("]")].split(","):
            if kv:
                k, _, v = kv.partition("=")
                props[k] = v
    out = {"Name": "minecraft:" + name}
    if props:
        out["Properties"] = props
    return out


def pack(indices, bits):
    vpl = 64 // bits
    n = math.ceil(4096 / vpl)
    longs = []
    for i in range(n):
        v = 0
        for j in range(vpl):
            k = i * vpl + j
            if k >= 4096:
                break
            v |= indices[k] << (j * bits)
        if v >= 1 << 63:
            v -= 1 << 64
        longs.append(v)
    return LongArray(longs)


def build_world(out_dir):
    w = town.build()
    for c in w.late:                       # fountain water etc.
        p = c.split()
        w.set(int(p[1]), int(p[2]), int(p[3]), p[4].replace("minecraft:", ""))
    bents = {(x, y, z): (state, nbt) for (x, y, z, state, nbt) in w.bents}

    x0a, z0a, x1a, z1a = AREA
    chunks = {}
    for cx in range(x0a // 16, x1a // 16 + 1):
        for cz in range(z0a // 16, z1a // 16 + 1):
            chunks[(cx, cz)] = True
    # explicit blocks per chunk
    per_chunk = {}
    for (x, y, z), s in w.b.items():
        per_chunk.setdefault((x >> 4, z >> 4), {})[(x, y, z)] = s

    region = {}
    ymax = max(y for (_, y, _) in w.b) if w.b else 120
    for (cx, cz) in chunks:
        blocks = per_chunk.get((cx, cz), {})
        sections = []
        for sy in range(-4, 20):
            ybase = sy * 16
            if ybase + 15 < BASE_Y0 or ybase > ymax:
                sections.append({"Y": Byte(sy), "block_states": {"palette": [{"Name": "minecraft:air"}]},
                                 "biomes": {"palette": ["minecraft:plains"]}})
                continue
            pal = {}
            plist = []
            idx = [0] * 4096
            for ly in range(16):
                y = ybase + ly
                for lz in range(16):
                    z = cz * 16 + lz
                    for lx in range(16):
                        x = cx * 16 + lx
                        inside = x0a <= x <= x1a and z0a <= z <= z1a
                        s = blocks.get((x, y, z))
                        if s is None:
                            s = (w.default(y) or "air") if inside else "air"
                        if s not in pal:
                            pal[s] = len(plist)
                            plist.append(s)
                        idx[(ly * 16 + lz) * 16 + lx] = pal[s]
            sec = {"Y": Byte(sy), "biomes": {"palette": ["minecraft:plains"]}}
            bs = {"palette": [parse_state(s) for s in plist]}
            if len(plist) > 1:
                bits = max(4, (len(plist) - 1).bit_length())
                bs["data"] = pack(idx, bits)
            sec["block_states"] = bs
            sections.append(sec)
        bes = []
        for (x, y, z), (state, nbt) in bents.items():
            if (x >> 4, z >> 4) == (cx, cz):
                be = block_entity(state.split("[")[0], x, y, z, nbt)
                if be:
                    bes.append(be)
        chunk = {
            "DataVersion": Int(DATA_VERSION), "xPos": Int(cx), "zPos": Int(cz), "yPos": Int(-4),
            "Status": "minecraft:full", "LastUpdate": Long(0), "InhabitedTime": Long(0), "isLightOn": Byte(0),
            "sections": sections, "block_entities": bes, "Heightmaps": {},
            "structures": {"References": {}, "starts": {}}, "block_ticks": [], "fluid_ticks": [],
            "PostProcessing": [[] for _ in range(24)],
        }
        region.setdefault((cx >> 5, cz >> 5), {})[(cx & 31, cz & 31)] = chunk

    rdir = os.path.join(out_dir, "region")
    os.makedirs(rdir, exist_ok=True)
    for (rx, rz), chs in region.items():
        write_region(os.path.join(rdir, f"r.{rx}.{rz}.mca"), chs)
    write_level(out_dir)
    print("chunks:", len(chunks))


def write_region(path, chs):
    header_loc = bytearray(4096)
    header_ts = bytearray(4096)
    body = bytearray()
    sector = 2
    now = int(time.time())
    for (lx, lz), chunk in sorted(chs.items()):
        data = zlib.compress(nbt_bytes(chunk))
        blob = struct.pack(">ib", len(data) + 1, 2) + data
        pad = (-len(blob)) % 4096
        blob += b"\x00" * pad
        n = len(blob) // 4096
        i = (lx + lz * 32) * 4
        header_loc[i:i + 4] = struct.pack(">I", (sector << 8) | n)
        header_ts[i:i + 4] = struct.pack(">I", now)
        body += blob
        sector += n
    with open(path, "wb") as f:
        f.write(header_loc + header_ts + body)


def write_level(out_dir):
    sx, sy, sz = int(M1_START[0]), 65, int(M1_START[2])
    rules = {"doDaylightCycle": "false", "doWeatherCycle": "false", "doMobSpawning": "false", "mobGriefing": "false",
             "doFireTick": "false", "keepInventory": "true", "doPatrolSpawning": "false", "doTraderSpawning": "false",
             "doInsomnia": "false", "announceAdvancements": "false"}
    flat = {"type": "minecraft:flat", "settings": {
        "layers": [{"block": "minecraft:air", "height": Int(1)}], "biome": "minecraft:the_void",
        "features": Byte(0), "lakes": Byte(0), "structure_overrides": []}}
    data = {
        "DataVersion": Int(DATA_VERSION), "version": Int(19133), "LevelName": WORLD_NAME,
        "GameType": Int(1), "Difficulty": Byte(2), "DifficultyLocked": Byte(0), "hardcore": Byte(0),
        "allowCommands": Byte(1), "initialized": Byte(1), "Time": Long(0), "DayTime": Long(6000),
        "LastPlayed": Long(int(time.time() * 1000)), "SpawnX": Int(sx), "SpawnY": Int(sy), "SpawnZ": Int(sz),
        "SpawnAngle": Float(180.0), "raining": Byte(0), "rainTime": Int(0), "thundering": Byte(0), "thunderTime": Int(0),
        "clearWeatherTime": Int(0), "WasModded": Byte(0), "ServerBrands": ["vanilla"],
        "Version": {"Id": Int(DATA_VERSION), "Name": "1.21.4", "Series": "main", "Snapshot": Byte(0)},
        "GameRules": rules,
        "DataPacks": {"Enabled": ["vanilla"], "Disabled": []},
        "WorldGenSettings": {"seed": Long(20261031), "generate_features": Byte(0), "bonus_chest": Byte(0), "dimensions": {
            "minecraft:overworld": {"type": "minecraft:overworld", "generator": flat},
            "minecraft:the_nether": {"type": "minecraft:the_nether", "generator": {
                "type": "minecraft:noise", "settings": "minecraft:nether",
                "biome_source": {"type": "minecraft:multi_noise", "preset": "minecraft:nether"}}},
            "minecraft:the_end": {"type": "minecraft:the_end", "generator": {
                "type": "minecraft:noise", "settings": "minecraft:end", "biome_source": {"type": "minecraft:the_end"}}},
        }},
        "BorderCenterX": Double(0), "BorderCenterZ": Double(0), "BorderSize": Double(59999968),
        "BorderSafeZone": Double(5), "BorderWarningBlocks": Double(5), "BorderWarningTime": Double(15),
        "BorderSizeLerpTarget": Double(59999968), "BorderSizeLerpTime": Long(0),
        "BorderDamagePerBlock": Double(0.2), "WanderingTraderSpawnDelay": Int(24000), "WanderingTraderSpawnChance": Int(25),
        "ScheduledEvents": [], "CustomBossEvents": {}, "DragonFight": {"NeedsStateScanning": Byte(1), "DragonKilled": Byte(0), "PreviouslyKilled": Byte(0)},
        "enabled_features": ["minecraft:vanilla"],
    }
    raw = nbt_bytes({"Data": data})
    with gzip.open(os.path.join(out_dir, "level.dat"), "wb") as f:
        f.write(raw)


def main():
    out = os.path.join("/tmp", "rufu_world_build", WORLD_NAME)
    if os.path.exists(os.path.dirname(out)):
        shutil.rmtree(os.path.dirname(out))
    os.makedirs(out)
    build_world(out)
    # preview icon
    try:
        from PIL import Image
        Image.open(os.path.join(ROOT, "docs", "town_iso.png")).convert("RGB").resize((64, 64)).save(os.path.join(out, "icon.png"))
    except Exception as e:
        print("icon skipped", e)
    dist = os.path.join(ROOT, "dist")
    os.makedirs(dist, exist_ok=True)
    zp = os.path.join(dist, "rufu_town_world.zip")
    if os.path.exists(zp):
        os.remove(zp)
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(out):
            for f in files:
                full = os.path.join(root, f)
                z.write(full, os.path.relpath(full, os.path.dirname(out)))
    print("zip:", zp, os.path.getsize(zp) // 1024, "KB")


if __name__ == "__main__":
    main()
