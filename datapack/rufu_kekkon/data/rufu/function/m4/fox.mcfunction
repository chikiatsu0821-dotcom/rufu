execute store result score #h rufu run data get entity @s HurtTime
execute if score #h rufu matches 10 run return run function rufu:m4/fox_hit
execute if score @s rufu.fz matches 1.. run return run function rufu:m4/fox_frozen
execute store result score #near rufu if entity @a[tag=rufu_p,gamemode=!spectator,distance=..3.2]
execute if score #near rufu >= #fox_need rufu run return run function rufu:m4/fox_freeze
execute if entity @a[tag=rufu_p,distance=..6,predicate=rufu:hold_berries] run return run function rufu:m4/fox_lured
execute if entity @a[tag=rufu_p,gamemode=!spectator,distance=..7] run return run function rufu:m4/fox_flee
function rufu:m4/fox_wander
