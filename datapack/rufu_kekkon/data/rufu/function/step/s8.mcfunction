scoreboard players set #step rufu 8
data modify storage rufu:hud now set value "8. オチ「やっぱパンだけでよかった」"
data modify storage rufu:hud next set value "9. 試練2 評価"
scoreboard players set #seq rufu 0
scoreboard players set #retry_step rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 8. オチ「やっぱパンだけでよかった」",color:"dark_green"}
scoreboard players set #lock rufu 1
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 8
