scoreboard players add #gt rufu 1
scoreboard players operation #m5 rufu = #gt rufu
scoreboard players operation #m5 rufu %= #c5 rufu
scoreboard players operation #m20 rufu = #gt rufu
scoreboard players operation #m20 rufu %= #c20 rufu
execute as @a[scores={rufu.use=1..}] run function rufu:gm/use
execute as @a[scores={rufu.judge=1..}] run function rufu:annoy/judge
execute if score #seq rufu matches 1.. run function rufu:seq/tick
execute if score #ev rufu matches 1.. run function rufu:ev/tick
function rufu:npc/tick
execute as @e[type=interaction,tag=rufu_click] if data entity @s interaction run function rufu:click/got
execute as @e[type=interaction,tag=rufu_click] if data entity @s attack run function rufu:click/got_attack
execute if score #mission rufu matches 1 run function rufu:m1/tick
execute if score #mission rufu matches 2 run function rufu:m2/tick
execute if score #mission rufu matches 3 run function rufu:m3/tick
execute if score #mission rufu matches 4 run function rufu:m4/tick
execute if score #active rufu matches 1 run function rufu:mission/tick
execute if score #fx rufu matches 1.. run function rufu:fx/tick
function rufu:hud/tick
