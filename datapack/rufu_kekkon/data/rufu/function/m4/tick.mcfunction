execute unless score #active rufu matches 1 run return 0
execute as @e[type=fox,tag=rufu_fox] at @s run function rufu:m4/fox
execute if score #m4p rufu matches 0 if score #m20 rufu matches 0 run title @a[tag=rufu_p] actionbar {text:"🦊 指輪をくわえたキツネを 2人以上で囲んで止めて、叩け！",color:"gold"}
execute if score #m4p rufu matches 1 run function rufu:m4/phase1
execute if score #m4p rufu matches 2 as @e[type=text_display,tag=rufu_sign,limit=1] at @s run function rufu:m4/sign_tick
execute if score #m4p rufu matches 2 as @e[type=text_display,tag=rufu_sign,limit=1] at @s run tp @e[type=interaction,tag=rufu_sign_hit] ~ ~-0.6 ~
execute if score #m5 rufu matches 0 run function rufu:m4/circle_fx
