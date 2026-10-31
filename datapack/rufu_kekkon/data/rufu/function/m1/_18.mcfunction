function rufu:m1/db/down
scoreboard players set #db_s rufu 2
execute store result score #db_t rufu run random value 40..70
