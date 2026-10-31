"""Core systems: load/tick, HUD, GM remotes, step engine, roles menu, clicks, annoyances."""

from core import *  # noqa
from core import _flat
from mc import T, snbt, click_cmd, item_components, item_arg


# ====================================================================== step engine
class Step:
    def __init__(self, label, t0=None, tl=None, retry=None, mission=None):
        self.label = label
        self.t0 = t0 or []
        self.tl = tl or {}
        self.retry = retry        # None keep, 0 clear, 'self' -> this step
        self.mission = mission    # set #mission (None keep)


STEPS = [None]      # index 0 unused
EVENTS = {}         # name -> (id, tl)


def add_step(st):
    STEPS.append(st)
    return len(STEPS) - 1


def event(name, tl):
    eid = len(EVENTS) + 1
    EVENTS[name] = (eid, tl)
    return call(f"ev/start/{name}")


def ev_start(name):
    return call(f"ev/start/{name}")


def emit_steps():
    n = len(STEPS) - 1
    # step functions
    for i in range(1, n + 1):
        st = STEPS[i]
        nxt = STEPS[i + 1].label if i < n else "（おわり）"
        cmds = [sset("#step", i),
                f"data modify storage rufu:hud now set value {q(f'{i}. ' + st.label)}",
                f"data modify storage rufu:hud next set value {q((f'{i + 1}. ' if i < n else '') + nxt)}",
                sset("#seq", 0)]
        if st.retry == "self":
            cmds.append(sset("#retry_step", i))
        elif st.retry == 0:
            cmds.append(sset("#retry_step", 0))
        elif isinstance(st.retry, int):
            cmds.append(sset("#retry_step", st.retry))
        if st.mission is not None:
            cmds.append(sset("#mission", st.mission))
        cmds += [tellraw(GM, T(f"[GM] ▶ {i}. {st.label}", color="dark_green"))]
        cmds += st.t0
        if st.tl:
            cmds += [sset("#seq_t", 0), sset("#seq", i)]
        fn(f"step/s{i}", *cmds)
        if st.tl:
            emit_timeline(f"seq/s{i}", st.tl, "#seq_t", "#seq")
    fn("seq/tick", sadd("#seq_t", 1),
       *[f"execute if score #seq rufu matches {i} run {call(f'seq/s{i}')}" for i in range(1, n + 1) if STEPS[i].tl])
    fn("step/goto",
       "execute store result storage rufu:tmp n int 1 run scoreboard players get #step rufu",
       f"{call('step/goto_m')} with storage rufu:tmp")
    fn("step/goto_m", "$function rufu:step/s$(n)")
    fn("const/steps", sset("#last", n))
    # events
    lines = [sadd("#ev_t", 1)]
    for name, (eid, tl) in EVENTS.items():
        fn(f"ev/start/{name}", sset("#ev_t", 0), sset("#ev", eid), *(tl.get(0, [])))
        tl2 = {k: v for k, v in tl.items() if k != 0}
        if tl2:
            emit_timeline(f"ev/{name}", tl2, "#ev_t", "#ev")
            lines.append(f"execute if score #ev rufu matches {eid} run {call(f'ev/{name}')}")
        else:
            fn(f"ev/start/{name}", sset("#ev", 0))
    fn("ev/tick", *lines)


def emit_timeline(name, tl, tvar, chan):
    lines = []
    last = max(tl.keys())
    for t in sorted(tl.keys()):
        cmds = [c for c in _flat(tl[t]) if c]
        if t == 0:
            continue
        if not cmds:
            continue
        if len(cmds) == 1 and not cmds[0].startswith("$"):
            lines.append(f"execute if score {tvar} rufu matches {t} run {cmds[0]}")
        else:
            fn(f"{name}/t{t}", *cmds)
            lines.append(f"execute if score {tvar} rufu matches {t} run {call(f'{name}/t{t}')}")
    lines.append(f"execute if score {tvar} rufu matches {last}.. run scoreboard players set {chan} rufu 0")
    fn(name, *lines)
    # t0 commands of timelines are executed by the caller (step t0)
    if 0 in tl:
        pass


