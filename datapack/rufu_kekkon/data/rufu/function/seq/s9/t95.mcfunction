execute at @e[type=item,tag=rufu_throw] run particle minecraft:end_rod ~ ~ ~ 0.3 0.3 0.3 0.1 20 force
execute as @a at @s run playsound minecraft:entity.firework_rocket.twinkle master @s ~ ~ ~ 1 1.6
kill @e[type=item,tag=rufu_throw]
