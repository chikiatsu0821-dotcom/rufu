scoreboard players set #step rufu 3
data modify storage rufu:hud now set value "3. 試練1 説明「私より早く広場に来て」"
data modify storage rufu:hud next set value "4. 試練1 開始（45秒）"
scoreboard players set #seq rufu 0
scoreboard players set #retry_step rufu 0
scoreboard players set #mission rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 3. 試練1 説明「私より早く広場に来て」",color:"dark_green"}
kill @e[tag=rufu_rules]
effect give @a[tag=rufu_p] minecraft:blindness 2 0 true
time set 1000
tp @a[tag=rufu_p] 128.5 65 235.5 180 0
gamemode adventure @a[tag=rufu_p]
kill @e[tag=rufu_part_heroine]
summon minecraft:mannequin 132.5 65 234.5 {profile:{texture:"entity/player/slim/alex",model:"slim"},CustomName:{text:"ヒロイン",color:"light_purple",bold:true},CustomNameVisible:true,hide_description:true,immovable:true,Invulnerable:true,Silent:true,Rotation:[90.0f,0.0f],Tags:["rufu_npc","rufu_npc_heroine","rufu_part_heroine","rufu_look"],equipment:{chest:{id:"minecraft:leather_chestplate",count:1,components:{dyed_color:16033480}}},Passengers:[{id:"minecraft:text_display",Tags:["rufu_bub","rufu_bub_heroine","rufu_part_heroine","rufu_npcpart"],billboard:"center",text:{text:""},background:0,line_width:180,shadow:false,see_through:false,transformation:{translation:[0.0f,0.9f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.0f,1.0f,1.0f]}}]}
data modify entity @e[type=mannequin,tag=rufu_npc_heroine,limit=1] CustomName set from entity @e[type=marker,tag=rufu_namebox,limit=1] CustomName
summon minecraft:interaction 132.5 65 234.5 {Tags:["rufu_click","rufu_hit_heroine","rufu_part_heroine"],width:0.95f,height:2.05f,response:true}
title @a times 10 70 15
title @a subtitle {text:"私より早く広場に来て（制限時間45秒）",color:"white"}
title @a title {text:"試練1",color:"gold",bold:true}
execute as @a at @s run playsound minecraft:block.note_block.bell master @s ~ ~ ~ 1 1.0
function rufu:m1/reset
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 3
