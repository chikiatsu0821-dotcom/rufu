execute as @a[tag=rufu_p] run rotate @s facing 128.5 84 71.5
execute as @e[type=mannequin,tag=rufu_npc] at @s run tp @s ~ ~ ~ facing 128.5 84 71.5
execute as @a at @s run playsound minecraft:entity.player.attack.sweep master @s ~ ~ ~ 1 0.6
