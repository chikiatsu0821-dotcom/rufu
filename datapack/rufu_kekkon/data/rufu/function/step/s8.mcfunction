scoreboard players set #step rufu 8
data modify storage rufu:hud now set value "8. 試練2 開始（4分）"
data modify storage rufu:hud next set value "9. オチ「やっぱパンだけでよかった」"
scoreboard players set #seq rufu 0
scoreboard players set #retry_step rufu 8
scoreboard players set #mission rufu 2
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 8. 試練2 開始（4分）",color:"dark_green"}
scoreboard players set #mission rufu 2
scoreboard players set #active rufu 0
scoreboard players set #lock rufu 1
scoreboard players set #ev rufu 0
scoreboard players set #fx rufu 0
scoreboard players set #love rufu 100
function rufu:hud/love
scoreboard players set #timer rufu 4800
bossbar set rufu:time max 4800
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
execute store result score #intr_at rufu run random value 700..2100
execute store result score #np rufu if entity @a[tag=rufu_p]
scoreboard players set @a rufu.death 0
effect clear @a[tag=rufu_p] minecraft:resistance
effect clear @a[tag=rufu_p] minecraft:fire_resistance
effect give @a[tag=rufu_p] minecraft:saturation infinite 0 true
effect give @a[tag=rufu_p] minecraft:instant_health 1 10 true
gamemode adventure @a[tag=rufu_p]
spawnpoint @a[tag=rufu_p] 128 65 134
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
function rufu:m2/reset
scoreboard players set #got1 rufu 0
scoreboard players set #got2 rufu 0
scoreboard players set #got3 rufu 0
data modify storage rufu:m2 s1 set value "✘"
data modify storage rufu:m2 s2 set value "✘"
data modify storage rufu:m2 s3 set value "✘"
execute unless score #orig1 rufu matches 1.. run function rufu:m2/assign
scoreboard players operation #own1 rufu = #orig1 rufu
scoreboard players operation #own2 rufu = #orig2 rufu
scoreboard players operation #own3 rufu = #orig3 rufu
function rufu:m2/apply_roles
kill @e[tag=rufu_part_heroine]
summon minecraft:mannequin 128.5 65 128.5 {profile:{texture:"entity/player/slim/alex",model:"slim"},CustomName:{text:"ヒロイン",color:"light_purple",bold:true},CustomNameVisible:true,hide_description:true,immovable:true,Invulnerable:true,Silent:true,Rotation:[0.0f,0.0f],Tags:["rufu_npc","rufu_npc_heroine","rufu_part_heroine","rufu_look"],equipment:{chest:{id:"minecraft:leather_chestplate",count:1,components:{dyed_color:16033480}}},Passengers:[{id:"minecraft:text_display",Tags:["rufu_bub","rufu_bub_heroine","rufu_part_heroine","rufu_npcpart"],billboard:"center",text:{text:""},background:0,line_width:180,shadow:false,see_through:false,transformation:{translation:[0.0f,0.9f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.0f,1.0f,1.0f]}}]}
summon minecraft:interaction 128.5 65 128.5 {Tags:["rufu_click","rufu_hit_heroine","rufu_part_heroine"],width:0.95f,height:2.05f,response:true}
tp @a[tag=rufu_p] 128.5 65 136.5 180 0
execute as @a[tag=rufu_p] run function rufu:m2/_42
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 8
