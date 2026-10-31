scoreboard players set #step rufu 20
data modify storage rufu:hud now set value "20. 総合評価（リトライ回数・タイム → D 理由：顔）"
data modify storage rufu:hud next set value "21. 結婚式へ（教会に移動）"
scoreboard players set #seq rufu 0
scoreboard players set #retry_step rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 20. 総合評価（リトライ回数・タイム → D 理由：顔）",color:"dark_green"}
scoreboard players set #lock rufu 1
scoreboard players set #mission rufu 0
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 20
