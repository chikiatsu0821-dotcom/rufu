scoreboard players set #step rufu 35
data modify storage rufu:hud now set value "35. アップデートのお知らせ：さくら・みお・ひなた実装"
data modify storage rufu:hud next set value "36. 選ばれた子「やっと選んでくれたね……」"
scoreboard players set #seq rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 35. アップデートのお知らせ：さくら・みお・ひなた実装",color:"dark_green"}
scoreboard players set #lock rufu 1
scoreboard players set #chosen rufu 0
kill @e[tag=rufu_part_priest]
tp @a[tag=rufu_p] 128.5 65 68.5 180 0
title @a times 10 70 20
title @a subtitle {text:"さくら・みお・ひなたが実装されました！",color:"white",bold:true}
title @a title {text:"📢 アップデートのお知らせ",color:"aqua",bold:true}
function rufu:song/fanfare
tellraw @a {text:"",extra:[{text:"📢 アップデートのお知らせ：",color:"aqua",bold:true},{text:"さくら・みお・ひなたが実装されました！",color:"white"}]}
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 35
