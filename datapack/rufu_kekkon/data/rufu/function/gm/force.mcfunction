tellraw @a {text:"⏭ GMが強制的に進めました",color:"gray"}
scoreboard players set #active rufu 0
scoreboard players set #lock rufu 0
scoreboard players set #ev rufu 0
bossbar set rufu:time visible false
bossbar set rufu:out visible false
execute as @a run attribute @s minecraft:movement_speed base reset
execute as @a run attribute @s minecraft:jump_strength base reset
scoreboard players add #step rufu 1
function rufu:step/goto
