scoreboard players set #step rufu 32
data modify storage rufu:hud now set value "32. エンディング：神父「ハァン……」"
data modify storage rufu:hud next set value "33. 婚約指輪が「返品された指輪」に"
scoreboard players set #seq rufu 0
scoreboard players set #retry_step rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 32. エンディング：神父「ハァン……」",color:"dark_green"}
scoreboard players set #lock rufu 1
scoreboard players set #fx rufu 0
kill @e[tag=rufu_pig]
kill @e[tag=rufu_part_heroine]
kill @e[tag=rufu_part_leon]
effect give @a[tag=rufu_p] minecraft:blindness 2 0 true
tp @a[tag=rufu_p] 128.5 65 70.5 180 0
kill @e[tag=rufu_part_priest]
summon minecraft:mannequin 128.5 66 60.5 {profile:{texture:"entity/player/wide/steve",model:"wide"},CustomName:{text:"神父",color:"gold",bold:true},CustomNameVisible:true,hide_description:true,immovable:true,Invulnerable:true,Silent:true,Rotation:[0.0f,0.0f],Tags:["rufu_npc","rufu_npc_priest","rufu_part_priest","rufu_look"],equipment:{chest:{id:"minecraft:leather_chestplate",count:1,components:{dyed_color:1710618}},legs:{id:"minecraft:leather_leggings",count:1,components:{dyed_color:1710618}},feet:{id:"minecraft:leather_boots",count:1,components:{dyed_color:1710618}},mainhand:{id:"minecraft:book",count:1}},Passengers:[{id:"minecraft:text_display",Tags:["rufu_bub","rufu_bub_priest","rufu_part_priest","rufu_npcpart"],billboard:"center",text:{text:""},background:0,line_width:180,shadow:false,see_through:false,transformation:{translation:[0.0f,0.9f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.0f,1.0f,1.0f]}}]}
weather rain
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 32
