kill @e[tag=rufu_ghast]
summon minecraft:happy_ghast 128.5 100 70.5 {Tags:["rufu_ghast"],NoAI:true,NoGravity:true,Invulnerable:true,PersistenceRequired:true,equipment:{body:{id:"minecraft:pink_harness",count:1}},Rotation:[0.0f,0.0f]}
kill @e[tag=rufu_part_leon]
summon minecraft:mannequin 128.5 101 70.5 {profile:{texture:"entity/player/wide/kai",model:"wide"},CustomName:{text:"レオン",color:"aqua",bold:true},CustomNameVisible:true,hide_description:true,immovable:true,Invulnerable:true,Silent:true,Rotation:[0.0f,0.0f],Tags:["rufu_npc","rufu_npc_leon","rufu_part_leon"],equipment:{chest:{id:"minecraft:leather_chestplate",count:1,components:{dyed_color:1976900}},legs:{id:"minecraft:leather_leggings",count:1,components:{dyed_color:2829099}},feet:{id:"minecraft:leather_boots",count:1,components:{dyed_color:3877402}}},Passengers:[{id:"minecraft:text_display",Tags:["rufu_bub","rufu_bub_leon","rufu_part_leon","rufu_npcpart"],billboard:"center",text:{text:""},background:0,line_width:180,shadow:false,see_through:false,transformation:{translation:[0.0f,0.9f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.0f,1.0f,1.0f]}}]}
ride @e[type=mannequin,tag=rufu_npc_leon,limit=1] mount @e[type=happy_ghast,tag=rufu_ghast,limit=1]
scoreboard players set #fx rufu 2
scoreboard players set #ghy rufu 0
execute as @a at @s run playsound minecraft:entity.happy_ghast.ambient master @s ~ ~ ~ 1 1.0