# ====================================================================== load / setup basics
def system():
    objectives = [
        ("rufu", "dummy"), ("rufu.t", "dummy"), ("rufu.id", "dummy"), ("rufu.pi", "dummy"),
        ("rufu.role", "dummy"), ("rufu.d", "dummy"), ("rufu.bt", "dummy"), ("rufu.fz", "dummy"),
        ("rufu.death", "deathCount"), ("rufu.use", "minecraft.used:minecraft.carrot_on_a_stick"),
        ("rufu.judge", "trigger"), ("rufu.side", "dummy"), ("rufu.hp", "dummy"),
    ]
    load = [f"scoreboard objectives add {o} {c}" for o, c in objectives]
    consts = [2, 3, 5, 10, 20, 60, 100, 1000]
    load += [sset(f"#c{c}", c) for c in consts]
    load += [
        "bossbar add rufu:love {text:\"♥ 好感度\"}",
        "bossbar set rufu:love color pink",
        "bossbar set rufu:love style notched_10",
        "bossbar set rufu:love max 100",
        "bossbar add rufu:time {text:\"⏱ 残り時間\"}",
        "bossbar set rufu:time color yellow",
        "bossbar add rufu:out {text:\"アウトゲージ\"}",
        "bossbar set rufu:out color red",
        "bossbar set rufu:out max 200",
        "bossbar set rufu:out style notched_20",
        "bossbar add rufu:build {text:\"町を建設中…\"}",
        "bossbar set rufu:build color green",
        "team add rufu_bread",
        "team add rufu_cake",
        "team add rufu_meat",
        "team add rufu_npc",
        f"team modify rufu_bread suffix {snbt(T(' 【パン担当】', color='gold', bold=True))}",
        f"team modify rufu_cake suffix {snbt(T(' 【ケーキ担当】', color='light_purple', bold=True))}",
        f"team modify rufu_meat suffix {snbt(T(' 【お肉担当】', color='red', bold=True))}",
        "team modify rufu_bread color gold",
        "team modify rufu_cake color light_purple",
        "team modify rufu_meat color red",
        "team modify rufu_npc collisionRule never",
        call("const/steps"),
        f"execute unless score #init rufu matches 1 run {call('init')}",
        tellraw("@a", T("💍 [恋 結婚の試練] ", color="light_purple", bold=True),
                T("データパックを読み込みました。 ", color="white"),
                click_cmd(T("[町を建設する]", color="green", underlined=True), "/function rufu:setup",
                          T("/function rufu:setup")),
                T(" ", color="white"),
                click_cmd(T("[メニュー]", color="aqua", underlined=True), "/function rufu:menu",
                          T("/function rufu:menu"))),
    ]
    fn("load", *load)
    fn("init", sset("#init", 1), sset("#step", 0), sset("#love", 100), sset("#retry", 0), sset("#mission", 0),
       sset("#active", 0), sset("#lock", 0), sset("#seq", 0), sset("#ev", 0), sset("#nextid", 0),
       sset("#retry_step", 0), sset("#t_total", 0), sset("#built", 0),
       'data modify storage rufu:hud now set value "0. 準備中"',
       'data modify storage rufu:hud next set value "1. オープニング"')

    # ---------------------------------------------------------------- tick
    fn("tick",
       sadd("#gt", 1),
       "scoreboard players operation #m5 rufu = #gt rufu",
       "scoreboard players operation #m5 rufu %= #c5 rufu",
       "scoreboard players operation #m20 rufu = #gt rufu",
       "scoreboard players operation #m20 rufu %= #c20 rufu",
       f"execute as @a[scores={{rufu.use=1..}}] run {call('gm/use')}",
       f"execute as @a[scores={{rufu.judge=1..}}] run {call('annoy/judge')}",
       f"execute if score #seq rufu matches 1.. run {call('seq/tick')}",
       f"execute if score #ev rufu matches 1.. run {call('ev/tick')}",
       call("npc/tick"),
       f"execute as @e[type=interaction,tag=rufu_click] if data entity @s interaction run {call('click/got')}",
       f"execute as @e[type=interaction,tag=rufu_click] if data entity @s attack run {call('click/got_attack')}",
       f"execute if score #mission rufu matches 1 run {call('m1/tick')}",
       f"execute if score #mission rufu matches 2 run {call('m2/tick')}",
       f"execute if score #mission rufu matches 3 run {call('m3/tick')}",
       f"execute if score #mission rufu matches 4 run {call('m4/tick')}",
       f"execute if score #active rufu matches 1 run {call('mission/tick')}",
       f"execute if score #fx rufu matches 1.. run {call('fx/tick')}",
       call("hud/tick"),
       )

    # ---------------------------------------------------------------- NPC tick
    fn("npc/tick",
       "execute as @e[type=text_display,tag=rufu_bub,scores={rufu.bt=1}] run data merge entity @s {text:\"\",background:0}",
       "scoreboard players remove @e[type=text_display,tag=rufu_bub,scores={rufu.bt=1..}] rufu.bt 1",
       "execute as @e[type=mannequin,tag=rufu_npc_heroine,limit=1] at @s run tp @e[type=interaction,tag=rufu_hit_heroine] ~ ~ ~",
       f"execute if score #m20 rufu matches 0 as @e[type=mannequin,tag=rufu_look] at @s if entity @a[tag=rufu_p,distance=..12] run tp @s ~ ~ ~ facing entity @p[tag=rufu_p] eyes",
       f"execute if score #m5 rufu matches 0 as @e[type=mannequin,tag=rufu_look] at @s unless entity @a[tag=rufu_p,distance=..12] if entity @a[distance=..12] run tp @s ~ ~ ~ facing entity @p eyes",
       )

    # ---------------------------------------------------------------- HUD
    fn("hud/love",
       "execute store result bossbar rufu:love value run scoreboard players get #love rufu",
       f"bossbar set rufu:love name {snbt(T('', extra=[T('♥ 好感度 ', color='light_purple', bold=True), {'score': {'name': '#love', 'objective': 'rufu'}, 'color': 'white', 'bold': True}, T(' / 100', color='gray')]))}",
       "execute if score #love rufu matches 50.. run bossbar set rufu:love color pink",
       "execute if score #love rufu matches 25..49 run bossbar set rufu:love color yellow",
       "execute if score #love rufu matches ..24 run bossbar set rufu:love color red")
    fn("hud/time",
       "scoreboard players operation #sec rufu = #timer rufu",
       "scoreboard players add #sec rufu 19",
       "scoreboard players operation #sec rufu /= #c20 rufu",
       "scoreboard players operation #mm rufu = #sec rufu",
       "scoreboard players operation #mm rufu /= #c60 rufu",
       "scoreboard players operation #ss rufu = #sec rufu",
       "scoreboard players operation #ss rufu %= #c60 rufu",
       "execute store result bossbar rufu:time value run scoreboard players get #timer rufu",
       f"execute if score #ss rufu matches 10.. run bossbar set rufu:time name {snbt(T('', extra=[T('⏱ 残り ', color='yellow', bold=True), {'score': {'name': '#mm', 'objective': 'rufu'}, 'color': 'white', 'bold': True}, T(':', color='white'), {'score': {'name': '#ss', 'objective': 'rufu'}, 'color': 'white', 'bold': True}]))}",
       f"execute if score #ss rufu matches ..9 run bossbar set rufu:time name {snbt(T('', extra=[T('⏱ 残り ', color='yellow', bold=True), {'score': {'name': '#mm', 'objective': 'rufu'}, 'color': 'white', 'bold': True}, T(':0', color='white'), {'score': {'name': '#ss', 'objective': 'rufu'}, 'color': 'white', 'bold': True}]))}",
       "execute if score #timer rufu matches ..200 run bossbar set rufu:time color red",
       "execute if score #timer rufu matches 201.. run bossbar set rufu:time color yellow")
    fn("hud/tick",
       f"execute if score #m5 rufu matches 0 if score #active rufu matches 1 run {call('hud/time')}",
       f"execute if score #m20 rufu matches 0 run {call('hud/gm')}",
       f"execute if score #m20 rufu matches 0 run {call('hud/side')}")
    status = [
        ("#lock rufu matches 0", T("● 待機中（次へで進む）", color="green")),
        ("#active rufu matches 1", T("▶ 試練進行中（自動判定）", color="gold")),
    ]
    fn("hud/gm",
       f"execute if score #active rufu matches 1 run title @a[tag=rufu_gm] actionbar {snbt(T('', extra=[T('今：', color='gray'), {'storage': 'rufu:hud', 'nbt': 'now', 'color': 'white', 'bold': True}, T('  ▶進行中  ', color='gold'), T('次：', color='gray'), {'storage': 'rufu:hud', 'nbt': 'next', 'color': 'aqua'}]))}",
       f"execute if score #active rufu matches 0 if score #lock rufu matches 1 run title @a[tag=rufu_gm] actionbar {snbt(T('', extra=[T('今：', color='gray'), {'storage': 'rufu:hud', 'nbt': 'now', 'color': 'white', 'bold': True}, T('  ⏸準備中/判定中  ', color='yellow'), T('次：', color='gray'), {'storage': 'rufu:hud', 'nbt': 'next', 'color': 'aqua'}]))}",
       f"execute if score #lock rufu matches 0 run title @a[tag=rufu_gm] actionbar {snbt(T('', extra=[T('今：', color='gray'), {'storage': 'rufu:hud', 'nbt': 'now', 'color': 'white', 'bold': True}, T('  ✔次へOK  ', color='green'), T('次：', color='gray'), {'storage': 'rufu:hud', 'nbt': 'next', 'color': 'aqua'}]))}")
    fn("hud/side",
       "scoreboard players operation retry rufu.side = #retry rufu",
       "scoreboard players operation trial rufu.side = #mission rufu")
    fn("hud/show",
       "bossbar set rufu:love players @a",
       "bossbar set rufu:love visible true",
       call("hud/love"),
       "scoreboard objectives add rufu.side dummy",
       f"scoreboard objectives modify rufu.side displayname {snbt(T('💍 結婚の試練', color='light_purple', bold=True))}",
       "scoreboard objectives setdisplay sidebar rufu.side",
       f"scoreboard players display name retry rufu.side {snbt(T('リトライ回数', color='red'))}",
       f"scoreboard players display name trial rufu.side {snbt(T('試練', color='gold'))}",
       "scoreboard objectives modify rufu.side numberformat styled {color:\"white\",bold:true}",
       call("hud/side"))
    fn("hud/hide",
       "bossbar set rufu:love visible false",
       "bossbar set rufu:time visible false",
       "bossbar set rufu:out visible false",
       "scoreboard objectives setdisplay sidebar")

    # ---------------------------------------------------------------- GM remotes & panel
    fn("gm/use",
       "scoreboard players set @s rufu.use 0",
       f"execute unless entity @s[tag=rufu_gm] run return run {sub('gm', tellraw('@s', T('このリモコンは るふ（GM）専用です。/function rufu:menu でGMになれます', color='gray')))}",
       f"execute if predicate rufu:hold_next run return run {call('gm/next')}",
       f"execute if predicate rufu:hold_again run return run {call('gm/again')}",
       f"execute if predicate rufu:hold_redo run return run {call('gm/redo')}")
    fn("gm/next",
       f"execute if score #lock rufu matches 1 run return run {sub('gm', tellraw('@s', T('⏸ 今は試練の進行中/判定中です。クリアすると「次へ」が使えます（強制的に進めるなら チャットパネルの[強制スキップ]）', color='yellow')), 'playsound minecraft:block.note_block.bass master @s ~ ~ ~ 1 0.6')}",
       f"execute if score #step rufu >= #last rufu run return run {sub('gm', tellraw('@s', T('おわりまで進みました。最初からは /function rufu:show/prepare', color='gray')))}",
       "playsound minecraft:ui.button.click master @s ~ ~ ~ 0.6 1.4",
       sadd("#step", 1),
       call("step/goto"))
    fn("gm/again",
       f"execute if score #step rufu matches ..0 run return run {sub('gm', tellraw('@s', T('まだ始まっていません。「次へ」で開始', color='gray')))}",
       "playsound minecraft:ui.button.click master @s ~ ~ ~ 0.6 1.0",
       call("step/goto"))
    fn("gm/redo",
       f"execute unless score #retry_step rufu matches 1.. run return run {sub('gm', tellraw('@s', T('今はやり直せるミッションがありません', color='gray')))}",
       "playsound minecraft:ui.button.click master @s ~ ~ ~ 0.6 0.7",
       tellraw("@a", T("⟲ ミッションを最初からやり直します（GM操作）", color="gray")),
       call("mission/restart"))
    fn("gm/force",
       tellraw("@a", T("⏭ GMが強制的に進めました", color="gray")),
       sset("#active", 0), sset("#lock", 0), sset("#ev", 0),
       "bossbar set rufu:time visible false", "bossbar set rufu:out visible false",
       *unfreeze(),
       sadd("#step", 1), call("step/goto"))
    fn("gm/remotes",
       "clear @s minecraft:carrot_on_a_stick[custom_data~{rufu_remote:\"next\"}]",
       "clear @s minecraft:carrot_on_a_stick[custom_data~{rufu_remote:\"again\"}]",
       "clear @s minecraft:carrot_on_a_stick[custom_data~{rufu_remote:\"redo\"}]",
       give("@s", "carrot_on_a_stick", remote_item("next")),
       give("@s", "carrot_on_a_stick", remote_item("again")),
       give("@s", "carrot_on_a_stick", remote_item("redo")))
    fn("gm/jump", "$scoreboard players set #step rufu $(n)",
       sset("#active", 0), sset("#lock", 0), sset("#ev", 0), *unfreeze(), call("step/goto"))
    fn("gm/panel",
       tellraw("@s", T("━━━━━━ 💍 GMパネル ━━━━━━", color="light_purple", bold=True)),
       tellraw("@s",
               click_cmd(T("[▶ 次へ]", color="green", bold=True), "/function rufu:gm/next", T("次の段階へ")), " ",
               click_cmd(T("[↻ もう一回]", color="yellow", bold=True), "/function rufu:gm/again", T("今の段階をもう一度")), " ",
               click_cmd(T("[⟲ やり直し]", color="red", bold=True), "/function rufu:gm/redo", T("今のミッションを最初から")), " ",
               click_cmd(T("[⏭ 強制スキップ]", color="gray"), "/function rufu:gm/force", T("判定を無視して次へ（トラブル用）"))),
       tellraw("@s",
               click_cmd(T("[📋 段階一覧/ジャンプ]", color="aqua"), "/function rufu:gm/list"), " ",
               click_cmd(T("[🎮 リモコン再配布]", color="aqua"), "/function rufu:gm/remotes"), " ",
               click_cmd(T("[👥 役割メニュー]", color="aqua"), "/function rufu:menu"), " ",
               click_cmd(T("[🔁 最初から]", color="gold"), "/function rufu:show/prepare")))
    # step list is generated after steps exist (see emit_gm_list)


