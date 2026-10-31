scoreboard players set #love rufu 100
function rufu:hud/show
execute as @a[tag=rufu_p] run function rufu:op/_49
tellraw @a[tag=rufu_p] {text:"✂ 「花ばさみ」をもらった。町の花をつんでヒロインに右クリックで渡すと 好感度+20（各試練1回）",color:"light_purple"}
