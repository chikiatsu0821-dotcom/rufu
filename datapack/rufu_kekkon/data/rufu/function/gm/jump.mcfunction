$scoreboard players set #step rufu $(n)
scoreboard players set #active rufu 0
scoreboard players set #lock rufu 0
scoreboard players set #ev rufu 0
execute as @a run attribute @s minecraft:movement_speed base reset
execute as @a run attribute @s minecraft:jump_strength base reset
function rufu:step/goto
