"""Regenerates src/static/logo-light.webp and logo-dark.webp (not part of the
build; needs: pip install fonttools brotli uharfbuzz pillow numpy). If the output
size changes, update LOGO_SIZE in src/generate.py.

Renders the site logo (green % badge + "Percentage Calculators" wordmark in
DM Sans) to lossless transparent WebP, light and dark variants, at 3x of a
32px-high logo. Text is kerned with HarfBuzz and drawn at 8x then downsampled."""
import os, tempfile
import numpy as np
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = ROOT + "/src/static"
SCRATCH = tempfile.mkdtemp(prefix="logo_fonts_")

H = 32            # logical logo height (css px), same as the old .logo-icon
BADGE_R = 10      # rounded-[10px]
GAP = 10          # gap-2.5
WORD_PX = 16.8    # text-[1.05rem], font-bold
PCT_PX = 14       # text-sm, font-extrabold
SCALE = 3         # output pixel ratio
SS = 8            # supersampling factor
K = SCALE * SS

THEMES = {
    "light": dict(text=(23, 23, 23), a=(22, 163, 74), b=(20, 83, 45)),
    "dark": dict(text=(248, 250, 252), a=(74, 222, 128), b=(22, 163, 74)),
}
WORDMARK = "Percentage Calculators"


def instance(weight):
    font = TTFont(ROOT + "/src/fonts/dm-sans-variable.woff2")
    inst = instancer.instantiateVariableFont(font, {"wght": weight, "opsz": 14} if "opsz" in [a.axisTag for a in font["fvar"].axes] else {"wght": weight})
    inst.flavor = None
    path = f"{SCRATCH}/dmsans-{weight}.ttf"
    inst.save(path)
    return path


def shape(path, text, px):
    """[(glyph_id, x_px)] with kerning, plus total advance and cap height (px)."""
    blob = hb.Blob.from_file_path(path)
    face = hb.Face(blob)
    f = hb.Font(face)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(f, buf, {"kern": True, "liga": False})
    upem = face.upem
    x = 0
    out = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        out.append((info.codepoint, (x + pos.x_offset) * px / upem))
        x += pos.x_advance
    cap = TTFont(path)["OS/2"].sCapHeight * px / upem
    return out, x * px / upem, cap


def draw_glyphs(draw, path, glyphs, px_big, x0, baseline, fill):
    font = ImageFont.truetype(path, size=round(px_big))
    tt = TTFont(path)
    order = tt.getGlyphOrder()
    cmap_rev = {}
    for cp, name in tt.getBestCmap().items():
        cmap_rev.setdefault(name, cp)
    for gid, gx in glyphs:
        ch = chr(cmap_rev[order[gid]])
        draw.text((x0 + gx, baseline), ch, font=font, fill=fill, anchor="ls")


def build(theme):
    c = THEMES[theme]
    bold = instance(700)
    xbold = instance(800)
    word_glyphs, word_w, cap = shape(bold, WORDMARK, WORD_PX * K)
    word_w_css = word_w / K
    total_w_css = H + GAP + word_w_css
    W, HH = int(round(total_w_css * K)) + 2 * K, H * K   # small right pad avoids clipping
    img = Image.new("RGBA", (W, HH), (0, 0, 0, 0))

    # badge: top-left -> bottom-right gradient (bg-gradient-to-br), rounded square
    S = H * K
    yy, xx = np.mgrid[0:S, 0:S]
    t = ((xx + yy) / (2.0 * (S - 1)))[..., None]
    a = np.array(c["a"], dtype=float)
    b = np.array(c["b"], dtype=float)
    grad = (a * (1 - t) + b * t).astype(np.uint8)
    badge = Image.fromarray(np.dstack([grad, np.full((S, S, 1), 255, np.uint8)]), "RGBA")
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, S - 1, S - 1), radius=BADGE_R * K, fill=255)
    img.paste(badge, (0, 0), mask)

    # "%" centred in the badge by its ink box
    d = ImageDraw.Draw(img)
    pct_font = ImageFont.truetype(xbold, size=round(PCT_PX * K))
    l, tp, r, bt = d.textbbox((0, 0), "%", font=pct_font, anchor="ls")
    d.text((S / 2 - (l + r) / 2, S / 2 - (tp + bt) / 2), "%", font=pct_font, fill=(255, 255, 255, 255), anchor="ls")

    # wordmark, vertically centred on cap height
    baseline = HH / 2 + cap / 2
    draw_glyphs(d, bold, word_glyphs, WORD_PX * K, (H + GAP) * K, baseline, c["text"] + (255,))

    out_w, out_h = W // SS, HH // SS
    img = img.resize((out_w, out_h), Image.LANCZOS)
    path = f"{OUT}/logo-{theme}.webp"
    img.save(path, "WEBP", lossless=True, quality=100, method=6)
    print(theme, img.size, "->", os.path.getsize(path), "bytes; logical", round(out_w / SCALE, 1), "x", out_h / SCALE)
    return out_w, out_h


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for th in THEMES:
        build(th)
