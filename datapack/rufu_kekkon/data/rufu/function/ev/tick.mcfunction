scoreboard players add #ev_t rufu 1
execute if score #ev rufu matches 1 run function rufu:ev/fail
execute if score #ev rufu matches 2 run function rufu:ev/m1_clear
execute if score #ev rufu matches 3 run function rufu:ev/m2_shuffle
execute if score #ev rufu matches 4 run function rufu:ev/m2_clear
execute if score #ev rufu matches 5 run function rufu:ev/m3_lap1_end
execute if score #ev rufu matches 6 run function rufu:ev/m3_clear
execute if score #ev rufu matches 7 run function rufu:ev/m4_yes1
execute if score #ev rufu matches 8 run function rufu:ev/m4_yes2
