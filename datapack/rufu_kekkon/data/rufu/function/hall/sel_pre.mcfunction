execute if entity @s[tag=rufu_sel1] run scoreboard players set #hit rufu 1
execute if entity @s[tag=rufu_sel2] run scoreboard players set #hit rufu 2
execute if entity @s[tag=rufu_sel3] run scoreboard players set #hit rufu 3
execute if entity @s[tag=rufu_sel4] run scoreboard players set #hit rufu 4
execute as @a[tag=rufu_clicker,limit=1] run function rufu:hall/sel_click
