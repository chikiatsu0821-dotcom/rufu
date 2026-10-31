tp @e[type=marker,tag=rufu_wpm] 86.5 65 136.5
scoreboard players set #spd rufu 6
scoreboard players set #mode rufu 0
scoreboard players set #pause rufu 0
summon minecraft:creeper 86.5 65 145.0 {Tags:["rufu_mob"],PersistenceRequired:true,ExplosionRadius:2b}
tellraw @a[tag=rufu_p] {text:"💥 クリーパー注意！",color:"green"}
execute as @r[tag=rufu_p,gamemode=!spectator] at @s run function rufu:m3/lightning
