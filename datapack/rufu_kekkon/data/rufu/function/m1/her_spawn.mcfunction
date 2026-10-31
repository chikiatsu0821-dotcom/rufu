kill @e[tag=rufu_part_heroine]
summon minecraft:mannequin ~ ~ ~ {profile:{texture:"entity/player/slim/alex",model:"slim"},CustomName:{text:"ヒロイン",color:"light_purple",bold:true},CustomNameVisible:true,hide_description:true,immovable:true,Invulnerable:true,Silent:true,Rotation:[0.0f,0.0f],Tags:["rufu_npc","rufu_npc_heroine","rufu_part_heroine"],equipment:{chest:{id:"minecraft:leather_chestplate",count:1,components:{dyed_color:16033480}}},Passengers:[{id:"minecraft:text_display",Tags:["rufu_bub","rufu_bub_heroine","rufu_part_heroine","rufu_npcpart"],billboard:"center",text:{text:""},background:0,line_width:180,shadow:false,see_through:false,transformation:{translation:[0.0f,0.9f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.0f,1.0f,1.0f]}}]}
data modify entity @e[type=mannequin,tag=rufu_npc_heroine,limit=1] CustomName set from entity @e[type=marker,tag=rufu_namebox,limit=1] CustomName
summon minecraft:interaction ~ ~ ~ {Tags:["rufu_click","rufu_hit_heroine","rufu_part_heroine"],width:0.95f,height:2.05f,response:true}
execute as @e[type=mannequin,tag=rufu_npc_heroine] at @s run tp @s ~ ~ ~ facing 128.5 65 128.5
execute as @e[type=text_display,tag=rufu_bub_heroine] run data merge entity @s {text:{text:"おっ先～♪",color:"#7a1f5c"},background:-503321354}
scoreboard players set @e[type=text_display,tag=rufu_bub_heroine] rufu.bt 40
tellraw @a {text:"",extra:[{selector:"@e[type=marker,tag=rufu_namebox,limit=1]",color:"light_purple",bold:true},{text:"",color:"light_purple",bold:true},{text:"「おっ先～♪」",color:"white"}]}
execute as @e[tag=rufu_npc_heroine] at @s run playsound minecraft:entity.allay.ambient_without_item voice @a ~ ~ ~ 1.4 1.25
playsound minecraft:entity.breeze.wind_burst master @a ~ ~ ~ 1 1.4
