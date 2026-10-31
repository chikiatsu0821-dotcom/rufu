tp @e[type=marker,tag=rufu_wpm] 63.5 65 136.5
scoreboard players set #spd rufu 3
scoreboard players set #mode rufu 1
scoreboard players set #pause rufu 20
execute as @e[type=text_display,tag=rufu_bub_heroine] run data merge entity @s {text:{text:"ほらほら、離れないで？",color:"#7a1f5c"},background:-503321354}
scoreboard players set @e[type=text_display,tag=rufu_bub_heroine] rufu.bt 60
tellraw @a {text:"",extra:[{selector:"@e[type=marker,tag=rufu_namebox,limit=1]",color:"light_purple",bold:true},{text:"",color:"light_purple",bold:true},{text:"「ほらほら、離れないで？」",color:"white"}]}
execute as @e[tag=rufu_npc_heroine] at @s run playsound minecraft:entity.allay.ambient_without_item voice @a ~ ~ ~ 1.4 1.25
summon minecraft:zombie 71.25 65 136.5 {Tags:["rufu_mob"],PersistenceRequired:true,IsBaby:false,CanPickUpLoot:false,equipment:{head:{id:"minecraft:leather_helmet",count:1}},drop_chances:{head:0.0f},attributes:[{id:"minecraft:spawn_reinforcements",base:0.0d}]}
summon minecraft:zombie 72.75 65 136.5 {Tags:["rufu_mob"],PersistenceRequired:true,IsBaby:false,CanPickUpLoot:false,equipment:{head:{id:"minecraft:leather_helmet",count:1}},drop_chances:{head:0.0f},attributes:[{id:"minecraft:spawn_reinforcements",base:0.0d}]}
particle minecraft:large_smoke 72.0 66 136.5 1.5 0.5 1.5 0.02 30 force
tellraw @a[tag=rufu_p] {text:"🧟 ゾンビの群れだ！ 距離を保ちながら戦え！",color:"dark_green"}
