scoreboard players set #step rufu 29
data modify storage rufu:hud now set value "29. ヒロイン「レオンくん……！」好感度が0に"
data modify storage rufu:hud next set value "30. 「こっちにする」→ 雷雨"
scoreboard players set #seq rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 29. ヒロイン「レオンくん……！」好感度が0に",color:"dark_green"}
scoreboard players set #lock rufu 1
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 29
