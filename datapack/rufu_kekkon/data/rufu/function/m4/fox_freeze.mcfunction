scoreboard players set @s rufu.fz 50
data merge entity @s {Glowing:true}
playsound minecraft:entity.fox.screech master @a ~ ~ ~ 1 1.3
title @a[tag=rufu_p,distance=..10] actionbar {text:"キツネが動けない！ 今のうちに叩け！",color:"gold",bold:true}
