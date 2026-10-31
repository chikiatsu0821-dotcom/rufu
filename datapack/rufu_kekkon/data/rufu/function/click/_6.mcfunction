execute as @e[type=text_display,tag=rufu_bub_heroine] run data merge entity @s {text:{text:"なぁに？ 今いそがしいんだけど。",color:"#7a1f5c"},background:-503321354}
scoreboard players set @e[type=text_display,tag=rufu_bub_heroine] rufu.bt 50
tellraw @a {text:"",extra:[{text:"ヒロイン",color:"light_purple",bold:true},{text:"「なぁに？ 今いそがしいんだけど。」",color:"white"}]}
execute as @e[tag=rufu_npc_heroine] at @s run playsound minecraft:entity.allay.ambient_without_item voice @a ~ ~ ~ 1.4 1.25
