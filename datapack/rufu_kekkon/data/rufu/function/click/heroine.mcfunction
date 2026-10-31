execute if score #active rufu matches 1 if predicate rufu:hold_flower run return run function rufu:click/flower
execute if score #mission rufu matches 2 if score #active rufu matches 1 if entity @s[tag=rufu_p] run return run function rufu:m2/deliver
execute if entity @s[tag=rufu_p] run function rufu:click/_6
