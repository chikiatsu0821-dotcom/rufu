execute as @e[type=mannequin,tag=rufu_npc_q,limit=1] at @s facing entity @p[tag=rufu_hero] feet rotated ~ 0 positioned ^ ^ ^1 run tp @s ~ ~ ~ facing entity @p[tag=rufu_hero] eyes
execute as @a[tag=rufu_hero] at @s run playsound minecraft:entity.warden.heartbeat master @s ~ ~ ~ 1.5 1
schedule function rufu:hall/heartbeat2 8t
execute if score #pick rufu matches 1 run function rufu:hall/_42
execute if score #pick rufu matches 2 run function rufu:hall/_43
execute if score #pick rufu matches 3 run function rufu:hall/dark
execute if score #pick rufu matches 4.. run function rufu:hall/_44
