#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mendieta — Carrusel de PEDIDOS Y ENVÍOS (3 slides, 1080x1350).
  1) Cómo pedir (24h, WhatsApp, pago por anticipado)
  2) Envío a domicilio · Zonas 1 y 2 (precio + códigos postales)
  3) Envío a domicilio · Zonas 3 y 4 (precio + códigos postales)

Salidas: assets/brand/templates/envios-{1,2,3}.png  + copia en
         Documentos/Mendieta/publicado/carrusel-envios/
"""
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent.parent
LOGO = BASE / "assets" / "brand" / "logos" / "mendieta-perro-tinta.png"
TPL = BASE / "assets" / "brand" / "templates"
OUTDIR = Path(r"C:/Users/facun/Documentos/Mendieta/publicado/carrusel-envios")
OUTDIR.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1350
CREMA = (251, 244, 198); BORDO = (119, 35, 27); CACAO = (83, 49, 24)
MOSTAZA = (237, 199, 125); CARAMELO = (147, 109, 76)
F_RYE = r"C:/Users/facun/AppData/Local/Temp/Rye.ttf"
F_PLAY = r"C:/Users/facun/AppData/Local/Temp/PlayfairBlack.ttf"
F_MONT = r"C:/Users/facun/AppData/Local/Temp/Montserrat.ttf"

ZONAS = {
    1: ("4,50€", "7,50€", ["08006", "08007", "08008", "08009", "08010", "08011",
                            "08012", "08013", "08021", "08025", "08036", "08037"]),
    2: ("6,50€", "9,50€", ["08001", "08002", "08003", "08015", "08018", "08026", "08029"]),
    3: ("7,50€", "10,50€", ["08004", "08005", "08014", "08016", "08019",
                            "08020", "08027", "08028", "08030", "08041"]),
    4: ("8,50€", "11,50€", ["08017", "08022", "08023", "08024", "08031",
                            "08032", "08033", "08034", "08035", "08042"]),
}


def font(p, s): return ImageFont.truetype(p, s)
def mont(s, w=600):
    f = ImageFont.truetype(F_MONT, s); f.set_variation_by_axes([w]); return f
def tw(d, t, f):
    b = d.textbbox((0, 0), t, font=f); return b[2] - b[0], b[3] - b[1], b[1]


def cline(d, y, t, f, fill, ls=0):
    if ls:
        total = sum(tw(d, ch, f)[0] + ls for ch in t) - ls; x = (W - total) // 2
        for ch in t:
            d.text((x, y), ch, font=f, fill=fill); x += tw(d, ch, f)[0] + ls
        return
    w, h, oy = tw(d, t, f); d.text(((W - w) // 2, y), t, font=f, fill=fill)


def destello(d, cx, cy, r, color):
    iw = r * 0.32
    d.polygon([(cx, cy - r), (cx + iw, cy - iw), (cx + r, cy), (cx + iw, cy + iw),
               (cx, cy + r), (cx - iw, cy + iw), (cx - r, cy), (cx - iw, cy - iw)], fill=color)


def divider(d, cy, half=230):
    d.line([(W // 2 - half, cy), (W // 2 - 55, cy)], fill=CARAMELO, width=3)
    d.line([(W // 2 + 55, cy), (W // 2 + half, cy)], fill=CARAMELO, width=3)
    destello(d, W // 2, cy, 18, BORDO)


def frame(img):
    d = ImageDraw.Draw(img); m, L, wd = 46, 92, 4
    for (px, py, dx, dy) in [(m, m, 1, 1), (W - m, m, -1, 1), (m, H - m, 1, -1), (W - m, H - m, -1, -1)]:
        d.line([(px, py), (px + dx * L, py)], fill=BORDO, width=wd)
        d.line([(px, py), (px, py + dy * L)], fill=BORDO, width=wd)


def pill(d, cy, text, f, fill_bg, fill_tx, pad=70, h=78):
    w = d.textlength(text, font=f); pw = w + pad * 2; px = (W - pw) // 2
    d.rounded_rectangle([px, cy, px + pw, cy + h], radius=h // 2, fill=fill_bg)
    b = d.textbbox((0, 0), text, font=f)
    d.text(((W - (b[2] - b[0])) // 2, cy + (h - (b[3] - b[1])) // 2 - b[1]), text, font=f, fill=fill_tx)


def zone_block(d, y0, num, lab, fest, cps):
    pill(d, y0, f"ZONA {num}", mont(40, 800), BORDO, CREMA, pad=60, h=74)
    cline(d, y0 + 96, f"{lab} laborables  ·  {fest} festivos", mont(34, 700), CACAO)
    # códigos postales en 2 columnas
    half = (len(cps) + 1) // 2
    cols = [cps[:half], cps[half:]]
    fcp = mont(33, 500); rowh = 44; y = y0 + 150
    colx = [W // 2 - 150, W // 2 + 150]
    for ci, col in enumerate(cols):
        yy = y
        for cp in col:
            w = d.textlength(cp, font=fcp)
            d.text((colx[ci] - w // 2, yy), cp, font=fcp, fill=BORDO); yy += rowh


def header(img, sub):
    d = ImageDraw.Draw(img)
    lg = Image.open(LOGO).convert("RGBA"); s = 96 / lg.height
    lg = lg.resize((int(lg.width * s), 96), Image.LANCZOS)
    img.paste(lg, ((W - lg.width) // 2, 44), lg)
    cline(d, 150, "ENVÍO A DOMICILIO", font(F_RYE, 48), BORDO)
    cline(d, 224, sub, font(F_PLAY, 30), CACAO)


def slide1():
    img = Image.new("RGB", (W, H), CREMA); frame(img); d = ImageDraw.Draw(img)
    lg = Image.open(LOGO).convert("RGBA"); s = 150 / lg.height
    lg = lg.resize((int(lg.width * s), 150), Image.LANCZOS)
    img.paste(lg, ((W - lg.width) // 2, 70), lg)
    cline(d, 242, "PASTELERÍA ARGENTINA · BARCELONA", mont(24, 600), CARAMELO, ls=4)
    cline(d, 288, "PEDIDOS Y ENVÍOS", font(F_RYE, 64), BORDO)
    divider(d, 410)
    cline(d, 452, "CÓMO PEDIR", mont(30, 700), MOSTAZA, ls=6)
    cline(d, 516, "Encargá con 24h de antelación", mont(40, 600), BORDO)
    cline(d, 584, "Pedí por WhatsApp", mont(34, 500), CACAO)
    cline(d, 630, "696 98 53 85", font(F_RYE, 66), BORDO)
    cline(d, 738, "Pago por anticipado", mont(38, 700), BORDO)
    cline(d, 792, "Bizum o transferencia inmediata", mont(34, 600), CACAO)
    divider(d, 882)
    cline(d, 924, "ENVÍOS", mont(30, 700), MOSTAZA, ls=6)
    cline(d, 986, "A domicilio según tu zona", mont(40, 600), BORDO)
    cline(d, 1044, "o retirá en tienda · Mallorca 517, BCN", mont(34, 600), BORDO)
    pill(d, 1120, "Deslizá para ver tu zona y precio  →", mont(32, 700), MOSTAZA, CACAO, pad=44, h=70)
    cline(d, 1238, "@pasteleriamendieta", mont(34, 700), BORDO)
    return img


def slide_zones(za, zb, sub, last=False):
    img = Image.new("RGB", (W, H), CREMA); frame(img); header(img, sub)
    d = ImageDraw.Draw(img)
    zone_block(d, 312, za, *ZONAS[za])
    divider(d, 788)
    zone_block(d, 824, zb, *ZONAS[zb])
    foot = "¿No ves tu código? Escribinos por WhatsApp" if last else "Seguí deslizando  →"
    cline(d, 1262, foot, mont(28, 600), CARAMELO)
    return img


def main():
    outs = [("envios-1.png", slide1()),
            ("envios-2.png", slide_zones(1, 2, "Precio según tu código postal")),
            ("envios-3.png", slide_zones(3, 4, "Precio según tu código postal", last=True))]
    for name, im in outs:
        (TPL / name).parent.mkdir(parents=True, exist_ok=True)
        im.save(TPL / name, quality=96); shutil.copyfile(TPL / name, OUTDIR / name)
        print("OK:", TPL / name)


if __name__ == "__main__":
    main()
