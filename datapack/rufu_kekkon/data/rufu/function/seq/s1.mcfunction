execute if score #seq_t rufu matches 8 run function rufu:seq/s1/t8
execute if score #seq_t rufu matches 16 run execute as @a at @s run playsound minecraft:block.amethyst_block.chime master @s ~ ~ ~ 1 1.6
execute if score #seq_t rufu matches 24 run execute as @a at @s run playsound minecraft:block.amethyst_block.resonate master @s ~ ~ ~ 1 1.0
execute if score #seq_t rufu matches 110 run function rufu:seq/s1/t110
execute if score #seq_t rufu matches 110.. run scoreboard players set #seq rufu 0
