time add -400
execute as @a at @s run particle minecraft:reverse_portal ~ ~1 ~ 2 1 2 0.2 20
title @a times 5 60 10
title @a subtitle {text:"空が逆回りしている",color:"white"}
title @a title {text:"◀◀ 巻き戻し中……",color:"aqua",bold:true}
execute as @a at @s run playsound minecraft:block.portal.trigger master @s ~ ~ ~ 0.6 2.0
execute as @a at @s run playsound minecraft:item.trident.return master @s ~ ~ ~ 1 0.5
