"""Isometric preview of the generated town (for checking the build)."""
import sys
from PIL import Image, ImageDraw

import town
from render import color
from layout import AREA, G


def main(out="town_iso.png", s=3, region=None):
    w = town.build()
    x0, z0, x1, z1 = region or AREA
    vox = {}
    for (x, y, z), st in w.b.items():
        if x0 <= x <= x1 and z0 <= z <= z1 and y >= G - 6:
            vox[(x, y, z)] = st
    # ground surface defaults
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if (x, G, z) not in vox:
                vox[(x, G, z)] = "grass_block"
    solid = {k: v for k, v in vox.items() if v != "air"}

    def exposed(x, y, z):
        for d in ((0, 1, 0), (1, 0, 0), (0, 0, 1), (-1, 0, 0), (0, 0, -1)):
            n = (x + d[0], y + d[1], z + d[2])
            nv = vox.get(n)
            if nv is None:
                if n[1] > G:
                    return True
                continue
            if nv == "air" or not town.is_solid(town.bid(nv)):
                return True
        return False

    items = [(k, v) for k, v in solid.items() if exposed(*k)]
    # view from south-east: screen x = (x - z), depth = x + z
    items.sort(key=lambda kv: (kv[0][0] + kv[0][2], kv[0][1]))
    W = ((x1 - x0) + (z1 - z0) + 4) * s * 2
    H = ((x1 - x0) + (z1 - z0)) * s + 80 * s * 2
    img = Image.new("RGB", (W, H), (150, 200, 240))
    dr = ImageDraw.Draw(img)
    ox = (z1 - z0 + 2) * s * 2
    oy = 70 * s * 2

    for (x, y, z), st in items:
        c = color(st)
        if st.startswith("water"):
            c = (60, 110, 220)
        sx = ox + ((x - x0) - (z - z0)) * 2 * s
        sy = oy + ((x - x0) + (z - z0)) * s - (y - G) * 2 * s
        top = [(sx, sy - s), (sx + 2 * s, sy), (sx, sy + s), (sx - 2 * s, sy)]
        left = [(sx - 2 * s, sy), (sx, sy + s), (sx, sy + 3 * s), (sx - 2 * s, sy + 2 * s)]
        right = [(sx, sy + s), (sx + 2 * s, sy), (sx + 2 * s, sy + 2 * s), (sx, sy + 3 * s)]
        dr.polygon(top, fill=c)
        dr.polygon(left, fill=tuple(int(v * 0.72) for v in c))
        dr.polygon(right, fill=tuple(int(v * 0.85) for v in c))
    img.save(out)
    print("saved", out, img.size)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "town_iso.png"
    s = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    region = tuple(map(int, sys.argv[3].split(","))) if len(sys.argv) > 3 else None
    main(out, s, region)
