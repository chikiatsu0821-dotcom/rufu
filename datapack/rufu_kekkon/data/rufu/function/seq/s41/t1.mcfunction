kill @e[tag=rufu_part_leon]
kill @e[tag=rufu_clone]
kill @e[tag=rufu_ghast]
scoreboard players set #fx rufu 0
title @a times 10 140 30
title @a subtitle {text:"仕掛け人：Rufu",color:"white",bold:true}
title @a title {text:"ドッキリ大成功！",color:"gold",bold:true}
tellraw @a {text:"",extra:[{text:"🎉 ドッキリ大成功！ ",color:"gold",bold:true},{text:"仕掛け人：Rufu",color:"white",bold:true}]}
function rufu:song/fanfare
execute as @a at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1.0