def emit_gm_list():
    lines = [tellraw("@s", T("━━ 段階一覧（クリックでジャンプ） ━━", color="aqua", bold=True))]
    for i in range(1, len(STEPS)):
        lines.append(tellraw("@s", click_cmd(T(f" {i:>2}. {STEPS[i].label}", color="white"),
                                             f"/function rufu:gm/jump {{n:{i - 1}}}" if False else f"/function rufu:gm/jump {{n:{i}}}",
                                             T("ここへジャンプ"))))
    fn("gm/list", *lines)


# ====================================================================== clicks
def clicks():
    fn("click/find",
       "tag @a remove rufu_clicker",
       f"execute as @a run {call('click/cmp')}")
    fn("click/cmp",
       "data modify storage rufu:tmp cmp set from entity @s UUID",
       "execute store success score #diff rufu run data modify storage rufu:tmp cmp set from storage rufu:tmp uuid",
       "execute if score #diff rufu matches 0 run tag @s add rufu_clicker")
    fn("click/got",
       "data modify storage rufu:tmp uuid set from entity @s interaction.player",
       "data remove entity @s interaction",
       call("click/find"),
       call("click/dispatch"),
       "tag @a remove rufu_clicker")
    fn("click/got_attack",
       "data modify storage rufu:tmp uuid set from entity @s attack.player",
       "data remove entity @s attack",
       call("click/find"),
       call("click/dispatch"),
       "tag @a remove rufu_clicker")
    fn("click/dispatch",
       f"execute if entity @s[tag=rufu_hit_heroine] as @a[tag=rufu_clicker,limit=1] run return run {call('click/heroine')}",
       f"execute if entity @s[tag=rufu_ask] as @a[tag=rufu_clicker,limit=1] run return run {call('annoy/ask_click')}",
       f"execute if entity @s[tag=rufu_sign_hit] as @a[tag=rufu_clicker,limit=1] run return run {call('m4/sign_click')}",
       f"execute if entity @s[tag=rufu_girl_hit] run return run {call('end/girl_pre')}")
    # clicking the heroine: food deliveries (mission 2) and flower gifts (any mission)
    fn("click/heroine",
       f"execute if score #active rufu matches 1 if predicate rufu:hold_flower run return run {call('click/flower')}",
       f"execute if score #mission rufu matches 2 if score #active rufu matches 1 if entity @s[tag=rufu_p] run return run {call('m2/deliver')}",
       f"execute if entity @s[tag=rufu_p] run {sub('click', *say('heroine', 'なぁに？ 今いそがしいんだけど。', dur=50, sub_title=False))}")
    fn("click/flower",
       f"execute if score #gift rufu matches 1 run return run {sub('click', *say('heroine', 'お花はもうもらったよ？ 一回で十分。', dur=60, sub_title=False))}",
       sset("#gift", 1),
       "clear @s #minecraft:small_flowers 1",
       *say("heroine", "わぁ、お花！ ……まぁ、許してあげる♡", dur=70),
       particles_heart("@e[type=mannequin,tag=rufu_npc_heroine]", 12),
       *love(20, "緊急プレゼント！（このミッションではもう使えない）"))


