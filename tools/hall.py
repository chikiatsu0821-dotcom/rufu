"""Prologue in the selection hall: 4 girls, only ??? can really be chosen, naming, declaration."""

from core import *  # noqa
from system import Step, add_step, event, ev_start
from mc import T, snbt, item_components

PROFILES = {
    "sakura": ("さくら", "#ff8fc8", "清楚系／生徒会長", "entity/player/slim/sunny"),
    "mio": ("みお", "#7fb8ff", "クール系／弓道部", "entity/player/slim/noor"),
    "hinata": ("ひなた", "#ffd34d", "元気系／幼なじみ", "entity/player/slim/efe"),
    "q": ("？？？", "gold", "★おすすめ★", "entity/player/slim/alex"),
}
NB = "@e[type=marker,tag=rufu_namebox,limit=1]"
QSEL = "@e[type=mannequin,tag=rufu_npc_q,limit=1]"


def name_comp(color="light_purple", bold=True):
    return {"selector": NB, "color": color, "bold": bold}


def girl_spawn(key, x, z, y):
    jp, col, desc, tex = PROFILES[key]
    nbt = {
        "profile": {"texture": tex, "model": "slim"},
        "CustomName": T(jp, color=col, bold=True),
        "CustomNameVisible": True,
        "description": T(desc, color="gold" if key == "q" else "white", bold=key == "q"),
        "hide_description": False,
        "immovable": True, "Invulnerable": True, "Silent": True, "NoGravity": key == "q",
        "Rotation": [f_(0.0), f_(0.0)],
        "Tags": ["rufu_npc", "rufu_hallgirl", f"rufu_npc_{key}", f"rufu_part_{key}"] + (["rufu_qlook"] if key == "q" else []),
        "equipment": {"chest": {"id": "minecraft:leather_chestplate", "count": 1,
                                "components": {"dyed_color": {"sakura": 0xFFC0DD, "mio": 0x9CC8FF, "hinata": 0xFFE07A, "q": 0xF4A6C8}[key]}}},
        "Passengers": [{
            "id": "minecraft:text_display", "Tags": ["rufu_bub", f"rufu_bub_{key}", f"rufu_part_{key}", "rufu_npcpart"],
            "billboard": "center", "text": T(""), "background": 0, "line_width": 180,
            "transformation": {"translation": [f_(0.0), f_(1.25), f_(0.0)], "left_rotation": [f_(0.0), f_(0.0), f_(0.0), f_(1.0)],
                               "right_rotation": [f_(0.0), f_(0.0), f_(0.0), f_(1.0)], "scale": [f_(1.0), f_(1.0), f_(1.0)]}}],
    }
    if key == "q":
        nbt["Glowing"] = True
    return [f"kill @e[tag=rufu_part_{key}]", f"summon minecraft:mannequin {x} {y} {z} {snbt(nbt)}"]


def setup_hall():
    """Commands for 'stage 0' (right after the start command)."""
    px, py, pz = HALL_PLAYERS
    out = ["kill @e[tag=rufu_hallgirl]", "kill @e[tag=rufu_sel]", "kill @e[tag=rufu_part_q]",
           "kill @e[type=marker,tag=rufu_namebox]",
           f"summon minecraft:marker {NAMEBOX[0]} {NAMEBOX[1]} {NAMEBOX[2]} {snbt({'Tags': ['rufu_namebox'], 'CustomName': T('ゆめりあ')})}",
           sset("#pick", 0), sset("#qchosen", 0), sset("#named", 0), sset("#naming", 0)]
    for (key, x, z, y) in HALL_GIRLS:
        out += girl_spawn(key, x, z, y)
    out += [f"tp @a[tag=rufu_p] {px} {py} {pz} 180 0",
            f"tp @a[tag=!rufu_p] {px} {py} {pz + 5} 180 0",
            f"spawnpoint @a[tag=rufu_p] {int(px)} {py} {int(pz)}",
            "time set 6000", "weather clear",
            "effect give @a[tag=rufu_p] minecraft:resistance infinite 4 true",
            "effect give @a[tag=rufu_p] minecraft:fire_resistance infinite 0 true"]
    return out


