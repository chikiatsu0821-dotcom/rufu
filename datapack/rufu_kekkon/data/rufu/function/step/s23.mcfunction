scoreboard players set #step rufu 23
data modify storage rufu:hud now set value "23. ヒロイン「誓います♡」と花火"
data modify storage rufu:hud next set value "24. 神父「それでは、誓いのキスを」"
scoreboard players set #seq rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 23. ヒロイン「誓います♡」と花火",color:"dark_green"}
scoreboard players set #lock rufu 1
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 23
