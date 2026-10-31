execute at @e[type=mannequin,tag=rufu_npc_sakura] run particle minecraft:large_smoke ~ ~1 ~ 0.5 1 0.5 0.05 60 force
execute at @e[type=mannequin,tag=rufu_npc_mio] run particle minecraft:large_smoke ~ ~1 ~ 0.5 1 0.5 0.05 60 force
execute at @e[type=mannequin,tag=rufu_npc_hinata] run particle minecraft:large_smoke ~ ~1 ~ 0.5 1 0.5 0.05 60 force
execute as @a at @s run playsound minecraft:entity.illusioner.cast_spell master @s ~ ~ ~ 1 1.0
execute as @a at @s run playsound minecraft:entity.evoker.prepare_summon master @s ~ ~ ~ 1 1.2
