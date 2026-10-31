execute if score #ev_t rufu matches 40 run function rufu:ev/m2_clear/t40
execute if score #ev_t rufu matches 60 run tellraw @a[tag=rufu_gm] {text:"[GM] 試練2クリア！ 「次へ」でオチ（やっぱパンだけでよかった）",color:"green"}
execute if score #ev_t rufu matches 60.. run scoreboard players set #ev rufu 0
