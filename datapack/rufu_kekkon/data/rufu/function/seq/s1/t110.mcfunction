function rufu:hall/signs
title @a[tag=rufu_hero,limit=1] times 5 70 10
title @a[tag=rufu_hero,limit=1] subtitle {text:"「この子にする」を右クリックで、ヒロインを選んでね",color:"light_purple"}
title @a[tag=rufu_hero,limit=1] title {text:""}
tellraw @a {text:"💗 主人公は「この子にする」を右クリックしてヒロインを選んでね",color:"light_purple"}
scoreboard players set #lock rufu 0
