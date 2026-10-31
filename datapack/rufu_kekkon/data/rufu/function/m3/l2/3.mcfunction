tp @e[type=marker,tag=rufu_wpm] 62.5 65 112.5
scoreboard players set #spd rufu 4
scoreboard players set #mode rufu 0
scoreboard players set #pause rufu 20
execute as @r[tag=rufu_p,gamemode=!spectator] at @s run function rufu:m3/lightning
