bossbar set rufu:build visible false
kill @e[type=item]
kill @e[tag=rufu_deco]
summon minecraft:villager 41.5 65 117.5 {Tags:["rufu_deco"],NoAI:true,Silent:true,Invulnerable:true,PersistenceRequired:true,Rotation:[0.0f,0.0f],VillagerData:{profession:"minecraft:farmer",type:"minecraft:plains",level:2}}
summon minecraft:villager 44.5 65 125.5 {Tags:["rufu_deco"],NoAI:true,Silent:true,Invulnerable:true,PersistenceRequired:true,Rotation:[180.0f,0.0f],VillagerData:{profession:"minecraft:librarian",type:"minecraft:plains",level:2}}
summon minecraft:villager 57.5 65 117.5 {Tags:["rufu_deco"],NoAI:true,Silent:true,Invulnerable:true,PersistenceRequired:true,Rotation:[0.0f,0.0f],VillagerData:{profession:"minecraft:cleric",type:"minecraft:plains",level:2}}
summon minecraft:villager 60.5 65 125.5 {Tags:["rufu_deco"],NoAI:true,Silent:true,Invulnerable:true,PersistenceRequired:true,Rotation:[180.0f,0.0f],VillagerData:{profession:"minecraft:butcher",type:"minecraft:plains",level:2}}
summon minecraft:villager 73.5 65 117.5 {Tags:["rufu_deco"],NoAI:true,Silent:true,Invulnerable:true,PersistenceRequired:true,Rotation:[0.0f,0.0f],VillagerData:{profession:"minecraft:fisherman",type:"minecraft:plains",level:2}}
summon minecraft:villager 76.5 65 125.5 {Tags:["rufu_deco"],NoAI:true,Silent:true,Invulnerable:true,PersistenceRequired:true,Rotation:[180.0f,0.0f],VillagerData:{profession:"minecraft:shepherd",type:"minecraft:plains",level:2}}
summon minecraft:villager 89.5 65 117.5 {Tags:["rufu_deco"],NoAI:true,Silent:true,Invulnerable:true,PersistenceRequired:true,Rotation:[0.0f,0.0f],VillagerData:{profession:"minecraft:fletcher",type:"minecraft:plains",level:2}}
summon minecraft:villager 92.5 65 125.5 {Tags:["rufu_deco"],NoAI:true,Silent:true,Invulnerable:true,PersistenceRequired:true,Rotation:[180.0f,0.0f],VillagerData:{profession:"minecraft:toolsmith",type:"minecraft:plains",level:2}}
summon minecraft:villager 150.5 65 116.5 {Tags:["rufu_deco"],NoAI:true,Silent:true,Invulnerable:true,PersistenceRequired:true,Rotation:[90.0f,0.0f],VillagerData:{profession:"minecraft:farmer",type:"minecraft:plains",level:2}}
summon minecraft:villager 112.5 65 108.5 {Tags:["rufu_deco"],NoAI:true,Silent:true,Invulnerable:true,PersistenceRequired:true,Rotation:[-45.0f,0.0f],VillagerData:{profession:"minecraft:cleric",type:"minecraft:plains",level:2}}
summon minecraft:villager 146.5 65 132.5 {Tags:["rufu_deco"],NoAI:true,Silent:true,Invulnerable:true,PersistenceRequired:true,Rotation:[135.0f,0.0f],VillagerData:{profession:"minecraft:librarian",type:"minecraft:plains",level:2}}
summon minecraft:villager 176.5 65 141.5 {Tags:["rufu_deco"],NoAI:true,Silent:true,Invulnerable:true,PersistenceRequired:true,Rotation:[0.0f,0.0f],VillagerData:{profession:"minecraft:farmer",type:"minecraft:plains",level:2}}
summon minecraft:villager 190.5 65 135.5 {Tags:["rufu_deco"],NoAI:true,Silent:true,Invulnerable:true,PersistenceRequired:true,Rotation:[90.0f,0.0f],VillagerData:{profession:"minecraft:shepherd",type:"minecraft:plains",level:2}}
summon minecraft:villager 126.5 65 194.5 {Tags:["rufu_deco"],NoAI:true,Silent:true,Invulnerable:true,PersistenceRequired:true,Rotation:[180.0f,0.0f],VillagerData:{profession:"minecraft:mason",type:"minecraft:plains",level:2}}
summon minecraft:villager 60.5 65 84.5 {Tags:["rufu_deco"],NoAI:true,Silent:true,Invulnerable:true,PersistenceRequired:true,Rotation:[0.0f,0.0f],VillagerData:{profession:"minecraft:librarian",type:"minecraft:plains",level:2}}
summon minecraft:villager 140.5 65 88.5 {Tags:["rufu_deco"],NoAI:true,Silent:true,Invulnerable:true,PersistenceRequired:true,Rotation:[0.0f,0.0f],VillagerData:{profession:"minecraft:cleric",type:"minecraft:plains",level:2}}
summon minecraft:cat 70.5 65 145.5 {Tags:["rufu_deco"],PersistenceRequired:true,Invulnerable:true,Sitting:true}
summon minecraft:cat 86.5 65 140.5 {Tags:["rufu_deco"],PersistenceRequired:true,Invulnerable:true,Sitting:true}
summon minecraft:cat 120.5 65 196.5 {Tags:["rufu_deco"],PersistenceRequired:true,Invulnerable:true,Sitting:true}
summon minecraft:cat 58.5 65 70.5 {Tags:["rufu_deco"],PersistenceRequired:true,Invulnerable:true,Sitting:true}
setworldspawn 128 65 235
scoreboard players set #built rufu 1
execute as @a run tp @s 128.5 65 235.5 180 0
tellraw @a {text:"",extra:[{text:"🏰 町が完成しました！ ",color:"green",bold:true},{text:"[役割メニューを開く]",color:"aqua",underlined:true,click_event:{action:"run_command",command:"/function rufu:menu"},hover_event:{action:"show_text",value:{text:"/function rufu:menu"}}}]}
execute as @a at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
