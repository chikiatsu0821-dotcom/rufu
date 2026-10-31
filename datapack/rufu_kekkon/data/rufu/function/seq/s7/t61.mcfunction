title @a times 0 30 10
title @a subtitle {text:"3人全員クリアが条件！",color:"white"}
title @a title {text:"スタート！",color:"green",bold:true}
execute as @a at @s run playsound minecraft:block.note_block.pling master @s ~ ~ ~ 1 2.0
execute as @a at @s run playsound minecraft:entity.firework_rocket.launch master @s ~ ~ ~ 1 1.2
execute as @a run attribute @s minecraft:movement_speed base reset
execute as @a run attribute @s minecraft:jump_strength base reset
scoreboard players set #active rufu 1
tellraw @a[tag=rufu_p] {text:"🔪 万能ナイフで小麦・サトウキビ・花を刈れる。牛と豚もこれで。",color:"gray"}
