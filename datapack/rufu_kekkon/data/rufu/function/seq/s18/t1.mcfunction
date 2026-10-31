execute as @e[type=text_display,tag=rufu_bub_heroine] run data merge entity @s {text:{text:"……やっぱりなかったことにして。",color:"#7a1f5c"},background:-503321354}
scoreboard players set @e[type=text_display,tag=rufu_bub_heroine] rufu.bt 100
tellraw @a {text:"",extra:[{text:"ヒロイン",color:"light_purple",bold:true},{text:"「……やっぱりなかったことにして。」",color:"white"}]}
title @a times 3 90 8
title @a subtitle {text:"",extra:[{text:"ヒロイン：",color:"light_purple",bold:true},{text:"「……やっぱりなかったことにして。」",color:"white"}]}
title @a title {text:"……やっぱりなかったことにして。",color:"light_purple",bold:true}
execute as @e[tag=rufu_npc_heroine] at @s run playsound minecraft:entity.allay.ambient_without_item voice @a ~ ~ ~ 1.4 1.25
execute as @a at @s run playsound minecraft:block.note_block.didgeridoo master @s ~ ~ ~ 1 0.6
