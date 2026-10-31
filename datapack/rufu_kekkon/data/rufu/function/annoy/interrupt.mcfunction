scoreboard players set #intr_live rufu 300
scoreboard players set @a rufu.judge 0
scoreboard players enable @a[tag=rufu_helper] rufu.judge
scoreboard players enable @a[tag=rufu_gm] rufu.judge
execute store result score #r rufu run random value 0..4
execute if score #r rufu matches 0 run function rufu:annoy/_9
execute if score #r rufu matches 1 run function rufu:annoy/_10
execute if score #r rufu matches 2 run function rufu:annoy/_11
execute if score #r rufu matches 3 run function rufu:annoy/_12
execute if score #r rufu matches 4 run function rufu:annoy/_13
execute as @a at @s run playsound minecraft:block.note_block.bell master @s ~ ~ ~ 1 0.8
tellraw @a[tag=rufu_helper] {text:"",extra:[{text:"🎤 割り込み！ 主人公の答えを判定してね → ",color:"yellow"},{text:"[ 〇 合格 ]",color:"green",bold:true,click_event:{action:"run_command",command:"/trigger rufu.judge set 1"},hover_event:{action:"show_text",value:{text:"好感度 +10"}}},{text:" "},{text:"[ × 不合格 ]",color:"red",bold:true,click_event:{action:"run_command",command:"/trigger rufu.judge set 2"},hover_event:{action:"show_text",value:{text:"好感度 -10"}}}]}
tellraw @a[tag=rufu_gm] {text:"",extra:[{text:"[GM] 割り込み発生。判定: ",color:"gray"},{text:"[〇]",color:"green",click_event:{action:"run_command",command:"/trigger rufu.judge set 1"}},{text:" "},{text:"[×]",color:"red",click_event:{action:"run_command",command:"/trigger rufu.judge set 2"}}]}
title @a[tag=rufu_hero,limit=1] times 5 60 10
title @a[tag=rufu_hero,limit=1] subtitle {text:"（助っ人が 〇 / × で判定します）",color:"white"}
title @a[tag=rufu_hero,limit=1] title {text:"💬 声で答えて！",color:"yellow",bold:true}
