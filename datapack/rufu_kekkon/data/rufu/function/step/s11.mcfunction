scoreboard players set #step rufu 11
data modify storage rufu:hud now set value "11. 試練3 説明「結婚報告パレード」"
data modify storage rufu:hud next set value "12. 試練3 開始（1周目・昼）"
scoreboard players set #seq rufu 0
scoreboard players set #retry_step rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 11. 試練3 説明「結婚報告パレード」",color:"dark_green"}
scoreboard players set #mission rufu 0
scoreboard players set #lock rufu 1
time set 6000
kill @e[tag=rufu_part_heroine]
summon minecraft:mannequin 128.5 65 133.5 {profile:{texture:"entity/player/slim/alex",model:"slim"},CustomName:{text:"ヒロイン",color:"light_purple",bold:true},CustomNameVisible:true,hide_description:true,immovable:true,Invulnerable:true,Silent:true,Rotation:[0.0f,0.0f],Tags:["rufu_npc","rufu_npc_heroine","rufu_part_heroine","rufu_look"],equipment:{chest:{id:"minecraft:leather_chestplate",count:1,components:{dyed_color:16033480}}},Passengers:[{id:"minecraft:text_display",Tags:["rufu_bub","rufu_bub_heroine","rufu_part_heroine","rufu_npcpart"],billboard:"center",text:{text:""},background:0,line_width:180,shadow:false,see_through:false,transformation:{translation:[0.0f,0.9f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.0f,1.0f,1.0f]}}]}
summon minecraft:interaction 128.5 65 133.5 {Tags:["rufu_click","rufu_hit_heroine","rufu_part_heroine"],width:0.95f,height:2.05f,response:true}
tp @a[tag=rufu_p] 128.5 65 137.5 180 0
title @a times 10 70 15
title @a subtitle {text:"結婚報告パレードで私についてきて",color:"white"}
title @a title {text:"試練3",color:"gold",bold:true}
execute as @a at @s run playsound minecraft:block.note_block.bell master @s ~ ~ ~ 1 1.0
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 11
