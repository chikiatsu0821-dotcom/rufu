execute as @e[type=text_display,tag=rufu_bub_heroine] run data merge entity @s {text:{text:"誓います♡",color:"#7a1f5c"},background:-503321354}
scoreboard players set @e[type=text_display,tag=rufu_bub_heroine] rufu.bt 80
tellraw @a {text:"",extra:[{text:"ヒロイン",color:"light_purple",bold:true},{text:"「誓います♡」",color:"white"}]}
title @a times 3 70 8
title @a subtitle {text:"",extra:[{text:"ヒロイン：",color:"light_purple",bold:true},{text:"「誓います♡」",color:"white"}]}
title @a title {text:"誓います♡",color:"light_purple",bold:true}
execute as @e[tag=rufu_npc_heroine] at @s run playsound minecraft:entity.allay.ambient_without_item voice @a ~ ~ ~ 1.4 1.25
execute at @e[type=mannequin,tag=rufu_npc_heroine] run particle minecraft:heart ~ ~2.2 ~ 0.5 0.4 0.5 0 20 force
