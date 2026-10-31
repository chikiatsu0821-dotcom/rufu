"""Wedding ceremony, escape, ending and the final prank reveal."""

import math
from core import *  # noqa
from system import Step, add_step, event, ev_start
from mc import T, snbt, item_components

HX, HY, HZ = WED_HERO
WX, WY, WZ = WED_HEROINE
AX, AY, AZ = ALTAR

# ---------------------------------------------------------------- music
# Wagner "Bridal Chorus" (public domain). harp pitch index: 0 = F#3 ... 24 = F#5
BRIDAL = [  # (semitone index, beats)
    (6, 1), (11, 1.5), (11, 0.5), (11, 2),
    (6, 1), (13, 1.5), (10, 0.5), (11, 2),
    (6, 1), (11, 1.5), (16, 0.5), (16, 1), (15, 1.5), (13, 0.5), (11, 1), (10, 1.5), (11, 0.5), (13, 2),
    (6, 1), (11, 1.5), (11, 0.5), (11, 2),
    (6, 1), (13, 1.5), (10, 0.5), (11, 2),
    (6, 1), (11, 1.5), (16, 0.5), (16, 1), (15, 1), (13, 1), (11, 1), (10, 1), (13, 1), (11, 3),
]
FANFARE = [(11, 0.5), (15, 0.5), (18, 0.5), (23, 1.5), (18, 0.5), (23, 2)]


def pitch(n):
    return round(2 ** ((n - 12) / 12), 4)


def song(name, notes, beat=9, inst=("block.note_block.harp", "block.note_block.bell"), bass=True):
    t = 0
    sched = {}
    for (n, beats) in notes:
        cmds = [f"execute as @a at @s run playsound minecraft:{inst[0]} record @s ~ ~ ~ 0.9 {pitch(n)}"]
        if inst[1]:
            cmds.append(f"execute as @a at @s run playsound minecraft:{inst[1]} record @s ~ ~ ~ 0.35 {pitch(min(24, max(0, n - 12 + 12)) if n <= 12 else n - 12)}")
        if bass and beats >= 1:
            cmds.append(f"execute as @a at @s run playsound minecraft:block.note_block.bass record @s ~ ~ ~ 0.6 {pitch(max(0, n - 12) if n >= 12 else n)}")
        sched.setdefault(int(round(t)), []).extend(cmds)
        t += beats * beat
    starts = []
    for k, (tick, cmds) in enumerate(sorted(sched.items())):
        fn(f"song/{name}/{k}", *cmds)
        starts.append(f"schedule function rufu:song/{name}/{k} {max(1, tick)}t append")
    fn(f"song/{name}", *starts)


def build_music():
    song("bridal", BRIDAL, beat=9)
    song("bridal_short", BRIDAL[:8], beat=8)
    song("fanfare", FANFARE, beat=5, inst=("block.note_block.pling", "block.note_block.bell"), bass=False)
    song("sad", [(11, 1), (10, 1), (8, 1), (6, 3)], beat=10, inst=("block.note_block.didgeridoo", None), bass=False)


# ---------------------------------------------------------------- helpers
def leon_flight():
    """Keyframes for Leon's elytra entrance through the roof hole."""
    pts = [(160.5, 104, 40.5), (146.5, 96, 56.5), (134.5, 88, 66.5), (129.5, 82, 70.5), (128.5, 76, 71.5),
           (128.5, 70, 72.5), (128.5, 66, 73.0), (128.5, 65, 73.5)]
    frames = []
    steps_per = 6
    for i in range(len(pts) - 1):
        a, b_ = pts[i], pts[i + 1]
        for s in range(steps_per):
            u = s / steps_per
            frames.append(tuple(a[j] + (b_[j] - a[j]) * u for j in range(3)))
    frames.append(pts[-1])
    return frames


def pig_route():
    pts = [(128.5, 73.5), (128.5, 89.5), (151.5, 90.5), (151.5, 62.0)]
    return pts


