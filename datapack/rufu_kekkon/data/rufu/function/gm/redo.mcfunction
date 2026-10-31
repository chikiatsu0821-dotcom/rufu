execute unless score #retry_step rufu matches 1.. run return run function rufu:gm/_5
playsound minecraft:ui.button.click master @s ~ ~ ~ 0.6 0.7
tellraw @a {text:"⟲ ミッションを最初からやり直します（GM操作）",color:"gray"}
function rufu:mission/restart
