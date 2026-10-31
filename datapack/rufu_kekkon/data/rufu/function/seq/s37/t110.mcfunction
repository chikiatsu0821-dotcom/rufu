execute as @e[type=text_display,tag=rufu_bub_hinata] run data merge entity @s {text:{text:"……ふふっ",color:"#7a5a00"},background:-503318047}
scoreboard players set @e[type=text_display,tag=rufu_bub_hinata] rufu.bt 60
tellraw @a {text:"",extra:[{text:"ひなた",color:"#ffd34d",bold:true},{text:"「……ふふっ」",color:"white"}]}
title @a times 3 50 8
title @a subtitle {text:"",extra:[{text:"ひなた：",color:"#ffd34d",bold:true},{text:"「……ふふっ」",color:"white"}]}
title @a title {text:""}
execute as @e[tag=rufu_npc_hinata] at @s run playsound minecraft:entity.allay.ambient_with_item voice @a ~ ~ ~ 1.4 1.6