def wedding_steps(top_y):
    seats = SEATS
    hole = ROOF_HOLE
    # 21 to the church
    add_step(Step("結婚式へ（教会に移動）", retry=0, mission=0, t0=[
        sset("#lock", 1), sset("#active", 0), call("hud/hide"),
        "bossbar set rufu:love visible true",
        "kill @e[tag=rufu_mob]", "kill @e[tag=rufu_mob4]", "kill @e[tag=rufu_fox]", "kill @e[type=marker,tag=rufu_m4m]",
        "effect give @a[tag=rufu_p] minecraft:resistance infinite 4 true",
        "effect give @a[tag=rufu_p] minecraft:fire_resistance infinite 0 true",
        "effect give @a[tag=rufu_p] minecraft:blindness 2 0 true",
        "time set 11500", "weather clear",
        sset("#love", 100), call("hud/love"),
        *npc_spawn("heroine", WX, WY, WZ, 90, outfit="wedding", look=False),
        *npc_spawn("priest", AX, AY, AZ, 0, outfit="priest", look=False),
        "kill @e[tag=rufu_seat]",
        f"summon minecraft:item_display {seats[0][0]} {seats[0][1]} {seats[0][2]} {{Tags:[\"rufu_seat\",\"rufu_seat1\"]}}",
        f"summon minecraft:item_display {seats[1][0]} {seats[1][1]} {seats[1][2]} {{Tags:[\"rufu_seat\",\"rufu_seat2\"]}}",
        f"tp @a[tag=rufu_hero] {HX} {HY} {HZ} -90 0",
        "tag @a remove rufu_sat",
        f"execute as @a[tag=rufu_helper,limit=1,sort=arbitrary] run {call('wed/seat1')}",
        f"execute as @a[tag=rufu_helper,tag=!rufu_sat,limit=1,sort=arbitrary] run {call('wed/seat2')}",
        *title("@a", T("～ 結婚式 ～", color="light_purple", bold=True), T("町の奥の教会", color="white"), (20, 60, 20)),
    ], tl={
        10: [tellraw("@a[tag=rufu_helper]", T("🎩 助っ人のふたりは「友人代表」として最前列に座っています（スニークで立てます）", color="gray"))],
        40: [sset("#lock", 0)],
    }))
    fn("wed/seat1", f"tp @s {seats[0][0]} 66 {seats[0][2]} 180 0", "ride @s mount @e[type=item_display,tag=rufu_seat1,limit=1]", "tag @s add rufu_sat")
    fn("wed/seat2", f"tp @s {seats[1][0]} 66 {seats[1][2]} 180 0", "ride @s mount @e[type=item_display,tag=rufu_seat2,limit=1]", "tag @s add rufu_sat")
    # 22 bells + march
    add_step(Step("鐘と結婚行進曲", t0=[sset("#lock", 1)], tl={
        1: ["playsound minecraft:block.bell.use master @a 128 88 85 4 0.9"],
        12: ["playsound minecraft:block.bell.use master @a 128 88 85 4 0.75"],
        24: ["playsound minecraft:block.bell.use master @a 128 88 85 4 0.9"],
        36: ["playsound minecraft:block.bell.resonate master @a 128 88 85 3 1"],
        50: [call("song/bridal"), *narr("♪ 結婚行進曲 ♪", "light_purple", True)],
        60: ["execute positioned 128.5 70 70 run particle minecraft:cherry_leaves ~ ~ ~ 6 3 10 0 120 force"],
        120: ["execute positioned 128.5 70 70 run particle minecraft:cherry_leaves ~ ~ ~ 6 3 10 0 120 force", sset("#lock", 0)],
        200: ["execute positioned 128.5 70 70 run particle minecraft:cherry_leaves ~ ~ ~ 6 3 10 0 120 force"],
    }))
    # 23 priest
    add_step(Step("神父の誓いの言葉", t0=[sset("#lock", 1)], tl={
        1: say("priest", "病めるときも、健やかなるときも、", dur=80),
        80: say("priest", "整地するときも、クリーパーに爆破されたときも……", dur=90),
        170: say("priest", "……誓いますか？", dur=80, big=True),
        250: title(HERO, T("「誓います」", color="green", bold=True), T("（声で言ってね）", color="white"), (5, 60, 10)) +
             [tellraw("@a", T("主人公", color="green", bold=True), T("「誓います」", color="white"))],
        260: [sset("#lock", 0)],
    }))
    # 24 heroine vows + fireworks
    add_step(Step("ヒロイン「誓います♡」と花火", t0=[sset("#lock", 1)], tl={
        1: say("heroine", "誓います♡", dur=80, big=True) + [particles_heart("@e[type=mannequin,tag=rufu_npc_heroine]", 20)],
        20: [firework(124.5, 66, 70.5), firework(132.5, 66, 70.5), gsound("entity.villager.celebrate", 1, 1.3)],
        35: [firework(126.5, 66, 76.5, colors=(0xFFD700, 0xFFFFFF)), firework(130.5, 66, 76.5, colors=(0x9AD9FF, 0xFFFFFF))],
        50: [firework(128.5, 66, 66.5, colors=(0xFF5FA2,), shape="star"), sset("#lock", 0)],
    }))
    # 25
    add_step(Step("神父「それでは、誓いのキスを」", t0=[sset("#lock", 1)], tl={
        1: say("priest", "それでは、誓いのキスを。", dur=90, big=True),
        30: [sset("#lock", 0)],
    }))
    # 26 approach
    approach = {}
    for i in range(1, 31):
        x = WX - (WX - HX - 0.75) * i / 30
        approach[i] = [f"tp @e[type=mannequin,tag=rufu_npc_heroine] {x:.3f} {WY} {WZ} 90 0"]
    approach[1] += say("heroine", "ん～～～♡", dur=120, big=True)
    for t in (5, 15, 25, 35):
        approach.setdefault(t, []).append(particles_heart("@e[type=mannequin,tag=rufu_npc_heroine]", 6))
        approach[t].append("execute at @e[type=mannequin,tag=rufu_npc_heroine] run playsound minecraft:entity.allay.ambient_with_item voice @a ~ ~ ~ 1 0.7")
    approach[40] = [sset("#lock", 0)]
    add_step(Step("ヒロインが近づく「ん～～～♡」", t0=[sset("#lock", 1), f"tp @a[tag=rufu_hero] {HX} {HY} {HZ} -90 0"], tl=approach))
    # 27 objection!
    add_step(Step("「ちょっと待ったーー！！」", t0=[sset("#lock", 1),
        "title @a times 0 50 10",
        f"title @a subtitle {snbt(T(''))}",
        f"title @a title {snbt(T('ちょっと待ったーー！！', color='red', bold=True))}",
        gsound("entity.ravager.roar", 1, 1.2), gsound("block.bell.use", 1, 0.5), gsound("entity.lightning_bolt.thunder", 0.6, 1.4),
        tellraw("@a", T("？？？", color="red", bold=True), T("「ちょっと待ったーー！！」", color="white", bold=True)),
        f"tp @e[type=mannequin,tag=rufu_npc_heroine] {WX} {WY} {WZ} 90 0",
    ], tl={
        12: [f"execute as @a[tag=rufu_p] run rotate @s facing 128.5 84 71.5", "execute as @e[type=mannequin,tag=rufu_npc] at @s run tp @s ~ ~ ~ facing 128.5 84 71.5",
             gsound("entity.player.attack.sweep", 1, 0.6)],
        20: [sset("#lock", 0)],
    }))
    # 28 roof explodes + Leon
    frames = leon_flight()
    tl = {
        1: [f"particle minecraft:explosion_emitter 128.5 86 71.5 2 1 2 0 4 force",
            f"particle minecraft:large_smoke 128.5 84 71.5 4 2 4 0.05 80 force",
            gsound("entity.generic.explode", 1, 0.8), gsound("entity.dragon_fireball.explode", 0.6, 1.0),
            f"fill {hole['x0']} 77 {hole['z0']} {hole['x1']} 90 {hole['z1']} minecraft:air"],
    }
    for k in range(6):
        vx = round(math.cos(k) * 0.35, 3)
        vz = round(math.sin(k) * 0.35, 3)
        tl[1].append(f"summon minecraft:falling_block 128.5 84 71.5 " + snbt({
            "BlockState": "minecraft:deepslate_tiles", "Time": 1, "DropItem": False, "CancelDrop": True, "HurtEntities": False,
            "Motion": [d(vx), d(0.6), d(vz)], "Tags": ["rufu_debris"]}))
    tl[18] = ["kill @e[type=falling_block,tag=rufu_debris]", "particle minecraft:poof 128.5 72 71.5 4 2 4 0.02 40 force"]
    tl[4] = npc_spawn("leon", *frames[0], 200, outfit="leon_fly", look=False,
                      extra={"pose": "fall_flying", "NoGravity": True}) + [gsound("item.elytra.flying", 1, 1.2)]
    for i, p in enumerate(frames):
        tl.setdefault(5 + i, []).append(f"execute as @e[type=mannequin,tag=rufu_npc_leon] at @s run tp @s {p[0]:.2f} {p[1]:.2f} {p[2]:.2f} facing {p[0] + (0 if i + 1 >= len(frames) else frames[i + 1][0] - p[0]) * 3:.2f} {p[1]:.2f} {p[2] + (0.5 if i + 1 >= len(frames) else frames[i + 1][2] - p[2]) * 3 + 0.01:.2f}")
    land = 6 + len(frames)
    tl[land] = ["data merge entity @e[type=mannequin,tag=rufu_npc_leon,limit=1] {pose:\"standing\",NoGravity:false,equipment:" + snbt(OUTFITS["leon"]) + "}",
                "tp @e[type=mannequin,tag=rufu_npc_leon] 128.5 65 73.5 180 0",
                "particle minecraft:cloud 128.5 65.2 73.5 0.6 0.1 0.6 0.05 20 force",
                gsound("entity.player.big_fall", 1, 0.8)]
    tl[land + 10] = say("leon", "その結婚、ちょっと待った！", dur=80, big=True)
    tl[land + 90] = say("leon", "迎えに来たぜ。", dur=80) + ["tag @e[type=mannequin,tag=rufu_npc_leon] add rufu_look", sset("#lock", 0)]
    add_step(Step("屋根が爆発して元彼レオンがエリトラで乱入", t0=[sset("#lock", 1)], tl=tl))
    # 29 heroine -> love drains
    drain = {1: say("heroine", "レオンくん……！", dur=100, big=True) + ["execute as @e[type=mannequin,tag=rufu_npc_heroine] at @s run tp @s ~ ~ ~ facing 128.5 66 73.5"]}
    for i in range(10):
        drain[30 + i * 4] = [sadd("#love", -10), call("hud/love"),
                             f"execute as @a at @s run playsound minecraft:block.note_block.bass master @s ~ ~ ~ 1 {round(1.2 - i * 0.07, 3)}"]
    drain[72] = [sset("#love", 0), call("hud/love"), gsound("entity.zombie_villager.cure", 0.6, 0.8),
                 tellraw("@a", T("💔 好感度が 0 になった", color="red", bold=True)), sset("#lock", 0)]
    add_step(Step("ヒロイン「レオンくん……！」好感度が0に", t0=[sset("#lock", 1)], tl=drain))
    # 30 storm
    add_step(Step("「こっちにする」→ 雷雨", t0=[sset("#lock", 1)], tl={
        1: say("heroine", "……こっちにする。", dur=90, big=True),
        30: ["weather thunder", "summon minecraft:lightning_bolt 100 65 70", "summon minecraft:lightning_bolt 155 65 95",
             gsound("entity.lightning_bolt.thunder", 1, 0.8), call("song/sad")],
        60: ["summon minecraft:lightning_bolt 112 65 60", sset("#lock", 0)],
        100: ["summon minecraft:lightning_bolt 145 65 72"],
    }))
    # 31 escape on pigs
    add_step(Step("豚でのろのろ逃走（追いつけない）", t0=[sset("#lock", 1),
        "kill @e[tag=rufu_pig]",
        "summon minecraft:pig 128.5 65 74.5 {Tags:[\"rufu_pig\",\"rufu_pig1\"],NoAI:true,Invulnerable:true,PersistenceRequired:true,equipment:{saddle:{id:\"minecraft:saddle\",count:1}},Rotation:[0f,0f]}",
        "summon minecraft:pig 128.5 65 72.5 {Tags:[\"rufu_pig\",\"rufu_pig2\"],NoAI:true,Invulnerable:true,PersistenceRequired:true,equipment:{saddle:{id:\"minecraft:saddle\",count:1}},Rotation:[0f,0f]}",
        "ride @e[type=mannequin,tag=rufu_npc_heroine,limit=1] mount @e[type=pig,tag=rufu_pig1,limit=1]",
        "ride @e[type=mannequin,tag=rufu_npc_leon,limit=1] mount @e[type=pig,tag=rufu_pig2,limit=1]",
        "tag @e[type=mannequin,tag=rufu_npc_heroine] remove rufu_look",
        "tag @e[type=mannequin,tag=rufu_npc_leon] remove rufu_look",
        "kill @e[type=item_display,tag=rufu_seat]",
        "kill @e[type=marker,tag=rufu_pigwp]",
        "summon minecraft:marker 128.5 65 89.5 {Tags:[\"rufu_pigwp\"]}",
        sset("#pigwp", 1), sset("#fx", 1),
    ], tl={
        2: say("leon", "行くぜ、しっかりつかまってな！", dur=70),
        60: say("heroine", "じゃあね～♡", dur=60, sub_title=False),
        80: [sset("#lock", 0), tellraw(GM, T("[GM] 豚が門に着くと自動でネザーゲートへ。終わったら「次へ」", color="gray"))],
    }))
    pr = pig_route()
    fn("fx/tick",
       f"execute if score #fx rufu matches 1 run {call('wed/pig_tick')}",
       f"execute if score #fx rufu matches 2 run {call('end/ghast_tick')}")
    fn("wed/pig_tick",
       "execute as @e[type=pig,tag=rufu_pig] at @s facing entity @e[type=marker,tag=rufu_pigwp,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^0.12 facing ^ ^ ^5",
       f"execute as @e[type=pig,tag=rufu_pig1] at @s if entity @e[type=marker,tag=rufu_pigwp,distance=..0.4] run {call('wed/pig_next')}",
       "execute as @a[tag=rufu_p] at @s if entity @e[type=pig,tag=rufu_pig,distance=..4.5] facing entity @e[type=pig,tag=rufu_pig,sort=nearest,limit=1] feet rotated ~180 0 run tp @s ^ ^ ^0.6",
       "execute as @a[tag=rufu_p] at @s if entity @e[type=pig,tag=rufu_pig,distance=..6] run title @s actionbar {text:\"……なぜか追いつけない！\",color:\"gray\",italic:true}",
       "execute as @a[tag=rufu_p] at @s if entity @e[type=pig,tag=rufu_pig,distance=..6] run particle minecraft:sweep_attack ~ ~1 ~ 0.3 0.3 0.3 0 1",
       "execute if score #m20 rufu matches 0 at @e[type=pig,tag=rufu_pig] run playsound minecraft:entity.pig.ambient neutral @a ~ ~ ~ 1 0.8")
    nx = ["scoreboard players add #pigwp rufu 1"]
    for i, (x, z) in enumerate(pr[1:], start=2):
        if i - 1 < len(pr):
            pass
    for i in range(2, len(pr)):
        x, z = pr[i]
        nx.append(f"execute if score #pigwp rufu matches {i} run tp @e[type=marker,tag=rufu_pigwp] {x} 65 {z}")
    nx.append(f"execute if score #pigwp rufu matches {len(pr)}.. run {call('wed/portal')}")
    fn("wed/pig_next", *nx)
    P = PORTAL
    fn("wed/portal",
       sset("#fx", 0),
       "execute at @e[type=pig,tag=rufu_pig] run particle minecraft:portal ~ ~1 ~ 0.5 1 0.5 0.5 80 force",
       "playsound minecraft:block.portal.trigger master @a 151.5 66 60 2 1.4",
       "kill @e[tag=rufu_part_heroine]", "kill @e[tag=rufu_part_leon]", "kill @e[tag=rufu_pig]",
       tellraw("@a", T("（ふたりはネザーゲートの向こうへ消えた……）", color="dark_purple", italic=True)),
       f"schedule function rufu:wed/portal_boom 50t")
    fn("wed/portal_boom",
       f"particle minecraft:explosion_emitter 151.5 67 {P['z']} 1 1 1 0 3 force",
       "playsound minecraft:entity.generic.explode master @a 151.5 67 60 4 0.7",
       f"fill {P['x0']} {P['y0']} {P['z']} {P['x1']} {P['y1']} {P['z']} minecraft:air",
       f"fill {P['x0']} {P['y0']} {P['z']} {P['x1']} {P['y0']} {P['z']} minecraft:crying_obsidian",
       f"setblock {P['x0']} {P['y0'] + 1} {P['z']} minecraft:obsidian",
       *title("@a", T("ゲートが爆破された", color="dark_purple", bold=True), T("もう追いかけられない", color="gray"), (5, 50, 15)))


