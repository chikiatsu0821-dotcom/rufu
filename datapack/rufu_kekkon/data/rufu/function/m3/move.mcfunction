execute if score #pause rufu matches 1.. run return run scoreboard players remove #pause rufu 1
execute if entity @e[type=marker,tag=rufu_wpm,distance=..0.4] run return run function rufu:m3/arrive
execute if score #spd rufu matches 1 if score #mode rufu matches 0 facing entity @e[type=marker,tag=rufu_wpm,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^0.11 facing ^ ^ ^5
execute if score #spd rufu matches 1 if score #mode rufu matches 1 facing entity @e[type=marker,tag=rufu_wpm,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^0.11 facing ^ ^ ^-5
execute if score #spd rufu matches 2 if score #mode rufu matches 0 facing entity @e[type=marker,tag=rufu_wpm,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^0.16 facing ^ ^ ^5
execute if score #spd rufu matches 2 if score #mode rufu matches 1 facing entity @e[type=marker,tag=rufu_wpm,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^0.16 facing ^ ^ ^-5
execute if score #spd rufu matches 3 if score #mode rufu matches 0 facing entity @e[type=marker,tag=rufu_wpm,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^0.2 facing ^ ^ ^5
execute if score #spd rufu matches 3 if score #mode rufu matches 1 facing entity @e[type=marker,tag=rufu_wpm,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^0.2 facing ^ ^ ^-5
execute if score #spd rufu matches 4 if score #mode rufu matches 0 facing entity @e[type=marker,tag=rufu_wpm,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^0.25 facing ^ ^ ^5
execute if score #spd rufu matches 4 if score #mode rufu matches 1 facing entity @e[type=marker,tag=rufu_wpm,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^0.25 facing ^ ^ ^-5
execute if score #spd rufu matches 5 if score #mode rufu matches 0 facing entity @e[type=marker,tag=rufu_wpm,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^0.31 facing ^ ^ ^5
execute if score #spd rufu matches 5 if score #mode rufu matches 1 facing entity @e[type=marker,tag=rufu_wpm,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^0.31 facing ^ ^ ^-5
execute if score #spd rufu matches 6 if score #mode rufu matches 0 facing entity @e[type=marker,tag=rufu_wpm,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^0.36 facing ^ ^ ^5
execute if score #spd rufu matches 6 if score #mode rufu matches 1 facing entity @e[type=marker,tag=rufu_wpm,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^0.36 facing ^ ^ ^-5
execute if score #spd rufu matches 5.. run particle minecraft:cloud ~ ~0.1 ~ 0.2 0 0.2 0 1
