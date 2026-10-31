title @a times 15 50 15
title @a subtitle {text:"ノーマルエンド：返品",color:"white"}
title @a title {text:"END",color:"white",bold:true}
tellraw @a {text:"",extra:[{text:"  END  ",color:"white",bold:true},{text:"ノーマルエンド：返品",color:"white"}]}
execute as @a at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 0.6
