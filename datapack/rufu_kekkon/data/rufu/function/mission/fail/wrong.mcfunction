execute unless score #active rufu matches 1 run return 0
scoreboard players set #active rufu 0
scoreboard players add #retry rufu 1
kill @e[tag=rufu_ask]
scoreboard players set #intr_live rufu 0
title @a times 5 50 15
title @a subtitle {text:"指名と違う人が渡した！",color:"white"}
title @a title {text:"失敗…",color:"red",bold:true}
execute as @a at @s run playsound minecraft:entity.wither.death master @s ~ ~ ~ 0.35 1.6
execute as @a at @s run playsound minecraft:block.note_block.didgeridoo master @s ~ ~ ~ 1 0.6
tellraw @a {text:"",extra:[{text:"✖ ミッション失敗：",color:"red",bold:true},{text:"指名と違う人が渡した！",color:"white"},{text:"　→ 3人そろって最初からやり直し！",color:"gray"}]}
function rufu:ev/start/fail
