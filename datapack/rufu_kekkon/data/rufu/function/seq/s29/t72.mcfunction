scoreboard players set #love rufu 0
function rufu:hud/love
execute as @a at @s run playsound minecraft:entity.zombie_villager.cure master @s ~ ~ ~ 0.6 0.8
tellraw @a {text:"💔 好感度が 0 になった",color:"red",bold:true}
scoreboard players set #lock rufu 0
