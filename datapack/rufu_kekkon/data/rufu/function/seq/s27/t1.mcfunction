particle minecraft:explosion_emitter 128.5 86 71.5 2 1 2 0 4 force
particle minecraft:large_smoke 128.5 84 71.5 4 2 4 0.05 80 force
execute as @a at @s run playsound minecraft:entity.generic.explode master @s ~ ~ ~ 1 0.8
execute as @a at @s run playsound minecraft:entity.dragon_fireball.explode master @s ~ ~ ~ 0.6 1.0
fill 124 77 68 132 90 74 minecraft:air
summon minecraft:falling_block 128.5 84 71.5 {BlockState:"minecraft:deepslate_tiles",Time:1,DropItem:false,CancelDrop:true,HurtEntities:false,Motion:[0.35d,0.6d,0.0d],Tags:["rufu_debris"]}
summon minecraft:falling_block 128.5 84 71.5 {BlockState:"minecraft:deepslate_tiles",Time:1,DropItem:false,CancelDrop:true,HurtEntities:false,Motion:[0.189d,0.6d,0.295d],Tags:["rufu_debris"]}
summon minecraft:falling_block 128.5 84 71.5 {BlockState:"minecraft:deepslate_tiles",Time:1,DropItem:false,CancelDrop:true,HurtEntities:false,Motion:[-0.146d,0.6d,0.318d],Tags:["rufu_debris"]}
summon minecraft:falling_block 128.5 84 71.5 {BlockState:"minecraft:deepslate_tiles",Time:1,DropItem:false,CancelDrop:true,HurtEntities:false,Motion:[-0.346d,0.6d,0.049d],Tags:["rufu_debris"]}
summon minecraft:falling_block 128.5 84 71.5 {BlockState:"minecraft:deepslate_tiles",Time:1,DropItem:false,CancelDrop:true,HurtEntities:false,Motion:[-0.229d,0.6d,-0.265d],Tags:["rufu_debris"]}
summon minecraft:falling_block 128.5 84 71.5 {BlockState:"minecraft:deepslate_tiles",Time:1,DropItem:false,CancelDrop:true,HurtEntities:false,Motion:[0.099d,0.6d,-0.336d],Tags:["rufu_debris"]}
