execute unless entity @s[tag=rufu_hero] run return run function rufu:m4/_38
execute store result score #hr rufu run clear @s minecraft:gold_nugget[custom_data~{rufu_ring:1b}] 0
execute if score #hr rufu matches 0 run return run function rufu:m4/_39
execute positioned 195.5 81 89.5 store result score #inc rufu if entity @a[tag=rufu_p,distance=..5.1]
execute if score #inc rufu < #np rufu run return run function rufu:m4/_40
clear @s minecraft:gold_nugget[custom_data~{rufu_ring:1b}] 1
kill @e[tag=rufu_sign]
kill @e[tag=rufu_sign_hit]
scoreboard players set #m4p rufu 3
execute if score #m4try rufu matches 1 run function rufu:m4/yes1
execute if score #m4try rufu matches 2 run function rufu:m4/yes2
