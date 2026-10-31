"""Opening + Mission 1 「私より早く広場に来て」"""

from core import *  # noqa
from system import Step, add_step, event, ev_start
from mission import mission_begin, countdown_tl, clear_cmds, clear_title, evaluation_tl
from mc import T, snbt, item_components, click_cmd

SX, SY, SZ = M1_START
HER_HOUSE = (132.5, 65, 234.5)


def pickaxe():
    return item_components(name=T("⛏ たった1本のツルハシ", color="aqua", bold=True, italic=False),
                           lore=["崩れた城壁（ひび割れた石レンガ）だけ壊せる", "誰が持って先に行く？"],
                           data={"rufu_m": b(1)}, can_break="minecraft:cracked_stone_bricks", glint=True)


def bridge_blocks():
    return item_components(name=T("🪵 橋用ブロック", color="yellow", italic=False),
                           lore=["堀のふち（凝灰岩レンガ）か", "このブロックの横に置ける"],
                           data={"rufu_m": b(1)}, can_place_on=["minecraft:tuff_bricks", "minecraft:bamboo_mosaic"])


def flower_shears():
    return item_components(name=T("✂ 花ばさみ", color="light_purple", italic=False),
                           lore=["町の花をつめる", "花をヒロインに右クリックで渡すと 好感度+20（各試練1回）"],
                           data={"rufu_tool": b(1)}, can_break="#minecraft:small_flowers", unbreakable=True)


def cells():
    P = PIT
    for c in range(P["cols"]):
        for r in range(P["rows"]):
            x0 = P["x0"] + 3 * c
            z0 = P["z0"] + 3 * r
            yield c, r, x0, z0


