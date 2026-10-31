"""Mission 3 「結婚報告パレードで私についてきて」"""

from core import *  # noqa
from system import Step, add_step, event, ev_start
from mission import mission_begin, countdown_tl, clear_cmds, clear_title, evaluation_tl
from mc import T, snbt

SPEEDS = {1: 0.11, 2: 0.16, 3: 0.2, 4: 0.25, 5: 0.31, 6: 0.36}
# (x, z, speed, mode('f' forward / 'b' backwards), pause-before-moving, events)
LAP1 = [
    (128.5, 133.5, 2, "f", 0, []),
    (114.5, 128.5, 2, "f", 0, []),
    (104.5, 121.5, 2, "f", 0, ["zombies:88,121.5:3"]),
    (92.5, 121.5, 4, "f", 30, ["say:ちょっと急ぐね！"]),
    (84.5, 121.5, 2, "f", 0, ["anvil"]),
    (90.5, 121.5, 3, "f", 25, ["say:あ、忘れ物。"]),
    (80.5, 121.5, 2, "f", 15, ["say:……やっぱいいや。"]),
    (80.5, 129.5, 5, "f", 0, ["say:こっち！", "creeper:80.5,133.5"]),
    (80.5, 136.5, 2, "f", 0, []),
    (63.5, 136.5, 1, "b", 25, ["say:ちゃんとついてきてる～？", "zombies:70,136.5:2"]),
    (63.5, 121.5, 2, "f", 20, ["anvil"]),
    (62.5, 112.5, 4, "f", 0, []),
    (62.5, 99.5, 2, "f", 30, ["zombies:58,92:2", "anvil"]),
    (64.5, 88.5, 3, "f", 0, []),
    (64.5, 77.5, 2, "f", 0, []),
]
LAP2 = [
    (64.5, 77.5, 3, "f", 0, []),
    (64.5, 88.5, 3, "f", 0, []),
    (62.5, 99.5, 4, "f", 0, ["zombies:62.5,108:3"]),
    (62.5, 112.5, 3, "f", 20, ["lightning"]),
    (62.5, 121.5, 3, "f", 0, []),
    (50.5, 121.5, 5, "f", 0, ["say:近道しよっか♪", "creeper:50.5,140"]),
    (50.5, 136.5, 3, "f", 0, ["zombies:50.5,150:3"]),
    (50.5, 160.5, 4, "f", 25, ["lightning"]),
    (86.5, 160.5, 3, "f", 0, ["zombies:75,160.5:3", "say:暗いね～。こわーい。"]),
    (86.5, 136.5, 5, "f", 0, ["creeper:86.5,145", "lightning"]),
    (63.5, 136.5, 2, "b", 20, ["say:ほらほら、離れないで？", "zombies:72,136.5:2"]),
    (63.5, 121.5, 4, "f", 0, ["lightning"]),
    (62.5, 112.5, 3, "f", 25, ["zombies:62.5,104:3"]),
    (62.5, 99.5, 5, "f", 0, ["anvil"]),
    (64.5, 88.5, 3, "f", 0, []),
    (64.5, 77.5, 2, "f", 0, []),
]
M3_START = (128.5, 65, 137.5)


def mob_cmds(spec):
    kind, _, rest = spec.partition(":")
    out = []
    if kind == "zombies":
        pos, _, n = rest.rpartition(":")
        x, z = map(float, pos.split(","))
        for i in range(int(n)):
            dx = (i - (int(n) - 1) / 2) * 1.5
            out.append(f"summon minecraft:zombie {x + dx} 65 {z} " + snbt({
                "Tags": ["rufu_mob"], "PersistenceRequired": True, "IsBaby": False, "CanPickUpLoot": False,
                "equipment": {"head": {"id": "minecraft:leather_helmet", "count": 1}}, "drop_chances": {"head": f_(0.0)},
                "attributes": [{"id": "minecraft:spawn_reinforcements", "base": d(0.0)}]}))
        out.append(f"particle minecraft:large_smoke {x} 66 {z} 1.5 0.5 1.5 0.02 30 force")
        out.append(tellraw("@a[tag=rufu_p]", T("🧟 ゾンビの群れだ！ 距離を保ちながら戦え！", color="dark_green")))
    elif kind == "creeper":
        x, z = map(float, rest.split(","))
        out.append(f"summon minecraft:creeper {x} 65 {z} " + snbt({"Tags": ["rufu_mob"], "PersistenceRequired": True, "ExplosionRadius": b(2)}))
        out.append(tellraw("@a[tag=rufu_p]", T("💥 クリーパー注意！", color="green")))
    elif kind == "anvil":
        out.append(f"execute as @r[tag=rufu_p,gamemode=!spectator] at @s run {call('m3/anvil')}")
    elif kind == "lightning":
        out.append(f"execute as @r[tag=rufu_p,gamemode=!spectator] at @s run {call('m3/lightning')}")
    elif kind == "say":
        out += say("heroine", rest, dur=60, sub_title=False)
    return out


