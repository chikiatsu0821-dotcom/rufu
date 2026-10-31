kill @e[tag=rufu_ask]
scoreboard players set #ev rufu 0
execute as @a run attribute @s minecraft:movement_speed base reset
execute as @a run attribute @s minecraft:jump_strength base reset
scoreboard players operation #step rufu = #retry_step rufu
function rufu:step/goto
