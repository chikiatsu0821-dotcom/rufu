tp @e[type=marker,tag=rufu_wpm] 62.5 65 99.5
scoreboard players set #spd rufu 5
scoreboard players set #mode rufu 0
scoreboard players set #pause rufu 0
summon minecraft:zombie 61.0 65 108.0 {Tags:["rufu_mob"],PersistenceRequired:true,IsBaby:false,CanPickUpLoot:false,equipment:{head:{id:"minecraft:leather_helmet",count:1}},drop_chances:{head:0.0f},attributes:[{id:"minecraft:spawn_reinforcements",base:0.0d}]}
summon minecraft:zombie 62.5 65 108.0 {Tags:["rufu_mob"],PersistenceRequired:true,IsBaby:false,CanPickUpLoot:false,equipment:{head:{id:"minecraft:leather_helmet",count:1}},drop_chances:{head:0.0f},attributes:[{id:"minecraft:spawn_reinforcements",base:0.0d}]}
summon minecraft:zombie 64.0 65 108.0 {Tags:["rufu_mob"],PersistenceRequired:true,IsBaby:false,CanPickUpLoot:false,equipment:{head:{id:"minecraft:leather_helmet",count:1}},drop_chances:{head:0.0f},attributes:[{id:"minecraft:spawn_reinforcements",base:0.0d}]}
particle minecraft:large_smoke 62.5 66 108.0 1.5 0.5 1.5 0.02 30 force
tellraw @a[tag=rufu_p] {text:"🧟 ゾンビの群れだ！ 距離を保ちながら戦え！",color:"dark_green"}
