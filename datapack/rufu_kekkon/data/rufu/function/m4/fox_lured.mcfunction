tp @s ~ ~ ~ facing entity @p[tag=rufu_p,predicate=rufu:hold_berries]
execute if score #m20 rufu matches 0 run particle minecraft:heart ~ ~0.8 ~ 0.2 0.2 0.2 0 1
execute if score #m20 rufu matches 0 run playsound minecraft:entity.fox.sniff master @a ~ ~ ~ 1 1.2
