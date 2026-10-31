scoreboard players set #fx rufu 0
execute at @e[type=pig,tag=rufu_pig] run particle minecraft:portal ~ ~1 ~ 0.5 1 0.5 0.5 80 force
playsound minecraft:block.portal.trigger master @a 151.5 66 60 2 1.4
kill @e[tag=rufu_part_heroine]
kill @e[tag=rufu_part_leon]
kill @e[tag=rufu_pig]
tellraw @a {text:"（ふたりはネザーゲートの向こうへ消えた……）",color:"dark_purple",italic:true}
schedule function rufu:wed/portal_boom 50t
