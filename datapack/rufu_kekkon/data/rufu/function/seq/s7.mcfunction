execute if score #seq_t rufu matches 30 run function rufu:seq/s7/t30
execute if score #seq_t rufu matches 130 run function rufu:seq/s7/t130
execute if score #seq_t rufu matches 150 run tellraw @a[tag=rufu_p] {text:"🍞 材料は町はずれの農場（東）とパン屋に。小麦畑・サトウキビ・牛・豚・かまど・バケツと卵のチェスト",color:"yellow"}
execute if score #seq_t rufu matches 200 run function rufu:seq/s7/t200
execute if score #seq_t rufu matches 200.. run scoreboard players set #seq rufu 0
