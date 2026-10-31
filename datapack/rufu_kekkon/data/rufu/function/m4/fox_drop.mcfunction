summon minecraft:item ~ ~0.6 ~ {Item:{id:"minecraft:gold_nugget",count:1,components:{custom_name:{text:"💍 婚約指輪",color:"gold",bold:true,italic:false},lore:[{text:"ヒロインに渡すための指輪。",color:"gray",italic:false},{text:"キツネの大好物ではない。",color:"gray",italic:false}],custom_data:{rufu_ring:1b,rufu_m:1b},enchantment_glint_override:true}},PickupDelay:10s,Age:-32768s,Motion:[0.0d,0.35d,0.0d],Tags:["rufu_ringitem","rufu_keep"],Glowing:true}
playsound minecraft:entity.fox.spit master @a ~ ~ ~ 1 1
playsound minecraft:entity.player.levelup master @a ~ ~ ~ 1 1.6
particle minecraft:end_rod ~ ~0.8 ~ 0.3 0.3 0.3 0.05 20 force
title @a[tag=rufu_p] times 5 50 10
title @a[tag=rufu_p] subtitle {text:"主人公が持って、3人全員で光る円へ！",color:"white"}
title @a[tag=rufu_p] title {text:"指輪を取り返した！",color:"gold",bold:true}
execute at @e[tag=rufu_fox] run particle minecraft:poof ~ ~0.4 ~ 0.3 0.3 0.3 0.02 12 force
kill @e[tag=rufu_fox]
scoreboard players set #m4p rufu 1
