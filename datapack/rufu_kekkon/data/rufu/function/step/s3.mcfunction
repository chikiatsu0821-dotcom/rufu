scoreboard players set #step rufu 3
data modify storage rufu:hud now set value "3. 「結婚したければ、4つの試練をクリアして。」＋ルール看板"
data modify storage rufu:hud next set value "4. 試練1 説明「私より早く広場に来て」"
scoreboard players set #seq rufu 0
tellraw @a[tag=rufu_gm] {text:"[GM] ▶ 3. 「結婚したければ、4つの試練をクリアして。」＋ルール看板",color:"dark_green"}
execute as @e[type=text_display,tag=rufu_bub_heroine] run data merge entity @s {text:{text:"結婚したければ、4つの試練をクリアして。",color:"#7a1f5c"},background:-503321354}
scoreboard players set @e[type=text_display,tag=rufu_bub_heroine] rufu.bt 100
tellraw @a {text:"",extra:[{text:"ヒロイン",color:"light_purple",bold:true},{text:"「結婚したければ、4つの試練をクリアして。」",color:"white"}]}
title @a times 3 90 8
title @a subtitle {text:"",extra:[{text:"ヒロイン：",color:"light_purple",bold:true},{text:"「結婚したければ、4つの試練をクリアして。」",color:"white"}]}
title @a title {text:"結婚したければ、4つの試練をクリアして。",color:"light_purple",bold:true}
execute as @e[tag=rufu_npc_heroine] at @s run playsound minecraft:entity.allay.ambient_without_item voice @a ~ ~ ~ 1.4 1.25
kill @e[tag=rufu_rules]
summon minecraft:text_display 128.5 67.6 232.0 {Tags:["rufu_rules","rufu_stage"],billboard:"vertical",text:{text:"",extra:[{text:"💍 結婚の試練 ルール 💍\n",color:"light_purple",bold:true},{text:"結婚したければ、4つの試練をクリアして。\n\n",color:"white",bold:true},{text:"・3人全員がクリア条件を満たすこと\n",color:"white"},{text:"・1人でも失敗 → 3人そろって最初から\n",color:"white"},{text:"・好感度は100から。0になってもやり直し\n",color:"white"},{text:"・どの試練にも制限時間あり\n",color:"white"},{text:"・雷・金床・クリーパー・モブは本当に痛い\n",color:"red"},{text:"・誰か死んだら そのミッションは失敗\n",color:"red"},{text:"・持ち物は消えない（その試練で集めた物は没収）\n",color:"white"},{text:"・クリアすると評価が出る（理由は聞かないで）",color:"gray"}]},background:-769127906,line_width:260,alignment:"left",transformation:{translation:[0.0f,0.0f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.6f,1.6f,1.6f]}}
execute at @e[tag=rufu_rules] run particle minecraft:end_rod ~ ~1 ~ 1.5 1.2 0.2 0 40 force
execute as @a at @s run playsound minecraft:ui.toast.in master @s ~ ~ ~ 1 1
tellraw @a {text:"",extra:[{text:"▶ ",color:"gray"},{text:"ルール看板が立った！",color:"yellow"}]}
function rufu:hud/show
scoreboard players set #love rufu 100
function rufu:hud/love
execute as @a[tag=rufu_p] run function rufu:op/_41
tellraw @a[tag=rufu_p] {text:"✂ 「花ばさみ」をもらった。町の花をつんでヒロインに右クリックで渡すと 好感度+20（各試練1回）",color:"light_purple"}
scoreboard players set #seq_t rufu 0
scoreboard players set #seq rufu 3
