execute store result score #pin rufu if entity @a[tag=rufu_p,tag=!rufu_hero,gamemode=!spectator,distance=..2.3]
execute if score #pin rufu >= #pin_need rufu run return run function rufu:m4/sign_pinned
execute if entity @a[tag=rufu_hero,distance=..4.5] run function rufu:m4/sign_flee
execute if score #m5 rufu matches 0 run particle minecraft:heart ~ ~0.6 ~ 0.4 0.2 0.1 0 1
