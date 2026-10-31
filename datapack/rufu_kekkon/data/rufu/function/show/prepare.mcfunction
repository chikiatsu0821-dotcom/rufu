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
data modify storage rufu:hud next set value "1. オープニング（タイトル）"
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
tp @a[tag=rufu_p] 128.5 65 235.5 180 0
spawnpoint @a[tag=rufu_p] 128 65 235
function rufu:m1/reset
function rufu:m1/db/up
tellraw @a[tag=rufu_gm] {text:"✅ 準備OK！ 緑のリモコン「▶ 次へ」でオープニング開始。",color:"green",bold:true}
tellraw @a[tag=rufu_gm] {text:"",extra:[{text:"   GMパネル：",color:"gray"},{text:"[開く]",color:"aqua",underlined:true,click_event:{action:"run_command",command:"/function rufu:gm/panel"}}]}
