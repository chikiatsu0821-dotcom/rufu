bossbar set rufu:love players @a
bossbar set rufu:love visible true
function rufu:hud/love
scoreboard objectives add rufu.side dummy
scoreboard objectives modify rufu.side displayname {text:"💍 結婚の試練",color:"light_purple",bold:true}
scoreboard objectives setdisplay sidebar rufu.side
scoreboard players display name retry rufu.side {text:"リトライ回数",color:"red"}
scoreboard players display name trial rufu.side {text:"試練",color:"gold"}
scoreboard objectives modify rufu.side numberformat styled {color:"white",bold:true}
function rufu:hud/side
