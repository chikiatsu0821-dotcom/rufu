execute if score #seq_t rufu matches 10 run function rufu:seq/s1/t10
execute if score #seq_t rufu matches 30 run execute as @a at @s run playsound minecraft:block.bell.use master @s ~ ~ ~ 1 1.0
execute if score #seq_t rufu matches 50 run function rufu:seq/s1/t50
execute if score #seq_t rufu matches 140 run scoreboard players set #lock rufu 0
execute if score #seq_t rufu matches 140.. run scoreboard players set #seq rufu 0
