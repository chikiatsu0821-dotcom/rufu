execute as @e[type=text_display,tag=rufu_bub_priest] run data merge entity @s {text:{text:"病めるときも、健やかなるときも、",color:"#5b4316"},background:-503318303}
scoreboard players set @e[type=text_display,tag=rufu_bub_priest] rufu.bt 80
tellraw @a {text:"",extra:[{text:"神父",color:"gold",bold:true},{text:"「病めるときも、健やかなるときも、」",color:"white"}]}
title @a times 3 70 8
title @a subtitle {text:"",extra:[{text:"神父：",color:"gold",bold:true},{text:"「病めるときも、健やかなるときも、」",color:"white"}]}
title @a title {text:""}
execute as @e[tag=rufu_npc_priest] at @s run playsound minecraft:entity.villager.ambient voice @a ~ ~ ~ 1.4 0.6
