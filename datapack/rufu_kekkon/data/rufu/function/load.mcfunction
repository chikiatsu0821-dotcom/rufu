scoreboard objectives add rufu dummy
scoreboard objectives add rufu.t dummy
scoreboard objectives add rufu.id dummy
scoreboard objectives add rufu.pi dummy
scoreboard objectives add rufu.role dummy
scoreboard objectives add rufu.d dummy
scoreboard objectives add rufu.bt dummy
scoreboard objectives add rufu.fz dummy
scoreboard objectives add rufu.death deathCount
scoreboard objectives add rufu.use minecraft.used:minecraft.carrot_on_a_stick
scoreboard objectives add rufu.judge trigger
scoreboard objectives add rufu.side dummy
scoreboard objectives add rufu.hp dummy
scoreboard players set #c2 rufu 2
scoreboard players set #c3 rufu 3
scoreboard players set #c5 rufu 5
scoreboard players set #c10 rufu 10
scoreboard players set #c20 rufu 20
scoreboard players set #c60 rufu 60
scoreboard players set #c100 rufu 100
scoreboard players set #c1000 rufu 1000
bossbar add rufu:love {text:"♥ 好感度"}
bossbar set rufu:love color pink
bossbar set rufu:love style notched_10
bossbar set rufu:love max 100
bossbar add rufu:time {text:"⏱ 残り時間"}
bossbar set rufu:time color yellow
bossbar add rufu:out {text:"アウトゲージ"}
bossbar set rufu:out color red
bossbar set rufu:out max 200
bossbar set rufu:out style notched_20
bossbar add rufu:build {text:"町を建設中…"}
bossbar set rufu:build color green
team add rufu_bread
team add rufu_cake
team add rufu_meat
team add rufu_npc
team modify rufu_bread suffix {text:" 【パン担当】",color:"gold",bold:true}
team modify rufu_cake suffix {text:" 【ケーキ担当】",color:"light_purple",bold:true}
team modify rufu_meat suffix {text:" 【お肉担当】",color:"red",bold:true}
team modify rufu_bread color gold
team modify rufu_cake color light_purple
team modify rufu_meat color red
team modify rufu_npc collisionRule never
function rufu:const/steps
execute unless score #init rufu matches 1 run function rufu:init
tellraw @a {text:"",extra:[{text:"💍 [恋 結婚の試練] ",color:"light_purple",bold:true},{text:"データパックを読み込みました。 ",color:"white"},{text:"[町を建設する]",color:"green",underlined:true,click_event:{action:"run_command",command:"/function rufu:setup"},hover_event:{action:"show_text",value:{text:"/function rufu:setup"}}},{text:" ",color:"white"},{text:"[メニュー]",color:"aqua",underlined:true,click_event:{action:"run_command",command:"/function rufu:menu"},hover_event:{action:"show_text",value:{text:"/function rufu:menu"}}}]}
