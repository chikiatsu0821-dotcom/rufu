execute unless entity @s[tag=rufu_hero] run return run function rufu:annoy/_8
execute at @e[type=text_display,tag=rufu_askdisp] run particle minecraft:heart ~ ~0.3 ~ 0.4 0.3 0.4 0 4
kill @e[tag=rufu_ask]
scoreboard players set #ask_live rufu 0
playsound minecraft:entity.experience_orb.pickup master @s ~ ~ ~ 1 1.4
tellraw @a {text:"",extra:[{text:"📱 主人公が返信した：「今いそがしい！」 ",color:"gray"},{text:"（ヒロイン：「ふーん。」）",color:"light_purple"}]}
