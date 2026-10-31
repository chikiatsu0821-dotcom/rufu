execute as @e[type=text_display,tag=rufu_bub_priest] run data merge entity @s {text:{text:"ハァン……",color:"#5b4316"},background:-503318303}
scoreboard players set @e[type=text_display,tag=rufu_bub_priest] rufu.bt 90
tellraw @a {text:"",extra:[{text:"神父",color:"gold",bold:true},{text:"「ハァン……」",color:"white"}]}
title @a times 3 80 8
title @a subtitle {text:"",extra:[{text:"神父：",color:"gold",bold:true},{text:"「ハァン……」",color:"white"}]}
title @a title {text:"ハァン……",color:"gold",bold:true}
execute as @e[tag=rufu_npc_priest] at @s run playsound minecraft:entity.villager.ambient voice @a ~ ~ ~ 1.4 0.6
execute as @a at @s run playsound minecraft:entity.villager.no master @s ~ ~ ~ 1 0.5
