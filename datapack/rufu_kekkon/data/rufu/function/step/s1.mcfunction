scoreboard players set #step rufu 1
data modify storage rufu:hud now set value "1. オープニング（タイトル）"
data modify storage rufu:hud next set value "2. ヒロイン登場"
scoreboard players set #seq rufu 0
scoreboard players set #retry_step rufu 0
scoreboard players set #mission rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 1. オープニング（タイトル）",color:"dark_green"}
scoreboard players set #lock rufu 1
scoreboard players set #active rufu 0
function rufu:hud/hide
time set 1000
weather clear
tp @a[tag=rufu_p] 128.5 65 235.5 180 0
effect give @a[tag=rufu_p] minecraft:resistance infinite 4 true
effect give @a[tag=rufu_p] minecraft:saturation infinite 0 true
effect give @a[tag=rufu_p] minecraft:darkness 3 0 true
gamemode adventure @a[tag=rufu_p]
kill @e[tag=rufu_part_heroine]
kill @e[tag=rufu_rules]
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 1
