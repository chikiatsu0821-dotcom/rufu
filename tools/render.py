"""Render a top-down preview (and an oblique view) of the generated town."""
import sys
from PIL import Image, ImageDraw

import town
from layout import AREA, G

COL = [
    ("water", (60, 110, 220)), ("stone_brick", (130, 130, 130)), ("flower", (230, 120, 200)), ("poppy", (220, 40, 40)), ("dandelion", (240, 220, 40)), ("tulip", (240, 120, 160)), ("bluet", (200, 200, 255)), ("allium", (180, 100, 220)), ("cornflower", (90, 120, 240)), ("daisy", (240, 240, 240)), ("lily_of", (240, 240, 240)), ("lava", (240, 110, 20)), ("magma", (200, 80, 20)),
    ("poplar_leaves", (235, 190, 40)), ("cherry_leaves", (240, 160, 200)), ("leaves", (60, 130, 50)),
    ("copper", (80, 170, 140)), ("deepslate_tile", (60, 60, 70)), ("brick", (160, 70, 55)),
    ("nether_brick", (90, 30, 35)), ("mud_brick", (150, 110, 80)), ("granite", (170, 110, 90)),
    ("dark_oak", (70, 50, 30)), ("spruce", (110, 80, 50)), ("oak", (160, 130, 80)), ("poplar", (180, 160, 120)),
    ("wheat", (220, 200, 90)), ("farmland", (110, 70, 40)), ("sugar_cane", (140, 200, 100)),
    ("dirt_path", (170, 140, 90)), ("coarse_dirt", (120, 90, 60)), ("packed_mud", (140, 110, 80)),
    ("rooted_dirt", (130, 100, 70)), ("grass_block", (100, 170, 70)), ("dirt", (130, 95, 60)),
    ("tuff", (100, 105, 95)), ("cracked", (230, 40, 40)), ("hay", (210, 180, 60)),
    ("wool", (220, 220, 220)), ("terracotta", (200, 160, 130)), ("calcite", (230, 230, 225)),
    ("shroomlight", (255, 170, 60)), ("obsidian", (40, 20, 60)), ("portal", (150, 60, 220)),
    ("stone_brick", (130, 130, 130)), ("andesite", (140, 140, 140)), ("diorite", (210, 210, 210)),
    ("cobble", (115, 115, 115)), ("stone", (120, 120, 120)), ("gravel", (135, 125, 120)), ("sand", (220, 210, 160)),
    ("glass", (180, 220, 240)), ("carpet", (200, 30, 30)), ("lantern", (255, 220, 120)),
]


def color(state):
    for k, c in COL:
        if k in state:
            return c
    return (180, 180, 180)


def main(out="town_top.png", scale=4):
    w = town.build()
    x0, z0, x1, z1 = AREA
    img = Image.new("RGB", ((x1 - x0 + 1) * scale, (z1 - z0 + 1) * scale), (30, 30, 30))
    dr = ImageDraw.Draw(img)
    cols = {}
    for (x, y, z), s in w.b.items():
        if s == "air":
            continue
        k = (x, z)
        if k not in cols or cols[k][0] < y:
            cols[k] = (y, s)
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            # walk down from top to find the first non-air block
            top = cols.get((x, z))
            if top and top[0] >= G:
                y, s = top
            else:
                y = G
                s = w.get(x, G, z)
                while s == "air" and y > 40:
                    y -= 1
                    s = w.get(x, y, z)
            c = color(s)
            shade = max(0.55, min(1.4, 1 + (y - G) * 0.025))
            c = tuple(min(255, int(v * shade)) for v in c)
            dr.rectangle([(x - x0) * scale, (z - z0) * scale, (x - x0 + 1) * scale - 1, (z - z0 + 1) * scale - 1], fill=c)
    img.save(out)
    print("saved", out)


if __name__ == "__main__":
    main(*(sys.argv[1:2] or []))
