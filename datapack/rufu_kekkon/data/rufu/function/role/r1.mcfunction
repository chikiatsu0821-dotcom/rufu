tag @a remove rufu_hero
tag @s remove rufu_p
tag @s remove rufu_hero
tag @s remove rufu_helper
tag @s add rufu_p
tag @s add rufu_hero
tellraw @a[tag=rufu_gm] {text:"",extra:[{text:"★ 主人公：",color:"green"},{selector:"@s"}]}
