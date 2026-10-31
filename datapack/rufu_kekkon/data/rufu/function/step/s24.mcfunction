scoreboard players set #step rufu 24
data modify storage rufu:hud now set value "24. 神父「それでは、誓いのキスを」"
data modify storage rufu:hud next set value "25. ヒロインが近づく「ん～～～♡」"
scoreboard players set #seq rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 24. 神父「それでは、誓いのキスを」",color:"dark_green"}
scoreboard players set #lock rufu 1
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 24
