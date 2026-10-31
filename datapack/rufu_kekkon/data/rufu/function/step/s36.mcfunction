scoreboard players set #step rufu 36
data modify storage rufu:hud now set value "36. 3人「……でもね」「実は私たち……」"
data modify storage rufu:hud next set value "37. 3人ともヒロインに変身"
scoreboard players set #seq rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 36. 3人「……でもね」「実は私たち……」",color:"dark_green"}
scoreboard players set #lock rufu 1
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 36
