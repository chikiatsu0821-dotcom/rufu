scoreboard players set #step rufu 29
data modify storage rufu:hud now set value "29. 「こっちにする」→ 雷雨"
data modify storage rufu:hud next set value "30. 豚でのろのろ逃走（追いつけない）"
scoreboard players set #seq rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 29. 「こっちにする」→ 雷雨",color:"dark_green"}
scoreboard players set #lock rufu 1
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 29
