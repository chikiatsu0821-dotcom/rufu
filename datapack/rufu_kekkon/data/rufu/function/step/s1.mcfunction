scoreboard players set #step rufu 1
data modify storage rufu:hud now set value "1. タイトル → ヒロイン選択（看板）"
data modify storage rufu:hud next set value "2. 試練の宣言「結婚したければ、4つの試練をクリアして。」"
scoreboard players set #seq rufu 0
scoreboard players set #retry_step rufu 0
scoreboard players set #mission rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 1. タイトル → ヒロイン選択（看板）",color:"dark_green"}
scoreboard players set #lock rufu 1
scoreboard players set #active rufu 0
title @a times 15 70 25
title @a subtitle {text:"～結婚の試練～",color:"white",bold:true}
title @a title {text:"恋",color:"light_purple",bold:true}
execute as @a at @s run playsound minecraft:block.amethyst_block.chime master @s ~ ~ ~ 1 1.0
execute at @a run particle minecraft:heart ~ ~2 ~ 3 1.5 3 0 30 force
tag @e[type=mannequin,tag=rufu_npc_q] add rufu_glow
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 1
