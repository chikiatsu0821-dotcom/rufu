execute if score #ev_t rufu matches 40 run function rufu:ev/m3_clear/t40
execute if score #ev_t rufu matches 60 run tellraw @a[tag=rufu_gm] {text:"[GM] 試練3クリア！ 「次へ」で評価 → 丘の伝説の木へ",color:"green"}
execute if score #ev_t rufu matches 60.. run scoreboard players set #ev rufu 0
