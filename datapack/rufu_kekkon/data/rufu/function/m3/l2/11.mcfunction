tp @e[type=marker,tag=rufu_wpm] 63.5 65 121.5
scoreboard players set #spd rufu 5
scoreboard players set #mode rufu 0
scoreboard players set #pause rufu 0
execute as @r[tag=rufu_p,gamemode=!spectator] at @s run function rufu:m3/lightning
