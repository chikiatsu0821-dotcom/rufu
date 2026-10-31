execute as @e[type=text_display,tag=rufu_bub,scores={rufu.bt=1}] run data merge entity @s {text:"",background:0}
scoreboard players remove @e[type=text_display,tag=rufu_bub,scores={rufu.bt=1..}] rufu.bt 1
execute as @e[type=mannequin,tag=rufu_npc_heroine,limit=1] at @s run tp @e[type=interaction,tag=rufu_hit_heroine] ~ ~ ~
execute if score #m20 rufu matches 0 as @e[type=mannequin,tag=rufu_look] at @s if entity @a[tag=rufu_p,distance=..12] run tp @s ~ ~ ~ facing entity @p[tag=rufu_p] eyes
execute if score #m5 rufu matches 0 as @e[type=mannequin,tag=rufu_look] at @s unless entity @a[tag=rufu_p,distance=..12] if entity @a[distance=..12] run tp @s ~ ~ ~ facing entity @p eyes
