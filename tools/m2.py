"""Mission 2 「結婚式のごちそうを作って」"""

from core import *  # noqa
from system import Step, add_step, event, ev_start
from mission import mission_begin, countdown_tl, clear_cmds, clear_title, evaluation_tl, fail_fn
from mc import T, snbt, item_components

FOODS = {1: ("パン", "bread", "gold", "rufu_bread", "ふつう。"),
         2: ("ケーキ", "cake", "light_purple", "rufu_cake", "……重い。"),
         3: ("お肉", "meat", "red", "rufu_meat", "式に出すには地味。")}
PERMS = [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]
M2_SPAWN = (128.5, 65, 134.5)


def knife():
    return item_components(name=T("🔪 万能ナイフ", color="white", bold=True, italic=False),
                           lore=["小麦・サトウキビ・花を刈れる", "牛も豚もこれで"],
                           data={"rufu_m": b(1)}, can_break=["minecraft:wheat", "minecraft:sugar_cane", "#minecraft:small_flowers"],
                           unbreakable=True)


def build_m2():
    WH = WHEAT
    reset = []
    # farmland + wheat (skip the water columns)
    xs = []
    x = WH["x0"]
    segs = []
    start = WH["x0"]
    for x in range(WH["x0"], WH["x1"] + 2):
        if x in WH["water"] or x == WH["x1"] + 1:
            if start <= x - 1:
                segs.append((start, x - 1))
            start = x + 1
    for (a, b_) in segs:
        reset.append(f"fill {a} 64 {WH['z0']} {b_} 64 {WH['z1']} minecraft:farmland[moisture=7] strict")
        reset.append(f"fill {a} 65 {WH['z0']} {b_} 65 {WH['z1']} minecraft:wheat[age=7] strict")
    CN = CANE
    for x in (CN["x"] - 1, CN["x"] + 1):
        reset.append(f"fill {x} 65 {CN['z0']} {x} 67 {CN['z1']} minecraft:sugar_cane strict")
    reset += [
        "kill @e[tag=rufu_farm]",
        f"kill @e[type=item,x={FARM['x0']},y=55,z={FARM['z0']},dx=60,dy=30,dz=70]",
    ]
    for (x, z) in [(200.5, 150.5), (204.5, 153.5), (207.5, 149.5)]:
        reset.append(f"summon minecraft:cow {x} 65 {z} " + snbt({"Tags": ["rufu_farm"], "PersistenceRequired": True, "Age": 0}))
    for (x, z) in [(201.5, 166.5), (206.5, 168.5)]:
        reset.append(f"summon minecraft:pig {x} 65 {z} " + snbt({"Tags": ["rufu_farm"], "PersistenceRequired": True, "Age": 0}))
    chest_items = [item_nbt("minecraft:bucket", 3, None, slot=11), item_nbt("minecraft:egg", 3, None, slot=15)]
    reset += [
        "setblock 185 65 172 minecraft:air strict",
        f"setblock 185 65 172 minecraft:chest[facing=west]{snbt({'Items': chest_items, 'CustomName': T('バケツと卵', color='dark_green')})} strict",
    ]
    fuel = snbt({"Items": [item_nbt("minecraft:coal", 16, None, slot=1)]})
    for z in (172, 174, 176):
        reset += [f"setblock 173 65 {z} minecraft:air strict", f"setblock 173 65 {z} minecraft:furnace[facing=east]{fuel} strict"]
    reset += ["setblock 149 65 112 minecraft:air strict", f"setblock 149 65 112 minecraft:furnace[facing=east]{fuel} strict",
              "setblock 149 65 113 minecraft:air strict", f"setblock 149 65 113 minecraft:smoker[facing=east]{fuel} strict"]
    fn("m2/reset", *reset)

    # ------------------------------------------------------------ roles
    lines = ["scoreboard players set @a rufu.pi 0", sset("#pi", 0),
             f"execute as @a[tag=rufu_p,sort=random] run {sub('m2', sadd('#pi', 1), 'scoreboard players operation @s rufu.pi = #pi rufu')}",
             rnd("#perm", 0, 5)]
    for i, p in enumerate(PERMS):
        lines.append(run_block(f"if score #perm rufu matches {i}", [sset("#own1", p[0]), sset("#own2", p[1]), sset("#own3", p[2])], "m2"))
    lines += ["scoreboard players operation #orig1 rufu = #own1 rufu",
              "scoreboard players operation #orig2 rufu = #own2 rufu",
              "scoreboard players operation #orig3 rufu = #own3 rufu"]
    lines.append(call("m2/apply_roles"))
    fn("m2/assign", *lines)
    ap = ["scoreboard players set @a rufu.role 0",
          "team leave @a[tag=rufu_p]"]
    for f in (1, 2, 3):
        ap.append(f"execute as @a[tag=rufu_p] if score @s rufu.pi = #own{f} rufu run scoreboard players set @s rufu.role {f}")
    for f, (jp, key, col, team, _) in FOODS.items():
        ap.append(f"team join {team} @a[tag=rufu_p,scores={{rufu.role={f}}}]")
    for f, (jp, key, col, team, _) in FOODS.items():
        ap += title(f"@a[tag=rufu_p,scores={{rufu.role={f}}}]", T(f"あなたは {jp}担当", color=col, bold=True),
                    T("頭の上にも表示されています", color="white"), (5, 50, 10))
    ap.append(gsound("block.note_block.chime", 1, 1.2))
    fn("m2/apply_roles", *ap)
    fn("m2/shuffle",
       rnd("#k", 1, 2),
       "scoreboard players operation #own1 rufu += #k rufu",
       "scoreboard players operation #own2 rufu += #k rufu",
       "scoreboard players operation #own3 rufu += #k rufu",
       "execute if score #own1 rufu matches 4.. run scoreboard players remove #own1 rufu 3",
       "execute if score #own2 rufu matches 4.. run scoreboard players remove #own2 rufu 3",
       "execute if score #own3 rufu matches 4.. run scoreboard players remove #own3 rufu 3",
       call("m2/apply_roles"))
    event("m2_shuffle", {
        0: say("heroine", "やっぱ担当交代！", dur=80, big=True) + [gsound("entity.villager.celebrate", 1, 1.4),
                                                                    gsound("block.note_block.bit", 1, 0.7)],
        10: [call("m2/shuffle"),
             tellraw("@a[tag=rufu_p]", T("🔄 担当がシャッフルされた！ 持ってる物を渡し合えば間に合う！", color="yellow"))],
    })

    # ------------------------------------------------------------ deliveries
    preds = {1: "rufu:hold_bread", 2: "rufu:hold_cake", 3: "rufu:hold_meat"}
    items = {1: ["bread"], 2: ["cake"], 3: ["cooked_beef", "cooked_porkchop"]}
    dl = []
    for f in (1, 2, 3):
        dl.append(f"execute if predicate {preds[f]} run return run {call(f'm2/give{f}')}")
    dl.append(f"execute if entity @s[tag=rufu_p] run {sub('m2', *say('heroine', 'それ、ごちそうじゃないでしょ。パン、ケーキ、焼いたお肉！', dur=60, sub_title=False))}")
    fn("m2/deliver", *dl)
    for f, (jp, key, col, team, react) in FOODS.items():
        clear_item = [f"execute if predicate rufu:hold_{key if key != 'meat' else 'meat'} run clear @s minecraft:{items[f][0]} 1"] if len(items[f]) == 1 else \
            ["execute store success score #ok rufu run clear @s minecraft:cooked_beef 1",
             "execute if score #ok rufu matches 0 run clear @s minecraft:cooked_porkchop 1"]
        fn(f"m2/give{f}",
           f"execute if score #got{f} rufu matches 1 run return run {sub('m2', *say('heroine', f'{jp}はもうもらったってば。', dur=50, sub_title=False))}",
           # wrong person: the food is assigned to someone who is playing and it is not you
           f"execute if score #own{f} rufu <= #np rufu unless score @s rufu.pi = #own{f} rufu run return run {sub('m2', *say('heroine', f'{jp}は あなたの担当じゃないでしょ！', dur=70, big=True), call('mission/fail/wrong'))}",
           *clear_item,
           sset(f"#got{f}", 1),
           f"data modify storage rufu:m2 s{f} set value \"✔\"",
           *say("heroine", react, dur=70),
           f"execute at @e[type=mannequin,tag=rufu_npc_heroine] run particle minecraft:happy_villager ~ ~1.5 ~ 0.5 0.5 0.5 0 15 force",
           "playsound minecraft:entity.player.burp master @a ~ ~ ~ 1 1.2",
           tellraw("@a", T(f"🍽 {jp} をわたした！ ", color=col, bold=True), T("（", color="gray"), {"selector": "@s"}, T(f"） 反応：「{react}」", color="gray")),
           "scoreboard players operation #gotn rufu = #got1 rufu",
           "scoreboard players operation #gotn rufu += #got2 rufu",
           "scoreboard players operation #gotn rufu += #got3 rufu",
           f"execute if score #gotn rufu matches 3 run {call('m2/clear')}")

    # ------------------------------------------------------------ tick
    hud = []
    for f, (jp, key, col, team, _) in FOODS.items():
        hud.append(f"title @a[tag=rufu_p,scores={{rufu.role={f}}}] actionbar " + snbt(T("", extra=[
            T(f"あなた：{jp}担当", color=col, bold=True), T("　｜　", color="dark_gray"),
            T("パン", color="gold"), {"storage": "rufu:m2", "nbt": "s1", "color": "white"}, T(" ケーキ", color="light_purple"),
            {"storage": "rufu:m2", "nbt": "s2", "color": "white"}, T(" お肉", color="red"), {"storage": "rufu:m2", "nbt": "s3", "color": "white"},
            T("　→噴水のヒロインに右クリックで渡す", color="gray")])))
    hud.append("title @a[tag=rufu_p,scores={rufu.role=0}] actionbar " + snbt(T("", extra=[
        T("パン", color="gold"), {"storage": "rufu:m2", "nbt": "s1", "color": "white"}, T(" ケーキ", color="light_purple"),
        {"storage": "rufu:m2", "nbt": "s2", "color": "white"}, T(" お肉", color="red"), {"storage": "rufu:m2", "nbt": "s3", "color": "white"}])))
    fn("m2/hud", *hud)
    fn("m2/tick",
       "execute unless score #active rufu matches 1 run return 0",
       f"execute if score #elapsed rufu matches 2400 run {ev_start('m2_shuffle')}",
       f"execute if score #elapsed rufu matches 2200 run {sub('m2', tellraw('@a[tag=rufu_p]', T('……ヒロインが何か言いたそうにしている', color='gray')))}",
       f"execute if score #m20 rufu matches 0 run {call('m2/hud')}")
    fn("m2/clear", *clear_cmds(), "team leave @a[tag=rufu_p]", ev_start("m2_clear"))
    event("m2_clear", {
        0: clear_title(T("ごちそうが3品そろった！", color="white")),
        40: say("heroine", "うん、そろったね。", dur=70),
        60: [tellraw(GM, T("[GM] 試練2クリア！ 「次へ」でオチ（やっぱパンだけでよかった）", color="green"))],
    })


