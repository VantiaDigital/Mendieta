#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mendieta — STORY (1080x1920) match-day: Argentina juega esta noche (Mundial 2026).
Se sube el viernes 3 de julio: Argentina vs Cabo Verde, 00h (hora Barcelona).
Estilo Mendieta (crema + marco bordó). Voz: voseo argentino.

Salida: Clientes/Mendieta/7 mundial-julio/FINAL/story-matchday-cabo-verde.png
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent.parent
LOGO = BASE / "assets" / "brand" / "logos" / "mendieta-perro-tinta.png"
OUT = Path(r"C:/Users/facun/Documentos/Vantia Digital/Clientes/Mendieta/7 mundial-julio/FINAL/story-matchday-cabo-verde.png")

W, H = 1080, 1920
CREMA = (251, 244, 198); BORDO = (119, 35, 27); CACAO = (83, 49, 24)
MOSTAZA = (237, 199, 125); CARAMELO = (147, 109, 76)
F_RYE = r"C:/Users/facun/AppData/Local/Temp/Rye.ttf"
F_PLAY = r"C:/Users/facun/AppData/Local/Temp/PlayfairBlack.ttf"
F_MONT = r"C:/Users/facun/AppData/Local/Temp/Montserrat.ttf"


def font(p, s): return ImageFont.truetype(p, s)
def mont(s, w=600):
    f = ImageFont.truetype(F_MONT, s); f.set_variation_by_axes([w]); return f
def tw(d, t, f):
    b = d.textbbox((0, 0), t, font=f); return b[2]-b[0]


def cline(d, y, t, f, fill, ls=0):
    if ls:
        total = sum(tw(d, ch, f)+ls for ch in t)-ls; x = (W-total)//2
        for ch in t:
            d.text((x, y), ch, font=f, fill=fill); x += tw(d, ch, f)+ls
        return
    d.text(((W-tw(d, t, f))//2, y), t, font=f, fill=fill)


def destello(d, cx, cy, r, color):
    iw = r*0.32
    d.polygon([(cx, cy-r), (cx+iw, cy-iw), (cx+r, cy), (cx+iw, cy+iw),
               (cx, cy+r), (cx-iw, cy+iw), (cx-r, cy), (cx-iw, cy-iw)], fill=color)


def divider(d, cy):
    d.line([(W//2-220, cy), (W//2-54, cy)], fill=CARAMELO, width=3)
    d.line([(W//2+54, cy), (W//2+220, cy)], fill=CARAMELO, width=3)
    destello(d, W//2, cy, 16, BORDO)


def frame(d):
    m, L, wd = 46, 92, 4
    for (px, py, dx, dy) in [(m, m, 1, 1), (W-m, m, -1, 1), (m, H-m, 1, -1), (W-m, H-m, -1, -1)]:
        d.line([(px, py), (px+dx*L, py)], fill=BORDO, width=wd)
        d.line([(px, py), (px, py+dy*L)], fill=BORDO, width=wd)


def pill(d, cy, text, f, fbg, ftx, pad=58, h=82):
    w = d.textlength(text, font=f); pw = w+pad*2; px = (W-pw)//2
    d.rounded_rectangle([px, cy, px+pw, cy+h], radius=h//2, fill=fbg)
    b = d.textbbox((0, 0), text, font=f)
    d.text(((W-(b[2]-b[0]))//2, cy+(h-(b[3]-b[1]))//2-b[1]), text, font=f, fill=ftx)


def main():
    img = Image.new("RGB", (W, H), CREMA)
    d = ImageDraw.Draw(img)
    frame(d)

    # destellos sutiles alrededor del hero
    for (x, y, r, c) in [(176, 400, 20, MOSTAZA), (918, 452, 24, MOSTAZA),
                         (240, 590, 14, BORDO), (866, 640, 15, BORDO),
                         (150, 760, 11, CARAMELO), (940, 800, 12, CARAMELO)]:
        destello(d, x, y, r, c)

    # logo
    lg = Image.open(LOGO).convert("RGBA"); s = 168/lg.height
    lg = lg.resize((int(lg.width*s), 168), Image.LANCZOS)
    img.paste(lg, ((W-lg.width)//2, 250), lg)

    cline(d, 452, "PASTELERÍA ARGENTINA · BARCELONA", mont(23, 600), CARAMELO, ls=4)
    divider(d, 516)
    cline(d, 566, "MUNDIAL 2026", font(F_RYE, 56), BORDO)

    # hero
    cline(d, 664, "Esta noche", font(F_RYE, 100), BORDO)
    cline(d, 796, "juega Argentina", font(F_RYE, 88), BORDO)

    pill(d, 962, "vs Cabo Verde · 00h", mont(40, 700), MOSTAZA, CACAO, pad=56, h=82)

    divider(d, 1112)

    cline(d, 1166, "La mesa puesta, la tele lista:", font(F_PLAY, 40), CACAO)
    cline(d, 1226, "se mira como en casa", font(F_PLAY, 40), CACAO)

    cline(d, 1326, "Sanguchitos de miga, medialunas", mont(31, 600), BORDO)
    cline(d, 1372, "y algo dulce para el entretiempo", mont(31, 600), BORDO)

    cline(d, 1462, "Encargá tu picada · WhatsApp 696 98 53 85", mont(33, 800), BORDO)

    divider(d, 1552)
    cline(d, 1598, "¡Vamos Argentina!", font(F_RYE, 62), BORDO)
    cline(d, 1716, "@pasteleriamendieta", mont(32, 700), CACAO)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, quality=96)
    print("OK:", OUT)


if __name__ == "__main__":
    main()
