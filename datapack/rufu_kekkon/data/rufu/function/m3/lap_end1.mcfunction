scoreboard players set #active rufu 0
scoreboard players set #lock rufu 0
bossbar set rufu:time visible false
bossbar set rufu:out visible false
kill @e[tag=rufu_mob]
kill @e[tag=rufu_ask]
scoreboard players set #intr_live rufu 0
scoreboard players operation #t_total rufu += #elapsed rufu
effect give @a[tag=rufu_p] minecraft:resistance infinite 4 true
effect give @a[tag=rufu_p] minecraft:instant_health 1 10 true
tag @e[type=mannequin,tag=rufu_npc_heroine] add rufu_look
function rufu:ev/start/m3_lap1_end
