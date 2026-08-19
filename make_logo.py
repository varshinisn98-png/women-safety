# -*- coding: utf-8 -*-
"""
Generate a beautiful aesthetic logo for Suraksha Safety Platform.
Design: Glowing shield with a female silhouette, crown of stars,
purple-to-pink-to-cyan gradient — perfectly matching the app theme.
Output: frontend/assets/logo.png  (512x512 + 128x128 favicon)
"""
import os, math
from PIL import Image, ImageDraw, ImageFilter, ImageChops

SIZE = 512
W, H = SIZE, SIZE
out_dir = "frontend/assets"
os.makedirs(out_dir, exist_ok=True)

# ── Color palette (matches app CSS variables) ────────────────────────────────
C_BG        = (5,   1,  15, 0)     # transparent
C_PURPLE    = (139, 92, 246)
C_PINK      = (236, 72, 153)
C_CYAN      = (6,  182, 212)
C_WHITE     = (255, 255, 255)
C_LIGHT_PUR = (196, 181, 253)
C_DEEP_PUR  = (91,  33, 182)

def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i]-c1[i])*t) for i in range(3))

def rgba(rgb, a):
    return (*rgb, a)

def draw_gradient_rect(img, x0, y0, x1, y1, c1, c2, alpha=255):
    """Vertical gradient fill on a temp layer."""
    layer = Image.new("RGBA", (x1-x0, y1-y0), (0,0,0,0))
    d = ImageDraw.Draw(layer)
    for y in range(y1-y0):
        t = y / max(1, y1-y0-1)
        col = lerp_color(c1, c2, t) + (alpha,)
        d.line([(0,y),(x1-x0,y)], fill=col)
    img.alpha_composite(layer, (x0, y0))

# ── Glow helper: draw shape on layer then blur + composite ───────────────────
def glow_layer(size, draw_fn, blur_radius=18, alpha_scale=0.7):
    layer = Image.new("RGBA", (size, size), (0,0,0,0))
    d = ImageDraw.Draw(layer)
    draw_fn(d)
    r, g, b, a = layer.split()
    a = a.point(lambda x: int(x * alpha_scale))
    layer = Image.merge("RGBA", (r, g, b, a))
    return layer.filter(ImageFilter.GaussianBlur(blur_radius))

# ────────────────────────────────────────────────────────────────────────────
# BUILD LOGO
# ────────────────────────────────────────────────────────────────────────────
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

# ── 1. Outer glow aura ───────────────────────────────────────────────────────
aura = Image.new("RGBA", (W, H), (0,0,0,0))
ad = ImageDraw.Draw(aura)
ad.ellipse([64, 64, W-64, H-64], fill=rgba(C_PURPLE, 60))
aura = aura.filter(ImageFilter.GaussianBlur(40))
img.alpha_composite(aura)

aura2 = Image.new("RGBA", (W, H), (0,0,0,0))
ad2 = ImageDraw.Draw(aura2)
ad2.ellipse([100, 100, W-100, H-100], fill=rgba(C_CYAN, 40))
aura2 = aura2.filter(ImageFilter.GaussianBlur(30))
img.alpha_composite(aura2)

