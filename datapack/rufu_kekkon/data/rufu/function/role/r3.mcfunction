tag @s remove rufu_p
tag @s remove rufu_hero
tag @s remove rufu_helper
tag @s add rufu_gm
function rufu:gm/remotes
tag @s add rufu_hasremote
tellraw @a[tag=rufu_gm] {text:"",extra:[{text:"🎮 GM：",color:"gold"},{selector:"@s"}]}
