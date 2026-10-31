scoreboard players set #step rufu 17
data modify storage rufu:hud now set value "17. 「やっぱりなかったことにして」空が巻き戻る"
data modify storage rufu:hud next set value "18. 試練4 2回目開始（キツネ3匹・3分）"
scoreboard players set #seq rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 17. 「やっぱりなかったことにして」空が巻き戻る",color:"dark_green"}
scoreboard players set #lock rufu 1
kill @e[tag=rufu_demo]
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 17
