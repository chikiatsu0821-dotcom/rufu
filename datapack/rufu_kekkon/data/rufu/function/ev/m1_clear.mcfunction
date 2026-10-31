execute if score #ev_t rufu matches 30 run function rufu:ev/m1_clear/t30
execute if score #ev_t rufu matches 80 run function rufu:ev/m1_clear/t80
execute if score #ev_t rufu matches 90 run tellraw @a[tag=rufu_gm] {text:"[GM] 試練1クリア！ 「次へ」で評価発表",color:"green"}
execute if score #ev_t rufu matches 90.. run scoreboard players set #ev rufu 0
