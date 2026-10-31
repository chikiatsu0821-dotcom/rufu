scoreboard players set #step rufu 34
data modify storage rufu:hud now set value "34. スタッフロール →「END ノーマルエンド：返品」"
data modify storage rufu:hud next set value "35. アップデートのお知らせ：さくら・みお・ひなた実装"
scoreboard players set #seq rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 34. スタッフロール →「END ノーマルエンド：返品」",color:"dark_green"}
scoreboard players set #lock rufu 1
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 34
