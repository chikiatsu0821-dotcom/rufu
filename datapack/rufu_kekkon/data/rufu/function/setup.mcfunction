tellraw @a {text:"💍 町を建設します。少し重くなります（数十秒）…",color:"light_purple"}
gamerule keep_inventory true
gamerule advance_time false
gamerule advance_weather false
gamerule spawn_mobs false
gamerule spawn_monsters false
gamerule mob_griefing false
gamerule fire_spread_radius_around_player 0
gamerule command_block_output false
gamerule show_advancement_messages false
gamerule immediate_respawn true
gamerule allow_entering_nether_using_portals false
gamerule spawn_phantoms false
gamerule spawn_wandering_traders false
gamerule spawn_patrols false
gamerule raids false
gamerule max_block_modifications 1000000
gamerule players_sleeping_percentage 101
difficulty normal
time set 1000
weather clear
forceload add 8 16 247 255
kill @e[tag=rufu_deco]
kill @e[tag=rufu_npc]
kill @e[tag=rufu_npcpart]
bossbar set rufu:build max 98
bossbar set rufu:build value 0
bossbar set rufu:build players @a
bossbar set rufu:build visible true
execute as @a run tp @s 128.5 110 235.5
effect give @a minecraft:slow_falling 30 0 true
schedule function rufu:build/p0 20t
