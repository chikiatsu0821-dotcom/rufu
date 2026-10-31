title @a times 0 30 10
title @a subtitle {text:"3人全員クリアが条件！",color:"white"}
title @a title {text:"パレード開始！",color:"green",bold:true}
execute as @a at @s run playsound minecraft:block.note_block.pling master @s ~ ~ ~ 1 2.0
execute as @a at @s run playsound minecraft:entity.firework_rocket.launch master @s ~ ~ ~ 1 1.2
execute as @a run attribute @s minecraft:movement_speed base reset
execute as @a run attribute @s minecraft:jump_strength base reset
scoreboard players set #active rufu 1
scoreboard players set #wp rufu 1
function rufu:m3/wp_go
