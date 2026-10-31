scoreboard players set @a rufu.pi 0
scoreboard players set #pi rufu 0
execute as @a[tag=rufu_p,sort=random] run function rufu:m2/_22
execute store result score #perm rufu run random value 0..5
execute if score #perm rufu matches 0 run function rufu:m2/_23
execute if score #perm rufu matches 1 run function rufu:m2/_24
execute if score #perm rufu matches 2 run function rufu:m2/_25
execute if score #perm rufu matches 3 run function rufu:m2/_26
execute if score #perm rufu matches 4 run function rufu:m2/_27
execute if score #perm rufu matches 5 run function rufu:m2/_28
scoreboard players operation #orig1 rufu = #own1 rufu
scoreboard players operation #orig2 rufu = #own2 rufu
scoreboard players operation #orig3 rufu = #own3 rufu
function rufu:m2/apply_roles
