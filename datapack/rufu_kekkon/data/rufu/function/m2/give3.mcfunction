execute if score #got3 rufu matches 1 run return run function rufu:m2/_34
execute if score #own3 rufu <= #np rufu unless score @s rufu.pi = #own3 rufu run return run function rufu:m2/_35
execute store success score #ok rufu run clear @s minecraft:cooked_beef 1
execute if score #ok rufu matches 0 run clear @s minecraft:cooked_porkchop 1
scoreboard players set #got3 rufu 1
data modify storage rufu:m2 s3 set value "✔"
execute as @e[type=text_display,tag=rufu_bub_heroine] run data merge entity @s {text:{text:"式に出すには地味。",color:"#7a1f5c"},background:-503321354}
scoreboard players set @e[type=text_display,tag=rufu_bub_heroine] rufu.bt 70
tellraw @a {text:"",extra:[{selector:"@e[type=marker,tag=rufu_namebox,limit=1]",color:"light_purple",bold:true},{text:"",color:"light_purple",bold:true},{text:"「式に出すには地味。」",color:"white"}]}
title @a times 3 60 8
title @a subtitle {text:"",extra:[{selector:"@e[type=marker,tag=rufu_namebox,limit=1]",color:"light_purple",bold:true},{text:"：",color:"light_purple",bold:true},{text:"「式に出すには地味。」",color:"white"}]}
title @a title {text:""}
execute as @e[tag=rufu_npc_heroine] at @s run playsound minecraft:entity.allay.ambient_without_item voice @a ~ ~ ~ 1.4 1.25
execute at @e[type=mannequin,tag=rufu_npc_heroine] run particle minecraft:happy_villager ~ ~1.5 ~ 0.5 0.5 0.5 0 15 force
playsound minecraft:entity.player.burp master @a ~ ~ ~ 1 1.2
tellraw @a {text:"",extra:[{text:"🍽 お肉 をわたした！ ",color:"red",bold:true},{text:"（",color:"gray"},{selector:"@s"},{text:"） 反応：「式に出すには地味。」",color:"gray"}]}
scoreboard players operation #gotn rufu = #got1 rufu
scoreboard players operation #gotn rufu += #got2 rufu
scoreboard players operation #gotn rufu += #got3 rufu
execute if score #gotn rufu matches 3 run function rufu:m2/clear
