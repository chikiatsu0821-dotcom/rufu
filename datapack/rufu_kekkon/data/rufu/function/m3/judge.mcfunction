scoreboard players set #outnow rufu 0
execute as @a[tag=rufu_p,gamemode=!spectator] at @s unless entity @e[type=mannequin,tag=rufu_npc_heroine,distance=2..5] run scoreboard players set #outnow rufu 1
execute if score #outnow rufu matches 1 run scoreboard players add #outg rufu 2
execute if score #outnow rufu matches 0 if score #outg rufu matches 1.. run scoreboard players remove #outg rufu 1
execute store result bossbar rufu:out value run scoreboard players get #outg rufu
execute if score #outg rufu matches 200.. run return run function rufu:mission/fail/out
