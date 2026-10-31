"""Mission 4 「指輪を取り返して、伝説の木の下で告白して」 + result."""

from core import *  # noqa
from system import Step, add_step, event, ev_start
from mission import mission_begin, countdown_tl, clear_cmds, clear_title, evaluation_tl
from mc import T, snbt, item_components

HC = (HILL_C[0] + 0.5, 81, HILL_C[1] + 0.5)
CX, CY, CZ = CIRCLE
M4_SPAWN = (195.5, 81, 95.5)
HER_TREE = (195.5, 81, 85.5)
FOX_SPEED = {1: 0.27, 2: 0.31}
SIGN_SPEED = {1: 0.17, 2: 0.25}


def shovel():
    return item_components(name=T("🪏 宝さがしスコップ", color="yellow", italic=False),
                           lore=["地面の×印（荒い土）を掘れる", "丘には宝箱が3つ埋まっている"],
                           data={"rufu_m": b(1)}, can_break="minecraft:coarse_dirt", unbreakable=True)


def fox_nbt(real, tags):
    eq = {"mainhand": item_nbt("minecraft:gold_nugget", 1, ring_item())}
    return snbt({"Tags": ["rufu_fox", "rufu_mob4"] + list(tags) + (["rufu_fox_real"] if real else ["rufu_fox_fake"]),
                 "NoAI": True, "PersistenceRequired": True, "Silent": False, "Type": "red",
                 "attributes": [{"id": "minecraft:max_health", "base": d(1024.0)}], "Health": f_(1000.0),
                 "equipment": eq, "drop_chances": {"mainhand": f_(0.0)}})


