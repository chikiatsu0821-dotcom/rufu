playsound minecraft:entity.fox.aggro master @a ~ ~ ~ 1 1.4
function rufu:m4/fox_blink
tellraw @a[tag=rufu_p,distance=..12] {text:"ひらりとかわされた！ 2人以上で囲んで動きを止めよう",color:"gray"}
