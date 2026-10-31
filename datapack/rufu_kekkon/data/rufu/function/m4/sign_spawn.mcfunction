scoreboard players set #m4p rufu 2
kill @e[tag=rufu_sign]
summon minecraft:text_display 198.0 82.2 89.5 {Tags:["rufu_sign","rufu_mob4"],billboard:"center",teleport_duration:2,text:{text:"",extra:[{text:"💍 結婚してください 💍",color:"#d6246e",bold:true}]},background:-335546886,line_width:200,transformation:{translation:[0.0f,0.0f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.6f,1.6f,1.6f]}}
summon minecraft:interaction 198.0 81.6 89.5 {Tags:["rufu_sign_hit","rufu_click","rufu_mob4"],width:1.5f,height:1.3f,response:true}
title @a times 5 60 10
title @a subtitle {text:"「結婚してください」の看板を主人公が右クリック！…でも逃げる",color:"white"}
title @a title {text:"告白タイム！",color:"light_purple",bold:true}
execute as @a at @s run playsound minecraft:block.note_block.chime master @s ~ ~ ~ 1 1.0
execute as @a at @s run playsound minecraft:block.note_block.chime master @s ~ ~ ~ 1 1.5