def build_m4():
    hx, hy, hz = HC
    # ------------------------------------------------------------ reset
    tre = []
    chests = [
        [item_nbt("minecraft:sweet_berries", 4, item_components(name=T("🍓 スイートベリー", color="red", italic=False),
                                                                    lore=["手に持つと キツネが寄ってきて止まる…かも"], data={"rufu_m": b(1)}), slot=13)],
        [item_nbt("minecraft:poppy", 2, item_components(data={"rufu_m": b(1)}), slot=12),
         item_nbt("minecraft:dandelion", 1, item_components(data={"rufu_m": b(1)}), slot=14)],
        [item_nbt("minecraft:golden_apple", 1, item_components(name=T("ハズレ（でも金のリンゴ）", color="gold", italic=False), data={"rufu_m": b(1)}), slot=13)],
    ]
    for (x, z), items in zip(TREASURES, chests):
        tre += [f"setblock {x} {HILL_TOP - 1} {z} minecraft:air strict",
                f"setblock {x} {HILL_TOP - 1} {z} minecraft:chest[facing=south]{snbt({'Items': items})} strict",
                f"setblock {x} {HILL_TOP} {z} minecraft:coarse_dirt strict"]
    fn("m4/reset",
       "kill @e[tag=rufu_fox]", "kill @e[tag=rufu_mob4]", "kill @e[tag=rufu_sign]", "kill @e[tag=rufu_ringitem]",
       f"kill @e[type=item,x=168,y=70,z=52,dx=55,dy=40,dz=60]",
       "kill @e[type=marker,tag=rufu_m4m]",
       f"summon minecraft:marker {hx} 81 {hz} {{Tags:[\"rufu_hillc\",\"rufu_m4m\"]}}",
       f"summon minecraft:marker {TREE[0] + 1.0} 81 {TREE[1] + 1.0} {{Tags:[\"rufu_trunk\",\"rufu_m4m\"]}}",
       f"summon minecraft:marker {CX} 81 {CZ} {{Tags:[\"rufu_circ\",\"rufu_m4m\"]}}",
       *tre)

    # ------------------------------------------------------------ fox AI
    fox = [
        "execute store result score #h rufu run data get entity @s HurtTime",
        f"execute if score #h rufu matches 10 run return run {call('m4/fox_hit')}",
        f"execute if score @s rufu.fz matches 1.. run return run {call('m4/fox_frozen')}",
        "execute store result score #near rufu if entity @a[tag=rufu_p,gamemode=!spectator,distance=..3.2]",
        f"execute if score #near rufu >= #fox_need rufu run return run {call('m4/fox_freeze')}",
        f"execute if entity @a[tag=rufu_p,distance=..6,predicate=rufu:hold_berries] run return run {call('m4/fox_lured')}",
        f"execute if entity @a[tag=rufu_p,gamemode=!spectator,distance=..7] run return run {call('m4/fox_flee')}",
        call("m4/fox_wander"),
    ]
    fn("m4/fox", *fox)
    flee = []
    for k, v in FOX_SPEED.items():
        for rot in ("~180", "~110", "~-110", "~60", "~-60"):
            flee.append(f"execute if score #fspd rufu matches {k} facing entity @p[tag=rufu_p,gamemode=!spectator] feet rotated {rot} 0 positioned ^ ^ ^{v} positioned ~ 81 ~ "
                        f"if entity @e[type=marker,tag=rufu_hillc,distance=..11] unless entity @e[type=marker,tag=rufu_trunk,distance=..1.8] run return run tp @s ~ ~ ~ facing ^ ^ ^1")
    flee.append(call("m4/fox_blink"))
    fn("m4/fox_flee", *flee)
    fn("m4/fox_blink",
       "particle minecraft:poof ~ ~0.4 ~ 0.3 0.3 0.3 0.02 12 force",
       "playsound minecraft:entity.fox.teleport master @a ~ ~ ~ 1 1",
       "execute store result storage rufu:tmp a float 1 run random value 0..359",
       f"{call('m4/fox_blink_m')} with storage rufu:tmp",
       "execute at @s run particle minecraft:poof ~ ~0.4 ~ 0.3 0.3 0.3 0.02 12 force")
    fn("m4/fox_blink_m", f"$execute positioned {hx} 81 {hz} rotated $(a) 0 run tp @s ^ ^ ^7 facing ^ ^ ^12")
    fn("m4/fox_wander",
       "execute if score #m20 rufu matches 0 store result entity @s Rotation[0] float 1 run random value 0..359",
       f"execute rotated as @s rotated ~ 0 positioned ^ ^ ^0.07 if entity @e[type=marker,tag=rufu_hillc,distance=..10] unless entity @e[type=marker,tag=rufu_trunk,distance=..1.8] run tp @s ~ ~ ~")
    fn("m4/fox_lured",
       "tp @s ~ ~ ~ facing entity @p[tag=rufu_p,predicate=rufu:hold_berries]",
       "execute if score #m20 rufu matches 0 run particle minecraft:heart ~ ~0.8 ~ 0.2 0.2 0.2 0 1",
       "execute if score #m20 rufu matches 0 run playsound minecraft:entity.fox.sniff master @a ~ ~ ~ 1 1.2")
    fn("m4/fox_freeze",
       "scoreboard players set @s rufu.fz 50",
       "data merge entity @s {Glowing:true}",
       "playsound minecraft:entity.fox.screech master @a ~ ~ ~ 1 1.3",
       f"title @a[tag=rufu_p,distance=..10] actionbar {snbt(T('キツネが動けない！ 今のうちに叩け！', color='gold', bold=True))}")
    fn("m4/fox_frozen",
       "scoreboard players remove @s rufu.fz 1",
       "particle minecraft:crit ~ ~0.9 ~ 0.25 0.1 0.25 0 2",
       "execute if score @s rufu.fz matches 0 run data merge entity @s {Glowing:false}")
    fn("m4/fox_hit",
       "data modify entity @s Health set value 1000.0f",
       f"execute unless score @s rufu.fz matches 1.. run return run {sub('m4', 'playsound minecraft:entity.fox.aggro master @a ~ ~ ~ 1 1.4', call('m4/fox_blink'), tellraw('@a[tag=rufu_p,distance=..12]', T('ひらりとかわされた！ 2人以上で囲んで動きを止めよう', color='gray')))}",
       f"execute if entity @s[tag=rufu_fox_fake] run return run {call('m4/fox_fake')}",
       call("m4/fox_drop"))
    fn("m4/fox_fake",
       "particle minecraft:explosion ~ ~0.5 ~ 0.3 0.3 0.3 0 3 force",
       "summon minecraft:creeper ~ ~ ~ {Fuse:0s,ignited:true,ExplosionRadius:1b,Tags:[\"rufu_mob\"],Silent:true}",
       tellraw("@a", T("💥 偽物のキツネだった！", color="red", bold=True)),
       "kill @s")
    fn("m4/fox_drop",
       "summon minecraft:item ~ ~0.6 ~ " + snbt({"Item": item_nbt("minecraft:gold_nugget", 1, ring_item()), "PickupDelay": s_(10),
                                               "Age": s_(-32768), "Motion": [d(0.0), d(0.35), d(0.0)], "Tags": ["rufu_ringitem", "rufu_keep"], "Glowing": True}),
       "playsound minecraft:entity.fox.spit master @a ~ ~ ~ 1 1",
       "playsound minecraft:entity.player.levelup master @a ~ ~ ~ 1 1.6",
       "particle minecraft:end_rod ~ ~0.8 ~ 0.3 0.3 0.3 0.05 20 force",
       *title("@a[tag=rufu_p]", T("指輪を取り返した！", color="gold", bold=True), T("主人公が持って、3人全員で光る円へ！", color="white"), (5, 50, 10)),
       "execute at @e[tag=rufu_fox] run particle minecraft:poof ~ ~0.4 ~ 0.3 0.3 0.3 0.02 12 force",
       "kill @e[tag=rufu_fox]",
       sset("#m4p", 1))

    # ------------------------------------------------------------ circle & sign
    ring_hint = snbt(T("", extra=[T("💍 指輪を ", color="white"), T("主人公", color="green", bold=True),
                                  T(" が持って、3人全員で ", color="white"), T("木の下の光る円", color="gold", bold=True), T(" に入ろう", color="white")]))
    fn("m4/phase1",
       "execute store result score #hr rufu run clear @a[tag=rufu_hero,limit=1] minecraft:gold_nugget[custom_data~{rufu_ring:1b}] 0",
       f"execute positioned {CX} {CY} {CZ} store result score #inc rufu if entity @a[tag=rufu_p,distance=..{CIRCLE_R + 0.6}]",
       f"execute if score #hr rufu matches 1.. if score #inc rufu >= #np rufu run return run {call('m4/sign_spawn')}",
       f"execute if score #m20 rufu matches 0 run title @a[tag=rufu_p] actionbar {ring_hint}")
    fn("m4/sign_spawn",
       sset("#m4p", 2),
       "kill @e[tag=rufu_sign]",
       f"summon minecraft:text_display {CX + 2.5} 82.2 {CZ} " + snbt({
           "Tags": ["rufu_sign", "rufu_mob4"], "billboard": "center", "teleport_duration": 2,
           "text": T("", extra=[T("💍 結婚してください 💍", color="#d6246e", bold=True)]),
           "background": argb(235, 255, 245, 250), "line_width": 200,
           "transformation": {"translation": [f_(0.0), f_(0.0), f_(0.0)], "left_rotation": [f_(0.0), f_(0.0), f_(0.0), f_(1.0)],
                              "right_rotation": [f_(0.0), f_(0.0), f_(0.0), f_(1.0)], "scale": [f_(1.6), f_(1.6), f_(1.6)]}}),
       f"summon minecraft:interaction {CX + 2.5} 81.6 {CZ} " + snbt({"Tags": ["rufu_sign_hit", "rufu_click", "rufu_mob4"], "width": f_(1.5), "height": f_(1.3), "response": True}),
       *title("@a", T("告白タイム！", color="light_purple", bold=True), T("「結婚してください」の看板を主人公が右クリック！…でも逃げる", color="white"), (5, 60, 10)),
       gsound("block.note_block.chime", 1, 1.0), gsound("block.note_block.chime", 1, 1.5))
    sf = []
    for k, v in SIGN_SPEED.items():
        for rot in ("~180", "~120", "~-120", "~70", "~-70"):
            sf.append(f"execute if score #sspd rufu matches {k} facing entity @p[tag=rufu_hero] feet rotated {rot} 0 positioned ^ ^ ^{v} positioned ~ 82.2 ~ "
                      f"if entity @e[type=marker,tag=rufu_circ,distance=..{CIRCLE_R - 0.4}] run return run tp @s ~ ~ ~")
    sf.append(f"execute positioned {CX} 82.2 {CZ} facing entity @p[tag=rufu_hero] feet rotated ~180 0 positioned ^ ^ ^3 run tp @s ~ ~ ~")
    sf.append("particle minecraft:poof ~ ~ ~ 0.2 0.2 0.2 0.01 4")
    fn("m4/sign_flee", *sf)
    fn("m4/sign_tick",
       "execute store result score #pin rufu if entity @a[tag=rufu_p,tag=!rufu_hero,gamemode=!spectator,distance=..2.3]",
       f"execute if score #pin rufu >= #pin_need rufu run return run {call('m4/sign_pinned')}",
       f"execute if entity @a[tag=rufu_hero,distance=..4.5] run {call('m4/sign_flee')}",
       "execute if score #m5 rufu matches 0 run particle minecraft:heart ~ ~0.6 ~ 0.4 0.2 0.1 0 1")
    fn("m4/sign_pinned",
       "execute if score #m5 rufu matches 0 run particle minecraft:crit ~ ~ ~ 0.5 0.3 0.1 0 3",
       f"execute if score #m20 rufu matches 0 run title @a[tag=rufu_p] actionbar {snbt(T('看板を押さえた！ 主人公、今だ！ 右クリック！', color='gold', bold=True))}")
    fn("m4/sign_click",
       f"execute unless entity @s[tag=rufu_hero] run return run {sub('m4', tellraw('@s', T('告白は主人公の役目！ 助っ人は看板を押さえよう（2人で近くに立つと止まる）', color='gray')))}",
       "execute store result score #hr rufu run clear @s minecraft:gold_nugget[custom_data~{rufu_ring:1b}] 0",
       f"execute if score #hr rufu matches 0 run return run {sub('m4', tellraw('@s', T('指輪を持っていない！', color='red')))}",
       f"execute positioned {CX} {CY} {CZ} store result score #inc rufu if entity @a[tag=rufu_p,distance=..{CIRCLE_R + 0.6}]",
       f"execute if score #inc rufu < #np rufu run return run {sub('m4', tellraw('@a[tag=rufu_p]', T('3人全員が光る円の中にいないと ダメ！', color='red', bold=True)), 'playsound minecraft:entity.villager.no master @a ~ ~ ~ 1 1')}",
       "clear @s minecraft:gold_nugget[custom_data~{rufu_ring:1b}] 1",
       "kill @e[tag=rufu_sign]", "kill @e[tag=rufu_sign_hit]",
       sset("#m4p", 3),
       f"execute if score #m4try rufu matches 1 run {call('m4/yes1')}",
       f"execute if score #m4try rufu matches 2 run {call('m4/yes2')}")
    fn("m4/yes1", *clear_cmds(), ev_start("m4_yes1"))
    fn("m4/yes2", *clear_cmds(), ev_start("m4_yes2"))
    event("m4_yes1", {
        0: title("@a", T("「結婚してください」", color="light_purple", bold=True), T("主人公が指輪をさしだした", color="white"), (5, 40, 10)),
        45: say("heroine", "はい！", dur=90, big=True) + [particles_heart("@e[type=mannequin,tag=rufu_npc_heroine]", 30),
                                                         gsound("entity.player.levelup", 1, 1.2), firework(CX, 82, CZ - 4),
                                                         firework(CX + 4, 82, CZ), firework(CX - 4, 82, CZ)],
        90: [tellraw(GM, T("[GM] 告白成功（1回目）。「次へ」で『やっぱりなかったことにして』", color="green"))],
    })
    event("m4_yes2", {
        0: title("@a", T("「結婚してください」", color="light_purple", bold=True), T("（2回目）", color="white"), (5, 40, 10)),
        45: say("heroine", "……1回目の方がよかった。でもいいよ。", dur=110, big=True) + [particles_heart("@e[type=mannequin,tag=rufu_npc_heroine]", 30),
                                                                                gsound("entity.player.levelup", 1, 1.0),
                                                                                firework(CX, 82, CZ - 4), firework(CX + 4, 82, CZ)],
        100: [tellraw(GM, T("[GM] 試練4クリア！ 「次へ」で総合評価", color="green"))],
    })

    # ------------------------------------------------------------ tick
    fn("m4/tick",
       "execute unless score #active rufu matches 1 run return 0",
       f"execute as @e[type=fox,tag=rufu_fox] at @s run {call('m4/fox')}",
       f"execute if score #m4p rufu matches 0 if score #m20 rufu matches 0 run title @a[tag=rufu_p] actionbar {snbt(T('🦊 指輪をくわえたキツネを 2人以上で囲んで止めて、叩け！', color='gold'))}",
       f"execute if score #m4p rufu matches 1 run {call('m4/phase1')}",
       f"execute if score #m4p rufu matches 2 as @e[type=text_display,tag=rufu_sign,limit=1] at @s run {call('m4/sign_tick')}",
       f"execute if score #m4p rufu matches 2 as @e[type=text_display,tag=rufu_sign,limit=1] at @s run tp @e[type=interaction,tag=rufu_sign_hit] ~ ~-0.6 ~",
       f"execute if score #m5 rufu matches 0 run {call('m4/circle_fx')}")
    import math
    cfx = []
    for k in range(16):
        a = 2 * math.pi * k / 16
        cfx.append(f"particle minecraft:end_rod {CX + CIRCLE_R * math.cos(a):.2f} 81.1 {CZ + CIRCLE_R * math.sin(a):.2f} 0 0.2 0 0.01 1")
    fn("m4/circle_fx", *cfx)


