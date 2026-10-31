kill @e[tag=rufu_sel]
summon minecraft:text_display 23.5 68.75 225.5 {Tags:["rufu_sel","rufu_seltxt1"],billboard:"center",text:{text:"この子にする",color:"white",bold:true},background:-936897496,line_width:200,transformation:{translation:[0.0f,0.0f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.2f,1.2f,1.2f]}}
summon minecraft:interaction 23.5 66 225.5 {Tags:["rufu_sel","rufu_click","rufu_sel_hit","rufu_sel1"],width:1.1f,height:3.2f,response:true}
summon minecraft:text_display 28.5 68.75 225.5 {Tags:["rufu_sel","rufu_seltxt2"],billboard:"center",text:{text:"この子にする",color:"white",bold:true},background:-936897496,line_width:200,transformation:{translation:[0.0f,0.0f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.2f,1.2f,1.2f]}}
summon minecraft:interaction 28.5 66 225.5 {Tags:["rufu_sel","rufu_click","rufu_sel_hit","rufu_sel2"],width:1.1f,height:3.2f,response:true}
summon minecraft:text_display 36.5 68.75 225.5 {Tags:["rufu_sel","rufu_seltxt3"],billboard:"center",text:{text:"この子にする",color:"white",bold:true},background:-936897496,line_width:200,transformation:{translation:[0.0f,0.0f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.2f,1.2f,1.2f]}}
summon minecraft:interaction 36.5 66 225.5 {Tags:["rufu_sel","rufu_click","rufu_sel_hit","rufu_sel3"],width:1.1f,height:3.2f,response:true}
summon minecraft:text_display 41.5 69.75 225.5 {Tags:["rufu_sel","rufu_seltxt4"],billboard:"center",text:{text:"★この子にする★",color:"gold",bold:true},background:-600039926,line_width:200,transformation:{translation:[0.0f,0.0f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.2f,1.2f,1.2f]}}
summon minecraft:interaction 41.5 67 225.5 {Tags:["rufu_sel","rufu_click","rufu_sel_hit","rufu_sel4"],width:1.1f,height:3.2f,response:true}
execute at @e[type=text_display,tag=rufu_sel] run particle minecraft:end_rod ~ ~ ~ 0.5 0.2 0.1 0.02 8 force
execute as @a at @s run playsound minecraft:block.note_block.chime master @s ~ ~ ~ 1 1.2
