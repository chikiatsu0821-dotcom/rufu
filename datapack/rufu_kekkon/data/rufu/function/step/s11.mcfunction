scoreboard players set #step rufu 11
data modify storage rufu:hud now set value "11. 試練3 開始（1周目・昼）"
data modify storage rufu:hud next set value "12. オチ「この道じゃない方がよかった」→夜"
scoreboard players set #seq rufu 0
scoreboard players set #retry_step rufu 11
scoreboard players set #mission rufu 3
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 11. 試練3 開始（1周目・昼）",color:"dark_green"}
scoreboard players set #mission rufu 3
scoreboard players set #active rufu 0
scoreboard players set #lock rufu 1
scoreboard players set #ev rufu 0
scoreboard players set #fx rufu 0
scoreboard players set #love rufu 100
function rufu:hud/love
scoreboard players set #timer rufu 3600
bossbar set rufu:time max 3600
execute store result bossbar rufu:time value run scoreboard players get #timer rufu
bossbar set rufu:time players @a
bossbar set rufu:time visible true
function rufu:hud/time
scoreboard players set #elapsed rufu 0
scoreboard players set #ask_t rufu 0
scoreboard players set #ask_live rufu 0
scoreboard players set #intr_live rufu 0
scoreboard players set #gift rufu 0
kill @e[tag=rufu_ask]
execute store result score #intr_at rufu run random value 400..1100
execute store result score #np rufu if entity @a[tag=rufu_p]
scoreboard players set @a rufu.death 0
effect clear @a[tag=rufu_p] minecraft:resistance
effect clear @a[tag=rufu_p] minecraft:fire_resistance
effect give @a[tag=rufu_p] minecraft:saturation infinite 0 true
effect give @a[tag=rufu_p] minecraft:instant_health 1 10 true
gamemode adventure @a[tag=rufu_p]
spawnpoint @a[tag=rufu_p] 128 65 137
kill @e[tag=rufu_mob]
kill @e[type=item,tag=!rufu_keep]
kill @e[type=minecraft:arrow]
kill @e[type=minecraft:trident]
clear @a[tag=rufu_p] *[custom_data~{rufu_m:1b}]
clear @a[tag=rufu_p] minecraft:bread
clear @a[tag=rufu_p] minecraft:cake
clear @a[tag=rufu_p] minecraft:wheat
clear @a[tag=rufu_p] minecraft:wheat_seeds
clear @a[tag=rufu_p] minecraft:sugar
clear @a[tag=rufu_p] minecraft:sugar_cane
clear @a[tag=rufu_p] minecraft:egg
clear @a[tag=rufu_p] minecraft:bucket
clear @a[tag=rufu_p] minecraft:milk_bucket
clear @a[tag=rufu_p] minecraft:beef
clear @a[tag=rufu_p] minecraft:cooked_beef
clear @a[tag=rufu_p] minecraft:porkchop
clear @a[tag=rufu_p] minecraft:cooked_porkchop
clear @a[tag=rufu_p] minecraft:leather
clear @a[tag=rufu_p] minecraft:bamboo_mosaic
clear @a[tag=rufu_p] minecraft:cracked_stone_bricks
clear @a[tag=rufu_p] minecraft:coarse_dirt
clear @a[tag=rufu_p] minecraft:rotten_flesh
clear @a[tag=rufu_p] minecraft:bone
clear @a[tag=rufu_p] minecraft:arrow
clear @a[tag=rufu_p] minecraft:trident
clear @a[tag=rufu_p] minecraft:sweet_berries
clear @a[tag=rufu_p] minecraft:golden_apple
clear @a[tag=rufu_p] minecraft:carved_pumpkin
clear @a[tag=rufu_p] minecraft:leather_helmet
clear @a[tag=rufu_p] minecraft:iron_ingot
clear @a[tag=rufu_p] minecraft:carrot
clear @a[tag=rufu_p] minecraft:potato
function rufu:hud/show
time set 6000
weather clear
kill @e[type=marker,tag=rufu_wpm]
summon minecraft:marker 128.5 65 133.5 {Tags:["rufu_wpm"]}
kill @e[tag=rufu_part_heroine]
summon minecraft:mannequin 128.5 65 133.5 {profile:{texture:"entity/player/slim/alex",model:"slim"},CustomName:{text:"ヒロイン",color:"light_purple",bold:true},CustomNameVisible:true,hide_description:true,immovable:true,Invulnerable:true,Silent:true,Rotation:[180.0f,0.0f],Tags:["rufu_npc","rufu_npc_heroine","rufu_part_heroine"],equipment:{chest:{id:"minecraft:leather_chestplate",count:1,components:{dyed_color:16033480}}},Passengers:[{id:"minecraft:text_display",Tags:["rufu_bub","rufu_bub_heroine","rufu_part_heroine","rufu_npcpart"],billboard:"center",text:{text:""},background:0,line_width:180,shadow:false,see_through:false,transformation:{translation:[0.0f,0.9f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.0f,1.0f,1.0f]}}]}
data modify entity @e[type=mannequin,tag=rufu_npc_heroine,limit=1] CustomName set from entity @e[type=marker,tag=rufu_namebox,limit=1] CustomName
summon minecraft:interaction 128.5 65 133.5 {Tags:["rufu_click","rufu_hit_heroine","rufu_part_heroine"],width:0.95f,height:2.05f,response:true}
scoreboard players set #lap rufu 1
scoreboard players set #wp rufu 0
scoreboard players set #pause rufu 0
scoreboard players set #spd rufu 2
scoreboard players set #mode rufu 0
scoreboard players set #outg rufu 0
bossbar set rufu:out value 0
bossbar set rufu:out players @a
bossbar set rufu:out visible true
bossbar set rufu:out name {text:"アウトゲージ（誰か1人でも2〜5ブロックから外れると たまる）",color:"red"}
tp @a[tag=rufu_p] 128.5 65 137.5 180 0
function rufu:m3/skel1
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 11
