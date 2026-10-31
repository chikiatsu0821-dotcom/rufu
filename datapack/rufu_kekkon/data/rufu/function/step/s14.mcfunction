scoreboard players set #step rufu 14
data modify storage rufu:hud now set value "14. 試練3 2周目開始（夜・裏通り）"
data modify storage rufu:hud next set value "15. 試練3 評価 → 丘の伝説の木へ"
scoreboard players set #seq rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 14. 試練3 2周目開始（夜・裏通り）",color:"dark_green"}
scoreboard players set #mission rufu 3
scoreboard players set #active rufu 0
scoreboard players set #lock rufu 1
scoreboard players set #timer rufu 3600
bossbar set rufu:time max 3600
bossbar set rufu:time visible true
function rufu:hud/time
scoreboard players set #elapsed rufu 0
scoreboard players set #ask_t rufu 0
execute store result score #intr_at rufu run random value 300..900
scoreboard players set @a rufu.death 0
effect clear @a[tag=rufu_p] minecraft:resistance
time set 18000
kill @e[tag=rufu_mob]
kill @e[type=marker,tag=rufu_wpm]
summon minecraft:marker 64.5 65 77.5 {Tags:["rufu_wpm"]}
kill @e[tag=rufu_part_heroine]
summon minecraft:mannequin 64.5 65 77.5 {profile:{texture:"entity/player/slim/alex",model:"slim"},CustomName:{text:"ヒロイン",color:"light_purple",bold:true},CustomNameVisible:true,hide_description:true,immovable:true,Invulnerable:true,Silent:true,Rotation:[0.0f,0.0f],Tags:["rufu_npc","rufu_npc_heroine","rufu_part_heroine"],equipment:{chest:{id:"minecraft:leather_chestplate",count:1,components:{dyed_color:16033480}}},Passengers:[{id:"minecraft:text_display",Tags:["rufu_bub","rufu_bub_heroine","rufu_part_heroine","rufu_npcpart"],billboard:"center",text:{text:""},background:0,line_width:180,shadow:false,see_through:false,transformation:{translation:[0.0f,0.9f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.0f,1.0f,1.0f]}}]}
summon minecraft:interaction 64.5 65 77.5 {Tags:["rufu_click","rufu_hit_heroine","rufu_part_heroine"],width:0.95f,height:2.05f,response:true}
scoreboard players set #lap rufu 2
scoreboard players set #wp rufu 0
scoreboard players set #pause rufu 0
scoreboard players set #spd rufu 2
scoreboard players set #mode rufu 0
scoreboard players set #outg rufu 0
bossbar set rufu:out value 0
bossbar set rufu:out players @a
bossbar set rufu:out visible true
bossbar set rufu:out name {text:"アウトゲージ（誰か1人でも2〜5ブロックから外れると たまる）",color:"red"}
execute as @e[type=mannequin,tag=rufu_npc_heroine] at @s run tp @a[tag=rufu_p] ~ ~ ~4
function rufu:m3/skel2
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 14
