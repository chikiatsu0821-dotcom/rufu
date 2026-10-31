execute as @e[type=text_display,tag=rufu_bub_heroine] run data merge entity @s {text:{text:"跳ね橋とか、屋根とか、崩れた壁とか……まぁ、がんばって♡",color:"#7a1f5c"},background:-503321354}
scoreboard players set @e[type=text_display,tag=rufu_bub_heroine] rufu.bt 90
tellraw @a {text:"",extra:[{selector:"@e[type=marker,tag=rufu_namebox,limit=1]",color:"light_purple",bold:true},{text:"",color:"light_purple",bold:true},{text:"「跳ね橋とか、屋根とか、崩れた壁とか……まぁ、がんばって♡」",color:"white"}]}
title @a times 3 80 8
title @a subtitle {text:"",extra:[{selector:"@e[type=marker,tag=rufu_namebox,limit=1]",color:"light_purple",bold:true},{text:"：",color:"light_purple",bold:true},{text:"「跳ね橋とか、屋根とか、崩れた壁とか……まぁ、がんばって♡」",color:"white"}]}
title @a title {text:""}
execute as @e[tag=rufu_npc_heroine] at @s run playsound minecraft:entity.allay.ambient_without_item voice @a ~ ~ ~ 1.4 1.25
