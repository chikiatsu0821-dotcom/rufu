execute as @e[type=text_display,tag=rufu_bub_heroine] run data merge entity @s {text:{text:"夜の裏通りで、もう一周ね。今度はもっと速く歩くから。",color:"#7a1f5c"},background:-503321354}
scoreboard players set @e[type=text_display,tag=rufu_bub_heroine] rufu.bt 100
tellraw @a {text:"",extra:[{text:"ヒロイン",color:"light_purple",bold:true},{text:"「夜の裏通りで、もう一周ね。今度はもっと速く歩くから。」",color:"white"}]}
title @a times 3 90 8
title @a subtitle {text:"",extra:[{text:"ヒロイン：",color:"light_purple",bold:true},{text:"「夜の裏通りで、もう一周ね。今度はもっと速く歩くから。」",color:"white"}]}
title @a title {text:""}
execute as @e[tag=rufu_npc_heroine] at @s run playsound minecraft:entity.allay.ambient_without_item voice @a ~ ~ ~ 1.4 1.25
