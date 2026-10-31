execute if score #ev_t rufu matches 40 run function rufu:ev/m3_lap1_end/t40
execute if score #ev_t rufu matches 60 run tellraw @a[tag=rufu_gm] {text:"[GM] 1周目ゴール。「次へ」でオチ（この道じゃない方がよかった）",color:"green"}
execute if score #ev_t rufu matches 60.. run scoreboard players set #ev rufu 0