def build_hall_logic():
    # ??? keeps looking at the nearest player; falls gently when stepping off the pedestal
    fn("hall/tick",
       f"execute as @e[type=mannequin,tag=rufu_qlook] at @s run tp @s ~ ~ ~ facing entity @p eyes",
       "execute as @e[type=mannequin,tag=rufu_qlook] at @s if block ~ ~-0.3 ~ #minecraft:air run tp @s ~ ~-0.5 ~",
       "execute if score #m5 rufu matches 0 at @e[type=mannequin,tag=rufu_npc_q,tag=rufu_glow] run particle minecraft:end_rod ~ ~1 ~ 0.35 0.9 0.35 0.01 2",
       f"execute if score #naming rufu matches 1 if score #m5 rufu matches 0 run particle minecraft:wax_on {HALL_ANVIL[0] + 0.5} {HALL_ANVIL[1] + 1.1} {HALL_ANVIL[2] + 0.5} 0.4 0.3 0.4 0 4 force",
       f"execute if score #naming rufu matches 1 if score #m20 rufu matches 0 run particle minecraft:end_rod {HALL_ANVIL[0] + 0.5} {HALL_ANVIL[1] + 1.4} {HALL_ANVIL[2] + 0.5} 0.3 0.3 0.3 0.02 6 force",
       "execute as @e[type=mannequin,tag=rufu_npc_q] at @s run tp @e[type=interaction,tag=rufu_hit_q] ~ ~ ~",
       "execute as @e[type=mannequin,tag=rufu_npc_q] at @s run tp @e[type=interaction,tag=rufu_sel4] ~ ~ ~",
       "execute as @e[type=mannequin,tag=rufu_npc_q] at @s run tp @e[type=text_display,tag=rufu_seltxt4] ~ ~2.75 ~")

    # selection signs (only the hero can press)
    sign = []
    for i, (key, x, z, y) in enumerate(HALL_GIRLS, start=1):
        q = key == "q"
        txt = T("★この子にする★", color="gold", bold=True) if q else T("この子にする", color="white", bold=True)
        sign.append(f"summon minecraft:text_display {x} {y + 2.75} {z} " + snbt({
            "Tags": ["rufu_sel", f"rufu_seltxt{i}"], "billboard": "center", "text": txt,
            "background": argb(220, 60, 30, 10) if q else argb(200, 40, 20, 40), "line_width": 200,
            "transformation": {"translation": [f_(0.0), f_(0.0), f_(0.0)], "left_rotation": [f_(0.0), f_(0.0), f_(0.0), f_(1.0)],
                               "right_rotation": [f_(0.0), f_(0.0), f_(0.0), f_(1.0)], "scale": [f_(1.2), f_(1.2), f_(1.2)]}}))
        sign.append(f"summon minecraft:interaction {x} {y} {z} " + snbt({
            "Tags": ["rufu_sel", "rufu_click", "rufu_sel_hit", f"rufu_sel{i}"], "width": f_(1.1), "height": f_(3.2), "response": True}))
    fn("hall/signs", "kill @e[tag=rufu_sel]", *sign,
       "execute at @e[type=text_display,tag=rufu_sel] run particle minecraft:end_rod ~ ~ ~ 0.5 0.2 0.1 0.02 8 force",
       gsound("block.note_block.chime", 1, 1.2))

    # dispatcher: runs as the interaction entity
    fn("hall/sel_pre",
       *[f"execute if entity @s[tag=rufu_sel{i}] run scoreboard players set #hit rufu {i}" for i in range(1, 5)],
       f"execute as @a[tag=rufu_clicker,limit=1] run {call('hall/sel_click')}")
    fn("hall/sel_click",
       f"execute unless entity @s[tag=rufu_hero] run return run {sub('hall', tellraw('@s', T('選べるのは主人公だけです', color='gray')), 'playsound minecraft:block.note_block.bass master @s ~ ~ ~ 1 0.6')}",
       f"execute if score #qchosen rufu matches 1 run return 0",
       f"execute if score #hit rufu matches 4 run return run {call('hall/pick_q')}",
       *[f"execute if score #hit rufu matches {i} run {call(f'hall/pick_{key}')}" for i, (key, x, z, y) in enumerate(HALL_GIRLS[:3], start=1)])

    for i, (key, x, z, y) in enumerate(HALL_GIRLS[:3], start=1):
        jp = PROFILES[key][0]
        fn(f"hall/pick_{key}",
           sadd("#pick", 1),
           f"execute at @e[type=mannequin,tag=rufu_npc_{key}] run summon minecraft:lightning_bolt ~ ~ ~",
           f"execute at @e[type=mannequin,tag=rufu_npc_{key}] run particle minecraft:large_smoke ~ ~1 ~ 0.5 1 0.5 0.03 60 force",
           f"execute at @e[type=mannequin,tag=rufu_npc_{key}] run particle minecraft:campfire_cosy_smoke ~ ~0.5 ~ 0.3 0.5 0.3 0.02 15 force",
           f"data merge entity @e[type=mannequin,tag=rufu_npc_{key},limit=1] {{description:{snbt(T('近日実装', color='red', bold=True))}}}",
           *title("@s", T(""), T("", extra=[T(f"{jp}は ", color="white"), T("近日実装", color="red", bold=True)]), (0, 40, 10)),
           tellraw("@a", T(f"⚡ {jp}は 近日実装 です", color="red", bold=True)),
           f"schedule function rufu:hall/clear_fire 30t",
           call("hall/q_react"))
    fn("hall/clear_fire", f"fill 15 65 221 49 70 231 minecraft:air replace #minecraft:fire")
    fn("hall/q_react",
       f"execute as {QSEL} at @s facing entity @p[tag=rufu_hero] feet rotated ~ 0 positioned ^ ^ ^1 run tp @s ~ ~ ~ facing entity @p[tag=rufu_hero] eyes",
       "execute as @a[tag=rufu_hero] at @s run playsound minecraft:entity.warden.heartbeat master @s ~ ~ ~ 1.5 1",
       "schedule function rufu:hall/heartbeat2 8t",
       f"execute if score #pick rufu matches 1 run {sub('hall', *say('q', '……', dur=60, sub_title=False))}",
       f"execute if score #pick rufu matches 2 run {sub('hall', *say('q', 'その子、まだいないよ？', dur=80))}",
       f"execute if score #pick rufu matches 3 run {call('hall/dark')}",
       f"execute if score #pick rufu matches 4.. run {sub('hall', *say('q', 'ねえ、私にしなよ', dur=80, big=True))}")
    fn("hall/heartbeat2", "execute as @a[tag=rufu_hero] at @s run playsound minecraft:entity.warden.heartbeat master @s ~ ~ ~ 1.5 1")
    fn("hall/dark",
       "effect give @a[tag=rufu_hero] minecraft:darkness 4 0 true",
       "effect give @a[tag=rufu_hero] minecraft:blindness 3 0 true",
       "execute as @a[tag=rufu_hero] at @s run playsound minecraft:entity.elder_guardian.curse master @s ~ ~ ~ 1 1",
       "schedule function rufu:hall/dark_end 50t")
    fn("hall/dark_end",
       f"execute as @a[tag=rufu_hero,limit=1] at @s rotated ~ 0 positioned ^ ^ ^1.4 run tp {QSEL} ~ ~ ~ facing entity @p[tag=rufu_hero] eyes",
       "execute as @a[tag=rufu_hero] at @s run playsound minecraft:entity.warden.heartbeat master @s ~ ~ ~ 2 0.8",
       *say("q", "……", dur=60, sub_title=False))

    fn("hall/pick_q",
       sset("#qchosen", 1),
       "kill @e[tag=rufu_sel]",
       f"data merge entity {QSEL} {{Glowing:false,description:{snbt(T('名前をつけてね', color='light_purple', bold=True))}}}",
       "tag @e[type=mannequin,tag=rufu_npc_q] remove rufu_glow",
       *say("q", "知ってた♡", dur=80, big=True),
       f"execute at {QSEL} run particle minecraft:heart ~ ~2 ~ 1 0.8 1 0 40 force",
       "execute as @a at @s run playsound minecraft:entity.player.levelup master @s ~ ~ ~ 1 1.2",
       give("@s", "name_tag", item_components(lore=["金床で名前を書いて、？？？に使おう"], data={"rufu_nametag": b(1)})),
       "experience add @s 3 levels",
       sset("#naming", 1),
       f"execute at {QSEL} run summon minecraft:interaction ~ ~ ~ {snbt({'Tags': ['rufu_click', 'rufu_hit_q', 'rufu_part_q'], 'width': f_(1.0), 'height': f_(2.1), 'response': True})}",
       f"playsound minecraft:block.anvil.use master @a {HALL_ANVIL[0]} {HALL_ANVIL[1]} {HALL_ANVIL[2]} 0.6 1.6",
       tellraw("@a", T("✨ ホールの金床が光っている……", color="gold")),
       *title("@s", T(""), T("金床で名札に名前を書いて、？？？に使おう", color="light_purple"), (5, 60, 10)))

    fn("hall/q_click",
       f"execute unless entity @s[tag=rufu_hero] run return run {sub('hall', *say('q', 'あなたじゃなくて、あの人に名前をつけてほしいの。', dur=60, sub_title=False))}",
       f"execute unless score #naming rufu matches 1 run return run {sub('hall', *say('q', '……♡', dur=40, sub_title=False))}",
       f"execute unless predicate rufu:hold_nametag run return run {sub('hall', *say('q', '金床で名札に名前を書いて、私に使って', dur=80))}",
       "execute store success score #ok rufu run data get entity @s SelectedItem.components.\"minecraft:custom_name\"",
       f"execute if score #ok rufu matches 0 run return run {sub('hall', *say('q', '金床で名札に名前を書いて、私に使って', dur=80))}",
       f"data modify entity {NB} CustomName set from entity @s SelectedItem.components.\"minecraft:custom_name\"",
       f"data modify entity {QSEL} CustomName set from entity {NB} CustomName",
       "clear @s minecraft:name_tag 1",
       call("hall/named"))
    fn("hall/named",
       sset("#naming", 0), sset("#named", 1),
       f"data merge entity {QSEL} {{description:{snbt(T('ヒロイン', color='light_purple'))}}}",
       f"execute as @e[type=text_display,tag=rufu_bub_q] run data merge entity @s {{text:{snbt(T('……いい名前♡', color='#7a1f5c'))},background:{SPEAKERS['heroine']['bg']}}}",
       "scoreboard players set @e[type=text_display,tag=rufu_bub_q] rufu.bt 100",
       tellraw("@a", name_comp(), T("「", color="white"), {"selector": NB, "color": "white"}, T("……いい名前♡」", color="white")),
       "title @a times 5 70 15",
       f"title @a subtitle {snbt(T('', extra=[{'selector': NB, 'color': 'white'}, T('……いい名前♡', color='white')]))}",
       f"title @a title {snbt(name_comp())}",
       gsound("block.note_block.chime", 1, 1.0),
       "schedule function rufu:hall/chime2 6t",
       f"execute at {QSEL} run particle minecraft:heart ~ ~2 ~ 0.8 0.6 0.8 0 25 force",
       call("hall/others_vanish"))
    fn("hall/chime2", gsound("block.note_block.chime", 1, 1.5), gsound("block.amethyst_block.chime", 1, 1.2))
    fn("hall/others_vanish",
       *[f"execute at @e[type=mannequin,tag=rufu_npc_{k}] run particle minecraft:poof ~ ~1 ~ 0.4 0.8 0.4 0.03 25 force" for k in ("sakura", "mio", "hinata")],
       *[f"kill @e[tag=rufu_part_{k}]" for k in ("sakura", "mio", "hinata")],
       "kill @e[tag=rufu_sel]")


