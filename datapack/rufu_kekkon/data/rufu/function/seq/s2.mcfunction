execute if score #seq_t rufu matches 10 run function rufu:seq/s2/t10
execute if score #seq_t rufu matches 14 run function rufu:seq/s2/t14
execute if score #seq_t rufu matches 22 run playsound minecraft:block.bell.use master @a 32.5 70 226 3 0.75
execute if score #seq_t rufu matches 34 run playsound minecraft:block.bell.resonate master @a 32.5 70 226 2 1
execute if score #seq_t rufu matches 40 run function rufu:seq/s2/t40
execute if score #seq_t rufu matches 140 run function rufu:seq/s2/t140
execute if score #seq_t rufu matches 140.. run scoreboard players set #seq rufu 0
