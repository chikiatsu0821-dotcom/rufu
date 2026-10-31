tag @s add rufu_gm
tag @s remove rufu_p
tag @s remove rufu_hero
tag @s remove rufu_helper
execute unless entity @s[tag=rufu_hasremote] run function rufu:gm/remotes
tag @s add rufu_hasremote
function rufu:menu/list
function rufu:gm/panel
