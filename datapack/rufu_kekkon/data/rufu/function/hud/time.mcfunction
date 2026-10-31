scoreboard players operation #sec rufu = #timer rufu
scoreboard players add #sec rufu 19
scoreboard players operation #sec rufu /= #c20 rufu
scoreboard players operation #mm rufu = #sec rufu
scoreboard players operation #mm rufu /= #c60 rufu
scoreboard players operation #ss rufu = #sec rufu
scoreboard players operation #ss rufu %= #c60 rufu
execute store result bossbar rufu:time value run scoreboard players get #timer rufu
execute if score #ss rufu matches 10.. run bossbar set rufu:time name {text:"",extra:[{text:"⏱ 残り ",color:"yellow",bold:true},{score:{name:"#mm",objective:"rufu"},color:"white",bold:true},{text:":",color:"white"},{score:{name:"#ss",objective:"rufu"},color:"white",bold:true}]}
execute if score #ss rufu matches ..9 run bossbar set rufu:time name {text:"",extra:[{text:"⏱ 残り ",color:"yellow",bold:true},{score:{name:"#mm",objective:"rufu"},color:"white",bold:true},{text:":0",color:"white"},{score:{name:"#ss",objective:"rufu"},color:"white",bold:true}]}
execute if score #timer rufu matches ..200 run bossbar set rufu:time color red
execute if score #timer rufu matches 201.. run bossbar set rufu:time color yellow