def ending_steps():
    girls = [("sakura", 124.5), ("mio", 128.5), ("hinata", 132.5)]
    add_step(Step("エンディング：神父「ハァン……」", retry=0, t0=[
        sset("#lock", 1), sset("#fx", 0), "kill @e[tag=rufu_pig]",
        "kill @e[tag=rufu_part_heroine]", "kill @e[tag=rufu_part_leon]",
        "effect give @a[tag=rufu_p] minecraft:blindness 2 0 true",
        f"tp @a[tag=rufu_p] 128.5 65 70.5 180 0",
        *npc_spawn("priest", AX, AY, AZ, 0, outfit="priest"),
        "weather rain",
    ], tl={
        30: say("priest", "ハァン……", dur=90, big=True) + [gsound("entity.villager.no", 1, 0.5)],
        60: [sset("#lock", 0)],
    }))
    add_step(Step("婚約指輪が「返品された指輪」に", t0=[
        sset("#lock", 1),
        "clear @a minecraft:gold_nugget[custom_data~{rufu_ring:1b}]",
        give(HERO, "gold_nugget", returned_ring_item()),
        *title("@a", T("💍 返品された指輪", color="gray", bold=True), T("返品理由：元彼が来たため", color="white"), (10, 80, 20)),
        gsound("block.note_block.didgeridoo", 1, 0.5),
        tellraw("@a", T("📦 婚約指輪が「返品された指輪」になった（返品理由：元彼が来たため）", color="gray")),
    ], tl={30: [sset("#lock", 0)]}))
    credits = [
        ("恋 ～結婚の試練～", "", "light_purple"),
        ("主演", {"selector": "@a[tag=rufu_hero]"}, "gold"),
        ("友人代表", {"selector": "@a[tag=rufu_helper]"}, "gold"),
        ("ヒロイン", {"selector": NB}, "light_purple"),
        ("元彼", "レオン", "aqua"),
        ("神父", "神父（ハァン……）", "gold"),
        ("キツネ", "キツネのみなさん", "gold"),
        ("町の人々", "このへんの村人", "gray"),
        ("企画・仕掛け人", "Rufu", "red"),
        ("END", "ノーマルエンド：返品", "white"),
    ]
    tl = {}
    t = 5
    for (a, b_, col) in credits:
        subc = b_ if isinstance(b_, dict) else T(b_, color="white")
        if isinstance(b_, dict):
            subc = dict(b_)
            subc["color"] = "white"
        tl[t] = ["title @a times 15 50 15", f"title @a subtitle {snbt(subc)}", f"title @a title {snbt(T(a, color=col, bold=True))}",
                 tellraw("@a", T(f"  {a}  ", color=col, bold=True), subc)]
        t += 80
    tl[5] += ["effect give @a minecraft:darkness 30 0 true", call("song/bridal"), "weather clear"]
    tl[t - 80] += [gsound("ui.toast.challenge_complete", 1, 0.6)]
    tl[t + 10] = [sset("#lock", 0), "effect clear @a minecraft:darkness"]
    add_step(Step("スタッフロール →「END ノーマルエンド：返品」", t0=[sset("#lock", 1)], tl=tl))
    # update notice
    sp = []
    for (g, x) in girls:
        sp += npc_spawn(g, x, AY, AZ + 1.5, 0, outfit="casual", tags=("rufu_girl", f"rufu_g_{g}"))
        sp.append(f"summon minecraft:interaction {x} {AY} {AZ + 1.5} " + snbt({"Tags": ["rufu_click", "rufu_girl_hit", f"rufu_gh_{g}", f"rufu_part_{g}"],
                                                                               "width": f_(0.9), "height": f_(2.0), "response": True}))
    add_step(Step("アップデートのお知らせ：さくら・みお・ひなた実装", t0=[
        sset("#lock", 1), sset("#chosen", 0), "kill @e[tag=rufu_part_priest]",
        f"tp @a[tag=rufu_p] 128.5 65 68.5 180 0",
        "title @a times 10 70 20",
        f"title @a subtitle {snbt(T('さくら・みお・ひなたが実装されました！', color='white', bold=True))}",
        f"title @a title {snbt(T('📢 アップデートのお知らせ', color='aqua', bold=True))}",
        call("song/fanfare"),
        tellraw("@a", T("📢 アップデートのお知らせ：", color="aqua", bold=True), T("さくら・みお・ひなたが実装されました！", color="white")),
    ], tl={
        40: sp + ["execute as @e[type=mannequin,tag=rufu_girl] at @s run particle minecraft:end_rod ~ ~1 ~ 0.4 1 0.4 0.05 30 force",
                  gsound("entity.player.levelup", 1, 1.4)],
        60: say("sakura", "はじめまして♡", dur=60, sub_title=False),
        75: say("mio", "よろしくね。", dur=60, sub_title=False),
        90: say("hinata", "えらんで、えらんで！", dur=60, sub_title=False),
        110: title(HERO, T("1人えらんで右クリック", color="light_purple", bold=True), T("さくら・みお・ひなた", color="white"), (5, 80, 10)) +
             [tellraw("@a", T("👉 主人公は気になる子を右クリックで選んでね", color="light_purple")), sset("#lock", 0)],
    }))
    fn("end/girl_pre",
       *[f"execute if entity @s[tag=rufu_gh_{g}] run scoreboard players set #hitg rufu {i + 1}" for i, (g, x) in enumerate(girls)],
       f"execute as @a[tag=rufu_clicker,limit=1] run {call('end/girl_click')}")
    fn("end/girl_click",
       f"execute unless entity @s[tag=rufu_hero] run return run {sub('end', tellraw('@s', T('選ぶのは主人公です', color='gray')))}",
       f"execute if score #chosen rufu matches 1.. run return run {sub('end', tellraw('@s', T('もう選んだよ', color='gray')))}",
       "scoreboard players operation #chosen rufu = #hitg rufu",
       *[run_block(f"if score #chosen rufu matches {i + 1}", [particles_heart(f"@e[type=mannequin,tag=rufu_npc_{g}]", 15),
                                                           tellraw("@a", T(f"💗 主人公は {SPEAKERS[g]['name']} を選んだ！", color="light_purple", bold=True))], "end")
         for i, (g, x) in enumerate(girls)],
       "playsound minecraft:entity.player.levelup master @a ~ ~ ~ 1 1.6",
       tellraw(GM, T("[GM] 選ばれました。「次へ」で『やっと選んでくれたね……』", color="green")))
    # note: click/got removes interaction data before dispatch, so record which one was hit there
    chosen_lines = [f"execute if score #chosen rufu matches 0 run {rnd('#chosen', 1, 3)}"]
    for i, (g, x) in enumerate(girls):
        chosen_lines.append(run_block(f"if score #chosen rufu matches {i + 1}", say(g, "やっと選んでくれたね……", dur=100, big=True), "end"))
    add_step(Step("選ばれた子「やっと選んでくれたね……」", t0=[sset("#lock", 1), *chosen_lines], tl={30: [sset("#lock", 0)]}))
    add_step(Step("3人「……でもね」「実は私たち……」", t0=[sset("#lock", 1)], tl={
        1: say("sakura", "……でもね", dur=60),
        50: say("mio", "実は私たち……", dur=70),
        110: say("hinata", "……ふふっ", dur=60),
        150: [sset("#lock", 0)],
    }))
    tr = {1: [*[f"execute at @e[type=mannequin,tag=rufu_npc_{g}] run particle minecraft:large_smoke ~ ~1 ~ 0.5 1 0.5 0.05 60 force" for g, x in girls],
              gsound("entity.illusioner.cast_spell", 1, 1.0), gsound("entity.evoker.prepare_summon", 1, 1.2)]}
    tr[20] = []
    for i, (g, x) in enumerate(girls):
        tr[20] += [f"kill @e[tag=rufu_part_{g}]"]
        tr[20] += [f"summon minecraft:mannequin {x} {AY} {AZ + 1.5} " + snbt({
            "profile": {"texture": SKINS["heroine"][0], "model": "slim"}, "CustomName": T("ヒロイン", color="light_purple", bold=True),
            "CustomNameVisible": True, "hide_description": True, "immovable": True, "Invulnerable": True, "Silent": True,
            "Rotation": [f_(0.0), f_(0.0)], "Tags": ["rufu_npc", "rufu_look", "rufu_clone", f"rufu_clone{i + 1}", "rufu_part_clones"],
            "equipment": OUTFITS["casual"]})]
        tr[20] += [f"data modify entity @e[type=mannequin,tag=rufu_clone{i + 1},limit=1] CustomName set from entity {NB} CustomName"]
    tr[22] = [*[f"execute at @e[type=mannequin,tag=rufu_clone] run particle minecraft:heart ~ ~2 ~ 0.4 0.3 0.4 0 8 force"],
              *title("@a", T("3人ともヒロインに変身！", color="light_purple", bold=True), T("", color="white"), (0, 60, 10)),
              gsound("entity.allay.ambient_without_item", 1, 1.0)]
    tr[40] = [tellraw("@a", T("ヒロイン×3", color="light_purple", bold=True), T("「「「じゃーん♡」」」", color="white")),
              "title @a times 3 60 10", f"title @a subtitle {snbt(T('ヒロイン×3：「「「じゃーん♡」」」', color='light_purple'))}", f"title @a title {snbt(T(''))}"]
    tr[60] = [sset("#lock", 0)]
    add_step(Step("3人ともヒロインに変身", t0=[sset("#lock", 1)], tl=tr))
    # happy ghast
    gh = {
        1: ["kill @e[tag=rufu_ghast]",
            "summon minecraft:happy_ghast 128.5 100 70.5 " + snbt({"Tags": ["rufu_ghast"], "NoAI": True, "NoGravity": True, "Invulnerable": True, "PersistenceRequired": True,
                                                                  "equipment": {"body": {"id": "minecraft:pink_harness", "count": 1}}, "Rotation": [f_(0.0), f_(0.0)]}),
            *npc_spawn("leon", 128.5, 101, 70.5, 0, outfit="leon", look=False),
            "ride @e[type=mannequin,tag=rufu_npc_leon,limit=1] mount @e[type=happy_ghast,tag=rufu_ghast,limit=1]",
            sset("#fx", 2), sset("#ghy", 0),
            gsound("entity.happy_ghast.ambient", 1, 1.0)],
        70: say("leon", "よっ。迎えに来たぜ、お前ら。", dur=100, big=True),
        100: [sset("#lock", 0)],
    }
    add_step(Step("元彼がハッピーガストで天窓から登場", t0=[sset("#lock", 1)], tl=gh))
    fn("end/ghast_tick",
       "execute if score #ghy rufu matches 0 as @e[type=happy_ghast,tag=rufu_ghast] at @s if entity @s[y=73,dy=100] run tp @s ~ ~-0.35 ~",
       "execute if score #ghy rufu matches 1 as @e[type=happy_ghast,tag=rufu_ghast] at @s run tp @s ~0.05 ~0.3 ~-0.12",
       "execute if score #ghy rufu matches 1 as @e[type=happy_ghast,tag=rufu_ghast] at @s if entity @s[y=160,dy=100] run kill @e[tag=rufu_part_leon]",
       "execute if score #ghy rufu matches 1 as @e[type=happy_ghast,tag=rufu_ghast] at @s if entity @s[y=160,dy=100] run kill @e[tag=rufu_clone]",
       "execute if score #ghy rufu matches 1 as @e[type=happy_ghast,tag=rufu_ghast] at @s if entity @s[y=160,dy=100] run kill @s")
    add_step(Step("「じゃ、全員もらってくわ」で空へ", t0=[sset("#lock", 1)], tl={
        1: say("leon", "じゃ、全員もらってくわ。", dur=90, big=True),
        30: ["ride @e[type=mannequin,tag=rufu_clone1,limit=1] mount @e[type=happy_ghast,tag=rufu_ghast,limit=1]",
             "ride @e[type=mannequin,tag=rufu_clone2,limit=1] mount @e[type=happy_ghast,tag=rufu_ghast,limit=1]",
             "ride @e[type=mannequin,tag=rufu_clone3,limit=1] mount @e[type=happy_ghast,tag=rufu_ghast,limit=1]",
             "tag @e[type=mannequin,tag=rufu_clone] remove rufu_look",
             "execute at @e[type=happy_ghast,tag=rufu_ghast] run particle minecraft:heart ~ ~2 ~ 1.5 1 1.5 0 20 force"],
        50: [sset("#ghy", 1), gsound("entity.happy_ghast.harness_goggles_down", 1, 1.0),
             tellraw("@a", T("ヒロイン×3", color="light_purple", bold=True), T("「「「ばいばーい♡」」」", color="white"))],
        120: [sset("#lock", 0)],
    }))
    fin = {
        1: ["kill @e[tag=rufu_part_leon]", "kill @e[tag=rufu_clone]", "kill @e[tag=rufu_ghast]", sset("#fx", 0),
            "title @a times 10 140 30",
            f"title @a subtitle {snbt(T('仕掛け人：Rufu', color='white', bold=True))}",
            f"title @a title {snbt(T('ドッキリ大成功！', color='gold', bold=True))}",
            tellraw("@a", T("🎉 ドッキリ大成功！ ", color="gold", bold=True), T("仕掛け人：Rufu", color="white", bold=True)),
            call("song/fanfare"), gsound("ui.toast.challenge_complete", 1, 1.0)],
    }
    spots = [(118.5, 95.5, 71.5), (138.5, 95.5, 71.5), (128.5, 98, 62.5), (128.5, 98, 82.5), (110.5, 92, 92.5), (146.5, 92, 92.5)]
    pal = [(0xFF6FB5, 0xFFFFFF), (0xFFD700, 0xFF8800), (0x7FDBFF, 0xFFFFFF), (0xB10DC9, 0xFF6FB5), (0x2ECC40, 0xFFFFFF)]
    for i in range(18):
        x, y, z = spots[i % len(spots)]
        c = pal[i % len(pal)]
        fin.setdefault(10 + i * 7, []).append(firework(x, y - 25, z, colors=c, shape=["large_ball", "star", "burst", "ball"][i % 4], life=25))
    fin[150] = [sset("#lock", 0), tellraw("@a", T("おわり。おつかれさまでした！", color="light_purple"))]
    add_step(Step("「ドッキリ大成功！ 仕掛け人：Rufu」で花火", retry=0, t0=[sset("#lock", 1), "weather clear", "time set 18000"], tl=fin))
