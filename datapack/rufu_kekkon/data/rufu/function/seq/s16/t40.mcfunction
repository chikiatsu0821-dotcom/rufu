execute as @e[type=text_display,tag=rufu_bub_heroine] run data merge entity @s {text:{text:"最後の試練。この木の下で告白されたら、ずっと幸せになれるんだって。",color:"#7a1f5c"},background:-503321354}
scoreboard players set @e[type=text_display,tag=rufu_bub_heroine] rufu.bt 110
tellraw @a {text:"",extra:[{text:"ヒロイン",color:"light_purple",bold:true},{text:"「最後の試練。この木の下で告白されたら、ずっと幸せになれるんだって。」",color:"white"}]}
title @a times 3 100 8
title @a subtitle {text:"",extra:[{text:"ヒロイン：",color:"light_purple",bold:true},{text:"「最後の試練。この木の下で告白されたら、ずっと幸せになれるんだって。」",color:"white"}]}
title @a title {text:""}
execute as @e[tag=rufu_npc_heroine] at @s run playsound minecraft:entity.allay.ambient_without_item voice @a ~ ~ ~ 1.4 1.25
