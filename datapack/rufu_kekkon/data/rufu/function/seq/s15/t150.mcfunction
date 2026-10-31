execute as @e[type=text_display,tag=rufu_bub_heroine] run data merge entity @s {text:{text:"指輪？……あの子が持ってっちゃった。",color:"#7a1f5c"},background:-503321354}
scoreboard players set @e[type=text_display,tag=rufu_bub_heroine] rufu.bt 90
tellraw @a {text:"",extra:[{selector:"@e[type=marker,tag=rufu_namebox,limit=1]",color:"light_purple",bold:true},{text:"",color:"light_purple",bold:true},{text:"「指輪？……あの子が持ってっちゃった。」",color:"white"}]}
title @a times 3 80 8
title @a subtitle {text:"",extra:[{selector:"@e[type=marker,tag=rufu_namebox,limit=1]",color:"light_purple",bold:true},{text:"：",color:"light_purple",bold:true},{text:"「指輪？……あの子が持ってっちゃった。」",color:"white"}]}
title @a title {text:"指輪？……あの子が持ってっちゃった。",color:"light_purple",bold:true}
execute as @e[tag=rufu_npc_heroine] at @s run playsound minecraft:entity.allay.ambient_without_item voice @a ~ ~ ~ 1.4 1.25
summon minecraft:fox 195.5 81 72.5 {Tags:["rufu_fox","rufu_mob4","rufu_demo","rufu_fox_real"],NoAI:true,PersistenceRequired:true,Silent:false,Type:"red",attributes:[{id:"minecraft:max_health",base:1024.0d}],Health:1000.0f,equipment:{mainhand:{id:"minecraft:gold_nugget",count:1,components:{custom_name:{text:"💍 婚約指輪",color:"gold",bold:true,italic:false},lore:[{text:"ヒロインに渡すための指輪。",color:"gray",italic:false},{text:"キツネの大好物ではない。",color:"gray",italic:false}],custom_data:{rufu_ring:1b,rufu_m:1b},enchantment_glint_override:true}}},drop_chances:{mainhand:0.0f}}
execute at @e[tag=rufu_demo] run particle minecraft:poof ~ ~0.5 ~ 0.3 0.3 0.3 0.02 15 force
playsound minecraft:entity.fox.ambient master @a 195.5 81 72.5 1 1.2
