scoreboard players set #step rufu 39
data modify storage rufu:hud now set value "39. 「じゃ、全員もらってくわ」で空へ"
data modify storage rufu:hud next set value "40. 「ドッキリ大成功！ 仕掛け人：Rufu」で花火"
scoreboard players set #seq rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 39. 「じゃ、全員もらってくわ」で空へ",color:"dark_green"}
scoreboard players set #lock rufu 1
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 39
