execute as @a unless score @s rufu.id matches 1.. run function rufu:menu/newid
tellraw @s {text:"━━━━━ 👥 役割メニュー ━━━━━",color:"aqua",bold:true}
tellraw @s {text:"主人公＝ドッキリのターゲット(1人)／助っ人＝協力プレイヤー(2人)／GM＝るふ（リモコン操作）",color:"gray"}
tellraw @s {text:"※ひとりでテストするときは、GMのまま自分を[主人公]にしてもOK",color:"dark_gray"}
execute as @a run function rufu:menu/line
tellraw @s {text:"",extra:[{text:"[✅ 準備完了 → スタート地点へ]",color:"green",bold:true,click_event:{action:"run_command",command:"/function rufu:show/prepare"},hover_event:{action:"show_text",value:{text:"全員を主人公の家の前に集めて、最初の状態にします"}}},{text:" "},{text:"[🔄 一覧を更新]",color:"aqua",click_event:{action:"run_command",command:"/function rufu:menu/list"}}]}
