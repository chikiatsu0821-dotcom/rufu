execute store result storage rufu:tmp id int 1 run scoreboard players get @s rufu.id
data modify storage rufu:tmp role set value "未設定"
execute if entity @s[tag=rufu_hero] run data modify storage rufu:tmp role set value "★主人公"
execute if entity @s[tag=rufu_helper] run data modify storage rufu:tmp role set value "助っ人"
execute if entity @s[tag=rufu_gm] run data modify storage rufu:tmp role set value "GM"
execute if entity @s[tag=rufu_gm,tag=rufu_hero] run data modify storage rufu:tmp role set value "GM+主人公"
execute if entity @s[tag=rufu_gm,tag=rufu_helper] run data modify storage rufu:tmp role set value "GM+助っ人"
function rufu:menu/line_m with storage rufu:tmp
