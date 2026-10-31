scoreboard players set #step rufu 15
data modify storage rufu:hud now set value "15. 試練4 説明「指輪？……あの子が持ってっちゃった」"
data modify storage rufu:hud next set value "16. 試練4 開始（1回目・3分）"
scoreboard players set #seq rufu 0
scoreboard players set #retry_step rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 15. 試練4 説明「指輪？……あの子が持ってっちゃった」",color:"dark_green"}
scoreboard players set #mission rufu 0
scoreboard players set #lock rufu 1
time set 18000
function rufu:m4/reset
kill @e[tag=rufu_part_heroine]
summon minecraft:mannequin 195.5 81 85.5 {profile:{texture:"entity/player/slim/alex",model:"slim"},CustomName:{text:"ヒロイン",color:"light_purple",bold:true},CustomNameVisible:true,hide_description:true,immovable:true,Invulnerable:true,Silent:true,Rotation:[0.0f,0.0f],Tags:["rufu_npc","rufu_npc_heroine","rufu_part_heroine","rufu_look"],equipment:{chest:{id:"minecraft:leather_chestplate",count:1,components:{dyed_color:16033480}}},Passengers:[{id:"minecraft:text_display",Tags:["rufu_bub","rufu_bub_heroine","rufu_part_heroine","rufu_npcpart"],billboard:"center",text:{text:""},background:0,line_width:180,shadow:false,see_through:false,transformation:{translation:[0.0f,0.9f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.0f,1.0f,1.0f]}}]}
data modify entity @e[type=mannequin,tag=rufu_npc_heroine,limit=1] CustomName set from entity @e[type=marker,tag=rufu_namebox,limit=1] CustomName
summon minecraft:interaction 195.5 81 85.5 {Tags:["rufu_click","rufu_hit_heroine","rufu_part_heroine"],width:0.95f,height:2.05f,response:true}
tp @a[tag=rufu_p] 195.5 81 95.5 0 0
title @a times 10 70 15
title @a subtitle {text:"指輪を取り返して、伝説の木の下で告白して",color:"white"}
title @a title {text:"試練4",color:"gold",bold:true}
execute as @a at @s run playsound minecraft:block.note_block.bell master @s ~ ~ ~ 1 1.0
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 15
