execute if score #gift rufu matches 1 run return run function rufu:click/_7
scoreboard players set #gift rufu 1
clear @s #minecraft:small_flowers 1
execute as @e[type=text_display,tag=rufu_bub_heroine] run data merge entity @s {text:{text:"わぁ、お花！ ……まぁ、許してあげる♡",color:"#7a1f5c"},background:-503321354}
scoreboard players set @e[type=text_display,tag=rufu_bub_heroine] rufu.bt 70
tellraw @a {text:"",extra:[{selector:"@e[type=marker,tag=rufu_namebox,limit=1]",color:"light_purple",bold:true},{text:"",color:"light_purple",bold:true},{text:"「わぁ、お花！ ……まぁ、許してあげる♡」",color:"white"}]}
title @a times 3 60 8
title @a subtitle {text:"",extra:[{selector:"@e[type=marker,tag=rufu_namebox,limit=1]",color:"light_purple",bold:true},{text:"：",color:"light_purple",bold:true},{text:"「わぁ、お花！ ……まぁ、許してあげる♡」",color:"white"}]}
title @a title {text:""}
execute as @e[tag=rufu_npc_heroine] at @s run playsound minecraft:entity.allay.ambient_without_item voice @a ~ ~ ~ 1.4 1.25
execute at @e[type=mannequin,tag=rufu_npc_heroine] run particle minecraft:heart ~ ~2.2 ~ 0.5 0.4 0.5 0 12 force
scoreboard players add #love rufu 20
execute if score #love rufu matches 101.. run scoreboard players set #love rufu 100
tellraw @a {text:"",extra:[{text:"♥ 好感度 +20 ",color:"light_purple",bold:true},{text:"緊急プレゼント！（このミッションではもう使えない）",color:"gray"}]}
execute as @a at @s run playsound minecraft:block.note_block.chime master @s ~ ~ ~ 0.8 1.6
function rufu:hud/love
