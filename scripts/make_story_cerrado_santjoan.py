#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mendieta — STORY (1080x1920) aviso: cerrado mañana 24 de junio por Sant Joan.
Estilo Mendieta (crema + marco bordó + chispas tipo fuegos de Sant Joan).
Voz: voseo argentino (como el resto del contenido de Mendieta).

Salida: Clientes/Mendieta/5 sant-joan/FINAL/story-cerrado-santjoan.png
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent.parent
LOGO = BASE / "assets" / "brand" / "logos" / "mendieta-perro-tinta.png"
OUT = Path(r"C:/Users/facun/Documentos/Vantia Digital/Clientes/Mendieta/5 sant-joan/FINAL/story-cerrado-santjoan.png")

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


def chispa(d, cx, cy, r, color, w=3):
    """Chispa/fuego de Sant Joan: rayos finos + diamante central."""
    d.line([(cx, cy-r), (cx, cy+r)], fill=color, width=w)
    d.line([(cx-r, cy), (cx+r, cy)], fill=color, width=w)
    dr = int(r*0.62)
    d.line([(cx-dr, cy-dr), (cx+dr, cy+dr)], fill=color, width=max(1, w-1))
    d.line([(cx-dr, cy+dr), (cx+dr, cy-dr)], fill=color, width=max(1, w-1))
    destello(d, cx, cy, int(r*0.42), color)


def divider(d, cy):
    d.line([(W//2-220, cy), (W//2-54, cy)], fill=CARAMELO, width=3)
    d.line([(W//2+54, cy), (W//2+220, cy)], fill=CARAMELO, width=3)
    destello(d, W//2, cy, 16, BORDO)


def frame(d):
    m, L, wd = 46, 92, 4
    for (px, py, dx, dy) in [(m, m, 1, 1), (W-m, m, -1, 1), (m, H-m, 1, -1), (W-m, H-m, -1, -1)]:
        d.line([(px, py), (px+dx*L, py)], fill=BORDO, width=wd)
        d.line([(px, py), (px, py+dy*L)], fill=BORDO, width=wd)


def pill(d, cy, text, f, fbg, ftx, pad=58, h=78):
    w = d.textlength(text, font=f); pw = w+pad*2; px = (W-pw)//2
    d.rounded_rectangle([px, cy, px+pw, cy+h], radius=h//2, fill=fbg)
    b = d.textbbox((0, 0), text, font=f)
    d.text(((W-(b[2]-b[0]))//2, cy+(h-(b[3]-b[1]))//2-b[1]), text, font=f, fill=ftx)


def main():
    img = Image.new("RGB", (W, H), CREMA)
    d = ImageDraw.Draw(img)
    frame(d)

    # chispas / fuegos de Sant Joan (sutiles)
    for (x, y, r, c, w) in [(176, 372, 26, MOSTAZA, 3), (918, 430, 32, MOSTAZA, 3),
                            (250, 560, 18, BORDO, 3), (860, 600, 20, BORDO, 3),
                            (150, 720, 14, CARAMELO, 2), (940, 760, 16, CARAMELO, 2)]:
        chispa(d, x, y, r, c, w)

    # logo
    lg = Image.open(LOGO).convert("RGBA"); s = 168/lg.height
    lg = lg.resize((int(lg.width*s), 168), Image.LANCZOS)
    img.paste(lg, ((W-lg.width)//2, 250), lg)

    cline(d, 452, "PASTELERÍA ARGENTINA · BARCELONA", mont(23, 600), CARAMELO, ls=4)
    divider(d, 516)
    cline(d, 566, "SANT JOAN", font(F_RYE, 56), BORDO)

    # hero
    cline(d, 664, "Mañana", font(F_RYE, 104), BORDO)
    cline(d, 800, "cerramos", font(F_RYE, 104), BORDO)

    pill(d, 968, "Miércoles 24 de junio", mont(40, 700), MOSTAZA, CACAO, pad=56, h=82)

    divider(d, 1116)

    cline(d, 1170, "Es festivo y descansamos", font(F_PLAY, 40), CACAO)
    cline(d, 1230, "por la diada de Sant Joan", font(F_PLAY, 40), CACAO)

    cline(d, 1330, "Hoy es la revetlla y te esperamos", mont(31, 600), BORDO)
    cline(d, 1376, "con nuestras cocas recién hechas", mont(31, 600), BORDO)

    cline(d, 1466, "Volvemos el jueves 25", mont(36, 800), BORDO)

    divider(d, 1556)
    cline(d, 1602, "¡Bona revetlla!", font(F_RYE, 64), BORDO)
    cline(d, 1716, "@pasteleriamendieta", mont(32, 700), CACAO)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, quality=96)
    print("OK:", OUT)


if __name__ == "__main__":
    main()
