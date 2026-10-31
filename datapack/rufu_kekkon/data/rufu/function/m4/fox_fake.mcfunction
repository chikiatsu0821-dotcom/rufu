particle minecraft:explosion ~ ~0.5 ~ 0.3 0.3 0.3 0 3 force
summon minecraft:creeper ~ ~ ~ {Fuse:0s,ignited:true,ExplosionRadius:1b,Tags:["rufu_mob"],Silent:true}
tellraw @a {text:"💥 偽物のキツネだった！",color:"red",bold:true}
kill @s
