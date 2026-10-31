execute as @a[tag=rufu_p] run attribute @s minecraft:movement_speed base set 0
execute as @a[tag=rufu_p] run attribute @s minecraft:jump_strength base set 0
title @a times 0 18 2
title @a title {text:"3",color:"red",bold:true}
execute as @a at @s run playsound minecraft:block.note_block.pling master @s ~ ~ ~ 1 0.8
