execute as @e[type=text_display,tag=rufu_bub_mio] run data merge entity @s {text:{text:"よろしくね。",color:"#1f3f7a"},background:-505089793}
scoreboard players set @e[type=text_display,tag=rufu_bub_mio] rufu.bt 60
tellraw @a {text:"",extra:[{text:"みお",color:"#7fb8ff",bold:true},{text:"「よろしくね。」",color:"white"}]}
execute as @e[tag=rufu_npc_mio] at @s run playsound minecraft:entity.allay.ambient_with_item voice @a ~ ~ ~ 1.4 1.35
