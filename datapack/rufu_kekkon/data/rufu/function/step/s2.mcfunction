scoreboard players set #step rufu 2
data modify storage rufu:hud now set value "2. ヒロイン登場"
data modify storage rufu:hud next set value "3. 「結婚したければ、4つの試練をクリアして。」＋ルール看板"
scoreboard players set #seq rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 2. ヒロイン登場",color:"dark_green"}
scoreboard players set #lock rufu 0
kill @e[tag=rufu_part_heroine]
summon minecraft:mannequin 132.5 65 234.5 {profile:{texture:"entity/player/slim/alex",model:"slim"},CustomName:{text:"ヒロイン",color:"light_purple",bold:true},CustomNameVisible:true,hide_description:true,immovable:true,Invulnerable:true,Silent:true,Rotation:[90.0f,0.0f],Tags:["rufu_npc","rufu_npc_heroine","rufu_part_heroine","rufu_look"],equipment:{chest:{id:"minecraft:leather_chestplate",count:1,components:{dyed_color:16033480}}},Passengers:[{id:"minecraft:text_display",Tags:["rufu_bub","rufu_bub_heroine","rufu_part_heroine","rufu_npcpart"],billboard:"center",text:{text:""},background:0,line_width:180,shadow:false,see_through:false,transformation:{translation:[0.0f,0.9f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.0f,1.0f,1.0f]}}]}
summon minecraft:interaction 132.5 65 234.5 {Tags:["rufu_click","rufu_hit_heroine","rufu_part_heroine"],width:0.95f,height:2.05f,response:true}
execute at @e[type=mannequin,tag=rufu_npc_heroine] run particle minecraft:poof ~ ~1 ~ 0.4 0.8 0.4 0.02 30 force
execute at @e[type=mannequin,tag=rufu_npc_heroine] run playsound minecraft:entity.illusioner.mirror_move master @a ~ ~ ~ 1 1.2
execute at @e[type=mannequin,tag=rufu_npc_heroine] run particle minecraft:heart ~ ~2 ~ 0.6 0.5 0.6 0 10 force
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 2
