execute if entity @s[tag=rufu_hit_heroine] as @a[tag=rufu_clicker,limit=1] run return run function rufu:click/heroine
execute if entity @s[tag=rufu_ask] as @a[tag=rufu_clicker,limit=1] run return run function rufu:annoy/ask_click
execute if entity @s[tag=rufu_sign_hit] as @a[tag=rufu_clicker,limit=1] run return run function rufu:m4/sign_click
execute if entity @s[tag=rufu_girl_hit] run return run function rufu:end/girl_pre
execute if entity @s[tag=rufu_sel_hit] run return run function rufu:hall/sel_pre
execute if entity @s[tag=rufu_hit_q] as @a[tag=rufu_clicker,limit=1] run return run function rufu:hall/q_click
