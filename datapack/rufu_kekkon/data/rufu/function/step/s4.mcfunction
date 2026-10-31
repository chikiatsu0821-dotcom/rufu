scoreboard players set #step rufu 4
data modify storage rufu:hud now set value "4. 試練1 説明「私より早く広場に来て」"
data modify storage rufu:hud next set value "5. 試練1 開始（45秒）"
scoreboard players set #seq rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 4. 試練1 説明「私より早く広場に来て」",color:"dark_green"}
kill @e[tag=rufu_rules]
title @a times 10 70 15
title @a subtitle {text:"私より早く広場に来て（制限時間45秒）",color:"white"}
title @a title {text:"試練1",color:"gold",bold:true}
execute as @a at @s run playsound minecraft:block.note_block.bell master @s ~ ~ ~ 1 1.0
function rufu:m1/reset
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 4
