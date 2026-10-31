execute as @e[type=pig,tag=rufu_pig] at @s facing entity @e[type=marker,tag=rufu_pigwp,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^0.12 facing ^ ^ ^5
execute as @e[type=pig,tag=rufu_pig1] at @s if entity @e[type=marker,tag=rufu_pigwp,distance=..0.4] run function rufu:wed/pig_next
execute as @a[tag=rufu_p] at @s if entity @e[type=pig,tag=rufu_pig,distance=..4.5] facing entity @e[type=pig,tag=rufu_pig,sort=nearest,limit=1] feet rotated ~180 0 run tp @s ^ ^ ^0.6
execute as @a[tag=rufu_p] at @s if entity @e[type=pig,tag=rufu_pig,distance=..6] run title @s actionbar {text:"……なぜか追いつけない！",color:"gray",italic:true}
execute as @a[tag=rufu_p] at @s if entity @e[type=pig,tag=rufu_pig,distance=..6] run particle minecraft:sweep_attack ~ ~1 ~ 0.3 0.3 0.3 0 1
execute if score #m20 rufu matches 0 at @e[type=pig,tag=rufu_pig] run playsound minecraft:entity.pig.ambient neutral @a ~ ~ ~ 1 0.8
