execute unless score #built rufu matches 1 run tellraw @s {text:"⚠ 先に /function rufu:setup で町を建設してください",color:"red"}
execute unless entity @a[tag=rufu_hero] run tellraw @s {text:"⚠ 主人公が設定されていません（テストなら自分を主人公にしてもOK）",color:"yellow"}
scoreboard players set #step rufu 0
scoreboard players set #retry rufu 0
scoreboard players set #t_total rufu 0
scoreboard players set #love rufu 100
scoreboard players set #mission rufu 0
scoreboard players set #active rufu 0
scoreboard players set #lock rufu 0
scoreboard players set #seq rufu 0
scoreboard players set #ev rufu 0
scoreboard players set #fx rufu 0
scoreboard players set #retry_step rufu 0
scoreboard players set #orig1 rufu 0
scoreboard players set #own1 rufu 0
data modify storage rufu:hud now set value "0. 準備完了"
data modify storage rufu:hud next set value "1. タイトル → ヒロイン選択（看板）"
kill @e[tag=rufu_npc]
kill @e[tag=rufu_npcpart]
kill @e[tag=rufu_mob]
kill @e[tag=rufu_mob4]
kill @e[tag=rufu_fox]
kill @e[tag=rufu_ask]
kill @e[tag=rufu_rules]
kill @e[tag=rufu_pig]
kill @e[tag=rufu_ghast]
kill @e[tag=rufu_seat]
kill @e[tag=rufu_sel]
clear @a minecraft:name_tag
kill @e[type=marker,tag=rufu_wpm]
kill @e[type=marker,tag=rufu_m4m]
kill @e[type=interaction,tag=rufu_click]
kill @e[type=item,tag=rufu_ringitem]
team leave @a
clear @a minecraft:gold_nugget[custom_data~{rufu_ring_returned:1b}]
time set 1000
weather clear
effect clear @a
effect give @a[tag=rufu_p] minecraft:resistance infinite 4 true
effect give @a[tag=rufu_p] minecraft:saturation infinite 0 true
gamemode adventure @a[tag=rufu_p]
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
execute as @a run attribute @s minecraft:movement_speed base reset
execute as @a run attribute @s minecraft:jump_strength base reset
function rufu:hud/hide
kill @e[tag=rufu_hallgirl]
kill @e[tag=rufu_sel]
kill @e[tag=rufu_part_q]
kill @e[type=marker,tag=rufu_namebox]
summon minecraft:marker 32.5 70 240.5 {Tags:["rufu_namebox"],CustomName:{text:"ゆめりあ"}}
scoreboard players set #pick rufu 0
scoreboard players set #qchosen rufu 0
scoreboard players set #named rufu 0
scoreboard players set #naming rufu 0
kill @e[tag=rufu_part_sakura]
summon minecraft:mannequin 23.5 66 225.5 {profile:{texture:"entity/player/slim/sunny",model:"slim"},CustomName:{text:"さくら",color:"#ff8fc8",bold:true},CustomNameVisible:true,description:{text:"清楚系／生徒会長",color:"white",bold:false},hide_description:false,immovable:true,Invulnerable:true,Silent:true,NoGravity:false,Rotation:[0.0f,0.0f],Tags:["rufu_npc","rufu_hallgirl","rufu_npc_sakura","rufu_part_sakura"],equipment:{chest:{id:"minecraft:leather_chestplate",count:1,components:{dyed_color:16761053}}},Passengers:[{id:"minecraft:text_display",Tags:["rufu_bub","rufu_bub_sakura","rufu_part_sakura","rufu_npcpart"],billboard:"center",text:{text:""},background:0,line_width:180,transformation:{translation:[0.0f,1.25f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.0f,1.0f,1.0f]}}]}
kill @e[tag=rufu_part_mio]
summon minecraft:mannequin 28.5 66 225.5 {profile:{texture:"entity/player/slim/noor",model:"slim"},CustomName:{text:"みお",color:"#7fb8ff",bold:true},CustomNameVisible:true,description:{text:"クール系／弓道部",color:"white",bold:false},hide_description:false,immovable:true,Invulnerable:true,Silent:true,NoGravity:false,Rotation:[0.0f,0.0f],Tags:["rufu_npc","rufu_hallgirl","rufu_npc_mio","rufu_part_mio"],equipment:{chest:{id:"minecraft:leather_chestplate",count:1,components:{dyed_color:10275071}}},Passengers:[{id:"minecraft:text_display",Tags:["rufu_bub","rufu_bub_mio","rufu_part_mio","rufu_npcpart"],billboard:"center",text:{text:""},background:0,line_width:180,transformation:{translation:[0.0f,1.25f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.0f,1.0f,1.0f]}}]}
kill @e[tag=rufu_part_hinata]
summon minecraft:mannequin 36.5 66 225.5 {profile:{texture:"entity/player/slim/efe",model:"slim"},CustomName:{text:"ひなた",color:"#ffd34d",bold:true},CustomNameVisible:true,description:{text:"元気系／幼なじみ",color:"white",bold:false},hide_description:false,immovable:true,Invulnerable:true,Silent:true,NoGravity:false,Rotation:[0.0f,0.0f],Tags:["rufu_npc","rufu_hallgirl","rufu_npc_hinata","rufu_part_hinata"],equipment:{chest:{id:"minecraft:leather_chestplate",count:1,components:{dyed_color:16769146}}},Passengers:[{id:"minecraft:text_display",Tags:["rufu_bub","rufu_bub_hinata","rufu_part_hinata","rufu_npcpart"],billboard:"center",text:{text:""},background:0,line_width:180,transformation:{translation:[0.0f,1.25f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.0f,1.0f,1.0f]}}]}
kill @e[tag=rufu_part_q]
summon minecraft:mannequin 41.5 67 225.5 {profile:{texture:"entity/player/slim/alex",model:"slim"},CustomName:{text:"？？？",color:"gold",bold:true},CustomNameVisible:true,description:{text:"★おすすめ★",color:"gold",bold:true},hide_description:false,immovable:true,Invulnerable:true,Silent:true,NoGravity:true,Rotation:[0.0f,0.0f],Tags:["rufu_npc","rufu_hallgirl","rufu_npc_q","rufu_part_q","rufu_qlook"],equipment:{chest:{id:"minecraft:leather_chestplate",count:1,components:{dyed_color:16033480}}},Passengers:[{id:"minecraft:text_display",Tags:["rufu_bub","rufu_bub_q","rufu_part_q","rufu_npcpart"],billboard:"center",text:{text:""},background:0,line_width:180,transformation:{translation:[0.0f,1.25f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.0f,1.0f,1.0f]}}],Glowing:true}
tp @a[tag=rufu_p] 32.5 65 246.5 180 0
tp @a[tag=!rufu_p] 32.5 65 251.5 180 0
spawnpoint @a[tag=rufu_p] 32 65 246
time set 6000
weather clear
effect give @a[tag=rufu_p] minecraft:resistance infinite 4 true
effect give @a[tag=rufu_p] minecraft:fire_resistance infinite 0 true
function rufu:m1/reset
function rufu:m1/db/up
tellraw @a[tag=rufu_gm] {text:"✅ 準備OK！ 選択ホールで待機中（段階0）。説明・雑談が終わったら 緑のリモコン「▶ 次へ」でタイトル→ヒロイン選択。",color:"green",bold:true}
tellraw @a[tag=rufu_gm] {text:"",extra:[{text:"   GMパネル：",color:"gray"},{text:"[開く]",color:"aqua",underlined:true,click_event:{action:"run_command",command:"/function rufu:gm/panel"}}]}
