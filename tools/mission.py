"""Shared mission machinery: start / countdown / fail / clear / evaluation."""

from core import *  # noqa
from system import event, ev_start
from mc import T, snbt

MISSION_ITEMS = ["bread", "cake", "wheat", "wheat_seeds", "sugar", "sugar_cane", "egg", "bucket", "milk_bucket",
                 "beef", "cooked_beef", "porkchop", "cooked_porkchop", "leather", "bamboo_mosaic",
                 "cracked_stone_bricks", "coarse_dirt", "rotten_flesh", "bone", "arrow", "trident", "sweet_berries",
                 "golden_apple", "carved_pumpkin", "leather_helmet", "iron_ingot", "carrot", "potato"]


def clear_mission_items():
    out = ["clear @a[tag=rufu_p] *[custom_data~{rufu_m:1b}]"]
    out += [f"clear @a[tag=rufu_p] minecraft:{i}" for i in MISSION_ITEMS]
    return out


def mission_begin(num, timer_ticks, intr_lo, intr_hi, spawn):
    """Commands for the beginning of a mission attempt (before the countdown)."""
    x, y, z = spawn
    return [
        sset("#mission", num), sset("#active", 0), sset("#lock", 1), sset("#ev", 0), sset("#fx", 0),
        sset("#love", 100), call("hud/love"),
        sset("#timer", timer_ticks), f"bossbar set rufu:time max {timer_ticks}",
        "execute store result bossbar rufu:time value run scoreboard players get #timer rufu",
        "bossbar set rufu:time players @a", "bossbar set rufu:time visible true", call("hud/time"),
        sset("#elapsed", 0), sset("#ask_t", 0), sset("#ask_live", 0), sset("#intr_live", 0), sset("#gift", 0),
        "kill @e[tag=rufu_ask]",
        rnd("#intr_at", intr_lo, intr_hi),
        "execute store result score #np rufu if entity @a[tag=rufu_p]",
        "scoreboard players set @a rufu.death 0",
        "effect clear @a[tag=rufu_p] minecraft:resistance",
        "effect clear @a[tag=rufu_p] minecraft:fire_resistance",
        "effect give @a[tag=rufu_p] minecraft:saturation infinite 0 true",
        "effect give @a[tag=rufu_p] minecraft:instant_health 1 10 true",
        "gamemode adventure @a[tag=rufu_p]",
        f"spawnpoint @a[tag=rufu_p] {int(x)} {int(y)} {int(z)}",
        "kill @e[tag=rufu_mob]",
        "kill @e[type=item,tag=!rufu_keep]",
        "kill @e[type=minecraft:arrow]",
        "kill @e[type=minecraft:trident]",
        *clear_mission_items(),
        call("hud/show"),
    ]


def countdown_tl(start_cmds, go_label="スタート！"):
    """Timeline dict for 3-2-1 countdown, freeze until go."""
    return {
        1: freeze() + title("@a", T("3", color="red", bold=True), None, (0, 18, 2)) + [gsound("block.note_block.pling", 1, 0.8)],
        21: title("@a", T("2", color="gold", bold=True), None, (0, 18, 2)) + [gsound("block.note_block.pling", 1, 0.9)],
        41: title("@a", T("1", color="yellow", bold=True), None, (0, 18, 2)) + [gsound("block.note_block.pling", 1, 1.0)],
        61: title("@a", T(go_label, color="green", bold=True), T("3人全員クリアが条件！", color="white"), (0, 30, 10))
            + [gsound("block.note_block.pling", 1, 2.0), gsound("entity.firework_rocket.launch", 1, 1.2)]
            + unfreeze() + [sset("#active", 1)] + start_cmds,
    }


def fail_fn(name, reason):
    fn(f"mission/fail/{name}",
       f"execute unless score #active rufu matches 1 run return 0",
       sset("#active", 0),
       sadd("#retry", 1),
       "kill @e[tag=rufu_ask]",
       sset("#intr_live", 0),
       *title("@a", T("失敗…", color="red", bold=True), T(reason, color="white"), (5, 50, 15)),
       gsound("entity.wither.death", 0.35, 1.6),
       gsound("block.note_block.didgeridoo", 1, 0.6),
       tellraw("@a", T("✖ ミッション失敗：", color="red", bold=True), T(reason, color="white"),
               T("　→ 3人そろって最初からやり直し！", color="gray")),
       ev_start("fail"))


def mission_common():
    fail_fn("time", "時間切れ！")
    fail_fn("love", "好感度が 0 になった……")
    fail_fn("death", "誰かが倒れた！")
    fail_fn("wrong", "指名と違う人が渡した！")
    fail_fn("out", "アウトゲージが満タン！ ついてこれてない！")
    event("fail", {
        0: [],
        30: [tellraw("@a", T("…やり直し準備中…", color="dark_gray"))],
        70: [call("mission/restart")],
    })
    fn("mission/restart",
       "kill @e[tag=rufu_ask]",
       sset("#ev", 0),
       *unfreeze(),
       "scoreboard players operation #step rufu = #retry_step rufu",
       call("step/goto"))
    fn("mission/tick",
       sadd("#timer", -1),
       sadd("#elapsed", 1),
       f"execute if score #timer rufu matches ..0 run return run {call('mission/fail/time')}",
       f"execute if score #love rufu matches ..0 run return run {call('mission/fail/love')}",
       f"execute if entity @a[tag=rufu_p,scores={{rufu.death=1..}}] run return run {call('mission/fail/death')}",
       call("annoy/tick"))


def clear_cmds():
    """Common commands when a mission (attempt) is cleared."""
    return [
        sset("#active", 0), sset("#lock", 0),
        "scoreboard players operation #t_total rufu += #elapsed rufu",
        "kill @e[tag=rufu_ask]", sset("#intr_live", 0),
        "kill @e[tag=rufu_mob]",
        "bossbar set rufu:time visible false",
        "bossbar set rufu:out visible false",
        "effect give @a[tag=rufu_p] minecraft:resistance infinite 4 true",
        "effect give @a[tag=rufu_p] minecraft:fire_resistance infinite 0 true",
        "effect give @a[tag=rufu_p] minecraft:instant_health 1 10 true",
        "execute as @a[tag=rufu_p] run attribute @s minecraft:movement_speed base reset",
    ]


def clear_title(sub_=None):
    return title("@a", T("CLEAR!", color="gold", bold=True), sub_ or T("3人全員クリア！", color="white"), (5, 40, 10)) + \
        [gsound("ui.toast.challenge_complete", 1, 1.0)]


def evaluation_tl(grade, reason, grade_color="red", extra_after=None):
    """Drum roll then 'Grade: X / Reason: ...'."""
    tl = {}
    t = 1
    gap = 6
    while t < 44:
        tl[t] = [gsound("block.note_block.snare", 0.8, 1.0)]
        t += gap
        if gap > 2:
            gap -= 1
    tl[1] = tl.get(1, []) + title("@a", T("評価は……", color="white", bold=True), T("ドゥルルルル……", color="gray"), (5, 60, 5))
    tl[50] = title("@a", T(f"評価：{grade}", color=grade_color, bold=True), T(f"理由：{reason}", color="white"), (0, 80, 20)) + [
        gsound("block.note_block.basedrum", 1, 0.6), gsound("entity.firework_rocket.blast", 1, 0.8),
        tellraw("@a", T(f"📋 評価：{grade}", color=grade_color, bold=True), T(f"　理由：{reason}", color="white"))]
    if extra_after:
        tl[100] = extra_after
    return tl
