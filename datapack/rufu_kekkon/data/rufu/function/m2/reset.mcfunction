fill 172 64 146 175 64 160 minecraft:farmland[moisture=7] strict
fill 172 65 146 175 65 160 minecraft:wheat[age=7] strict
fill 177 64 146 181 64 160 minecraft:farmland[moisture=7] strict
fill 177 65 146 181 65 160 minecraft:wheat[age=7] strict
fill 183 64 146 186 64 160 minecraft:farmland[moisture=7] strict
fill 183 65 146 186 65 160 minecraft:wheat[age=7] strict
fill 189 65 146 189 67 160 minecraft:sugar_cane strict
fill 191 65 146 191 67 160 minecraft:sugar_cane strict
kill @e[tag=rufu_farm]
kill @e[type=item,x=170,y=55,z=128,dx=60,dy=30,dz=70]
summon minecraft:cow 200.5 65 150.5 {Tags:["rufu_farm"],PersistenceRequired:true,Age:0}
summon minecraft:cow 204.5 65 153.5 {Tags:["rufu_farm"],PersistenceRequired:true,Age:0}
summon minecraft:cow 207.5 65 149.5 {Tags:["rufu_farm"],PersistenceRequired:true,Age:0}
summon minecraft:pig 201.5 65 166.5 {Tags:["rufu_farm"],PersistenceRequired:true,Age:0}
summon minecraft:pig 206.5 65 168.5 {Tags:["rufu_farm"],PersistenceRequired:true,Age:0}
setblock 185 65 172 minecraft:air strict
setblock 185 65 172 minecraft:chest[facing=west]{Items:[{Slot:11b,id:"minecraft:bucket",count:3},{Slot:15b,id:"minecraft:egg",count:3}],CustomName:{text:"バケツと卵",color:"dark_green"}} strict
setblock 173 65 172 minecraft:air strict
setblock 173 65 172 minecraft:furnace[facing=east]{Items:[{Slot:1b,id:"minecraft:coal",count:16}]} strict
setblock 173 65 174 minecraft:air strict
setblock 173 65 174 minecraft:furnace[facing=east]{Items:[{Slot:1b,id:"minecraft:coal",count:16}]} strict
setblock 173 65 176 minecraft:air strict
setblock 173 65 176 minecraft:furnace[facing=east]{Items:[{Slot:1b,id:"minecraft:coal",count:16}]} strict
setblock 149 65 112 minecraft:air strict
setblock 149 65 112 minecraft:furnace[facing=east]{Items:[{Slot:1b,id:"minecraft:coal",count:16}]} strict
setblock 149 65 113 minecraft:air strict
setblock 149 65 113 minecraft:smoker[facing=east]{Items:[{Slot:1b,id:"minecraft:coal",count:16}]} strict