def attempt(n):
    fox_cmds = []
    if n == 1:
        fox_cmds.append(f"summon minecraft:fox 195.5 81 70.5 {fox_nbt(True, [])}")
    else:
        fox_cmds += [rnd("#r", 0, 2)]
        spots = [(186.5, 74.5), (204.5, 74.5), (195.5, 69.5)]
        for i, (x, z) in enumerate(spots):
            fox_cmds.append(f"execute if score #r rufu matches {i} run summon minecraft:fox {x} 81 {z} {fox_nbt(True, [])}")
            fox_cmds.append(f"execute unless score #r rufu matches {i} run summon minecraft:fox {x} 81 {z} {fox_nbt(False, [])}")
    return [
        *mission_begin(4, 3600, 600, 2000, M4_SPAWN),
        call("m4/reset"),
        sset("#m4try", n), sset("#m4p", 0), sset("#fspd", n), sset("#sspd", n),
        sset("#fox_need", 2), "execute if score #np rufu matches ..1 run scoreboard players set #fox_need rufu 1",
        sset("#pin_need", 2), "execute if score #np rufu matches ..2 run scoreboard players set #pin_need rufu 1",
        "execute if score #np rufu matches ..1 run scoreboard players set #pin_need rufu 0",
        "time set 18000",
        *npc_spawn("heroine", *HER_TREE, 0),
        f"tp @a[tag=rufu_p] {M4_SPAWN[0]} {M4_SPAWN[1]} {M4_SPAWN[2]} 0 0",
        *fox_cmds,
        f"execute as @a[tag=rufu_p] run {sub('m4', give('@s', 'wooden_shovel', shovel()))}",
    ]


