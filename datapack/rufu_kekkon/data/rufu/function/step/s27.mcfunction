scoreboard players set #step rufu 27
data modify storage rufu:hud now set value "27. 「ちょっと待ったーー！！」"
data modify storage rufu:hud next set value "28. 屋根が爆発して元彼レオンがエリトラで乱入"
scoreboard players set #seq rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 27. 「ちょっと待ったーー！！」",color:"dark_green"}
scoreboard players set #lock rufu 1
title @a times 0 50 10
title @a subtitle {text:""}
title @a title {text:"ちょっと待ったーー！！",color:"red",bold:true}
execute as @a at @s run playsound minecraft:entity.ravager.roar master @s ~ ~ ~ 1 1.2
execute as @a at @s run playsound minecraft:block.bell.use master @s ~ ~ ~ 1 0.5
execute as @a at @s run playsound minecraft:entity.lightning_bolt.thunder master @s ~ ~ ~ 0.6 1.4
tellraw @a {text:"",extra:[{text:"？？？",color:"red",bold:true},{text:"「ちょっと待ったーー！！」",color:"white",bold:true}]}
tp @e[type=mannequin,tag=rufu_npc_heroine] 129.5 66 63.5 90 0
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 27
