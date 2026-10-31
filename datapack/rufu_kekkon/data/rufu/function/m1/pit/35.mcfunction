fill 137 64 218 139 64 220 minecraft:lava
fill 137 63 218 139 63 220 minecraft:blackstone strict
particle minecraft:lava 138.5 65 219.5 1 0.2 1 0 25 force
particle minecraft:large_smoke 138.5 65 219.5 1 0.5 1 0.02 20 force
playsound minecraft:block.lava.pop master @a 138.5 65 219.5 2 0.6
playsound minecraft:entity.blaze.shoot master @a 138.5 65 219.5 1 0.5
scoreboard players remove #love rufu 10
execute if score #love rufu matches ..-1 run scoreboard players set #love rufu 0
tellraw @a {text:"",extra:[{text:"💔 好感度 -10 ",color:"red",bold:true},{text:"落とし穴（溶岩）を踏んだ！",color:"gray"}]}
execute as @a at @s run playsound minecraft:entity.villager.no master @s ~ ~ ~ 0.9 1.2
function rufu:hud/love
