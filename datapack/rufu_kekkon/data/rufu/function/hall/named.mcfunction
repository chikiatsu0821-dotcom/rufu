scoreboard players set #naming rufu 0
scoreboard players set #named rufu 1
data merge entity @e[type=mannequin,tag=rufu_npc_q,limit=1] {description:{text:"ヒロイン",color:"light_purple"}}
execute as @e[type=text_display,tag=rufu_bub_q] run data merge entity @s {text:{text:"……いい名前♡",color:"#7a1f5c"},background:-503321354}
scoreboard players set @e[type=text_display,tag=rufu_bub_q] rufu.bt 100
tellraw @a {text:"",extra:[{selector:"@e[type=marker,tag=rufu_namebox,limit=1]",color:"light_purple",bold:true},{text:"「",color:"white"},{selector:"@e[type=marker,tag=rufu_namebox,limit=1]",color:"white"},{text:"……いい名前♡」",color:"white"}]}
title @a times 5 70 15
title @a subtitle {text:"",extra:[{selector:"@e[type=marker,tag=rufu_namebox,limit=1]",color:"white"},{text:"……いい名前♡",color:"white"}]}
title @a title {selector:"@e[type=marker,tag=rufu_namebox,limit=1]",color:"light_purple",bold:true}
execute as @a at @s run playsound minecraft:block.note_block.chime master @s ~ ~ ~ 1 1.0
schedule function rufu:hall/chime2 6t
execute at @e[type=mannequin,tag=rufu_npc_q,limit=1] run particle minecraft:heart ~ ~2 ~ 0.8 0.6 0.8 0 25 force
function rufu:hall/others_vanish
