tp @e[type=marker,tag=rufu_wpm] 80.5 65 129.5
scoreboard players set #spd rufu 5
scoreboard players set #mode rufu 0
scoreboard players set #pause rufu 0
execute as @e[type=text_display,tag=rufu_bub_heroine] run data merge entity @s {text:{text:"こっち！",color:"#7a1f5c"},background:-503321354}
scoreboard players set @e[type=text_display,tag=rufu_bub_heroine] rufu.bt 60
tellraw @a {text:"",extra:[{selector:"@e[type=marker,tag=rufu_namebox,limit=1]",color:"light_purple",bold:true},{text:"",color:"light_purple",bold:true},{text:"「こっち！」",color:"white"}]}
execute as @e[tag=rufu_npc_heroine] at @s run playsound minecraft:entity.allay.ambient_without_item voice @a ~ ~ ~ 1.4 1.25
summon minecraft:creeper 80.5 65 133.5 {Tags:["rufu_mob"],PersistenceRequired:true,ExplosionRadius:2b}
tellraw @a[tag=rufu_p] {text:"💥 クリーパー注意！",color:"green"}
