execute as @a[tag=rufu_hero,limit=1] at @s rotated ~ 0 positioned ^ ^ ^1.4 run tp @e[type=mannequin,tag=rufu_npc_q,limit=1] ~ ~ ~ facing entity @p[tag=rufu_hero] eyes
execute as @a[tag=rufu_hero] at @s run playsound minecraft:entity.warden.heartbeat master @s ~ ~ ~ 2 0.8
execute as @e[type=text_display,tag=rufu_bub_q] run data merge entity @s {text:{text:"……",color:"#7a1f5c"},background:-503321354}
scoreboard players set @e[type=text_display,tag=rufu_bub_q] rufu.bt 60
tellraw @a {text:"",extra:[{text:"？？？",color:"gold",bold:true},{text:"「……」",color:"white"}]}
execute as @e[tag=rufu_npc_q] at @s run playsound minecraft:entity.allay.ambient_without_item voice @a ~ ~ ~ 1.4 1.1
