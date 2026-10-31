execute as @e[type=text_display,tag=rufu_bub_leon] run data merge entity @s {text:{text:"行くぜ、しっかりつかまってな！",color:"#16425b"},background:-505285121}
scoreboard players set @e[type=text_display,tag=rufu_bub_leon] rufu.bt 70
tellraw @a {text:"",extra:[{text:"レオン",color:"aqua",bold:true},{text:"「行くぜ、しっかりつかまってな！」",color:"white"}]}
title @a times 3 60 8
title @a subtitle {text:"",extra:[{text:"レオン：",color:"aqua",bold:true},{text:"「行くぜ、しっかりつかまってな！」",color:"white"}]}
title @a title {text:""}
execute as @e[tag=rufu_npc_leon] at @s run playsound minecraft:entity.villager.trade voice @a ~ ~ ~ 1.4 0.85
