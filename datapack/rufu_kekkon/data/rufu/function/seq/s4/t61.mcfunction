title @a times 0 30 10
title @a subtitle {text:"3人全員クリアが条件！",color:"white"}
title @a title {text:"スタート！",color:"green",bold:true}
execute as @a at @s run playsound minecraft:block.note_block.pling master @s ~ ~ ~ 1 2.0
execute as @a at @s run playsound minecraft:entity.firework_rocket.launch master @s ~ ~ ~ 1 1.2
execute as @a run attribute @s minecraft:movement_speed base reset
execute as @a run attribute @s minecraft:jump_strength base reset
scoreboard players set #active rufu 1
execute at @e[type=mannequin,tag=rufu_npc_heroine] run particle minecraft:poof ~ ~1 ~ 0.4 0.8 0.4 0.02 30 force
execute at @e[type=mannequin,tag=rufu_npc_heroine] run playsound minecraft:entity.illusioner.mirror_move master @a ~ ~ ~ 1 1.2
execute as @e[type=text_display,tag=rufu_bub_heroine] run data merge entity @s {text:{text:"じゃ、広場で待ってるね～♪",color:"#7a1f5c"},background:-503321354}
scoreboard players set @e[type=text_display,tag=rufu_bub_heroine] rufu.bt 40
tellraw @a {text:"",extra:[{selector:"@e[type=marker,tag=rufu_namebox,limit=1]",color:"light_purple",bold:true},{text:"",color:"light_purple",bold:true},{text:"「じゃ、広場で待ってるね～♪」",color:"white"}]}
execute as @e[tag=rufu_npc_heroine] at @s run playsound minecraft:entity.allay.ambient_without_item voice @a ~ ~ ~ 1.4 1.25
kill @e[tag=rufu_part_heroine]
