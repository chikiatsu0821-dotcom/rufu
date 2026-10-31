playsound minecraft:block.anvil.place master @a ~ ~ ~ 1 2
title @s times 0 20 5
title @s subtitle {text:"⚠ 頭上注意！",color:"red",bold:true}
title @s title {text:""}
execute store result score #r rufu run random value 0..3
execute if score #r rufu matches 0 run summon minecraft:falling_block ~1 ~14 ~ {BlockState:"minecraft:anvil",Time:1,DropItem:false,HurtEntities:true,FallHurtMax:6,FallHurtAmount:1.0f,CancelDrop:true,Tags:["rufu_mob"]}
execute if score #r rufu matches 1 run summon minecraft:falling_block ~-1 ~14 ~ {BlockState:"minecraft:anvil",Time:1,DropItem:false,HurtEntities:true,FallHurtMax:6,FallHurtAmount:1.0f,CancelDrop:true,Tags:["rufu_mob"]}
execute if score #r rufu matches 2 run summon minecraft:falling_block ~ ~14 ~1 {BlockState:"minecraft:anvil",Time:1,DropItem:false,HurtEntities:true,FallHurtMax:6,FallHurtAmount:1.0f,CancelDrop:true,Tags:["rufu_mob"]}
execute if score #r rufu matches 3 run summon minecraft:falling_block ~ ~14 ~ {BlockState:"minecraft:anvil",Time:1,DropItem:false,HurtEntities:true,FallHurtMax:6,FallHurtAmount:1.0f,CancelDrop:true,Tags:["rufu_mob"]}
