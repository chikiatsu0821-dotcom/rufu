scoreboard players set #step rufu 33
data modify storage rufu:hud now set value "33. 婚約指輪が「返品された指輪」に"
data modify storage rufu:hud next set value "34. スタッフロール →「END ノーマルエンド：返品」"
scoreboard players set #seq rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 33. 婚約指輪が「返品された指輪」に",color:"dark_green"}
scoreboard players set #lock rufu 1
clear @a minecraft:gold_nugget[custom_data~{rufu_ring:1b}]
give @a[tag=rufu_hero,limit=1] minecraft:gold_nugget[custom_name={text:"💍 返品された指輪",color:"gray",italic:false},lore=[{text:"返品理由：元彼が来たため",color:"gray",italic:false},{text:"※返金はありません",color:"gray",italic:false}],custom_data={rufu_ring_returned:1b},enchantment_glint_override=false] 1
title @a times 10 80 20
title @a subtitle {text:"返品理由：元彼が来たため",color:"white"}
title @a title {text:"💍 返品された指輪",color:"gray",bold:true}
execute as @a at @s run playsound minecraft:block.note_block.didgeridoo master @s ~ ~ ~ 1 0.5
tellraw @a {text:"📦 婚約指輪が「返品された指輪」になった（返品理由：元彼が来たため）",color:"gray"}
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 33
