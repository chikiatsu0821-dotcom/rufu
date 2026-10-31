execute unless score #active rufu matches 1 run return 0
execute as @e[type=mannequin,tag=rufu_npc_heroine,limit=1] at @s run function rufu:m3/move
function rufu:m3/judge
execute as @a[tag=rufu_p] at @s run function rufu:m3/dist
execute as @a[tag=rufu_p] run function rufu:m3/bar
