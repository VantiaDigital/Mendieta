#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mendieta — Foto de DETALLES DE PEDIDO para el carrusel (video + esta foto).
Fondo crema del logo (#FBF4C6, no el gris). Pasos numerados, claros y legibles.

Salidas:
  assets/brand/templates/pedidos-detalles-post.png  (1080x1350, feed 4:5)
  + copia en Documentos/Mendieta/reel-mundial/editados/
"""
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent.parent
LOGO = BASE / "assets" / "brand" / "logos" / "mendieta-perro-tinta.png"
OUT = BASE / "assets" / "brand" / "templates" / "pedidos-detalles-post.png"
OUT2 = Path(r"C:/Users/facun/Documentos/Mendieta/reel-mundial/FINAL/pedidos-detalles-post.png")

W, H = 1080, 1350
CREMA = (251, 244, 198)
BORDO = (119, 35, 27)
CACAO = (83, 49, 24)
MOSTAZA = (237, 199, 125)
CARAMELO = (147, 109, 76)
F_RYE = r"C:/Users/facun/AppData/Local/Temp/Rye.ttf"
F_PLAY = r"C:/Users/facun/AppData/Local/Temp/PlayfairBlack.ttf"
F_MONT = r"C:/Users/facun/AppData/Local/Temp/Montserrat.ttf"


def font(p, s):
    return ImageFont.truetype(p, s)


def mont(s, w=600):
    """Montserrat es variable (default Thin 100). Forzamos peso real."""
    f = ImageFont.truetype(F_MONT, s)
    f.set_variation_by_axes([w])
    return f


def tw(d, t, f):
    b = d.textbbox((0, 0), t, font=f)
    return b[2] - b[0], b[3] - b[1], b[1]


def cline(d, y, t, f, fill, ls=0):
    if ls:
        # letter spacing manual
        total = sum(tw(d, ch, f)[0] + ls for ch in t) - ls
        x = (W - total) // 2
        for ch in t:
            d.text((x, y), ch, font=f, fill=fill)
            x += tw(d, ch, f)[0] + ls
        return
    w, h, oy = tw(d, t, f)
    d.text(((W - w) // 2, y), t, font=f, fill=fill)


def destello(d, cx, cy, r, color):
    iw = r * 0.32
    d.polygon([(cx, cy - r), (cx + iw, cy - iw), (cx + r, cy), (cx + iw, cy + iw),
               (cx, cy + r), (cx - iw, cy + iw), (cx - r, cy), (cx - iw, cy - iw)], fill=color)


def divider(d, cy):
    d.line([(W // 2 - 230, cy), (W // 2 - 55, cy)], fill=CARAMELO, width=3)
    d.line([(W // 2 + 55, cy), (W // 2 + 230, cy)], fill=CARAMELO, width=3)
    destello(d, W // 2, cy, 20, BORDO)
    destello(d, W // 2 - 45, cy, 9, MOSTAZA)
    destello(d, W // 2 + 45, cy, 9, MOSTAZA)


def step(d, cy, num, lines):
    # badge
    bx, r = 150, 40
    d.ellipse([bx - r, cy - r, bx + r, cy + r], fill=BORDO)
    fn = mont(44, 700)
    w, h, oy = tw(d, num, fn)
    d.text((bx - w // 2, cy - h // 2 - oy), num, font=fn, fill=CREMA)
    # text block (left aligned), vertically centered around cy
    heights = [tw(d, t, f)[1] for (t, f, _) in lines]
    gap = 12
    total = sum(heights) + gap * (len(lines) - 1)
    y = cy - total // 2
    tx = 232
    for (t, f, fill), hh in zip(lines, heights):
        oy = tw(d, t, f)[2]
        d.text((tx, y - oy), t, font=f, fill=fill)
        y += hh + gap


def main():
    img = Image.new("RGB", (W, H), CREMA)
    d = ImageDraw.Draw(img)

    # marco de esquinas
    m, L, wd = 46, 92, 4
    for (px, py, dx, dy) in [(m, m, 1, 1), (W - m, m, -1, 1), (m, H - m, 1, -1), (W - m, H - m, -1, -1)]:
        d.line([(px, py), (px + dx * L, py)], fill=BORDO, width=wd)
        d.line([(px, py), (px, py + dy * L)], fill=BORDO, width=wd)

    # logo
    lg = Image.open(LOGO).convert("RGBA")
    s = 168 / lg.height
    lg = lg.resize((int(lg.width * s), 168), Image.LANCZOS)
    img.paste(lg, ((W - lg.width) // 2, 66), lg)

    # eyebrow + título
    cline(d, 250, "PASTELERÍA ARGENTINA · BARCELONA", mont(24, 600), CARAMELO, ls=4)
    cline(d, 296, "PEDÍ PARA EL PARTIDO", font(F_RYE, 60), BORDO)
    cline(d, 392, "Encargá con tiempo y disfrutá sin apuro", font(F_PLAY, 33), CACAO)

    divider(d, 470)

    fT = mont(40, 600)      # línea principal de paso
    fS = mont(33, 500)      # línea secundaria
    step(d, 565, "1", [("Encargá con 24h de antelación", fT, BORDO)])
    step(d, 700, "2", [("Pedí por WhatsApp", fS, CACAO),
                       ("696 98 53 85", font(F_RYE, 56), BORDO)])
    step(d, 858, "3", [("Pagá por Bizum o", fT, BORDO),
                       ("transferencia bancaria", fT, BORDO)])
    step(d, 1010, "4", [("Mandá el comprobante", fT, BORDO),
                        ("y confirmamos tu pedido", fS, CACAO)])

    divider(d, 1130)
    cline(d, 1175, "Sándwiches de miga · Empanadas · Tartas y más salado",
          mont(27, 500), CARAMELO)
    cline(d, 1240, "@pasteleriamendieta", mont(34, 700), BORDO)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, quality=96)
    OUT2.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUT, OUT2)
    print(f"OK: {OUT}")
    print(f"OK: {OUT2}")


if __name__ == "__main__":
    main()
