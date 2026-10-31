tp @e[type=mannequin,tag=rufu_npc_heroine] 129.458 66 63.5 90 0
execute as @e[type=text_display,tag=rufu_bub_heroine] run data merge entity @s {text:{text:"ん～～～♡",color:"#7a1f5c"},background:-503321354}
scoreboard players set @e[type=text_display,tag=rufu_bub_heroine] rufu.bt 120
tellraw @a {text:"",extra:[{selector:"@e[type=marker,tag=rufu_namebox,limit=1]",color:"light_purple",bold:true},{text:"",color:"light_purple",bold:true},{text:"「ん～～～♡」",color:"white"}]}
title @a times 3 110 8
title @a subtitle {text:"",extra:[{selector:"@e[type=marker,tag=rufu_namebox,limit=1]",color:"light_purple",bold:true},{text:"：",color:"light_purple",bold:true},{text:"「ん～～～♡」",color:"white"}]}
title @a title {text:"ん～～～♡",color:"light_purple",bold:true}
execute as @e[tag=rufu_npc_heroine] at @s run playsound minecraft:entity.allay.ambient_without_item voice @a ~ ~ ~ 1.4 1.25