def m2_steps():
    hx, hy, hz = HEROINE_FOUNTAIN
    add_step(Step("試練2 説明（担当発表）", retry=0, t0=[
        sset("#mission", 0), sset("#lock", 1),
        *npc_spawn("heroine", hx, hy, hz, 0),
        f"tp @a[tag=rufu_p] {M2_SPAWN[0]} {M2_SPAWN[1]} {M2_SPAWN[2] + 2} 180 0",
        *title("@a", T("試練2", color="gold", bold=True), T("結婚式のごちそうを作って（制限時間4分）", color="white"), (10, 70, 15)),
        gsound("block.note_block.bell", 1, 1.0),
    ], tl={
        30: say("heroine", "次は結婚式のごちそう。パン、ケーキ、焼いたお肉。1人1品ね。", dur=100),
        130: say("heroine", "誰がどれを作るかは……私が決める♡", dur=70) + [call("m2/assign")],
        150: [tellraw("@a[tag=rufu_p]", T("🍞 材料は町はずれの農場（東）とパン屋に。小麦畑・サトウキビ・牛・豚・かまど・バケツと卵のチェスト", color="yellow"))],
        200: say("heroine", "渡すときは私に右クリック。担当じゃない人が渡したら最初からね。", dur=90) + [sset("#lock", 0)],
    }))
    add_step(Step("試練2 開始（4分）", retry="self", mission=2, t0=[
        *mission_begin(2, 4800, 700, 2100, M2_SPAWN),
        call("m2/reset"),
        sset("#got1", 0), sset("#got2", 0), sset("#got3", 0),
        'data modify storage rufu:m2 s1 set value "✘"',
        'data modify storage rufu:m2 s2 set value "✘"',
        'data modify storage rufu:m2 s3 set value "✘"',
        f"execute unless score #orig1 rufu matches 1.. run {call('m2/assign')}",
        "scoreboard players operation #own1 rufu = #orig1 rufu",
        "scoreboard players operation #own2 rufu = #orig2 rufu",
        "scoreboard players operation #own3 rufu = #orig3 rufu",
        call("m2/apply_roles"),
        *npc_spawn("heroine", hx, hy, hz, 0),
        f"tp @a[tag=rufu_p] {M2_SPAWN[0]} {M2_SPAWN[1]} {M2_SPAWN[2] + 2} 180 0",
        f"execute as @a[tag=rufu_p] run {sub('m2', give('@s', 'iron_sword', knife()))}",
    ], tl=countdown_tl([tellraw("@a[tag=rufu_p]", T("🔪 万能ナイフで小麦・サトウキビ・花を刈れる。牛と豚もこれで。", color="gray"))])))
    add_step(Step("オチ「やっぱパンだけでよかった」", retry=0, t0=[sset("#lock", 1)], tl={
        5: say("heroine", "……やっぱパンだけでよかった。", dur=90, big=True) + [gsound("block.note_block.didgeridoo", 1, 0.8)],
        60: ["execute at @e[type=mannequin,tag=rufu_npc_heroine] run summon minecraft:item ~ ~1.6 ~ " + snbt(
                {"Item": item_nbt("minecraft:cake", 1), "PickupDelay": s_(32767), "Motion": [d(0.25), d(1.6), d(-0.1)], "Tags": ["rufu_throw"]}),
             "execute at @e[type=mannequin,tag=rufu_npc_heroine] run summon minecraft:item ~ ~1.6 ~ " + snbt(
                {"Item": item_nbt("minecraft:cooked_beef", 1), "PickupDelay": s_(32767), "Motion": [d(-0.25), d(1.7), d(0.1)], "Tags": ["rufu_throw"]}),
             gsound("entity.witch.throw", 1, 0.8), gsound("entity.player.attack.sweep", 1, 0.6),
             tellraw("@a", T("（ケーキとお肉が空のかなたへ投げ捨てられた）", color="gray", italic=True))],
        95: ["execute at @e[type=item,tag=rufu_throw] run particle minecraft:end_rod ~ ~ ~ 0.3 0.3 0.3 0.1 20 force",
             gsound("entity.firework_rocket.twinkle", 1, 1.6),
             "kill @e[type=item,tag=rufu_throw]"],
        110: [sset("#lock", 0)],
    }))
    add_step(Step("試練2 評価", retry=0, t0=[sset("#lock", 1)],
                  tl={**evaluation_tl("C", "作りすぎ", "gold"), 120: [sset("#lock", 0)]}))