def hall_steps():
    hx, hy, hz = HALL_HEROINE
    # 1 title -> selection
    add_step(Step("タイトル → ヒロイン選択（看板）", retry=0, mission=0, t0=[
        sset("#lock", 1), sset("#active", 0),
        "title @a times 15 70 25",
        f"title @a subtitle {snbt(T('～結婚の試練～', color='white', bold=True))}",
        f"title @a title {snbt(T('恋', color='light_purple', bold=True))}",
        gsound("block.amethyst_block.chime", 1, 1.0),
        "execute at @a run particle minecraft:heart ~ ~2 ~ 3 1.5 3 0 30 force",
        "tag @e[type=mannequin,tag=rufu_npc_q] add rufu_glow",
    ], tl={
        8: [gsound("block.amethyst_block.chime", 1, 1.3), "execute positioned 32.5 72 226 run particle minecraft:heart ~ ~ ~ 8 3 2 0 30 force"],
        16: [gsound("block.amethyst_block.chime", 1, 1.6)],
        24: [gsound("block.amethyst_block.resonate", 1, 1.0)],
        110: [call("hall/signs"),
              *title(HERO, T(""), T("「この子にする」を右クリックで、ヒロインを選んでね", color="light_purple"), (5, 70, 10)),
              tellraw("@a", T("💗 主人公は「この子にする」を右クリックしてヒロインを選んでね", color="light_purple")),
              sset("#lock", 0)],
    }))
    # 2 declaration
    board = {"Tags": ["rufu_rules", "rufu_stage"], "billboard": "vertical",
             "text": T("", extra=[T("結婚の試練\n\n", color="light_purple", bold=True),
                                  T("・3人全員がクリアしないとやり直し\n", color="white"),
                                  T("・1人でも死んだらやり直し\n", color="white"),
                                  T("・好感度が0になってもやり直し\n", color="white"),
                                  T("・制限時間あり", color="white")]),
             "background": argb(215, 45, 8, 30), "line_width": 240, "alignment": "left",
             "transformation": {"translation": [f_(0.0), f_(0.0), f_(0.0)], "left_rotation": [f_(0.0), f_(0.0), f_(0.0), f_(1.0)],
                                "right_rotation": [f_(0.0), f_(0.0), f_(0.0), f_(1.0)], "scale": [f_(1.8), f_(1.8), f_(1.8)]}}
    add_step(Step("試練の宣言「結婚したければ、4つの試練をクリアして。」", t0=[
        sset("#lock", 1), sset("#naming", 0),
        "kill @e[tag=rufu_sel]",
        call("hall/others_vanish"),
        f"execute at {QSEL} run particle minecraft:poof ~ ~1 ~ 0.4 0.8 0.4 0.03 20 force",
        "kill @e[tag=rufu_part_q]",
        "clear @a minecraft:name_tag[custom_data~{rufu_nametag:1b}]",
        *npc_spawn("heroine", hx, hy, hz, 0, look=False),
        f"execute as @e[type=mannequin,tag=rufu_npc_heroine] at @s run tp @s ~ ~ ~ facing entity @p[tag=rufu_hero] eyes",
        "execute at @e[type=mannequin,tag=rufu_npc_heroine] run particle minecraft:end_rod ~ ~1 ~ 0.5 1 0.5 0.05 30 force",
        "kill @e[tag=rufu_rules]",
    ], tl={
        10: ["playsound minecraft:block.bell.use master @a 32.5 70 226 3 0.9",
             f"summon minecraft:text_display {HALL_CX + 0.5} 68.2 233.5 {snbt(board)}",
             "execute at @e[tag=rufu_rules] run particle minecraft:end_rod ~ ~1 ~ 2 1.5 0.2 0 40 force"],
        14: say("heroine", "結婚したければ、4つの試練をクリアして。", dur=120, big=True),
        22: ["playsound minecraft:block.bell.use master @a 32.5 70 226 3 0.75"],
        34: ["playsound minecraft:block.bell.resonate master @a 32.5 70 226 2 1"],
        40: [sset("#love", 100), call("hud/show"),
             f"execute as @a[tag=rufu_p] run {sub('op', 'clear @s minecraft:shears[custom_data~{rufu_tool:1b}]', give('@s', 'shears', __import__('m1').flower_shears()))}",
             tellraw("@a[tag=rufu_p]", T("✂ 「花ばさみ」をもらった。町の花をつんでヒロインに右クリックで渡すと 好感度+20（各試練1回）", color="light_purple"))],
        140: ["tag @e[type=mannequin,tag=rufu_npc_heroine] add rufu_look", sset("#lock", 0)],
    }))
