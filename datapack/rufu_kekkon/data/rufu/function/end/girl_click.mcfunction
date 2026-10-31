execute unless entity @s[tag=rufu_hero] run return run function rufu:end/_53
execute if score #chosen rufu matches 1.. run return run function rufu:end/_54
scoreboard players operation #chosen rufu = #hitg rufu
execute if score #chosen rufu matches 1 run function rufu:end/_55
execute if score #chosen rufu matches 2 run function rufu:end/_56
execute if score #chosen rufu matches 3 run function rufu:end/_57
playsound minecraft:entity.player.levelup master @a ~ ~ ~ 1 1.6
tellraw @a[tag=rufu_gm] {text:"[GM] 選ばれました。「次へ」で『やっと選んでくれたね……』",color:"green"}
