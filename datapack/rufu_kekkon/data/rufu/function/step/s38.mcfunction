scoreboard players set #step rufu 38
data modify storage rufu:hud now set value "38. 3人ともヒロインに変身"
data modify storage rufu:hud next set value "39. 元彼がハッピーガストで天窓から登場"
scoreboard players set #seq rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 38. 3人ともヒロインに変身",color:"dark_green"}
scoreboard players set #lock rufu 1
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 38
