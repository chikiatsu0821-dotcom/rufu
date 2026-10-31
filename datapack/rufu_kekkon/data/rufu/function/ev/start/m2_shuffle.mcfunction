scoreboard players set #ev_t rufu 0
scoreboard players set #ev rufu 3
execute as @e[type=text_display,tag=rufu_bub_heroine] run data merge entity @s {text:{text:"やっぱ担当交代！",color:"#7a1f5c"},background:-503321354}
scoreboard players set @e[type=text_display,tag=rufu_bub_heroine] rufu.bt 80
tellraw @a {text:"",extra:[{text:"ヒロイン",color:"light_purple",bold:true},{text:"「やっぱ担当交代！」",color:"white"}]}
title @a times 3 70 8
title @a subtitle {text:"",extra:[{text:"ヒロイン：",color:"light_purple",bold:true},{text:"「やっぱ担当交代！」",color:"white"}]}
title @a title {text:"やっぱ担当交代！",color:"light_purple",bold:true}
execute as @e[tag=rufu_npc_heroine] at @s run playsound minecraft:entity.allay.ambient_without_item voice @a ~ ~ ~ 1.4 1.25
execute as @a at @s run playsound minecraft:entity.villager.celebrate master @s ~ ~ ~ 1 1.4
execute as @a at @s run playsound minecraft:block.note_block.bit master @s ~ ~ ~ 1 0.7
