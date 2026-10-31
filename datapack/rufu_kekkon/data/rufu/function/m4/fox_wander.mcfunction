execute if score #m20 rufu matches 0 store result entity @s Rotation[0] float 1 run random value 0..359
execute rotated as @s rotated ~ 0 positioned ^ ^ ^0.07 if entity @e[type=marker,tag=rufu_hillc,distance=..10] unless entity @e[type=marker,tag=rufu_trunk,distance=..1.8] run tp @s ~ ~ ~
