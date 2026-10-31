tp @s 128.5 65 235.5 180 0
playsound minecraft:entity.player.splash master @a ~ ~ ~ 1 1
title @s times 0 30 10
title @s subtitle {text:"スタートに戻される…",color:"white"}
title @s title {text:"堀に落ちた！",color:"aqua",bold:true}
scoreboard players remove #love rufu 5
execute if score #love rufu matches ..-1 run scoreboard players set #love rufu 0
tellraw @a {text:"",extra:[{text:"💔 好感度 -5 ",color:"red",bold:true},{text:"堀に落ちた",color:"gray"}]}
execute as @a at @s run playsound minecraft:entity.villager.no master @s ~ ~ ~ 0.9 1.2
function rufu:hud/love
