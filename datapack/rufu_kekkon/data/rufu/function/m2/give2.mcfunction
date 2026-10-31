execute if score #got2 rufu matches 1 run return run function rufu:m2/_32
execute if score #own2 rufu <= #np rufu unless score @s rufu.pi = #own2 rufu run return run function rufu:m2/_33
execute if predicate rufu:hold_cake run clear @s minecraft:cake 1
scoreboard players set #got2 rufu 1
data modify storage rufu:m2 s2 set value "✔"
execute as @e[type=text_display,tag=rufu_bub_heroine] run data merge entity @s {text:{text:"……重い。",color:"#7a1f5c"},background:-503321354}
scoreboard players set @e[type=text_display,tag=rufu_bub_heroine] rufu.bt 70
tellraw @a {text:"",extra:[{selector:"@e[type=marker,tag=rufu_namebox,limit=1]",color:"light_purple",bold:true},{text:"",color:"light_purple",bold:true},{text:"「……重い。」",color:"white"}]}
title @a times 3 60 8
title @a subtitle {text:"",extra:[{selector:"@e[type=marker,tag=rufu_namebox,limit=1]",color:"light_purple",bold:true},{text:"：",color:"light_purple",bold:true},{text:"「……重い。」",color:"white"}]}
title @a title {text:""}
execute as @e[tag=rufu_npc_heroine] at @s run playsound minecraft:entity.allay.ambient_without_item voice @a ~ ~ ~ 1.4 1.25
execute at @e[type=mannequin,tag=rufu_npc_heroine] run particle minecraft:happy_villager ~ ~1.5 ~ 0.5 0.5 0.5 0 15 force
playsound minecraft:entity.player.burp master @a ~ ~ ~ 1 1.2
tellraw @a {text:"",extra:[{text:"🍽 ケーキ をわたした！ ",color:"light_purple",bold:true},{text:"（",color:"gray"},{selector:"@s"},{text:"） 反応：「……重い。」",color:"gray"}]}
scoreboard players operation #gotn rufu = #got1 rufu
scoreboard players operation #gotn rufu += #got2 rufu
scoreboard players operation #gotn rufu += #got3 rufu
execute if score #gotn rufu matches 3 run function rufu:m2/clear
