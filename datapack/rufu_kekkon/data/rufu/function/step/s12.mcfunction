scoreboard players set #step rufu 12
data modify storage rufu:hud now set value "12. オチ「この道じゃない方がよかった」→夜"
data modify storage rufu:hud next set value "13. 試練3 2周目開始（夜・裏通り）"
scoreboard players set #seq rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 12. オチ「この道じゃない方がよかった」→夜",color:"dark_green"}
scoreboard players set #lock rufu 1
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 12
