execute as @e[type=text_display,tag=rufu_bub_heroine] run data merge entity @s {text:{text:"……1回目の方がよかった。でもいいよ。",color:"#7a1f5c"},background:-503321354}
scoreboard players set @e[type=text_display,tag=rufu_bub_heroine] rufu.bt 110
tellraw @a {text:"",extra:[{selector:"@e[type=marker,tag=rufu_namebox,limit=1]",color:"light_purple",bold:true},{text:"",color:"light_purple",bold:true},{text:"「……1回目の方がよかった。でもいいよ。」",color:"white"}]}
title @a times 3 100 8
title @a subtitle {text:"",extra:[{selector:"@e[type=marker,tag=rufu_namebox,limit=1]",color:"light_purple",bold:true},{text:"：",color:"light_purple",bold:true},{text:"「……1回目の方がよかった。でもいいよ。」",color:"white"}]}
title @a title {text:"……1回目の方がよかった。でもいいよ。",color:"light_purple",bold:true}
execute as @e[tag=rufu_npc_heroine] at @s run playsound minecraft:entity.allay.ambient_without_item voice @a ~ ~ ~ 1.4 1.25
execute at @e[type=mannequin,tag=rufu_npc_heroine] run particle minecraft:heart ~ ~2.2 ~ 0.5 0.4 0.5 0 30 force
execute as @a at @s run playsound minecraft:entity.player.levelup master @s ~ ~ ~ 1 1.0
summon minecraft:firework_rocket 195.5 82 85.5 {LifeTime:20,FireworksItem:{id:"minecraft:firework_rocket",count:1,components:{fireworks:{flight_duration:1,explosions:[{shape:"large_ball",colors:[I;16740277,16777215],fade_colors:[I;16765416],has_trail:true,has_twinkle:true}]}}},Tags:["rufu_fw"]}
summon minecraft:firework_rocket 199.5 82 89.5 {LifeTime:20,FireworksItem:{id:"minecraft:firework_rocket",count:1,components:{fireworks:{flight_duration:1,explosions:[{shape:"large_ball",colors:[I;16740277,16777215],fade_colors:[I;16765416],has_trail:true,has_twinkle:true}]}}},Tags:["rufu_fw"]}