def build_m3(top_y):
    # skeletons on the roofs along the main street (lap 1) / more at night (lap 2)
    sk1 = [(70, 110), (86, 110), (44, 110), (56, 130), (72, 130), (40, 130)]
    sk2 = sk1 + [(45, 145), (68, 145), (78, 152), (40, 165), (60, 167), (80, 166)]

    def skel(points):
        out = []
        for (x, z) in points:
            y = top_y(x, z) + 1
            out.append(f"summon minecraft:skeleton {x + 0.5} {y} {z + 0.5} " + snbt({
                "Tags": ["rufu_mob"], "PersistenceRequired": True, "CanPickUpLoot": False,
                "equipment": {"head": {"id": "minecraft:iron_helmet", "count": 1}, "mainhand": {"id": "minecraft:bow", "count": 1}},
                "drop_chances": {"head": f_(0.0), "mainhand": f_(0.0)},
                "attributes": [{"id": "minecraft:follow_range", "base": d(24.0)}]}))
        return out

    fn("m3/skel1", *skel(sk1))
    fn("m3/skel2", *skel(sk2))

    # ------------------------------------------------------------ movement
    mv = ["execute if score #pause rufu matches 1.. run return run scoreboard players remove #pause rufu 1",
          f"execute if entity @e[type=marker,tag=rufu_wpm,distance=..0.4] run return run {call('m3/arrive')}"]
    for k, v in SPEEDS.items():
        mv.append(f"execute if score #spd rufu matches {k} if score #mode rufu matches 0 facing entity @e[type=marker,tag=rufu_wpm,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^{v} facing ^ ^ ^5")
        mv.append(f"execute if score #spd rufu matches {k} if score #mode rufu matches 1 facing entity @e[type=marker,tag=rufu_wpm,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^{v} facing ^ ^ ^-5")
    mv.append("execute if score #spd rufu matches 5.. run particle minecraft:cloud ~ ~0.1 ~ 0.2 0 0.2 0 1")
    fn("m3/move", *mv)
    fn("m3/arrive",
       "execute positioned as @e[type=marker,tag=rufu_wpm,limit=1] run tp @s ~ ~ ~",
       sadd("#wp", 1),
       call("m3/wp_go"))
    go = []
    for lap, route in ((1, LAP1), (2, LAP2)):
        n = len(route)
        for k in range(1, n):
            x, z, spd, mode, pause, evs = route[k]
            cmds = [f"tp @e[type=marker,tag=rufu_wpm] {x} 65 {z}", sset("#spd", spd + (1 if lap == 2 and spd < 6 else 0)),
                    sset("#mode", 0 if mode == "f" else 1), sset("#pause", pause)]
            for e in evs:
                cmds += mob_cmds(e)
            fn(f"m3/l{lap}/{k}", *cmds)
            go.append(f"execute if score #lap rufu matches {lap} if score #wp rufu matches {k} run return run {call(f'm3/l{lap}/{k}')}")
        go.append(f"execute if score #lap rufu matches {lap} if score #wp rufu matches {n}.. run return run {call(f'm3/lap_end{lap}')}")
    fn("m3/wp_go", *go)

    # ------------------------------------------------------------ hazards
    fn("m3/anvil",
       "playsound minecraft:block.anvil.place master @a ~ ~ ~ 1 2",
       *title("@s", T(""), T("⚠ 頭上注意！", color="red", bold=True), (0, 20, 5)),
       rnd("#r", 0, 3),
       "execute if score #r rufu matches 0 run summon minecraft:falling_block ~1 ~14 ~ {BlockState:\"minecraft:anvil\",Time:1,DropItem:false,HurtEntities:true,FallHurtMax:6,FallHurtAmount:1.0f,CancelDrop:true,Tags:[\"rufu_mob\"]}",
       "execute if score #r rufu matches 1 run summon minecraft:falling_block ~-1 ~14 ~ {BlockState:\"minecraft:anvil\",Time:1,DropItem:false,HurtEntities:true,FallHurtMax:6,FallHurtAmount:1.0f,CancelDrop:true,Tags:[\"rufu_mob\"]}",
       "execute if score #r rufu matches 2 run summon minecraft:falling_block ~ ~14 ~1 {BlockState:\"minecraft:anvil\",Time:1,DropItem:false,HurtEntities:true,FallHurtMax:6,FallHurtAmount:1.0f,CancelDrop:true,Tags:[\"rufu_mob\"]}",
       "execute if score #r rufu matches 3 run summon minecraft:falling_block ~ ~14 ~ {BlockState:\"minecraft:anvil\",Time:1,DropItem:false,HurtEntities:true,FallHurtMax:6,FallHurtAmount:1.0f,CancelDrop:true,Tags:[\"rufu_mob\"]}")
    fn("m3/lightning",
       rnd("#r", 0, 3),
       "execute if score #r rufu matches 0 run summon minecraft:lightning_bolt ~3 ~ ~2",
       "execute if score #r rufu matches 1 run summon minecraft:lightning_bolt ~-3 ~ ~1",
       "execute if score #r rufu matches 2 run summon minecraft:lightning_bolt ~2 ~ ~-3",
       "execute if score #r rufu matches 3 run summon minecraft:lightning_bolt ~1 ~ ~2")

    # ------------------------------------------------------------ distance gauge
    dist = ["scoreboard players set @s rufu.d 9"]
    for k in range(8, 0, -1):
        dist.append(f"execute if entity @e[type=mannequin,tag=rufu_npc_heroine,distance=..{k}] run scoreboard players set @s rufu.d {k}")
    fn("m3/dist", *dist)
    bars = []
    for dd in range(1, 10):
        parts = [T("ヒロインとの距離 ", color="white")]
        for i in range(1, 10):
            ok = 3 <= i <= 5
            if i == dd:
                parts.append(T("◆", color="white" if ok else "red", bold=True))
            else:
                parts.append(T("■", color="dark_green" if ok else "dark_gray"))
        if dd <= 2:
            parts.append(T("  近すぎ！", color="red", bold=True))
        elif dd >= 6:
            parts.append(T("  離れすぎ！", color="red", bold=True))
        else:
            parts.append(T("  OK", color="green", bold=True))
        bars.append(f"title @s[scores={{rufu.d={dd}}}] actionbar {snbt(T('', extra=parts))}")
    fn("m3/bar", *bars)
    fn("m3/judge",
       sset("#outnow", 0),
       f"execute as @a[tag=rufu_p,gamemode=!spectator] at @s unless entity @e[type=mannequin,tag=rufu_npc_heroine,distance=2..5] run scoreboard players set #outnow rufu 1",
       "execute if score #outnow rufu matches 1 run scoreboard players add #outg rufu 2",
       "execute if score #outnow rufu matches 0 if score #outg rufu matches 1.. run scoreboard players remove #outg rufu 1",
       "execute store result bossbar rufu:out value run scoreboard players get #outg rufu",
       f"execute if score #outg rufu matches 200.. run return run {call('mission/fail/out')}")
    fn("m3/tick",
       "execute unless score #active rufu matches 1 run return 0",
       f"execute as @e[type=mannequin,tag=rufu_npc_heroine,limit=1] at @s run {call('m3/move')}",
       call("m3/judge"),
       f"execute as @a[tag=rufu_p] at @s run {call('m3/dist')}",
       f"execute as @a[tag=rufu_p] run {call('m3/bar')}")

    fn("m3/lap_end1", sset("#active", 0), sset("#lock", 0),
       "bossbar set rufu:time visible false", "bossbar set rufu:out visible false",
       "kill @e[tag=rufu_mob]", "kill @e[tag=rufu_ask]", sset("#intr_live", 0),
       "scoreboard players operation #t_total rufu += #elapsed rufu",
       "effect give @a[tag=rufu_p] minecraft:resistance infinite 4 true",
       "effect give @a[tag=rufu_p] minecraft:instant_health 1 10 true",
       "tag @e[type=mannequin,tag=rufu_npc_heroine] add rufu_look",
       ev_start("m3_lap1_end"))
    event("m3_lap1_end", {
        0: title("@a", T("ゴール！", color="gold", bold=True), T("公園に到着", color="white"), (5, 40, 10)) + [gsound("ui.toast.challenge_complete", 1, 1.2)],
        40: say("heroine", "……………", dur=60),
        60: [tellraw(GM, T("[GM] 1周目ゴール。「次へ」でオチ（この道じゃない方がよかった）", color="green"))],
    })
    fn("m3/lap_end2", *clear_cmds(), "tag @e[type=mannequin,tag=rufu_npc_heroine] add rufu_look", ev_start("m3_clear"))
    event("m3_clear", {
        0: clear_title(T("パレード2周、完走！", color="white")),
        40: say("heroine", "うん。こっちの道のほうが好き。", dur=80),
        60: [tellraw(GM, T("[GM] 試練3クリア！ 「次へ」で評価 → 丘の伝説の木へ", color="green"))],
    })


