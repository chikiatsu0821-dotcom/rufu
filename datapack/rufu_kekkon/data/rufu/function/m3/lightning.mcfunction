execute store result score #r rufu run random value 0..3
execute if score #r rufu matches 0 run summon minecraft:lightning_bolt ~3 ~ ~2
execute if score #r rufu matches 1 run summon minecraft:lightning_bolt ~-3 ~ ~1
execute if score #r rufu matches 2 run summon minecraft:lightning_bolt ~2 ~ ~-3
execute if score #r rufu matches 3 run summon minecraft:lightning_bolt ~1 ~ ~2
