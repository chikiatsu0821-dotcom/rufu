execute as @e[type=text_display,tag=rufu_bub_leon] run data merge entity @s {text:{text:"迎えに来たぜ。",color:"#16425b"},background:-505285121}
scoreboard players set @e[type=text_display,tag=rufu_bub_leon] rufu.bt 80
tellraw @a {text:"",extra:[{text:"レオン",color:"aqua",bold:true},{text:"「迎えに来たぜ。」",color:"white"}]}
title @a times 3 70 8
title @a subtitle {text:"",extra:[{text:"レオン：",color:"aqua",bold:true},{text:"「迎えに来たぜ。」",color:"white"}]}
title @a title {text:""}
execute as @e[tag=rufu_npc_leon] at @s run playsound minecraft:entity.villager.trade voice @a ~ ~ ~ 1.4 0.85
tag @e[type=mannequin,tag=rufu_npc_leon] add rufu_look
scoreboard players set #lock rufu 0
