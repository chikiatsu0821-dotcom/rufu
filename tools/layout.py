"""All key coordinates of the town.  x = east, z = south, y = up.

Ground top block is y=64, so players stand at y=65 on streets.
"""

G = 64            # ground top block
W = 65            # walking level (feet)

# whole build area (forceloaded)
AREA = (8, 16, 247, 255)          # x0, z0, x1, z1
BASE_Y0 = 48                       # bottom of the generated island

# ---------------------------------------------------------------- walls
OW = dict(x0=32, x1=223, z0=48, z1=207, t=3, top=76)       # outer wall
MOAT = dict(x0=25, x1=230, z0=41, z1=214, y0=60, y1=63)    # water ring
RIM = dict(x0=24, x1=231, z0=40, z1=215)                   # tuff brick rim
GATE_S = dict(x0=126, x1=130, y0=65, y1=70)                # south gate opening
BRIDGE = dict(x0=126, x1=130, z0=208, z1=214, y=64)        # drawbridge deck
POSTERN = dict(x=117, y0=65, y1=66)                        # small side door

# ---------------------------------------------------------------- mission 1
HOUSE = dict(x0=120, x1=136, z0=238, z1=248)
M1_START = (128.5, 65, 235.5)       # facing north
PICK_POS = (124, 65, 235)           # pedestal block, item floats above
BARREL_POS = (139, 65, 235)
CORRIDOR = dict(x0=116, x1=140, z0=216, z1=237)
PIT = dict(x0=116, z0=218, cols=8, rows=5, size=3)         # 3x3 hidden pits
GATE_SQ = dict(x0=112, x1=144, z0=191, z1=204)
RING_ROAD = dict(z0=197, z1=204, x0=35, x1=220)
ROOF_HOUSES = [  # x0,x1,z0,z1,yt
    (123, 133, 181, 190, 69),
    (123, 133, 167, 176, 70),
    (123, 133, 154, 162, 69),
]
ALLEYS = [(118, 133, 177, 180), (118, 133, 163, 166)]       # x0,x1,z0,z1
LANE_E = (134, 136, 163, 191)
STRIP = dict(x0=121, x1=135, z0=151, z1=153)
PATCH = dict(x0=126, x1=130, y0=65, y1=67, z0=149, z1=150)  # cracked bricks

# ---------------------------------------------------------------- old town
IW = dict(x0=96, x1=160, z0=92, z1=150, top=72)             # inner wall (2 thick)
PC = (128, 121)                                             # plaza centre
PLAZA_R = 17
FOUNTAIN_R = 5
HEROINE_FOUNTAIN = (128.5, 65, 128.5)                       # where she waits
M1_GOAL_R = 9

MAIN_W = dict(x0=35, x1=95, z0=117, z1=125)
MAIN_E = dict(x0=161, x1=220, z0=117, z1=125)
NS_W = dict(x0=88, x1=94, z0=126, z1=196)
NS_E = dict(x0=162, x1=168, z0=126, z1=196)

# ---------------------------------------------------------------- park & alleys
PARK = dict(x0=35, x1=92, z0=51, z1=98)
PARK_C = (64, 76)
PARK_LANE = dict(x0=60, x1=64, z0=99, z1=116)
BACK_ALLEYS = [  # x0,x1,z0,z1  (dark back streets for the night lap)
    (49, 51, 126, 161),
    (49, 87, 159, 161),
    (85, 87, 135, 161),
    (49, 87, 135, 137),
    (62, 64, 126, 134),
    (79, 81, 126, 134),
]

# ---------------------------------------------------------------- church
CHURCH = dict(x0=120, x1=136, z0=58, z1=80, yt=76)           # nave
TOWER = dict(x0=123, x1=133, z0=81, z1=89)
CHURCH_DOOR = dict(x0=127, x1=129, z=89)
ALTAR = (128.5, 66, 60.5)
WED_HERO = (127.5, 66, 63.5)
WED_HEROINE = (129.5, 66, 63.5)
SEATS = [(124.5, 65.5, 66.5), (132.5, 65.5, 66.5)]
ROOF_HOLE = dict(x0=124, x1=132, z0=68, z1=74)
PORTAL = dict(x0=150, x1=153, y0=65, y1=69, z=60)
LANE_N = dict(x0=98, x1=166, z0=90, z1=91)

# ---------------------------------------------------------------- hill
HILL_C = (195, 80)
HILL_TOP = 80                # plateau top block, stand at 81
HILL_R_TOP = 13
HILL_R_BASE = 27
TREE = (195, 79)             # trunk 2x2 from this corner
CIRCLE = (195.5, 81, 89.5)
CIRCLE_R = 4.5
TREASURES = [(185, 72), (205, 73), (186, 89)]
RAMP = dict(x0=194, x1=196)

# ---------------------------------------------------------------- farm
FARM = dict(x0=170, x1=220, z0=128, z1=196)
WHEAT = dict(x0=172, x1=186, z0=146, z1=160, water=(176, 182))
CANE = dict(x=190, z0=146, z1=160)
COW_PEN = dict(x0=196, x1=210, z0=146, z1=158)
PIG_PEN = dict(x0=196, x1=210, z0=162, z1=172)
BARN = dict(x0=172, x1=186, z0=168, z1=184)

import random as _r
_pr = _r.Random(7)
PIT_SURF = [[_pr.choice(["coarse_dirt", "packed_mud", "rooted_dirt"]) for r in range(5)] for c in range(8)]

# ---------------------------------------------------------------- selection hall (prologue)
HALL = dict(x0=14, x1=50, z0=220, z1=254, y0=64, y1=81)
HALL_CX = 32
STAGE = dict(x0=15, x1=49, z0=221, z1=229)          # top block y=65 -> stand 66
HALL_GIRLS = [  # key, x, z, stand y
    ("sakura", 23.5, 225.5, 66),
    ("mio", 28.5, 225.5, 66),
    ("hinata", 36.5, 225.5, 66),
    ("q", 41.5, 225.5, 67),
]
HALL_PLAYERS = (32.5, 65, 246.5)
HALL_ANVIL = (46, 65, 244)
HALL_HEROINE = (32.5, 66, 226.5)
NAMEBOX = (32.5, 70, 240.5)
