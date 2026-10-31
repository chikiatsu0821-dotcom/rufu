particle minecraft:explosion_emitter 151.5 67 60 1 1 1 0 3 force
playsound minecraft:entity.generic.explode master @a 151.5 67 60 4 0.7
fill 150 65 60 153 69 60 minecraft:air
fill 150 65 60 153 65 60 minecraft:crying_obsidian
setblock 150 66 60 minecraft:obsidian
title @a times 5 50 15
title @a subtitle {text:"もう追いかけられない",color:"gray"}
title @a title {text:"ゲートが爆破された",color:"dark_purple",bold:true}
