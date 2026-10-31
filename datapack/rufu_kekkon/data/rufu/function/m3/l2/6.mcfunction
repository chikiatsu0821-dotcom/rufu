tp @e[type=marker,tag=rufu_wpm] 50.5 65 136.5
scoreboard players set #spd rufu 4
scoreboard players set #mode rufu 0
scoreboard players set #pause rufu 0
summon minecraft:zombie 49.0 65 150.0 {Tags:["rufu_mob"],PersistenceRequired:true,IsBaby:false,CanPickUpLoot:false,equipment:{head:{id:"minecraft:leather_helmet",count:1}},drop_chances:{head:0.0f},attributes:[{id:"minecraft:spawn_reinforcements",base:0.0d}]}
summon minecraft:zombie 50.5 65 150.0 {Tags:["rufu_mob"],PersistenceRequired:true,IsBaby:false,CanPickUpLoot:false,equipment:{head:{id:"minecraft:leather_helmet",count:1}},drop_chances:{head:0.0f},attributes:[{id:"minecraft:spawn_reinforcements",base:0.0d}]}
summon minecraft:zombie 52.0 65 150.0 {Tags:["rufu_mob"],PersistenceRequired:true,IsBaby:false,CanPickUpLoot:false,equipment:{head:{id:"minecraft:leather_helmet",count:1}},drop_chances:{head:0.0f},attributes:[{id:"minecraft:spawn_reinforcements",base:0.0d}]}
particle minecraft:large_smoke 50.5 66 150.0 1.5 0.5 1.5 0.02 30 force
tellraw @a[tag=rufu_p] {text:"🧟 ゾンビの群れだ！ 距離を保ちながら戦え！",color:"dark_green"}
