execute if score #ev_t rufu matches 45 run function rufu:ev/m4_yes2/t45
execute if score #ev_t rufu matches 100 run tellraw @a[tag=rufu_gm] {text:"[GM] 試練4クリア！ 「次へ」で総合評価",color:"green"}
execute if score #ev_t rufu matches 100.. run scoreboard players set #ev rufu 0
