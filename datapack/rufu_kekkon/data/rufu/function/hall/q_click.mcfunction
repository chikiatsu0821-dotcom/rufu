execute unless entity @s[tag=rufu_hero] run return run function rufu:hall/_45
execute unless score #naming rufu matches 1 run return run function rufu:hall/_46
execute unless predicate rufu:hold_nametag run return run function rufu:hall/_47
execute store success score #ok rufu run data get entity @s SelectedItem.components."minecraft:custom_name"
execute if score #ok rufu matches 0 run return run function rufu:hall/_48
data modify entity @e[type=marker,tag=rufu_namebox,limit=1] CustomName set from entity @s SelectedItem.components."minecraft:custom_name"
data modify entity @e[type=mannequin,tag=rufu_npc_q,limit=1] CustomName set from entity @e[type=marker,tag=rufu_namebox,limit=1] CustomName
clear @s minecraft:name_tag 1
function rufu:hall/named
