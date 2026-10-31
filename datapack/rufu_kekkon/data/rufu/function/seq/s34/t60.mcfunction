execute as @e[type=text_display,tag=rufu_bub_sakura] run data merge entity @s {text:{text:"はじめまして♡",color:"#8a2353"},background:-503322894}
scoreboard players set @e[type=text_display,tag=rufu_bub_sakura] rufu.bt 60
tellraw @a {text:"",extra:[{text:"さくら",color:"#ff8fc8",bold:true},{text:"「はじめまして♡」",color:"white"}]}
execute as @e[tag=rufu_npc_sakura] at @s run playsound minecraft:entity.allay.ambient_with_item voice @a ~ ~ ~ 1.4 1.5
