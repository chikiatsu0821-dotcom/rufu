execute if score #seq_t rufu matches 1 run function rufu:seq/s29/t1
execute if score #seq_t rufu matches 30 run function rufu:seq/s29/t30
execute if score #seq_t rufu matches 60 run function rufu:seq/s29/t60
execute if score #seq_t rufu matches 100 run summon minecraft:lightning_bolt 145 65 72
execute if score #seq_t rufu matches 100.. run scoreboard players set #seq rufu 0
