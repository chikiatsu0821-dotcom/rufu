scoreboard players set #step rufu 2
data modify storage rufu:hud now set value "2. 試練の宣言「結婚したければ、4つの試練をクリアして。」"
data modify storage rufu:hud next set value "3. 試練1 説明「私より早く広場に来て」"
scoreboard players set #seq rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 2. 試練の宣言「結婚したければ、4つの試練をクリアして。」",color:"dark_green"}
scoreboard players set #lock rufu 1
scoreboard players set #naming rufu 0
kill @e[tag=rufu_sel]
function rufu:hall/others_vanish
execute at @e[type=mannequin,tag=rufu_npc_q,limit=1] run particle minecraft:poof ~ ~1 ~ 0.4 0.8 0.4 0.03 20 force
kill @e[tag=rufu_part_q]
clear @a minecraft:name_tag[custom_data~{rufu_nametag:1b}]
kill @e[tag=rufu_part_heroine]
summon minecraft:mannequin 32.5 66 226.5 {profile:{texture:"entity/player/slim/alex",model:"slim"},CustomName:{text:"ヒロイン",color:"light_purple",bold:true},CustomNameVisible:true,hide_description:true,immovable:true,Invulnerable:true,Silent:true,Rotation:[0.0f,0.0f],Tags:["rufu_npc","rufu_npc_heroine","rufu_part_heroine"],equipment:{chest:{id:"minecraft:leather_chestplate",count:1,components:{dyed_color:16033480}}},Passengers:[{id:"minecraft:text_display",Tags:["rufu_bub","rufu_bub_heroine","rufu_part_heroine","rufu_npcpart"],billboard:"center",text:{text:""},background:0,line_width:180,shadow:false,see_through:false,transformation:{translation:[0.0f,0.9f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.0f,1.0f,1.0f]}}]}
data modify entity @e[type=mannequin,tag=rufu_npc_heroine,limit=1] CustomName set from entity @e[type=marker,tag=rufu_namebox,limit=1] CustomName
summon minecraft:interaction 32.5 66 226.5 {Tags:["rufu_click","rufu_hit_heroine","rufu_part_heroine"],width:0.95f,height:2.05f,response:true}
execute as @e[type=mannequin,tag=rufu_npc_heroine] at @s run tp @s ~ ~ ~ facing entity @p[tag=rufu_hero] eyes
execute at @e[type=mannequin,tag=rufu_npc_heroine] run particle minecraft:end_rod ~ ~1 ~ 0.5 1 0.5 0.05 30 force
kill @e[tag=rufu_rules]
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 2
