execute if score #ghy rufu matches 0 as @e[type=happy_ghast,tag=rufu_ghast] at @s if entity @s[y=73,dy=100] run tp @s ~ ~-0.35 ~
execute if score #ghy rufu matches 1 as @e[type=happy_ghast,tag=rufu_ghast] at @s run tp @s ~0.05 ~0.3 ~-0.12
execute if score #ghy rufu matches 1 as @e[type=happy_ghast,tag=rufu_ghast] at @s if entity @s[y=160,dy=100] run kill @e[tag=rufu_part_leon]
execute if score #ghy rufu matches 1 as @e[type=happy_ghast,tag=rufu_ghast] at @s if entity @s[y=160,dy=100] run kill @e[tag=rufu_clone]
execute if score #ghy rufu matches 1 as @e[type=happy_ghast,tag=rufu_ghast] at @s if entity @s[y=160,dy=100] run kill @s