# ====================================================================== annoyances (hero only)
ASK_PROMPTS = ["今なにしてる？", "ねぇ、今どこ？", "返信まだ？", "今だれといるの？"]
INTERRUPTS = [
    "ねぇ、私のいいところ3つ言って",
    "私の誕生日、いつか言ってみて",
    "今日の私、いつもとどこが違うか言って",
    "私のこと好き？ 10秒以内に叫んで",
    "結婚したら最初に何したいか言って",
]


def annoy():
    fn("annoy/tick",
       sadd("#ask_t", 1),
       f"execute if score #ask_t rufu matches 600.. run {call('annoy/ask_spawn')}",
       f"execute if score #ask_live rufu matches 1.. run {call('annoy/ask_tick')}",
       f"execute if score #elapsed rufu = #intr_at rufu run {call('annoy/interrupt')}",
       f"execute if score #intr_live rufu matches 1 run {call('annoy/intr_timeout')}",
       "execute if score #intr_live rufu matches 1.. run scoreboard players remove #intr_live rufu 1")
    spawn_lines = [sset("#ask_t", 0),
                   "kill @e[tag=rufu_ask]",
                   f"execute unless entity {HERO} run return 0",
                   rnd("#r", 0, len(ASK_PROMPTS) - 1),
                   ]
    for i, ptxt in enumerate(ASK_PROMPTS):
        disp = {"Tags": ["rufu_ask", "rufu_askdisp"], "billboard": "center",
                "text": T("", extra=[T("📱 ヒロイン\n", color="light_purple", bold=True), T(ptxt + "\n", color="black", bold=True),
                                     T("［右クリックで返信／5秒以内］", color="dark_gray")]),
                "background": argb(235, 255, 255, 255), "line_width": 160,
                "transformation": {"translation": [f_(0.0), f_(0.0), f_(0.0)], "left_rotation": [f_(0.0), f_(0.0), f_(0.0), f_(1.0)],
                                   "right_rotation": [f_(0.0), f_(0.0), f_(0.0), f_(1.0)], "scale": [f_(1.3), f_(1.3), f_(1.3)]}}
        spawn_lines.append(f"execute if score #r rufu matches {i} as {HERO} at @s anchored eyes positioned ^ ^ ^2.4 run summon minecraft:text_display ~ ~-0.35 ~ {snbt(disp)}")
    spawn_lines += [
        f"execute as {HERO} at @s anchored eyes positioned ^ ^ ^2.4 run summon minecraft:interaction ~ ~-0.85 ~ {snbt({'Tags': ['rufu_ask', 'rufu_click'], 'width': f_(1.6), 'height': f_(1.2), 'response': True})}",
        sset("#ask_live", 100),
        f"execute as {HERO} at @s run playsound minecraft:block.note_block.chime master @s ~ ~ ~ 1 2",
        f"execute as {HERO} at @s run playsound minecraft:block.note_block.chime master @s ~ ~ ~ 1 1.5",
    ]
    fn("annoy/ask_spawn", *spawn_lines)
    fn("annoy/ask_tick",
       sadd("#ask_live", -1),
       "execute at @e[type=text_display,tag=rufu_askdisp] run particle minecraft:end_rod ~ ~0.5 ~ 0.6 0.4 0.1 0 1",
       f"execute if score #ask_live rufu matches 0 run {call('annoy/ask_miss')}")
    fn("annoy/ask_miss",
       "execute at @e[type=text_display,tag=rufu_askdisp] run particle minecraft:angry_villager ~ ~ ~ 0.4 0.4 0.4 0 6",
       "kill @e[tag=rufu_ask]",
       *say("heroine", "……既読無視？", dur=60, sub_title=False),
       *love(-10, "「今なにしてる？」を5秒以内に返さなかった"))
    fn("annoy/ask_click",
       f"execute unless entity @s[tag=rufu_hero] run return run {sub('annoy', tellraw('@s', T('これは主人公あてのメッセージです', color='gray')))}",
       "execute at @e[type=text_display,tag=rufu_askdisp] run particle minecraft:heart ~ ~0.3 ~ 0.4 0.3 0.4 0 4",
       "kill @e[tag=rufu_ask]",
       sset("#ask_live", 0),
       "playsound minecraft:entity.experience_orb.pickup master @s ~ ~ ~ 1 1.4",
       tellraw("@a", T("📱 主人公が返信した：「今いそがしい！」 ", color="gray"), T("（ヒロイン：「ふーん。」）", color="light_purple")))
    # interrupts
    lines = [sset("#intr_live", 300), "scoreboard players set @a rufu.judge 0",
             "scoreboard players enable @a[tag=rufu_helper] rufu.judge",
             "scoreboard players enable @a[tag=rufu_gm] rufu.judge",
             rnd("#r", 0, len(INTERRUPTS) - 1)]
    for i, t in enumerate(INTERRUPTS):
        lines.append(run_block(f"if score #r rufu matches {i}", say("heroine", t, dur=100, big=True), "annoy"))
    lines += [
        gsound("block.note_block.bell", 1, 0.8),
        tellraw("@a[tag=rufu_helper]", T("🎤 割り込み！ 主人公の答えを判定してね → ", color="yellow"),
                click_cmd(T("[ 〇 合格 ]", color="green", bold=True), "/trigger rufu.judge set 1", T("好感度 +10")), " ",
                click_cmd(T("[ × 不合格 ]", color="red", bold=True), "/trigger rufu.judge set 2", T("好感度 -10"))),
        tellraw("@a[tag=rufu_gm]", T("[GM] 割り込み発生。判定: ", color="gray"),
                click_cmd(T("[〇]", color="green"), "/trigger rufu.judge set 1"), " ",
                click_cmd(T("[×]", color="red"), "/trigger rufu.judge set 2")),
        title(HERO, T("💬 声で答えて！", color="yellow", bold=True), T("（助っ人が 〇 / × で判定します）", color="white"), (5, 60, 10)),
    ]
    fn("annoy/interrupt", *lines)
    fn("annoy/intr_timeout",
       tellraw("@a", T("（割り込みの判定は時間切れ。ヒロイン：「……まぁいいや。」）", color="gray")))
    fn("annoy/judge",
       f"execute unless score #intr_live rufu matches 1.. run return run {sub('annoy', 'scoreboard players set @s rufu.judge 0', tellraw('@s', T('今は判定するものがありません', color='gray')))}",
       f"execute if score @s rufu.judge matches 1 run {sub('annoy', *say('heroine', 'えへへ……合格♡', dur=60), *love(10, '割り込みの答えが〇！'))}",
       f"execute if score @s rufu.judge matches 2 run {sub('annoy', *say('heroine', 'は？ 不合格。', dur=60), *love(-10, '割り込みの答えが×……'))}",
       sset("#intr_live", 0),
       "scoreboard players set @a rufu.judge 0")
