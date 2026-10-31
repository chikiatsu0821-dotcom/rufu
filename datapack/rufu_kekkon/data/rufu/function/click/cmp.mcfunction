data modify storage rufu:tmp cmp set from entity @s UUID
execute store success score #diff rufu run data modify storage rufu:tmp cmp set from storage rufu:tmp uuid
execute if score #diff rufu matches 0 run tag @s add rufu_clicker
