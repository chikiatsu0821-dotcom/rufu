execute unless entity @s[tag=rufu_hero] run return run function rufu:hall/_41
execute if score #qchosen rufu matches 1 run return 0
execute if score #hit rufu matches 4 run return run function rufu:hall/pick_q
execute if score #hit rufu matches 1 run function rufu:hall/pick_sakura
execute if score #hit rufu matches 2 run function rufu:hall/pick_mio
execute if score #hit rufu matches 3 run function rufu:hall/pick_hinata
