execute unless entity @s[tag=rufu_hero] run return run function rufu:end/_45
execute if score #chosen rufu matches 1.. run return run function rufu:end/_46
scoreboard players operation #chosen rufu = #hitg rufu
execute if score #chosen rufu matches 1 run function rufu:end/_47
execute if score #chosen rufu matches 2 run function rufu:end/_48
execute if score #chosen rufu matches 3 run function rufu:end/_49
playsound minecraft:entity.player.levelup master @a ~ ~ ~ 1 1.6
tellraw @a[tag=rufu_gm] {text:"[GM] 選ばれました。「次へ」で『やっと選んでくれたね……』",color:"green"}
