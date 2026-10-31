scoreboard players set #step rufu 31
data modify storage rufu:hud now set value "31. 豚でのろのろ逃走（追いつけない）"
data modify storage rufu:hud next set value "32. エンディング：神父「ハァン……」"
scoreboard players set #seq rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 31. 豚でのろのろ逃走（追いつけない）",color:"dark_green"}
scoreboard players set #lock rufu 1
kill @e[tag=rufu_pig]
summon minecraft:pig 128.5 65 74.5 {Tags:["rufu_pig","rufu_pig1"],NoAI:true,Invulnerable:true,PersistenceRequired:true,equipment:{saddle:{id:"minecraft:saddle",count:1}},Rotation:[0f,0f]}
summon minecraft:pig 128.5 65 72.5 {Tags:["rufu_pig","rufu_pig2"],NoAI:true,Invulnerable:true,PersistenceRequired:true,equipment:{saddle:{id:"minecraft:saddle",count:1}},Rotation:[0f,0f]}
ride @e[type=mannequin,tag=rufu_npc_heroine,limit=1] mount @e[type=pig,tag=rufu_pig1,limit=1]
ride @e[type=mannequin,tag=rufu_npc_leon,limit=1] mount @e[type=pig,tag=rufu_pig2,limit=1]
tag @e[type=mannequin,tag=rufu_npc_heroine] remove rufu_look
tag @e[type=mannequin,tag=rufu_npc_leon] remove rufu_look
kill @e[type=item_display,tag=rufu_seat]
kill @e[type=marker,tag=rufu_pigwp]
summon minecraft:marker 128.5 65 89.5 {Tags:["rufu_pigwp"]}
scoreboard players set #pigwp rufu 1
scoreboard players set #fx rufu 1
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 31
