scoreboard players set #ev_t rufu 0
scoreboard players set #ev rufu 2
title @a times 5 40 10
title @a subtitle {text:"3人全員クリア！",color:"white"}
title @a title {text:"CLEAR!",color:"gold",bold:true}
execute as @a at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1.0
