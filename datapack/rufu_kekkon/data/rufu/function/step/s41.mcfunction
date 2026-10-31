scoreboard players set #step rufu 41
data modify storage rufu:hud now set value "41. 「ドッキリ大成功！ 仕掛け人：Rufu」で花火"
data modify storage rufu:hud next set value "（おわり）"
scoreboard players set #seq rufu 0
scoreboard players set #retry_step rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 41. 「ドッキリ大成功！ 仕掛け人：Rufu」で花火",color:"dark_green"}
scoreboard players set #lock rufu 1
weather clear
time set 18000
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 41
