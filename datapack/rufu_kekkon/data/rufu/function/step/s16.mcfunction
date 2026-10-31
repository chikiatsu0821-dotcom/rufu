scoreboard players set #step rufu 16
data modify storage rufu:hud now set value "16. 試練4 開始（1回目・3分）"
data modify storage rufu:hud next set value "17. 「やっぱりなかったことにして」空が巻き戻る"
scoreboard players set #seq rufu 0
scoreboard players set #retry_step rufu 16
scoreboard players set #mission rufu 4
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 16. 試練4 開始（1回目・3分）",color:"dark_green"}
scoreboard players set #mission rufu 4
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
execute store result score #intr_at rufu run random value 600..2000
execute store result score #np rufu if entity @a[tag=rufu_p]
scoreboard players set @a rufu.death 0
effect clear @a[tag=rufu_p] minecraft:resistance
effect clear @a[tag=rufu_p] minecraft:fire_resistance
effect give @a[tag=rufu_p] minecraft:saturation infinite 0 true
effect give @a[tag=rufu_p] minecraft:instant_health 1 10 true
gamemode adventure @a[tag=rufu_p]
spawnpoint @a[tag=rufu_p] 195 81 95
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
function rufu:m4/reset
scoreboard players set #m4try rufu 1
scoreboard players set #m4p rufu 0
scoreboard players set #fspd rufu 1
scoreboard players set #sspd rufu 1
scoreboard players set #fox_need rufu 2
execute if score #np rufu matches ..1 run scoreboard players set #fox_need rufu 1
scoreboard players set #pin_need rufu 2
execute if score #np rufu matches ..2 run scoreboard players set #pin_need rufu 1
execute if score #np rufu matches ..1 run scoreboard players set #pin_need rufu 0
time set 18000
kill @e[tag=rufu_part_heroine]
summon minecraft:mannequin 195.5 81 85.5 {profile:{texture:"entity/player/slim/alex",model:"slim"},CustomName:{text:"ヒロイン",color:"light_purple",bold:true},CustomNameVisible:true,hide_description:true,immovable:true,Invulnerable:true,Silent:true,Rotation:[0.0f,0.0f],Tags:["rufu_npc","rufu_npc_heroine","rufu_part_heroine","rufu_look"],equipment:{chest:{id:"minecraft:leather_chestplate",count:1,components:{dyed_color:16033480}}},Passengers:[{id:"minecraft:text_display",Tags:["rufu_bub","rufu_bub_heroine","rufu_part_heroine","rufu_npcpart"],billboard:"center",text:{text:""},background:0,line_width:180,shadow:false,see_through:false,transformation:{translation:[0.0f,0.9f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.0f,1.0f,1.0f]}}]}
data modify entity @e[type=mannequin,tag=rufu_npc_heroine,limit=1] CustomName set from entity @e[type=marker,tag=rufu_namebox,limit=1] CustomName
summon minecraft:interaction 195.5 81 85.5 {Tags:["rufu_click","rufu_hit_heroine","rufu_part_heroine"],width:0.95f,height:2.05f,response:true}
tp @a[tag=rufu_p] 195.5 81 95.5 0 0
summon minecraft:fox 195.5 81 70.5 {Tags:["rufu_fox","rufu_mob4","rufu_fox_real"],NoAI:true,PersistenceRequired:true,Silent:false,Type:"red",attributes:[{id:"minecraft:max_health",base:1024.0d}],Health:1000.0f,equipment:{mainhand:{id:"minecraft:gold_nugget",count:1,components:{custom_name:{text:"💍 婚約指輪",color:"gold",bold:true,italic:false},lore:[{text:"ヒロインに渡すための指輪。",color:"gray",italic:false},{text:"キツネの大好物ではない。",color:"gray",italic:false}],custom_data:{rufu_ring:1b,rufu_m:1b},enchantment_glint_override:true}}},drop_chances:{mainhand:0.0f}}
execute as @a[tag=rufu_p] run function rufu:m4/_51
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 16
