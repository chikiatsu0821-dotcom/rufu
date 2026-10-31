execute unless score #active rufu matches 1 run return 0
function rufu:m1/pits
function rufu:m1/db/tick
execute as @a[tag=rufu_p,x=25,y=55,z=208,dx=205,dy=8,dz=6] at @s if block ~ ~ ~ minecraft:water run function rufu:m1/moat_fall
execute if score #m1_her rufu matches 0 if entity @a[tag=rufu_p,x=98,y=60,z=94,dx=60,dy=20,dz=54] run function rufu:m1/her_start
execute if score #m1_her rufu matches 1 as @e[type=mannequin,tag=rufu_npc_heroine,limit=1] at @s run function rufu:m1/her_run
execute store result score #n rufu if entity @a[tag=rufu_p,x=128.5,y=65,z=121.5,distance=..9]
execute if score #n rufu >= #np rufu run function rufu:m1/clear
execute if score #m20 rufu matches 0 run title @a[tag=rufu_p] actionbar {text:"",extra:[{text:"目的地：",color:"gray"},{text:"中央広場の噴水",color:"aqua",bold:true},{text:"　3人全員そろって到着！",color:"white"}]}
