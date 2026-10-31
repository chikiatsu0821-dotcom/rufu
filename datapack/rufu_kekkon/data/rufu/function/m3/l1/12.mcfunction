tp @e[type=marker,tag=rufu_wpm] 62.5 65 99.5
scoreboard players set #spd rufu 2
scoreboard players set #mode rufu 0
scoreboard players set #pause rufu 30
summon minecraft:zombie 57.25 65 92.0 {Tags:["rufu_mob"],PersistenceRequired:true,IsBaby:false,CanPickUpLoot:false,equipment:{head:{id:"minecraft:leather_helmet",count:1}},drop_chances:{head:0.0f},attributes:[{id:"minecraft:spawn_reinforcements",base:0.0d}]}
summon minecraft:zombie 58.75 65 92.0 {Tags:["rufu_mob"],PersistenceRequired:true,IsBaby:false,CanPickUpLoot:false,equipment:{head:{id:"minecraft:leather_helmet",count:1}},drop_chances:{head:0.0f},attributes:[{id:"minecraft:spawn_reinforcements",base:0.0d}]}
particle minecraft:large_smoke 58.0 66 92.0 1.5 0.5 1.5 0.02 30 force
tellraw @a[tag=rufu_p] {text:"🧟 ゾンビの群れだ！ 距離を保ちながら戦え！",color:"dark_green"}
execute as @r[tag=rufu_p,gamemode=!spectator] at @s run function rufu:m3/anvil