def m4_steps():
    add_step(Step("試練4 説明「指輪？……あの子が持ってっちゃった」", retry=0, t0=[
        sset("#mission", 0), sset("#lock", 1), "time set 18000",
        call("m4/reset"),
        *npc_spawn("heroine", *HER_TREE, 0),
        f"tp @a[tag=rufu_p] {M4_SPAWN[0]} {M4_SPAWN[1]} {M4_SPAWN[2]} 0 0",
        *title("@a", T("試練4", color="gold", bold=True), T("指輪を取り返して、伝説の木の下で告白して", color="white"), (10, 70, 15)),
        gsound("block.note_block.bell", 1, 1.0),
    ], tl={
        40: say("heroine", "最後の試練。この木の下で告白されたら、ずっと幸せになれるんだって。", dur=110),
        150: say("heroine", "指輪？……あの子が持ってっちゃった。", dur=90, big=True) +
             [f"summon minecraft:fox 195.5 81 72.5 {fox_nbt(True, ['rufu_demo'])}",
              "execute at @e[tag=rufu_demo] run particle minecraft:poof ~ ~0.5 ~ 0.3 0.3 0.3 0.02 15 force",
              "playsound minecraft:entity.fox.ambient master @a 195.5 81 72.5 1 1.2"],
        250: say("heroine", "2人以上で囲めば動けなくなるよ。取り返したら、3人で木の下の光る円に来てね。", dur=110) + [sset("#lock", 0)],
    }))
    add_step(Step("試練4 開始（1回目・3分）", retry="self", mission=4, t0=attempt(1), tl=countdown_tl([], "キツネを追え！")))
    rew = {1: say("heroine", "……やっぱりなかったことにして。", dur=100, big=True) + [gsound("block.note_block.didgeridoo", 1, 0.6)]}
    for t in range(60, 120):
        rew[t] = ["time add -400", "execute as @a at @s run particle minecraft:reverse_portal ~ ~1 ~ 2 1 2 0.2 20"]
    rew[60] += title("@a", T("◀◀ 巻き戻し中……", color="aqua", bold=True), T("空が逆回りしている", color="white"), (5, 60, 10)) + \
        [gsound("block.portal.trigger", 0.6, 2.0), gsound("item.trident.return", 1, 0.5)]
    rew[120] = ["time set 18000", "clear @a minecraft:gold_nugget[custom_data~{rufu_ring:1b}]",
                 f"summon minecraft:fox 195.5 81 84.5 {fox_nbt(True, ['rufu_demo'])}",
                 "execute at @e[tag=rufu_demo] run particle minecraft:poof ~ ~0.5 ~ 0.3 0.3 0.3 0.02 15 force",
                 "playsound minecraft:entity.fox.bite master @a 195.5 81 84.5 1 1.2",
                 tellraw("@a", T("🦊 指輪がまたキツネに取られた！", color="gold", bold=True))]
    rew[150] = say("heroine", "あ、あの子また持ってった。……今度は仲間も連れてるみたい。", dur=100)
    rew[230] = [sset("#lock", 0)]
    add_step(Step("「やっぱりなかったことにして」空が巻き戻る", t0=[sset("#lock", 1), "kill @e[tag=rufu_demo]"], tl=rew))
    add_step(Step("試練4 2回目開始（キツネ3匹・3分）", retry="self", mission=4, t0=attempt(2) + ["kill @e[tag=rufu_demo]"],
                  tl=countdown_tl([tellraw("@a[tag=rufu_p]", T("🦊 本物は1匹だけ。偽物を叩くと爆発する！", color="red"))], "本物を探せ！")))
    # results
    res = {
        1: title("@a", T("結果発表", color="gold", bold=True), T("", color="white"), (10, 50, 10)) + [gsound("ui.toast.challenge_complete", 1, 0.8)],
        40: ["scoreboard players operation #sec rufu = #t_total rufu",
             "scoreboard players operation #sec rufu /= #c20 rufu",
             "scoreboard players operation #mm rufu = #sec rufu",
             "scoreboard players operation #mm rufu /= #c60 rufu",
             "scoreboard players operation #ss rufu = #sec rufu",
             "scoreboard players operation #ss rufu %= #c60 rufu",
             "title @a times 5 70 10",
             f"title @a subtitle {snbt(T('', extra=[T('合計タイム ', color='white'), {'score': {'name': '#mm', 'objective': 'rufu'}, 'color': 'yellow'}, T('分', color='white'), {'score': {'name': '#ss', 'objective': 'rufu'}, 'color': 'yellow'}, T('秒', color='white')]))}",
             f"title @a title {snbt(T('', extra=[T('リトライ回数 ', color='white', bold=True), {'score': {'name': '#retry', 'objective': 'rufu'}, 'color': 'red', 'bold': True}, T(' 回', color='white', bold=True)]))}",
             tellraw("@a", T("📊 リトライ回数：", color="gold"), {"score": {"name": "#retry", "objective": "rufu"}, "color": "red", "bold": True},
                     T("回　合計タイム：", color="gold"), {"score": {"name": "#mm", "objective": "rufu"}, "color": "yellow"}, T("分", color="gold"),
                     {"score": {"name": "#ss", "objective": "rufu"}, "color": "yellow"}, T("秒", color="gold")),
             gsound("block.note_block.bell", 1, 1.2)],
    }
    ev = evaluation_tl("D", "顔", "red")
    for k, v in ev.items():
        res[k + 130] = v
    res[180] = title("@a", T("総合評価：D", color="red", bold=True), T("理由：顔", color="white"), (0, 90, 20)) + \
        [tellraw("@a", T("🏆 総合評価：D　理由：顔", color="red", bold=True))]
    res[290] = say("heroine", "……でも、結婚はしてあげる。行こ、教会。", dur=90)
    res[380] = [sset("#lock", 0)]
    add_step(Step("総合評価（リトライ回数・タイム → D 理由：顔）", retry=0, t0=[sset("#lock", 1), sset("#mission", 0)], tl=res))
