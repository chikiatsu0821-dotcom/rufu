execute store result score #k rufu run random value 1..2
scoreboard players operation #own1 rufu += #k rufu
scoreboard players operation #own2 rufu += #k rufu
scoreboard players operation #own3 rufu += #k rufu
execute if score #own1 rufu matches 4.. run scoreboard players remove #own1 rufu 3
execute if score #own2 rufu matches 4.. run scoreboard players remove #own2 rufu 3
execute if score #own3 rufu matches 4.. run scoreboard players remove #own3 rufu 3
function rufu:m2/apply_roles
