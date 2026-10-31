scoreboard players set @s rufu.use 0
execute unless entity @s[tag=rufu_gm] run return run function rufu:gm/_1
execute if predicate rufu:hold_next run return run function rufu:gm/next
execute if predicate rufu:hold_again run return run function rufu:gm/again
execute if predicate rufu:hold_redo run return run function rufu:gm/redo
