execute as @e[type=text_display,tag=rufu_bub_heroine] run data merge entity @s {text:{text:"は？ 不合格。",color:"#7a1f5c"},background:-503321354}
scoreboard players set @e[type=text_display,tag=rufu_bub_heroine] rufu.bt 60
tellraw @a {text:"",extra:[{text:"ヒロイン",color:"light_purple",bold:true},{text:"「は？ 不合格。」",color:"white"}]}
title @a times 3 50 8
title @a subtitle {text:"",extra:[{text:"ヒロイン：",color:"light_purple",bold:true},{text:"「は？ 不合格。」",color:"white"}]}
title @a title {text:""}
execute as @e[tag=rufu_npc_heroine] at @s run playsound minecraft:entity.allay.ambient_without_item voice @a ~ ~ ~ 1.4 1.25
scoreboard players remove #love rufu 10
execute if score #love rufu matches ..-1 run scoreboard players set #love rufu 0
tellraw @a {text:"",extra:[{text:"💔 好感度 -10 ",color:"red",bold:true},{text:"割り込みの答えが×……",color:"gray"}]}
execute as @a at @s run playsound minecraft:entity.villager.no master @s ~ ~ ~ 0.9 1.2
function rufu:hud/love
