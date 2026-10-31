execute at @e[type=mannequin,tag=rufu_npc_heroine] run summon minecraft:item ~ ~1.6 ~ {Item:{id:"minecraft:cake",count:1},PickupDelay:32767s,Motion:[0.25d,1.6d,-0.1d],Tags:["rufu_throw"]}
execute at @e[type=mannequin,tag=rufu_npc_heroine] run summon minecraft:item ~ ~1.6 ~ {Item:{id:"minecraft:cooked_beef",count:1},PickupDelay:32767s,Motion:[-0.25d,1.7d,0.1d],Tags:["rufu_throw"]}
execute as @a at @s run playsound minecraft:entity.witch.throw master @s ~ ~ ~ 1 0.8
execute as @a at @s run playsound minecraft:entity.player.attack.sweep master @s ~ ~ ~ 1 0.6
tellraw @a {text:"（ケーキとお肉が空のかなたへ投げ捨てられた）",color:"gray",italic:true}
