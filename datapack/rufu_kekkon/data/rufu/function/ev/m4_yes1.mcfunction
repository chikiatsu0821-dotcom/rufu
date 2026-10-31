execute if score #ev_t rufu matches 45 run function rufu:ev/m4_yes1/t45
execute if score #ev_t rufu matches 90 run tellraw @a[tag=rufu_gm] {text:"[GM] 告白成功（1回目）。「次へ」で『やっぱりなかったことにして』",color:"green"}
execute if score #ev_t rufu matches 90.. run scoreboard players set #ev rufu 0
