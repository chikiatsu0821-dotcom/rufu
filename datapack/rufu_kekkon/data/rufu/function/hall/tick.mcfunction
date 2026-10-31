execute as @e[type=mannequin,tag=rufu_qlook] at @s run tp @s ~ ~ ~ facing entity @p eyes
execute as @e[type=mannequin,tag=rufu_qlook] at @s if block ~ ~-0.3 ~ #minecraft:air run tp @s ~ ~-0.5 ~
execute if score #m5 rufu matches 0 at @e[type=mannequin,tag=rufu_npc_q,tag=rufu_glow] run particle minecraft:end_rod ~ ~1 ~ 0.35 0.9 0.35 0.01 2
execute if score #naming rufu matches 1 if score #m5 rufu matches 0 run particle minecraft:wax_on 46.5 66.1 244.5 0.4 0.3 0.4 0 4 force
execute if score #naming rufu matches 1 if score #m20 rufu matches 0 run particle minecraft:end_rod 46.5 66.4 244.5 0.3 0.3 0.3 0.02 6 force
execute as @e[type=mannequin,tag=rufu_npc_q] at @s run tp @e[type=interaction,tag=rufu_hit_q] ~ ~ ~
execute as @e[type=mannequin,tag=rufu_npc_q] at @s run tp @e[type=interaction,tag=rufu_sel4] ~ ~ ~
execute as @e[type=mannequin,tag=rufu_npc_q] at @s run tp @e[type=text_display,tag=rufu_seltxt4] ~ ~2.75 ~
