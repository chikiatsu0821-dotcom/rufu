title @a times 0 80 20
title @a subtitle {text:"理由：道が気に入らなかった",color:"white"}
title @a title {text:"評価：B",color:"yellow",bold:true}
execute as @a at @s run playsound minecraft:block.note_block.basedrum master @s ~ ~ ~ 1 0.6
execute as @a at @s run playsound minecraft:entity.firework_rocket.blast master @s ~ ~ ~ 1 0.8
tellraw @a {text:"",extra:[{text:"📋 評価：B",color:"yellow",bold:true},{text:"　理由：道が気に入らなかった",color:"white"}]}
