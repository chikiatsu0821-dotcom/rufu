execute as @e[type=text_display,tag=rufu_bub_q] run data merge entity @s {text:{text:"金床で名札に名前を書いて、私に使って",color:"#7a1f5c"},background:-503321354}
scoreboard players set @e[type=text_display,tag=rufu_bub_q] rufu.bt 80
tellraw @a {text:"",extra:[{text:"？？？",color:"gold",bold:true},{text:"「金床で名札に名前を書いて、私に使って」",color:"white"}]}
title @a times 3 70 8
title @a subtitle {text:"",extra:[{text:"？？？：",color:"gold",bold:true},{text:"「金床で名札に名前を書いて、私に使って」",color:"white"}]}
title @a title {text:""}
execute as @e[tag=rufu_npc_q] at @s run playsound minecraft:entity.allay.ambient_without_item voice @a ~ ~ ~ 1.4 1.1
