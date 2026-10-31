scoreboard players set #step rufu 40
data modify storage rufu:hud now set value "40. 「じゃ、全員もらってくわ」で空へ"
data modify storage rufu:hud next set value "41. 「ドッキリ大成功！ 仕掛け人：Rufu」で花火"
scoreboard players set #seq rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 40. 「じゃ、全員もらってくわ」で空へ",color:"dark_green"}
scoreboard players set #lock rufu 1
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 40
