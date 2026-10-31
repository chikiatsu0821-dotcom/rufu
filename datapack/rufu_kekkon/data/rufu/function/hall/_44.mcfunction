execute as @e[type=text_display,tag=rufu_bub_q] run data merge entity @s {text:{text:"ねえ、私にしなよ",color:"#7a1f5c"},background:-503321354}
scoreboard players set @e[type=text_display,tag=rufu_bub_q] rufu.bt 80
tellraw @a {text:"",extra:[{text:"？？？",color:"gold",bold:true},{text:"「ねえ、私にしなよ」",color:"white"}]}
title @a times 3 70 8
title @a subtitle {text:"",extra:[{text:"？？？：",color:"gold",bold:true},{text:"「ねえ、私にしなよ」",color:"white"}]}
title @a title {text:"ねえ、私にしなよ",color:"gold",bold:true}
execute as @e[tag=rufu_npc_q] at @s run playsound minecraft:entity.allay.ambient_without_item voice @a ~ ~ ~ 1.4 1.1
