"""Generate the datapack.

    python3 tools/build.py          -> writes datapack/ and dist/*.zip
"""

import json
import os
import shutil
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import town                       # noqa: E402
from core import *                # noqa: E402,F401
from core import F, fn, call, sub  # noqa: E402
import system                     # noqa: E402
from system import Step, add_step, STEPS, emit_steps, emit_gm_list  # noqa: E402
import mission                    # noqa: E402
import m1, m2, m3, m4, wed        # noqa: E402
from mc import T, snbt, click_cmd  # noqa: E402

ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "datapack", "rufu_kekkon")
DIST = os.path.join(ROOT, "dist")
PER_TICK = 1200


def world_build(w):
    x0a, z0a, x1a, z1a = AREA
    parts = []
    # base terrain, 4 chunks per tick
    base = []
    for cx in range(x0a // 16, x1a // 16 + 1):
        for cz in range(z0a // 16, z1a // 16 + 1):
            x0, x1 = max(cx * 16, x0a), min(cx * 16 + 15, x1a)
            z0, z1 = max(cz * 16, z0a), min(cz * 16 + 15, z1a)
            base.append([
                f"fill {x0} 65 {z0} {x1} 127 {z1} minecraft:air strict",
                f"fill {x0} 128 {z0} {x1} 191 {z1} minecraft:air strict",
                f"fill {x0} {BASE_Y0} {z0} {x1} {G - 4} {z1} minecraft:stone strict",
                f"fill {x0} {G - 3} {z0} {x1} {G - 1} {z1} minecraft:dirt strict",
                f"fill {x0} {G} {z0} {x1} {G} {z1} minecraft:grass_block strict",
            ])
    for i in range(0, len(base), 4):
        parts.append([c for grp in base[i:i + 4] for c in grp])
    cmds = w.to_commands()
    # prefix block ids with minecraft:
    fixed = []
    for c in cmds:
        sp = c.split(" ")
        if sp[0] == "fill":
            sp[7] = "minecraft:" + sp[7] if not sp[7].startswith("minecraft:") else sp[7]
        else:
            sp[4] = "minecraft:" + sp[4] if not sp[4].startswith("minecraft:") else sp[4]
        fixed.append(" ".join(sp))
    for i in range(0, len(fixed), PER_TICK):
        parts.append(fixed[i:i + PER_TICK])
    late = [c.replace(" water", " minecraft:water") for c in w.late]
    parts.append(late)
    n = len(parts)
    for i, p in enumerate(parts):
        nxt = [f"schedule function rufu:build/p{i + 1} 1t"] if i + 1 < n else [call("build/done")]
        fn(f"build/p{i}",
           *p,
           f"bossbar set rufu:build value {i + 1}",
           *nxt)
    return n


def decor_npcs():
    out = ["kill @e[tag=rufu_deco]"]
    profs = ["farmer", "librarian", "cleric", "butcher", "fisherman", "shepherd", "fletcher", "toolsmith", "cartographer", "mason"]
    k = 0
    for x in range(40, 92, 8):
        if 47 <= x <= 52 or 59 <= x <= 66 or 77 <= x <= 82:
            continue
        for (vx, vz, yaw) in [(x + 1.5, 117.5, 0), (x + 4.5, 125.5, 180)]:
            prof = profs[k % len(profs)]
            k += 1
            out.append(f"summon minecraft:villager {vx} 65 {vz} " + snbt({
                "Tags": ["rufu_deco"], "NoAI": True, "Silent": True, "Invulnerable": True, "PersistenceRequired": True,
                "Rotation": [f_(float(yaw)), f_(0.0)],
                "VillagerData": {"profession": f"minecraft:{prof}", "type": "minecraft:plains", "level": 2}}))
    for (x, z, yaw, prof) in [(150.5, 116.5, 90, "farmer"), (112.5, 108.5, -45, "cleric"), (146.5, 132.5, 135, "librarian"),
                              (176.5, 141.5, 0, "farmer"), (190.5, 135.5, 90, "shepherd"), (126.5, 194.5, 180, "mason"),
                              (60.5, 84.5, 0, "librarian"), (140.5, 88.5, 0, "cleric")]:
        out.append(f"summon minecraft:villager {x} 65 {z} " + snbt({
            "Tags": ["rufu_deco"], "NoAI": True, "Silent": True, "Invulnerable": True, "PersistenceRequired": True,
            "Rotation": [f_(float(yaw)), f_(0.0)],
            "VillagerData": {"profession": f"minecraft:{prof}", "type": "minecraft:plains", "level": 2}}))
    for (x, z) in [(70.5, 145.5), (86.5, 140.5), (120.5, 196.5), (58.5, 70.5)]:
        out.append(f"summon minecraft:cat {x} 65 {z} " + snbt({"Tags": ["rufu_deco"], "PersistenceRequired": True, "Invulnerable": True, "Sitting": True}))
    return out


def gamerules():
    rules = [("keep_inventory", "true"), ("advance_time", "false"), ("advance_weather", "false"),
             ("spawn_mobs", "false"), ("spawn_monsters", "false"), ("mob_griefing", "false"),
             ("fire_spread_radius_around_player", "0"), ("command_block_output", "false"),
             ("show_advancement_messages", "false"), ("immediate_respawn", "true"),
             ("allow_entering_nether_using_portals", "false"), ("spawn_phantoms", "false"),
             ("spawn_wandering_traders", "false"), ("spawn_patrols", "false"), ("raids", "false"),
             ("max_block_modifications", "1000000"), ("players_sleeping_percentage", "101")]
    return [f"gamerule {r} {v}" for r, v in rules]


def setup_and_menu(n_parts):
    x0, z0, x1, z1 = AREA
    fn("setup",
       tellraw("@a", T("💍 町を建設します。少し重くなります（数十秒）…", color="light_purple")),
       *gamerules(),
       "difficulty normal",
       "time set 1000", "weather clear",
       f"forceload add {x0} {z0} {x1} {z1}",
       "kill @e[tag=rufu_deco]", "kill @e[tag=rufu_npc]", "kill @e[tag=rufu_npcpart]",
       f"bossbar set rufu:build max {n_parts}", "bossbar set rufu:build value 0",
       "bossbar set rufu:build players @a", "bossbar set rufu:build visible true",
       f"execute as @a run tp @s {M1_START[0]} 110 {M1_START[2]}",
       "effect give @a minecraft:slow_falling 30 0 true",
       "schedule function rufu:build/p0 20t")
    fn("build/done",
       "bossbar set rufu:build visible false",
       "kill @e[type=item]",
       *decor_npcs(),
       f"setworldspawn {int(M1_START[0])} 65 {int(M1_START[2])}",
       sset("#built", 1),
       f"execute as @a run tp @s {M1_START[0]} 65 {M1_START[2]} 180 0",
       tellraw("@a", T("🏰 町が完成しました！ ", color="green", bold=True),
               click_cmd(T("[役割メニューを開く]", color="aqua", underlined=True), "/function rufu:menu", T("/function rufu:menu"))),
       gsound("ui.toast.challenge_complete", 1, 1))

    # ---------------------------------------------------------------- menu & roles
    fn("menu",
       "tag @s add rufu_gm",
       "tag @s remove rufu_p", "tag @s remove rufu_hero", "tag @s remove rufu_helper",
       f"execute unless entity @s[tag=rufu_hasremote] run {call('gm/remotes')}",
       "tag @s add rufu_hasremote",
       call("menu/list"),
       call("gm/panel"))
    fn("menu/list",
       f"execute as @a unless score @s rufu.id matches 1.. run {call('menu/newid')}",
       tellraw("@s", T("━━━━━ 👥 役割メニュー ━━━━━", color="aqua", bold=True)),
       tellraw("@s", T("主人公＝ドッキリのターゲット(1人)／助っ人＝協力プレイヤー(2人)／GM＝るふ（リモコン操作）", color="gray")),
       tellraw("@s", T("※ひとりでテストするときは、GMのまま自分を[主人公]にしてもOK", color="dark_gray")),
       f"execute as @a run {call('menu/line')}",
       tellraw("@s", click_cmd(T("[✅ 準備完了 → スタート地点へ]", color="green", bold=True), "/function rufu:show/prepare",
                               T("全員を主人公の家の前に集めて、最初の状態にします")), " ",
               click_cmd(T("[🔄 一覧を更新]", color="aqua"), "/function rufu:menu/list")))
    fn("menu/newid", sadd("#nextid", 1), "scoreboard players operation @s rufu.id = #nextid rufu")
    fn("menu/line",
       "execute store result storage rufu:tmp id int 1 run scoreboard players get @s rufu.id",
       'data modify storage rufu:tmp role set value "未設定"',
       'execute if entity @s[tag=rufu_hero] run data modify storage rufu:tmp role set value "★主人公"',
       'execute if entity @s[tag=rufu_helper] run data modify storage rufu:tmp role set value "助っ人"',
       'execute if entity @s[tag=rufu_gm] run data modify storage rufu:tmp role set value "GM"',
       'execute if entity @s[tag=rufu_gm,tag=rufu_hero] run data modify storage rufu:tmp role set value "GM+主人公"',
       'execute if entity @s[tag=rufu_gm,tag=rufu_helper] run data modify storage rufu:tmp role set value "GM+助っ人"',
       f"{call('menu/line_m')} with storage rufu:tmp")
    btn = lambda label, col, r: f'{{text:"{label}",color:"{col}",click_event:{{action:"run_command",command:"/function rufu:role/set {{id:$(id),r:{r}}}"}}}}'
    fn("menu/line_m",
       '$tellraw @a[tag=rufu_gm] ["",{text:" • ",color:"gray"},{selector:"@s",color:"white",bold:true},{text:" ($(role)) ",color:"yellow"},'
       + btn("[主人公]", "green", 1) + ',{text:" "},' + btn("[助っ人]", "aqua", 2) + ',{text:" "},' + btn("[GM]", "gold", 3) + ',{text:" "},' + btn("[外す]", "gray", 0) + ']')
    fn("role/set", "$execute as @a[scores={rufu.id=$(id)}] run function rufu:role/r$(r)", call("menu/list"))
    clr = ["tag @s remove rufu_p", "tag @s remove rufu_hero", "tag @s remove rufu_helper"]
    fn("role/r1", "tag @a remove rufu_hero", *clr, "tag @s add rufu_p", "tag @s add rufu_hero",
       tellraw("@a[tag=rufu_gm]", T("★ 主人公：", color="green"), {"selector": "@s"}))
    fn("role/r2", *clr, "tag @s add rufu_p", "tag @s add rufu_helper",
       tellraw("@a[tag=rufu_gm]", T("☆ 助っ人：", color="aqua"), {"selector": "@s"}))
    fn("role/r3", *clr, "tag @s add rufu_gm", call("gm/remotes"), "tag @s add rufu_hasremote",
       tellraw("@a[tag=rufu_gm]", T("🎮 GM：", color="gold"), {"selector": "@s"}))
    fn("role/r0", *clr, "tag @s remove rufu_gm", tellraw("@a[tag=rufu_gm]", T("— 外した：", color="gray"), {"selector": "@s"}))

    fn("show/prepare",
       f"execute unless score #built rufu matches 1 run tellraw @s {snbt(T('⚠ 先に /function rufu:setup で町を建設してください', color='red'))}",
       f"execute unless entity @a[tag=rufu_hero] run tellraw @s {snbt(T('⚠ 主人公が設定されていません（テストなら自分を主人公にしてもOK）', color='yellow'))}",
       sset("#step", 0), sset("#retry", 0), sset("#t_total", 0), sset("#love", 100), sset("#mission", 0),
       sset("#active", 0), sset("#lock", 0), sset("#seq", 0), sset("#ev", 0), sset("#fx", 0), sset("#retry_step", 0),
       sset("#orig1", 0), sset("#own1", 0),
       'data modify storage rufu:hud now set value "0. 準備完了"',
       f"data modify storage rufu:hud next set value {q('1. ' + STEPS[1].label)}",
       "kill @e[tag=rufu_npc]", "kill @e[tag=rufu_npcpart]", "kill @e[tag=rufu_mob]", "kill @e[tag=rufu_mob4]",
       "kill @e[tag=rufu_fox]", "kill @e[tag=rufu_ask]", "kill @e[tag=rufu_rules]", "kill @e[tag=rufu_pig]",
       "kill @e[tag=rufu_ghast]", "kill @e[tag=rufu_seat]", "kill @e[type=marker,tag=rufu_wpm]", "kill @e[type=marker,tag=rufu_m4m]",
       "kill @e[type=interaction,tag=rufu_click]", "kill @e[type=item,tag=rufu_ringitem]",
       *[c for c in [
           "team leave @a",
           "clear @a minecraft:gold_nugget[custom_data~{rufu_ring_returned:1b}]",
           "time set 1000", "weather clear",
           "effect clear @a",
           "effect give @a[tag=rufu_p] minecraft:resistance infinite 4 true",
           "effect give @a[tag=rufu_p] minecraft:saturation infinite 0 true",
           "gamemode adventure @a[tag=rufu_p]",
       ]],
       *mission.clear_mission_items(),
       *unfreeze(),
       call("hud/hide"),
       f"tp @a[tag=rufu_p] {M1_START[0]} {M1_START[1]} {M1_START[2]} 180 0",
       f"spawnpoint @a[tag=rufu_p] {int(M1_START[0])} 65 {int(M1_START[2])}",
       call("m1/reset"),
       call("m1/db/up"),
       tellraw("@a[tag=rufu_gm]", T("✅ 準備OK！ 緑のリモコン「▶ 次へ」でオープニング開始。", color="green", bold=True)),
       tellraw("@a[tag=rufu_gm]", T("   GMパネル：", color="gray"), click_cmd(T("[開く]", color="aqua", underlined=True), "/function rufu:gm/panel")))


def predicates():
    def hold(items, data=None):
        it = {"items": items}
        if data:
            it["predicates"] = {"minecraft:custom_data": data}
        return {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"equipment": {"mainhand": it}}}
    P = {
        "hold_next": hold("minecraft:carrot_on_a_stick", {"rufu_remote": "next"}),
        "hold_again": hold("minecraft:carrot_on_a_stick", {"rufu_remote": "again"}),
        "hold_redo": hold("minecraft:carrot_on_a_stick", {"rufu_remote": "redo"}),
        "hold_flower": hold("#minecraft:small_flowers"),
        "hold_bread": hold("minecraft:bread"),
        "hold_cake": hold("minecraft:cake"),
        "hold_meat": hold(["minecraft:cooked_beef", "minecraft:cooked_porkchop"]),
        "hold_berries": hold("minecraft:sweet_berries"),
    }
    return P


def generate():
    w = town.build()
    tops = {}
    for (x, y, z), s in w.b.items():
        if s != "air" and y >= G and y <= 120:
            if tops.get((x, z), G) < y:
                tops[(x, z)] = y

    def top_y(x, z):
        return tops.get((x, z), G)

    # systems
    system.system()
    system.clicks()
    system.annoy()
    mission.mission_common()
    m1.build_m1()
    m2.build_m2()
    m3.build_m3(top_y)
    m4.build_m4()
    wed.build_music()
    # steps in order
    m1.opening_steps()
    m1.m1_steps()
    m2.m2_steps()
    m3.m3_steps()
    m4.m4_steps()
    wed.wedding_steps(top_y)
    wed.ending_steps()
    emit_steps()
    emit_gm_list()
    n_parts = world_build(w)
    setup_and_menu(n_parts)
    return w


def write():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    meta = {"pack": {"description": [{"text": "恋 ～結婚の試練～ ", "color": "light_purple", "bold": True},
                                     {"text": "by Rufu / MC 26.3", "color": "gray"}],
                     "min_format": [121, 0], "max_format": 130}}
    with open(os.path.join(OUT, "pack.mcmeta"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    base = os.path.join(OUT, "data")
    for name, cmds in F.items():
        p = os.path.join(base, "rufu", "function", name + ".mcfunction")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write("\n".join(cmds) + "\n")
    for name, obj in predicates().items():
        p = os.path.join(base, "rufu", "predicate", name + ".json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
    for tag, val in (("load", ["rufu:load"]), ("tick", ["rufu:tick"])):
        p = os.path.join(base, "minecraft", "tags", "function", tag + ".json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            json.dump({"values": val}, f, indent=2)
    # zip
    os.makedirs(DIST, exist_ok=True)
    zp = os.path.join(DIST, "rufu_kekkon.zip")
    if os.path.exists(zp):
        os.remove(zp)
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(OUT):
            for fname in files:
                full = os.path.join(root, fname)
                z.write(full, os.path.relpath(full, OUT))
    total = sum(len(v) for v in F.values())
    print(f"functions: {len(F)}  commands: {total}  steps: {len(STEPS) - 1}")
    print("zip:", zp, os.path.getsize(zp) // 1024, "KB")


if __name__ == "__main__":
    generate()
    write()
