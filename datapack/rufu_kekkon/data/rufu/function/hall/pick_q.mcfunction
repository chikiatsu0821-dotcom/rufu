scoreboard players set #qchosen rufu 1
kill @e[tag=rufu_sel]
data merge entity @e[type=mannequin,tag=rufu_npc_q,limit=1] {Glowing:false,description:{text:"名前をつけてね",color:"light_purple",bold:true}}
tag @e[type=mannequin,tag=rufu_npc_q] remove rufu_glow
execute as @e[type=text_display,tag=rufu_bub_q] run data merge entity @s {text:{text:"知ってた♡",color:"#7a1f5c"},background:-503321354}
scoreboard players set @e[type=text_display,tag=rufu_bub_q] rufu.bt 80
tellraw @a {text:"",extra:[{text:"？？？",color:"gold",bold:true},{text:"「知ってた♡」",color:"white"}]}
title @a times 3 70 8
title @a subtitle {text:"",extra:[{text:"？？？：",color:"gold",bold:true},{text:"「知ってた♡」",color:"white"}]}
title @a title {text:"知ってた♡",color:"gold",bold:true}
execute as @e[tag=rufu_npc_q] at @s run playsound minecraft:entity.allay.ambient_without_item voice @a ~ ~ ~ 1.4 1.1
execute at @e[type=mannequin,tag=rufu_npc_q,limit=1] run particle minecraft:heart ~ ~2 ~ 1 0.8 1 0 40 force
execute as @a at @s run playsound minecraft:entity.player.levelup master @s ~ ~ ~ 1 1.2
give @s minecraft:name_tag[lore=[{text:"金床で名前を書いて、？？？に使おう",color:"gray",italic:false}],custom_data={rufu_nametag:1b}] 1
experience add @s 3 levels
scoreboard players set #naming rufu 1
execute at @e[type=mannequin,tag=rufu_npc_q,limit=1] run summon minecraft:interaction ~ ~ ~ {Tags:["rufu_click","rufu_hit_q","rufu_part_q"],width:1.0f,height:2.1f,response:true}
playsound minecraft:block.anvil.use master @a 46 65 244 0.6 1.6
tellraw @a {text:"✨ ホールの金床が光っている……",color:"gold"}
title @s times 5 60 10
title @s subtitle {text:"金床で名札に名前を書いて、？？？に使おう",color:"light_purple"}
title @s title {text:""}
