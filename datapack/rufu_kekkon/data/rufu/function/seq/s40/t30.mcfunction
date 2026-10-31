ride @e[type=mannequin,tag=rufu_clone1,limit=1] mount @e[type=happy_ghast,tag=rufu_ghast,limit=1]
ride @e[type=mannequin,tag=rufu_clone2,limit=1] mount @e[type=happy_ghast,tag=rufu_ghast,limit=1]
ride @e[type=mannequin,tag=rufu_clone3,limit=1] mount @e[type=happy_ghast,tag=rufu_ghast,limit=1]
tag @e[type=mannequin,tag=rufu_clone] remove rufu_look
execute at @e[type=happy_ghast,tag=rufu_ghast] run particle minecraft:heart ~ ~2 ~ 1.5 1 1.5 0 20 force