# ── 2. Dark circular background ─────────────────────────────────────────────
bg_layer = Image.new("RGBA", (W, H), (0,0,0,0))
bg_d = ImageDraw.Draw(bg_layer)
# Outer ring gradient stroke
for r in range(240, 248):
    t = (r - 240) / 8.0
    c = lerp_color(C_PURPLE, C_CYAN, t)
    bg_d.ellipse([W//2-r, H//2-r, W//2+r, H//2+r],
                 outline=rgba(c, int(180*(1-t)+80*t)), width=1)
# Inner filled circle
bg_d.ellipse([W//2-236, H//2-236, W//2+236, H//2+236],
             fill=(12, 5, 30, 240))
img.alpha_composite(bg_layer)

# ── 3. Gradient ring (conic-like via many arcs) ──────────────────────────────
ring_layer = Image.new("RGBA", (W, H), (0,0,0,0))
rd = ImageDraw.Draw(ring_layer)
cx, cy, r_ring = W//2, H//2, 238
ring_colors = [C_PURPLE, C_PINK, C_CYAN, C_PURPLE]
steps = 120
for i in range(steps):
    t = i / steps
    seg = t * 3
    idx = int(seg); frac = seg - idx
    c = lerp_color(ring_colors[idx % 3], ring_colors[(idx+1) % 3], frac)
    angle_start = (i / steps) * 360 - 90
    angle_end   = ((i+1) / steps) * 360 - 90
    rd.arc([cx-r_ring, cy-r_ring, cx+r_ring, cy+r_ring],
           start=angle_start, end=angle_end+1,
           fill=rgba(c, 220), width=6)
img.alpha_composite(ring_layer)

# ── 4. Shield shape ──────────────────────────────────────────────────────────
def shield_points(cx, cy, w, h):
    """Pointed shield polygon."""
    hw = w // 2
    return [
        (cx - hw,       cy - h//3),       # top-left
        (cx,            cy - h//2),       # top-center peak
        (cx + hw,       cy - h//3),       # top-right
        (cx + hw,       cy + h//10),      # right shoulder
        (cx + hw//2,    cy + h//3),       # lower-right
        (cx,            cy + h//2),       # bottom tip
        (cx - hw//2,    cy + h//3),       # lower-left
        (cx - hw,       cy + h//10),      # left shoulder
    ]

shield_layer = Image.new("RGBA", (W, H), (0,0,0,0))
sd = ImageDraw.Draw(shield_layer)
scx, scy = W//2, H//2 + 20
sw, sh = 220, 240

pts = shield_points(scx, scy, sw, sh)

# Glow behind shield
glow_s = Image.new("RGBA", (W, H), (0,0,0,0))
gd = ImageDraw.Draw(glow_s)
for offset in range(20, 0, -4):
    alpha = int(30 + offset * 4)
    expanded = [(x + (1 if x > scx else -1)*offset,
                 y + (1 if y > scy else -1)*offset//2)
                for x,y in pts]
    gd.polygon(expanded, fill=rgba(C_PURPLE, alpha))
glow_s = glow_s.filter(ImageFilter.GaussianBlur(12))
img.alpha_composite(glow_s)

# Shield fill — gradient from purple to deep purple
for row in range(sh):
    t = row / sh
    c = lerp_color(C_DEEP_PUR, (20, 8, 50), t)
    # Clip to shield shape using temp image
    pass

# Fill shield with dark purple
sd.polygon(pts, fill=(22, 8, 55, 235))
# Shield border gradient
border_colors = [C_PURPLE, C_PINK, C_CYAN, C_PURPLE]
for i in range(len(pts)):
    t = i / len(pts)
    seg = t * 3; idx = int(seg); frac = seg - idx
    c = lerp_color(border_colors[idx % 3], border_colors[(idx+1)%3], frac)
    p1 = pts[i]; p2 = pts[(i+1) % len(pts)]
    sd.line([p1, p2], fill=rgba(c, 240), width=4)

# Inner shield highlight (top sheen)
sd.polygon([(scx-70, scy-sh//2+10), (scx, scy-sh//2-10),
            (scx+70, scy-sh//2+10), (scx+50, scy-sh//5),
            (scx, scy-sh//4), (scx-50, scy-sh//5)],
           fill=(255,255,255,12))

img.alpha_composite(shield_layer)

# ── 5. Female silhouette inside shield ───────────────────────────────────────
sil = Image.new("RGBA", (W, H), (0,0,0,0))
sild = ImageDraw.Draw(sil)

fc_x, fc_y = scx, scy - 10  # figure center

# Head
head_r = 28
sild.ellipse([fc_x-head_r, fc_y-head_r-60,
              fc_x+head_r, fc_y-60+head_r],
             fill=rgba(C_LIGHT_PUR, 230))

# Hair — arc above head
for i in range(5):
    angle = -180 + i*36
    rad = math.radians(angle)
    hx = fc_x + math.cos(rad)*head_r
    hy = (fc_y - 60) + math.sin(rad)*head_r
    sild.ellipse([hx-6, hy-10, hx+6, hy+6],
                 fill=rgba(C_PURPLE, 200))

# Neck
sild.rectangle([fc_x-8, fc_y-32, fc_x+8, fc_y-16],
               fill=rgba(C_LIGHT_PUR, 200))

# Torso (rounded)
sild.ellipse([fc_x-38, fc_y-20, fc_x+38, fc_y+70],
             fill=rgba(C_PURPLE, 200))

# Dress/skirt flare
sild.polygon([(fc_x-38, fc_y+50), (fc_x-55, fc_y+110),
              (fc_x+55, fc_y+110), (fc_x+38, fc_y+50)],
             fill=rgba(C_PURPLE, 190))

# Arms
sild.ellipse([fc_x-65, fc_y-15, fc_x-38, fc_y+40],
             fill=rgba(C_PURPLE, 170))
sild.ellipse([fc_x+38, fc_y-15, fc_x+65, fc_y+40],
             fill=rgba(C_PURPLE, 170))

# Inner glow on silhouette
sil_glow = sil.filter(ImageFilter.GaussianBlur(8))
img.alpha_composite(sil_glow)
img.alpha_composite(sil)

# ── 6. Stars arc above silhouette ────────────────────────────────────────────
def draw_star_points(cx, cy, r_out, r_in, n=5):
    pts_s = []
    for i in range(n*2):
        angle = math.pi * i / n - math.pi/2
        r = r_out if i % 2 == 0 else r_in
        pts_s.append((cx + r*math.cos(angle), cy + r*math.sin(angle)))
    return pts_s

star_layer = Image.new("RGBA", (W, H), (0,0,0,0))
std = ImageDraw.Draw(star_layer)

star_configs = [
    # (cx_offset from scx, cy, size, color)
    (-90, scy - 175, 14, C_CYAN),
    (-45, scy - 200, 18, C_PINK),
    (  0, scy - 215, 22, C_LIGHT_PUR),
    ( 45, scy - 200, 18, C_PINK),
    ( 90, scy - 175, 14, C_CYAN),
]

for dx, star_y, sz, col in star_configs:
    sp = draw_star_points(scx + dx, star_y, sz, sz*0.42)
    # Glow
    glow_st = Image.new("RGBA", (W, H), (0,0,0,0))
    gd2 = ImageDraw.Draw(glow_st)
    gd2.polygon(sp, fill=rgba(col, 80))
    glow_st = glow_st.filter(ImageFilter.GaussianBlur(10))
    img.alpha_composite(glow_st)
    # Star fill
    std.polygon(sp, fill=rgba(col, 255))
    # Star outline
    std.polygon(sp, outline=rgba(C_WHITE, 120), width=1)

img.alpha_composite(star_layer)

# ── 7. Small dot sparkles ────────────────────────────────────────────────────
sparkles = [
    (W//2-110, H//2-120, 3, C_CYAN),
    (W//2+115, H//2-115, 2, C_PINK),
    (W//2-130, H//2-40,  2, C_PURPLE),
    (W//2+130, H//2-50,  3, C_CYAN),
    (W//2-80,  H//2+130, 2, C_LIGHT_PUR),
    (W//2+90,  H//2+125, 2, C_PINK),
]
spk_layer = Image.new("RGBA", (W, H), (0,0,0,0))
spkd = ImageDraw.Draw(spk_layer)
for sx, sy, sr, sc in sparkles:
    spkd.ellipse([sx-sr*3, sy-sr*3, sx+sr*3, sy+sr*3], fill=rgba(sc, 50))
    spkd.ellipse([sx-sr,   sy-sr,   sx+sr,   sy+sr],   fill=rgba(sc, 255))
spk_layer = spk_layer.filter(ImageFilter.GaussianBlur(2))
img.alpha_composite(spk_layer)

# ── 8. "S" letter mark at shield center bottom ───────────────────────────────
letter_layer = Image.new("RGBA", (W, H), (0,0,0,0))
ld = ImageDraw.Draw(letter_layer)
# Draw a stylized shield emblem: small inner shield outline
inner_pts = shield_points(scx, scy+30, 60, 65)
for i in range(len(inner_pts)):
    t = i / len(inner_pts)
    seg = t*3; idx = int(seg); frac = seg-idx
    c = lerp_color([C_PURPLE, C_PINK, C_CYAN][idx%3],
                   [C_PINK, C_CYAN, C_PURPLE][(idx+1)%3], frac)
    p1 = inner_pts[i]; p2 = inner_pts[(i+1)%len(inner_pts)]
    ld.line([p1, p2], fill=rgba(c, 180), width=2)
img.alpha_composite(letter_layer)

# ── 9. Final soft vignette ───────────────────────────────────────────────────
vig = Image.new("RGBA", (W, H), (0,0,0,0))
vd = ImageDraw.Draw(vig)
for r in range(256, 200, -4):
    alpha = int((256-r) * 1.2)
    vd.ellipse([W//2-r, H//2-r, W//2+r, H//2+r],
               outline=(0,0,0,min(alpha,60)), width=3)
img.alpha_composite(vig)

# ── Save outputs ─────────────────────────────────────────────────────────────
logo_path = os.path.join(out_dir, "logo.png")
icon_path = os.path.join(out_dir, "favicon.png")

img.save(logo_path, "PNG")
print("Logo saved:", logo_path, "(%d bytes)" % os.path.getsize(logo_path))

# 128x128 favicon
favicon = img.resize((128, 128), Image.LANCZOS)
favicon.save(icon_path, "PNG")
print("Favicon saved:", icon_path)