def lap_start(lap):
    route = LAP1 if lap == 1 else LAP2
    x, z = route[0][0], route[0][1]
    return [
        f"kill @e[type=marker,tag=rufu_wpm]",
        f"summon minecraft:marker {x} 65 {z} {{Tags:[\"rufu_wpm\"]}}",
        *npc_spawn("heroine", x, 65, z, 180 if lap == 1 else 0, look=False),
        sset("#lap", lap), sset("#wp", 0), sset("#pause", 0), sset("#spd", 2), sset("#mode", 0),
        sset("#outg", 0), "bossbar set rufu:out value 0", "bossbar set rufu:out players @a", "bossbar set rufu:out visible true",
        f"bossbar set rufu:out name {snbt(T('アウトゲージ（誰か1人でも2〜5ブロックから外れると たまる）', color='red'))}",
    ]


def m3_steps():
    sx, sy, sz = M3_START
    add_step(Step("試練3 説明「結婚報告パレード」", retry=0, t0=[
        sset("#mission", 0), sset("#lock", 1), "time set 6000",
        *npc_spawn("heroine", 128.5, 65, 133.5, 0),
        f"tp @a[tag=rufu_p] {sx} {sy} {sz} 180 0",
        *title("@a", T("試練3", color="gold", bold=True), T("結婚報告パレードで私についてきて", color="white"), (10, 70, 15)),
        gsound("block.note_block.bell", 1, 1.0),
    ], tl={
        30: say("heroine", "結婚報告パレード。町のみんなに見せびらかすの。", dur=90),
        120: say("heroine", "私から2〜5ブロック、ずっとその距離でついてきて。近すぎても遠すぎてもダメ。", dur=110),
        230: say("heroine", "ゴールは公園ね。じゃ、行こっか♡", dur=60) + [sset("#lock", 0)],
    }))
    add_step(Step("試練3 開始（1周目・昼）", retry="self", mission=3, t0=[
        *mission_begin(3, 3600, 400, 1100, M3_START),
        "time set 6000", "weather clear",
        *lap_start(1),
        f"tp @a[tag=rufu_p] {sx} {sy} {sz} 180 0",
        call("m3/skel1"),
    ], tl=countdown_tl([sset("#wp", 1), call("m3/wp_go")], "パレード開始！")))
    night = {}
    for t in range(40, 80):
        night[t] = ["time add 300"]
    night[1] = say("heroine", "……この道じゃない方がよかった。", dur=100, big=True) + [gsound("block.note_block.didgeridoo", 1, 0.7)]
    night[80] = ["time set 18000", gsound("entity.wolf.howl", 0.6, 1.0) if False else gsound("ambient.cave", 1, 1.0)]
    night[90] = say("heroine", "夜の裏通りで、もう一周ね。今度はもっと速く歩くから。", dur=100)
    night[190] = [sset("#lock", 0)]
    add_step(Step("オチ「この道じゃない方がよかった」→夜", t0=[sset("#lock", 1)], tl=night))
    add_step(Step("試練3 2周目開始（夜・裏通り）", t0=[
        sset("#mission", 3), sset("#active", 0), sset("#lock", 1),
        sset("#timer", 3600), "bossbar set rufu:time max 3600", "bossbar set rufu:time visible true", call("hud/time"),
        sset("#elapsed", 0), sset("#ask_t", 0), rnd("#intr_at", 300, 900),
        "scoreboard players set @a rufu.death 0",
        "effect clear @a[tag=rufu_p] minecraft:resistance",
        "time set 18000",
        "kill @e[tag=rufu_mob]",
        *lap_start(2),
        "execute as @e[type=mannequin,tag=rufu_npc_heroine] at @s run tp @a[tag=rufu_p] ~ ~ ~4",
        call("m3/skel2"),
    ], tl=countdown_tl([sset("#wp", 1), call("m3/wp_go")], "2周目スタート！")))
    add_step(Step("試練3 評価 → 丘の伝説の木へ", retry=0, t0=[sset("#lock", 1)], tl={
        **evaluation_tl("B", "道が気に入らなかった", "yellow"),
        130: say("heroine", "じゃ、最後。丘の上の伝説の木で待ってるね。", dur=80),
        200: ["effect give @a[tag=rufu_p] minecraft:blindness 3 0 true",
              *title("@a", T("～ 丘の上の伝説の木 ～", color="gold", bold=True), T("町を見下ろす丘", color="white"), (10, 50, 20))],
        215: [f"tp @a[tag=rufu_p] 195.5 81 95.5 180 0", *npc_spawn("heroine", 195.5, 81, 86.5, 0),
              "kill @e[type=marker,tag=rufu_wpm]", sset("#lock", 0)],
    }))