def build_m1():
    # ------------------------------------------------------------ course reset
    reset = []
    for c, r, x0, z0 in cells():
        k = c * PIT["rows"] + r
        reset += [
            f"fill {x0} 64 {z0} {x0 + 2} 64 {z0 + 2} minecraft:{PIT_SURF[c][r]} strict",
            rnd("#r", 1, 100),
            f"execute if score #r rufu matches ..30 run fill {x0} 63 {z0} {x0 + 2} 63 {z0 + 2} minecraft:magma_block strict",
            f"execute if score #r rufu matches 31.. run fill {x0} 63 {z0} {x0 + 2} 63 {z0 + 2} minecraft:stone strict",
        ]
    P = PATCH
    B = BRIDGE
    bx, by, bz = BARREL_POS
    px, py, pz = PICK_POS
    reset += [
        f"fill {P['x0']} {P['y0']} {P['z0']} {P['x1']} {P['y1']} {P['z1']} minecraft:cracked_stone_bricks strict",
        f"fill 112 60 208 144 63 214 minecraft:water replace minecraft:bamboo_mosaic",
        f"fill 112 64 208 144 68 216 minecraft:air replace minecraft:bamboo_mosaic",
        call("m1/db/up"),
        sset("#db_s", 0), rnd("#db_t", 60, 140),
        f"setblock {bx} {by} {bz} minecraft:air strict",
        f"setblock {bx} {by} {bz} minecraft:barrel[facing=up]{snbt({'Items': [item_nbt('minecraft:bamboo_mosaic', 12, bridge_blocks(), slot=13)]})} strict",
        item_entity(px + 0.5, py + 1.15, pz + 0.5, "iron_pickaxe", pickaxe(), tags=("rufu_m1item",),
                    extra={"NoGravity": True, "Age": s_(-32768), "Motion": [d(0), d(0), d(0)]}),
    ]
    # mobs
    for (x, z) in [(122.5, 178.5), (128.5, 179.5), (131.5, 177.5), (121.5, 164.5), (127.5, 165.5), (132.5, 163.5)]:
        reset.append(f"summon minecraft:zombie {x} 65 {z} " + snbt({
            "Tags": ["rufu_mob"], "PersistenceRequired": True, "IsBaby": False, "CanPickUpLoot": False,
            "equipment": {"head": {"id": "minecraft:leather_helmet", "count": 1}}, "drop_chances": {"head": f_(0.0)},
            "attributes": [{"id": "minecraft:spawn_reinforcements", "base": d(0.0)}]}))
    for (x, z, trident) in [(119.5, 211.5, False), (137.5, 210.5, True), (128.5, 213.5, False)]:
        eq = {"mainhand": {"id": "minecraft:trident", "count": 1}} if trident else {}
        reset.append(f"summon minecraft:drowned {x} 61 {z} " + snbt({
            "Tags": ["rufu_mob"], "PersistenceRequired": True, "IsBaby": False, "CanPickUpLoot": False,
            "equipment": eq, "drop_chances": {"mainhand": f_(0.0)}}))
    fn("m1/reset", *reset)

    # ------------------------------------------------------------ drawbridge
    deck = f"fill {B['x0']} {B['y']} {B['z0']} {B['x1']} {B['y']} {B['z1']}"
    fn("m1/db/up",
       f"fill {B['x0']} 65 {B['z0'] + 1} {B['x1']} 70 {B['z1']} minecraft:air strict",
       f"fill {B['x0']} {B['y']} {B['z0'] + 1} {B['x1']} {B['y']} {B['z1']} minecraft:air strict",
       f"fill {B['x0'] + 1} 64 {B['z0']} {B['x1'] - 1} 71 {B['z0']} minecraft:spruce_planks strict",
       f"fill {B['x0']} 64 {B['z0']} {B['x0']} 71 {B['z0']} minecraft:stripped_dark_oak_log[axis=y] strict",
       f"fill {B['x1']} 64 {B['z0']} {B['x1']} 71 {B['z0']} minecraft:stripped_dark_oak_log[axis=y] strict")
    mid = [f"fill {B['x0']} 65 {B['z0']} {B['x1']} 71 {B['z0']} minecraft:air strict",
           f"fill {B['x0']} {B['y']} {B['z0'] + 1} {B['x1']} {B['y']} {B['z1']} minecraft:air strict"]
    for k in range(0, 5):
        mid.append(f"fill {B['x0']} {65 + k} {B['z0'] + k} {B['x1']} {65 + k} {B['z0'] + k} minecraft:spruce_slab[type=bottom] strict")
        mid.append(f"fill {B['x0']} {64 + k} {B['z0'] + k} {B['x1']} {64 + k} {B['z0'] + k} minecraft:spruce_planks strict")
    fn("m1/db/mid", *mid,
       "playsound minecraft:block.chain.place master @a 128 68 208 2 0.5",
       "playsound minecraft:block.piston.contract master @a 128 68 208 2 0.5")
    fn("m1/db/down",
       f"fill {B['x0']} 64 {B['z0']} {B['x1']} 71 {B['z1']} minecraft:air strict",
       f"fill {B['x0'] + 1} {B['y']} {B['z0']} {B['x1'] - 1} {B['y']} {B['z1']} minecraft:spruce_planks strict",
       f"fill {B['x0']} {B['y']} {B['z0']} {B['x0']} {B['y']} {B['z1']} minecraft:stripped_dark_oak_log[axis=z] strict",
       f"fill {B['x1']} {B['y']} {B['z0']} {B['x1']} {B['y']} {B['z1']} minecraft:stripped_dark_oak_log[axis=z] strict",
       "playsound minecraft:block.wood.place master @a 128 65 211 2 0.6",
       "playsound minecraft:entity.zombie.attack_wooden_door master @a 128 65 211 1 0.6")
    fn("m1/db/tick",
       sadd("#db_t", -1),
       "execute if score #db_s rufu matches 2 if score #db_t rufu matches 14 run playsound minecraft:block.bell.use master @a 128 70 206 2 1.6",
       "execute if score #db_s rufu matches 2 if score #db_t rufu matches 7 run playsound minecraft:block.bell.use master @a 128 70 206 2 1.6",
       f"execute if score #db_t rufu matches ..0 run {call('m1/db/next')}")
    fn("m1/db/next",
       f"execute if score #db_s rufu matches 0 run return run {sub('m1', call('m1/db/mid'), sset('#db_s', 1), sset('#db_t', 6))}",
       f"execute if score #db_s rufu matches 1 run return run {sub('m1', call('m1/db/down'), sset('#db_s', 2), rnd('#db_t', 40, 70))}",
       f"execute if score #db_s rufu matches 2 run return run {sub('m1', call('m1/db/mid'), sset('#db_s', 3), sset('#db_t', 6))}",
       f"execute if score #db_s rufu matches 3 run return run {sub('m1', call('m1/db/up'), sset('#db_s', 0), rnd('#db_t', 70, 170))}")

    # ------------------------------------------------------------ pits
    pit_checks = []
    for c, r, x0, z0 in cells():
        k = c * PIT["rows"] + r
        fn(f"m1/pit/{k}",
           f"fill {x0} 64 {z0} {x0 + 2} 64 {z0 + 2} minecraft:lava",
           f"fill {x0} 63 {z0} {x0 + 2} 63 {z0 + 2} minecraft:blackstone strict",
           f"particle minecraft:lava {x0 + 1.5} 65 {z0 + 1.5} 1 0.2 1 0 25 force",
           f"particle minecraft:large_smoke {x0 + 1.5} 65 {z0 + 1.5} 1 0.5 1 0.02 20 force",
           f"playsound minecraft:block.lava.pop master @a {x0 + 1.5} 65 {z0 + 1.5} 2 0.6",
           f"playsound minecraft:entity.blaze.shoot master @a {x0 + 1.5} 65 {z0 + 1.5} 1 0.5",
           *love(-10, "落とし穴（溶岩）を踏んだ！"))
        pit_checks.append(f"execute if block {x0 + 1} 63 {z0 + 1} minecraft:magma_block if entity @a[tag=rufu_p,gamemode=!spectator,x={x0},y=64,z={z0},dx=2,dy=1,dz=2] run {call(f'm1/pit/{k}')}")
    fn("m1/pits", *pit_checks)

    # ------------------------------------------------------------ heroine overtake
    hx, hy, hz = HEROINE_FOUNTAIN
    fn("m1/her_start",
       sset("#m1_her", 1),
       f"execute as @a[tag=rufu_p,x=98,y=60,z=94,dx=60,dy=20,dz=54,limit=1] at @s rotated ~ 0 positioned ^ ^ ^-4 positioned ~ 65 ~ run {call('m1/her_spawn')}")
    fn("m1/her_spawn",
       *npc_spawn("heroine", "~", "~", "~", 0, look=False),
       "execute as @e[type=mannequin,tag=rufu_npc_heroine] at @s run tp @s ~ ~ ~ facing 128.5 65 128.5",
       *say("heroine", "おっ先～♪", dur=40, sub_title=False),
       "playsound minecraft:entity.breeze.wind_burst master @a ~ ~ ~ 1 1.4")
    fn("m1/her_run",
       f"execute if entity @s[x={hx},y={hy},z={hz},distance=..0.8] run return run {call('m1/her_arrive')}",
       f"execute facing {hx} {hy} {hz} run tp @s ^ ^ ^0.6 facing {hx} {hy} {hz}",
       "particle minecraft:cloud ~ ~0.1 ~ 0.2 0 0.2 0 1")
    fn("m1/her_arrive",
       sset("#m1_her", 2),
       f"tp @s {hx} {hy} {hz} 0 0",
       "tag @s add rufu_look")

    # ------------------------------------------------------------ main tick
    fn("m1/tick",
       f"execute unless score #active rufu matches 1 run return 0",
       call("m1/pits"),
       call("m1/db/tick"),
       f"execute as @a[tag=rufu_p,x=25,y=55,z=208,dx=205,dy=8,dz=6] at @s if block ~ ~ ~ minecraft:water run {call('m1/moat_fall')}",
       f"execute if score #m1_her rufu matches 0 if entity @a[tag=rufu_p,x=98,y=60,z=94,dx=60,dy=20,dz=54] run {call('m1/her_start')}",
       f"execute if score #m1_her rufu matches 1 as @e[type=mannequin,tag=rufu_npc_heroine,limit=1] at @s run {call('m1/her_run')}",
       "execute store result score #n rufu if entity @a[tag=rufu_p,x=128.5,y=65,z=121.5,distance=..9]",
       f"execute if score #n rufu >= #np rufu run {call('m1/clear')}",
       f"execute if score #m20 rufu matches 0 run title @a[tag=rufu_p] actionbar {snbt(T('', extra=[T('目的地：', color='gray'), T('中央広場の噴水', color='aqua', bold=True), T('　3人全員そろって到着！', color='white')]))}")
    fn("m1/moat_fall",
       f"tp @s {SX} {SY} {SZ} 180 0",
       "playsound minecraft:entity.player.splash master @a ~ ~ ~ 1 1",
       *title("@s", T("堀に落ちた！", color="aqua", bold=True), T("スタートに戻される…", color="white"), (0, 30, 10)),
       *love(-5, "堀に落ちた"))

    clear = clear_cmds() + [
        call("m1/db/down"), sset("#db_s", 9),
        f"execute unless score #m1_her rufu matches 2 run {sub('m1', *npc_spawn('heroine', hx, hy, hz, 0), sset('#m1_her', 2))}",
        "kill @e[tag=rufu_m1item]",
        ev_start("m1_clear"),
    ]
    fn("m1/clear", *clear)
    event("m1_clear", {
        0: clear_title(),
        30: say("heroine", "遅い！", dur=80, big=True) + [
            "execute at @e[type=mannequin,tag=rufu_npc_heroine] run particle minecraft:angry_villager ~ ~2 ~ 0.6 0.4 0.6 0 10 force",
            gsound("entity.villager.no", 1, 1.3)],
        80: say("heroine", "私より先に着かないと意味ないでしょ？", dur=80),
        90: [tellraw(GM, T("[GM] 試練1クリア！ 「次へ」で評価発表", color="green"))],
    })


