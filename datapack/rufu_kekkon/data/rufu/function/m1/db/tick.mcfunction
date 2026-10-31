scoreboard players remove #db_t rufu 1
execute if score #db_s rufu matches 2 if score #db_t rufu matches 14 run playsound minecraft:block.bell.use master @a 128 70 206 2 1.6
execute if score #db_s rufu matches 2 if score #db_t rufu matches 7 run playsound minecraft:block.bell.use master @a 128 70 206 2 1.6
execute if score #db_t rufu matches ..0 run function rufu:m1/db/next
