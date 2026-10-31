particle minecraft:poof ~ ~0.4 ~ 0.3 0.3 0.3 0.02 12 force
playsound minecraft:entity.fox.teleport master @a ~ ~ ~ 1 1
execute store result storage rufu:tmp a float 1 run random value 0..359
function rufu:m4/fox_blink_m with storage rufu:tmp
execute at @s run particle minecraft:poof ~ ~0.4 ~ 0.3 0.3 0.3 0.02 12 force
