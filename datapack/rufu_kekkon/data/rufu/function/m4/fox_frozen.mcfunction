scoreboard players remove @s rufu.fz 1
particle minecraft:crit ~ ~0.9 ~ 0.25 0.1 0.25 0 2
execute if score @s rufu.fz matches 0 run data merge entity @s {Glowing:false}
