scoreboard players set #step rufu 36
data modify storage rufu:hud now set value "36. 選ばれた子「やっと選んでくれたね……」"
data modify storage rufu:hud next set value "37. 3人「……でもね」「実は私たち……」"
scoreboard players set #seq rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 36. 選ばれた子「やっと選んでくれたね……」",color:"dark_green"}
scoreboard players set #lock rufu 1
execute if score #chosen rufu matches 0 run execute store result score #chosen rufu run random value 1..3
execute if score #chosen rufu matches 1 run function rufu:end/_50
execute if score #chosen rufu matches 2 run function rufu:end/_51
execute if score #chosen rufu matches 3 run function rufu:end/_52
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 36
