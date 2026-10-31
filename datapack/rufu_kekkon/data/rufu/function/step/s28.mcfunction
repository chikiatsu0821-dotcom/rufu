scoreboard players set #step rufu 28
data modify storage rufu:hud now set value "28. 屋根が爆発して元彼レオンがエリトラで乱入"
data modify storage rufu:hud next set value "29. ヒロイン「レオンくん……！」好感度が0に"
scoreboard players set #seq rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 28. 屋根が爆発して元彼レオンがエリトラで乱入",color:"dark_green"}
scoreboard players set #lock rufu 1
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 28
