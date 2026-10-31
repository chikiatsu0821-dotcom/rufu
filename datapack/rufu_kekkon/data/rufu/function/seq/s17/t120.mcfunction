time set 18000
clear @a minecraft:gold_nugget[custom_data~{rufu_ring:1b}]
summon minecraft:fox 195.5 81 84.5 {Tags:["rufu_fox","rufu_mob4","rufu_demo","rufu_fox_real"],NoAI:true,PersistenceRequired:true,Silent:false,Type:"red",attributes:[{id:"minecraft:max_health",base:1024.0d}],Health:1000.0f,equipment:{mainhand:{id:"minecraft:gold_nugget",count:1,components:{custom_name:{text:"💍 婚約指輪",color:"gold",bold:true,italic:false},lore:[{text:"ヒロインに渡すための指輪。",color:"gray",italic:false},{text:"キツネの大好物ではない。",color:"gray",italic:false}],custom_data:{rufu_ring:1b,rufu_m:1b},enchantment_glint_override:true}}},drop_chances:{mainhand:0.0f}}
execute at @e[tag=rufu_demo] run particle minecraft:poof ~ ~0.5 ~ 0.3 0.3 0.3 0.02 15 force
playsound minecraft:entity.fox.bite master @a 195.5 81 84.5 1 1.2
tellraw @a {text:"🦊 指輪がまたキツネに取られた！",color:"gold",bold:true}
