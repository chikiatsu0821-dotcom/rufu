execute at @e[type=mannequin,tag=rufu_clone] run particle minecraft:heart ~ ~2 ~ 0.4 0.3 0.4 0 8 force
title @a times 0 60 10
title @a subtitle {text:"",color:"white"}
title @a title {text:"3人ともヒロインに変身！",color:"light_purple",bold:true}
execute as @a at @s run playsound minecraft:entity.allay.ambient_without_item master @s ~ ~ ~ 1 1.0
