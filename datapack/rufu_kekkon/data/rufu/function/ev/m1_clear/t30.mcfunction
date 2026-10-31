execute as @e[type=text_display,tag=rufu_bub_heroine] run data merge entity @s {text:{text:"遅い！",color:"#7a1f5c"},background:-503321354}
scoreboard players set @e[type=text_display,tag=rufu_bub_heroine] rufu.bt 80
tellraw @a {text:"",extra:[{selector:"@e[type=marker,tag=rufu_namebox,limit=1]",color:"light_purple",bold:true},{text:"",color:"light_purple",bold:true},{text:"「遅い！」",color:"white"}]}
title @a times 3 70 8
title @a subtitle {text:"",extra:[{selector:"@e[type=marker,tag=rufu_namebox,limit=1]",color:"light_purple",bold:true},{text:"：",color:"light_purple",bold:true},{text:"「遅い！」",color:"white"}]}
title @a title {text:"遅い！",color:"light_purple",bold:true}
execute as @e[tag=rufu_npc_heroine] at @s run playsound minecraft:entity.allay.ambient_without_item voice @a ~ ~ ~ 1.4 1.25
execute at @e[type=mannequin,tag=rufu_npc_heroine] run particle minecraft:angry_villager ~ ~2 ~ 0.6 0.4 0.6 0 10 force
execute as @a at @s run playsound minecraft:entity.villager.no master @s ~ ~ ~ 1 1.3
