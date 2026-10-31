scoreboard players operation #sec rufu = #t_total rufu
scoreboard players operation #sec rufu /= #c20 rufu
scoreboard players operation #mm rufu = #sec rufu
scoreboard players operation #mm rufu /= #c60 rufu
scoreboard players operation #ss rufu = #sec rufu
scoreboard players operation #ss rufu %= #c60 rufu
title @a times 5 70 10
title @a subtitle {text:"",extra:[{text:"合計タイム ",color:"white"},{score:{name:"#mm",objective:"rufu"},color:"yellow"},{text:"分",color:"white"},{score:{name:"#ss",objective:"rufu"},color:"yellow"},{text:"秒",color:"white"}]}
title @a title {text:"",extra:[{text:"リトライ回数 ",color:"white",bold:true},{score:{name:"#retry",objective:"rufu"},color:"red",bold:true},{text:" 回",color:"white",bold:true}]}
tellraw @a {text:"",extra:[{text:"📊 リトライ回数：",color:"gold"},{score:{name:"#retry",objective:"rufu"},color:"red",bold:true},{text:"回　合計タイム：",color:"gold"},{score:{name:"#mm",objective:"rufu"},color:"yellow"},{text:"分",color:"gold"},{score:{name:"#ss",objective:"rufu"},color:"yellow"},{text:"秒",color:"gold"}]}
execute as @a at @s run playsound minecraft:block.note_block.bell master @s ~ ~ ~ 1 1.2
