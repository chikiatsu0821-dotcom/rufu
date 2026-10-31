scoreboard players set #step rufu 14
data modify storage rufu:hud now set value "14. 試練3 評価 → 丘の伝説の木へ"
data modify storage rufu:hud next set value "15. 試練4 説明「指輪？……あの子が持ってっちゃった」"
scoreboard players set #seq rufu 0
scoreboard players set #retry_step rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 14. 試練3 評価 → 丘の伝説の木へ",color:"dark_green"}
scoreboard players set #lock rufu 1
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 14
