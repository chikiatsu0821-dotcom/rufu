execute if score #seq_t rufu matches 1 run playsound minecraft:block.bell.use master @a 128 88 85 4 0.9
execute if score #seq_t rufu matches 12 run playsound minecraft:block.bell.use master @a 128 88 85 4 0.75
execute if score #seq_t rufu matches 24 run playsound minecraft:block.bell.use master @a 128 88 85 4 0.9
execute if score #seq_t rufu matches 36 run playsound minecraft:block.bell.resonate master @a 128 88 85 3 1
execute if score #seq_t rufu matches 50 run function rufu:seq/s21/t50
execute if score #seq_t rufu matches 60 run execute positioned 128.5 70 70 run particle minecraft:cherry_leaves ~ ~ ~ 6 3 10 0 120 force
execute if score #seq_t rufu matches 120 run function rufu:seq/s21/t120
execute if score #seq_t rufu matches 200 run execute positioned 128.5 70 70 run particle minecraft:cherry_leaves ~ ~ ~ 6 3 10 0 120 force
execute if score #seq_t rufu matches 200.. run scoreboard players set #seq rufu 0
