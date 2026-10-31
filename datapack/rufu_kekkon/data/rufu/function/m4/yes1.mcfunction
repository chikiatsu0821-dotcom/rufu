scoreboard players set #active rufu 0
scoreboard players set #lock rufu 0
scoreboard players operation #t_total rufu += #elapsed rufu
kill @e[tag=rufu_ask]
scoreboard players set #intr_live rufu 0
kill @e[tag=rufu_mob]
bossbar set rufu:time visible false
bossbar set rufu:out visible false
effect give @a[tag=rufu_p] minecraft:resistance infinite 4 true
effect give @a[tag=rufu_p] minecraft:fire_resistance infinite 0 true
effect give @a[tag=rufu_p] minecraft:instant_health 1 10 true
execute as @a[tag=rufu_p] run attribute @s minecraft:movement_speed base reset
function rufu:ev/start/m4_yes1
