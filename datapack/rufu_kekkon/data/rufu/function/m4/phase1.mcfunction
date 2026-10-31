execute store result score #hr rufu run clear @a[tag=rufu_hero,limit=1] minecraft:gold_nugget[custom_data~{rufu_ring:1b}] 0
execute positioned 195.5 81 89.5 store result score #inc rufu if entity @a[tag=rufu_p,distance=..5.1]
execute if score #hr rufu matches 1.. if score #inc rufu >= #np rufu run return run function rufu:m4/sign_spawn
execute if score #m20 rufu matches 0 run title @a[tag=rufu_p] actionbar {text:"",extra:[{text:"💍 指輪を ",color:"white"},{text:"主人公",color:"green",bold:true},{text:" が持って、3人全員で ",color:"white"},{text:"木の下の光る円",color:"gold",bold:true},{text:" に入ろう",color:"white"}]}
