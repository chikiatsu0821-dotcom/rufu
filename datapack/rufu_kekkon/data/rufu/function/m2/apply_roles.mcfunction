scoreboard players set @a rufu.role 0
team leave @a[tag=rufu_p]
execute as @a[tag=rufu_p] if score @s rufu.pi = #own1 rufu run scoreboard players set @s rufu.role 1
execute as @a[tag=rufu_p] if score @s rufu.pi = #own2 rufu run scoreboard players set @s rufu.role 2
execute as @a[tag=rufu_p] if score @s rufu.pi = #own3 rufu run scoreboard players set @s rufu.role 3
team join rufu_bread @a[tag=rufu_p,scores={rufu.role=1}]
team join rufu_cake @a[tag=rufu_p,scores={rufu.role=2}]
team join rufu_meat @a[tag=rufu_p,scores={rufu.role=3}]
title @a[tag=rufu_p,scores={rufu.role=1}] times 5 50 10
title @a[tag=rufu_p,scores={rufu.role=1}] subtitle {text:"頭の上にも表示されています",color:"white"}
title @a[tag=rufu_p,scores={rufu.role=1}] title {text:"あなたは パン担当",color:"gold",bold:true}
title @a[tag=rufu_p,scores={rufu.role=2}] times 5 50 10
title @a[tag=rufu_p,scores={rufu.role=2}] subtitle {text:"頭の上にも表示されています",color:"white"}
title @a[tag=rufu_p,scores={rufu.role=2}] title {text:"あなたは ケーキ担当",color:"light_purple",bold:true}
title @a[tag=rufu_p,scores={rufu.role=3}] times 5 50 10
title @a[tag=rufu_p,scores={rufu.role=3}] subtitle {text:"頭の上にも表示されています",color:"white"}
title @a[tag=rufu_p,scores={rufu.role=3}] title {text:"あなたは お肉担当",color:"red",bold:true}
execute as @a at @s run playsound minecraft:block.note_block.chime master @s ~ ~ ~ 1 1.2
