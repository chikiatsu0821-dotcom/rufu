execute if score #seq_t rufu matches 10 run tellraw @a[tag=rufu_helper] {text:"🎩 助っ人のふたりは「友人代表」として最前列に座っています（スニークで立てます）",color:"gray"}
execute if score #seq_t rufu matches 40 run scoreboard players set #lock rufu 0
execute if score #seq_t rufu matches 40.. run scoreboard players set #seq rufu 0
