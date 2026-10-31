scoreboard players add #pick rufu 1
execute at @e[type=mannequin,tag=rufu_npc_mio] run summon minecraft:lightning_bolt ~ ~ ~
execute at @e[type=mannequin,tag=rufu_npc_mio] run particle minecraft:large_smoke ~ ~1 ~ 0.5 1 0.5 0.03 60 force
execute at @e[type=mannequin,tag=rufu_npc_mio] run particle minecraft:campfire_cosy_smoke ~ ~0.5 ~ 0.3 0.5 0.3 0.02 15 force
data merge entity @e[type=mannequin,tag=rufu_npc_mio,limit=1] {description:{text:"近日実装",color:"red",bold:true}}
title @s times 0 40 10
title @s subtitle {text:"",extra:[{text:"みおは ",color:"white"},{text:"近日実装",color:"red",bold:true}]}
title @s title {text:""}
tellraw @a {text:"⚡ みおは 近日実装 です",color:"red",bold:true}
schedule function rufu:hall/clear_fire 30t
function rufu:hall/q_react
