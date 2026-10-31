execute store result bossbar rufu:love value run scoreboard players get #love rufu
bossbar set rufu:love name {text:"",extra:[{text:"♥ 好感度 ",color:"light_purple",bold:true},{score:{name:"#love",objective:"rufu"},color:"white",bold:true},{text:" / 100",color:"gray"}]}
execute if score #love rufu matches 50.. run bossbar set rufu:love color pink
execute if score #love rufu matches 25..49 run bossbar set rufu:love color yellow
execute if score #love rufu matches ..24 run bossbar set rufu:love color red
