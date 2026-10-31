scoreboard players add #ask_t rufu 1
execute if score #ask_t rufu matches 600.. run function rufu:annoy/ask_spawn
execute if score #ask_live rufu matches 1.. run function rufu:annoy/ask_tick
execute if score #elapsed rufu = #intr_at rufu run function rufu:annoy/interrupt
execute if score #intr_live rufu matches 1 run function rufu:annoy/intr_timeout
execute if score #intr_live rufu matches 1.. run scoreboard players remove #intr_live rufu 1
