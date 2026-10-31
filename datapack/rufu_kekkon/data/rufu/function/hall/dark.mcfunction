effect give @a[tag=rufu_hero] minecraft:darkness 4 0 true
effect give @a[tag=rufu_hero] minecraft:blindness 3 0 true
execute as @a[tag=rufu_hero] at @s run playsound minecraft:entity.elder_guardian.curse master @s ~ ~ ~ 1 1
schedule function rufu:hall/dark_end 50t
