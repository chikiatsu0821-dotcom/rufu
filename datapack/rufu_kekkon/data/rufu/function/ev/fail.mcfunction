execute if score #ev_t rufu matches 30 run tellraw @a {text:"…やり直し準備中…",color:"dark_gray"}
execute if score #ev_t rufu matches 70 run function rufu:mission/restart
execute if score #ev_t rufu matches 70.. run scoreboard players set #ev rufu 0
