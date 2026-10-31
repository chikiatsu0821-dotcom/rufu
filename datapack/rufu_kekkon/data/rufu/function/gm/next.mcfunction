execute if score #lock rufu matches 1 run return run function rufu:gm/_2
execute if score #step rufu >= #last rufu run return run function rufu:gm/_3
playsound minecraft:ui.button.click master @s ~ ~ ~ 0.6 1.4
scoreboard players add #step rufu 1
function rufu:step/goto
