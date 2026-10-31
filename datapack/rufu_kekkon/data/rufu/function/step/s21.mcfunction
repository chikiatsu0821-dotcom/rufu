scoreboard players set #step rufu 21
data modify storage rufu:hud now set value "21. 結婚式へ（教会に移動）"
data modify storage rufu:hud next set value "22. 鐘と結婚行進曲"
scoreboard players set #seq rufu 0
scoreboard players set #retry_step rufu 0
scoreboard players set #mission rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 21. 結婚式へ（教会に移動）",color:"dark_green"}
scoreboard players set #lock rufu 1
scoreboard players set #active rufu 0
function rufu:hud/hide
bossbar set rufu:love visible true
kill @e[tag=rufu_mob]
kill @e[tag=rufu_mob4]
kill @e[tag=rufu_fox]
kill @e[type=marker,tag=rufu_m4m]
effect give @a[tag=rufu_p] minecraft:resistance infinite 4 true
effect give @a[tag=rufu_p] minecraft:fire_resistance infinite 0 true
effect give @a[tag=rufu_p] minecraft:blindness 2 0 true
time set 11500
weather clear
scoreboard players set #love rufu 100
function rufu:hud/love
kill @e[tag=rufu_part_heroine]
summon minecraft:mannequin 129.5 66 63.5 {profile:{texture:"entity/player/slim/alex",model:"slim"},CustomName:{text:"ヒロイン",color:"light_purple",bold:true},CustomNameVisible:true,hide_description:true,immovable:true,Invulnerable:true,Silent:true,Rotation:[90.0f,0.0f],Tags:["rufu_npc","rufu_npc_heroine","rufu_part_heroine"],equipment:{chest:{id:"minecraft:leather_chestplate",count:1,components:{dyed_color:16777215}},legs:{id:"minecraft:leather_leggings",count:1,components:{dyed_color:16777215}},feet:{id:"minecraft:leather_boots",count:1,components:{dyed_color:16777215}},mainhand:{id:"minecraft:pink_tulip",count:1}},Passengers:[{id:"minecraft:text_display",Tags:["rufu_bub","rufu_bub_heroine","rufu_part_heroine","rufu_npcpart"],billboard:"center",text:{text:""},background:0,line_width:180,shadow:false,see_through:false,transformation:{translation:[0.0f,0.9f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.0f,1.0f,1.0f]}}]}
summon minecraft:interaction 129.5 66 63.5 {Tags:["rufu_click","rufu_hit_heroine","rufu_part_heroine"],width:0.95f,height:2.05f,response:true}
kill @e[tag=rufu_part_priest]
summon minecraft:mannequin 128.5 66 60.5 {profile:{texture:"entity/player/wide/steve",model:"wide"},CustomName:{text:"神父",color:"gold",bold:true},CustomNameVisible:true,hide_description:true,immovable:true,Invulnerable:true,Silent:true,Rotation:[0.0f,0.0f],Tags:["rufu_npc","rufu_npc_priest","rufu_part_priest"],equipment:{chest:{id:"minecraft:leather_chestplate",count:1,components:{dyed_color:1710618}},legs:{id:"minecraft:leather_leggings",count:1,components:{dyed_color:1710618}},feet:{id:"minecraft:leather_boots",count:1,components:{dyed_color:1710618}},mainhand:{id:"minecraft:book",count:1}},Passengers:[{id:"minecraft:text_display",Tags:["rufu_bub","rufu_bub_priest","rufu_part_priest","rufu_npcpart"],billboard:"center",text:{text:""},background:0,line_width:180,shadow:false,see_through:false,transformation:{translation:[0.0f,0.9f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.0f,1.0f,1.0f]}}]}
kill @e[tag=rufu_seat]
summon minecraft:item_display 124.5 65.5 66.5 {Tags:["rufu_seat","rufu_seat1"]}
summon minecraft:item_display 132.5 65.5 66.5 {Tags:["rufu_seat","rufu_seat2"]}
tp @a[tag=rufu_hero] 127.5 66 63.5 -90 0
tag @a remove rufu_sat
execute as @a[tag=rufu_helper,limit=1,sort=arbitrary] run function rufu:wed/seat1
execute as @a[tag=rufu_helper,tag=!rufu_sat,limit=1,sort=arbitrary] run function rufu:wed/seat2
title @a times 20 60 20
title @a subtitle {text:"町の奥の教会",color:"white"}
title @a title {text:"～ 結婚式 ～",color:"light_purple",bold:true}
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 21
