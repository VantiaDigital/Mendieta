#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mendieta — Foto GENERAL de pedidos y envíos para el feed (evergreen).
Dos secciones: Cómo pedir + Envíos. Fondo crema de marca.

Salidas:
  assets/brand/templates/pedidos-general-post.png  (1080x1350)
  + copia en Documentos/Mendieta/publicado/  (para tener a mano)
"""
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent.parent
LOGO = BASE / "assets" / "brand" / "logos" / "mendieta-perro-tinta.png"
OUT = BASE / "assets" / "brand" / "templates" / "pedidos-general-post.png"
OUT2 = Path(r"C:/Users/facun/Documentos/Mendieta/publicado/pedidos-general-post.png")

W, H = 1080, 1350
CREMA = (251, 244, 198); BORDO = (119, 35, 27); CACAO = (83, 49, 24)
MOSTAZA = (237, 199, 125); CARAMELO = (147, 109, 76)
F_RYE = r"C:/Users/facun/AppData/Local/Temp/Rye.ttf"
F_PLAY = r"C:/Users/facun/AppData/Local/Temp/PlayfairBlack.ttf"
F_MONT = r"C:/Users/facun/AppData/Local/Temp/Montserrat.ttf"


def font(p, s): return ImageFont.truetype(p, s)
def mont(s, w=600):
    f = ImageFont.truetype(F_MONT, s); f.set_variation_by_axes([w]); return f
def tw(d, t, f):
    b = d.textbbox((0, 0), t, font=f); return b[2] - b[0], b[3] - b[1], b[1]


def cline(d, y, t, f, fill, ls=0):
    if ls:
        total = sum(tw(d, ch, f)[0] + ls for ch in t) - ls
        x = (W - total) // 2
        for ch in t:
            d.text((x, y), ch, font=f, fill=fill); x += tw(d, ch, f)[0] + ls
        return
    w, h, oy = tw(d, t, f); d.text(((W - w) // 2, y), t, font=f, fill=fill)


def destello(d, cx, cy, r, color):
    iw = r * 0.32
    d.polygon([(cx, cy - r), (cx + iw, cy - iw), (cx + r, cy), (cx + iw, cy + iw),
               (cx, cy + r), (cx - iw, cy + iw), (cx - r, cy), (cx - iw, cy - iw)], fill=color)


def divider(d, cy):
    d.line([(W // 2 - 230, cy), (W // 2 - 55, cy)], fill=CARAMELO, width=3)
    d.line([(W // 2 + 55, cy), (W // 2 + 230, cy)], fill=CARAMELO, width=3)
    destello(d, W // 2, cy, 19, BORDO)
    destello(d, W // 2 - 44, cy, 9, MOSTAZA); destello(d, W // 2 + 44, cy, 9, MOSTAZA)


def main():
    img = Image.new("RGB", (W, H), CREMA); d = ImageDraw.Draw(img)
    m, L, wd = 46, 92, 4
    for (px, py, dx, dy) in [(m, m, 1, 1), (W - m, m, -1, 1), (m, H - m, 1, -1), (W - m, H - m, -1, -1)]:
        d.line([(px, py), (px + dx * L, py)], fill=BORDO, width=wd)
        d.line([(px, py), (px, py + dy * L)], fill=BORDO, width=wd)

    lg = Image.open(LOGO).convert("RGBA"); s = 150 / lg.height
    lg = lg.resize((int(lg.width * s), 150), Image.LANCZOS)
    img.paste(lg, ((W - lg.width) // 2, 58), lg)

    cline(d, 226, "PASTELERÍA ARGENTINA · BARCELONA", mont(24, 600), CARAMELO, ls=4)
    cline(d, 272, "PEDIDOS Y ENVÍOS", font(F_RYE, 62), BORDO)
    divider(d, 388)

    # --- CÓMO PEDIR ---
    cline(d, 430, "CÓMO PEDIR", mont(30, 700), MOSTAZA, ls=6)
    cline(d, 492, "Encargá con 24h de antelación", mont(40, 600), BORDO)
    cline(d, 560, "Pedí por WhatsApp", mont(34, 500), CACAO)
    cline(d, 606, "696 98 53 85", font(F_RYE, 66), BORDO)
    cline(d, 712, "Pago: Bizum, transferencia o en tienda", mont(34, 600), BORDO)

    divider(d, 800)

    # --- ENVÍOS ---
    cline(d, 842, "ENVÍOS", mont(30, 700), MOSTAZA, ls=6)
    cline(d, 904, "A domicilio según tu zona · desde 4,50€", mont(36, 600), BORDO)
    cline(d, 962, "o retirá en tienda · Mallorca 517, BCN", mont(36, 600), BORDO)
    cline(d, 1024, "Consultá tu zona por WhatsApp", font(F_PLAY, 34), CACAO)

    divider(d, 1118)
    cline(d, 1162, "Sándwiches de miga · Empanadas · Tartas y más", mont(26, 500), CARAMELO)
    cline(d, 1224, "@pasteleriamendieta", mont(34, 700), BORDO)

    OUT.parent.mkdir(parents=True, exist_ok=True); img.save(OUT, quality=96)
    OUT2.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(OUT, OUT2)
    print(f"OK: {OUT}"); print(f"OK: {OUT2}")


if __name__ == "__main__":
    main()
