scoreboard players remove #ask_live rufu 1
execute at @e[type=text_display,tag=rufu_askdisp] run particle minecraft:end_rod ~ ~0.5 ~ 0.6 0.4 0.1 0 1
execute if score #ask_live rufu matches 0 run function rufu:annoy/ask_miss
