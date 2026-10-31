scoreboard players remove #timer rufu 1
scoreboard players add #elapsed rufu 1
execute if score #timer rufu matches ..0 run return run function rufu:mission/fail/time
execute if score #love rufu matches ..0 run return run function rufu:mission/fail/love
execute if entity @a[tag=rufu_p,scores={rufu.death=1..}] run return run function rufu:mission/fail/death
function rufu:annoy/tick
