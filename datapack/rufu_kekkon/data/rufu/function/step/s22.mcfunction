scoreboard players set #step rufu 22
data modify storage rufu:hud now set value "22. 神父の誓いの言葉"
data modify storage rufu:hud next set value "23. ヒロイン「誓います♡」と花火"
scoreboard players set #seq rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 22. 神父の誓いの言葉",color:"dark_green"}
scoreboard players set #lock rufu 1
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 22