def opening_steps():
    hx, hy, hz = HER_HOUSE
    rules = [
        T("💍 結婚の試練 ルール 💍\n", color="light_purple", bold=True),
        T("結婚したければ、4つの試練をクリアして。\n\n", color="white", bold=True),
        T("・3人全員がクリア条件を満たすこと\n", color="white"),
        T("・1人でも失敗 → 3人そろって最初から\n", color="white"),
        T("・好感度は100から。0になってもやり直し\n", color="white"),
        T("・どの試練にも制限時間あり\n", color="white"),
        T("・雷・金床・クリーパー・モブは本当に痛い\n", color="red"),
        T("・誰か死んだら そのミッションは失敗\n", color="red"),
        T("・持ち物は消えない（その試練で集めた物は没収）\n", color="white"),
        T("・クリアすると評価が出る（理由は聞かないで）", color="gray"),
    ]
    board = {"Tags": ["rufu_rules", "rufu_stage"], "billboard": "vertical", "text": T("", extra=rules),
             "background": argb(210, 40, 10, 30), "line_width": 260, "alignment": "left",
             "transformation": {"translation": [f_(0.0), f_(0.0), f_(0.0)], "left_rotation": [f_(0.0), f_(0.0), f_(0.0), f_(1.0)],
                                "right_rotation": [f_(0.0), f_(0.0), f_(0.0), f_(1.0)], "scale": [f_(1.6), f_(1.6), f_(1.6)]}}
    # 1 opening
    add_step(Step("オープニング（タイトル）", retry=0, mission=0, t0=[
        sset("#lock", 1), sset("#active", 0), call("hud/hide"),
        "time set 1000", "weather clear",
        f"tp @a[tag=rufu_p] {SX} {SY} {SZ} 180 0",
        "effect give @a[tag=rufu_p] minecraft:resistance infinite 4 true",
        "effect give @a[tag=rufu_p] minecraft:saturation infinite 0 true",
        "effect give @a[tag=rufu_p] minecraft:darkness 3 0 true",
        "gamemode adventure @a[tag=rufu_p]",
        npc_kill("heroine"), "kill @e[tag=rufu_rules]",
    ], tl={
        10: title("@a", T("恋", color="light_purple", bold=True), T("～ 結婚の試練 ～", color="white", bold=True), (20, 80, 30)) +
            [gsound("block.bell.use", 1, 0.8), gsound("block.amethyst_block.chime", 1, 1.2)],
        30: [gsound("block.bell.use", 1, 1.0)],
        50: [gsound("block.bell.use", 1, 1.2), call("song/bridal_short")],
        140: [sset("#lock", 0)],
    }))
    # 2 heroine appears
    add_step(Step("ヒロイン登場", t0=[
        sset("#lock", 0),
        *npc_spawn("heroine", hx, hy, hz, 90),
        *poof("@e[type=mannequin,tag=rufu_npc_heroine]"),
        "execute at @e[type=mannequin,tag=rufu_npc_heroine] run particle minecraft:heart ~ ~2 ~ 0.6 0.5 0.6 0 10 force",
    ], tl={
        5: say("heroine", "ねぇ。私と結婚したいって、本気？", dur=90),
    }))
    # 3 rules
    add_step(Step("「結婚したければ、4つの試練をクリアして。」＋ルール看板", t0=[
        *say("heroine", "結婚したければ、4つの試練をクリアして。", dur=100, big=True),
        "kill @e[tag=rufu_rules]",
        f"summon minecraft:text_display {SX} 67.6 {SZ - 3.5} {snbt(board)}",
        "execute at @e[tag=rufu_rules] run particle minecraft:end_rod ~ ~1 ~ 1.5 1.2 0.2 0 40 force",
        gsound("ui.toast.in", 1, 1),
        *narr("ルール看板が立った！", "yellow", False),
        call("hud/show"),
        sset("#love", 100), call("hud/love"),
        f"execute as @a[tag=rufu_p] run {sub('op', 'clear @s minecraft:shears[custom_data~{rufu_tool:1b}]', give('@s', 'shears', flower_shears()))}",
        tellraw("@a[tag=rufu_p]", T("✂ 「花ばさみ」をもらった。町の花をつんでヒロインに右クリックで渡すと 好感度+20（各試練1回）", color="light_purple")),
    ], tl={
        110: say("heroine", "3人で、ね。1人でも失敗したら全員最初からだから。", dur=90),
    }))
    # 4 mission 1 briefing
    add_step(Step("試練1 説明「私より早く広場に来て」", t0=[
        "kill @e[tag=rufu_rules]",
        *title("@a", T("試練1", color="gold", bold=True), T("私より早く広場に来て（制限時間45秒）", color="white"), (10, 70, 15)),
        gsound("block.note_block.bell", 1, 1.0),
        call("m1/reset"),
    ], tl={
        40: say("heroine", "最初の試練。町の中央広場、噴水のところまで来て。45秒ね。", dur=90),
        130: say("heroine", "跳ね橋とか、屋根とか、崩れた壁とか……まぁ、がんばって♡", dur=90),
    }))


def m1_steps():
    hx, hy, hz = HER_HOUSE
    add_step(Step("試練1 開始（45秒）", retry="self", mission=1, t0=[
        *mission_begin(1, 900, 260, 560, (SX, SY, SZ)),
        sset("#m1_her", 0),
        call("m1/reset"),
        f"tp @a[tag=rufu_p] {SX} {SY} {SZ} 180 0",
        *npc_spawn("heroine", hx, hy, hz, 90),
        "kill @e[tag=rufu_rules]",
    ], tl={**countdown_tl([
        *poof("@e[type=mannequin,tag=rufu_npc_heroine]"),
        *say("heroine", "じゃ、広場で待ってるね～♪", dur=40, sub_title=False),
        npc_kill("heroine"),
    ], "スタート！"), 5: say("heroine", "よーい……", dur=50, sub_title=False)}))
    add_step(Step("試練1 評価", retry=0, t0=[sset("#lock", 1), *npc_spawn("heroine", *HEROINE_FOUNTAIN, 0)],
                  tl={**evaluation_tl("D", "私より遅い", "red"), 120: [sset("#lock", 0)]}))
