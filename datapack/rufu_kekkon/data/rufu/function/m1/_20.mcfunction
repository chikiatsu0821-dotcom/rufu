function rufu:m1/db/up
scoreboard players set #db_s rufu 0
execute store result score #db_t rufu run random value 70..170
