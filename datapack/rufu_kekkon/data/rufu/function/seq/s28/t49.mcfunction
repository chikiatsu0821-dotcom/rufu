data merge entity @e[type=mannequin,tag=rufu_npc_leon,limit=1] {pose:"standing",NoGravity:false,equipment:{chest:{id:"minecraft:leather_chestplate",count:1,components:{dyed_color:1976900}},legs:{id:"minecraft:leather_leggings",count:1,components:{dyed_color:2829099}},feet:{id:"minecraft:leather_boots",count:1,components:{dyed_color:3877402}}}}
tp @e[type=mannequin,tag=rufu_npc_leon] 128.5 65 73.5 180 0
particle minecraft:cloud 128.5 65.2 73.5 0.6 0.1 0.6 0.05 20 force
execute as @a at @s run playsound minecraft:entity.player.big_fall master @s ~ ~ ~ 1 0.8
