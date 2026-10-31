scoreboard players set #ev_t rufu 0
scoreboard players set #ev rufu 5
title @a times 5 40 10
title @a subtitle {text:"公園に到着",color:"white"}
title @a title {text:"ゴール！",color:"gold",bold:true}
execute as @a at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1.2
