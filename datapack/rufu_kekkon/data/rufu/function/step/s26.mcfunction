scoreboard players set #step rufu 26
data modify storage rufu:hud now set value "26. ヒロインが近づく「ん～～～♡」"
data modify storage rufu:hud next set value "27. 「ちょっと待ったーー！！」"
scoreboard players set #seq rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 26. ヒロインが近づく「ん～～～♡」",color:"dark_green"}
scoreboard players set #lock rufu 1
tp @a[tag=rufu_hero] 127.5 66 63.5 -90 0
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 26
