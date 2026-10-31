execute unless score #active rufu matches 1 run return 0
execute if score #elapsed rufu matches 2400 run function rufu:ev/start/m2_shuffle
execute if score #elapsed rufu matches 2200 run function rufu:m2/_36
execute if score #m20 rufu matches 0 run function rufu:m2/hud
