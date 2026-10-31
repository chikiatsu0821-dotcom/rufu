tp @e[type=marker,tag=rufu_wpm] 90.5 65 121.5
scoreboard players set #spd rufu 3
scoreboard players set #mode rufu 0
scoreboard players set #pause rufu 25
execute as @e[type=text_display,tag=rufu_bub_heroine] run data merge entity @s {text:{text:"あ、忘れ物。",color:"#7a1f5c"},background:-503321354}
scoreboard players set @e[type=text_display,tag=rufu_bub_heroine] rufu.bt 60
tellraw @a {text:"",extra:[{selector:"@e[type=marker,tag=rufu_namebox,limit=1]",color:"light_purple",bold:true},{text:"",color:"light_purple",bold:true},{text:"「あ、忘れ物。」",color:"white"}]}
execute as @e[tag=rufu_npc_heroine] at @s run playsound minecraft:entity.allay.ambient_without_item voice @a ~ ~ ~ 1.4 1.25
