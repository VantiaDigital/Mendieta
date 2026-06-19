#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mendieta — Carrusel PEDIDOS Y ENVÍOS en 1:1 (1080x1080) para feed.
Mismo contenido que la versión 4:5, recompaginado para cuadrado.

Salidas: assets/brand/templates/envios1x1-{1,2,3}.png
         + Clientes/Mendieta/4 carrusel-envios/1-1/envios-{1,2,3}.png
"""
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent.parent
LOGO = BASE / "assets" / "brand" / "logos" / "mendieta-perro-tinta.png"
TPL = BASE / "assets" / "brand" / "templates"
OUTDIR = Path(r"C:/Users/facun/Documentos/Vantia Digital/Clientes/Mendieta/4 carrusel-envios/1-1")

W, H = 1080, 1080
CREMA = (251, 244, 198); BORDO = (119, 35, 27); CACAO = (83, 49, 24)
MOSTAZA = (237, 199, 125); CARAMELO = (147, 109, 76)
F_RYE = r"C:/Users/facun/AppData/Local/Temp/Rye.ttf"
F_PLAY = r"C:/Users/facun/AppData/Local/Temp/PlayfairBlack.ttf"
F_MONT = r"C:/Users/facun/AppData/Local/Temp/Montserrat.ttf"

ZONAS = {
    1: ("5,50€", "9€", ["08006","08007","08008","08009","08010","08011",
                        "08012","08013","08021","08025","08036","08037"]),
    2: ("7,50€", "11€", ["08001","08002","08003","08015","08018","08026","08029"]),
    3: ("9€", "12€", ["08004","08005","08014","08016","08019",
                      "08020","08027","08028","08030","08041"]),
    4: ("10€", "13€", ["08017","08022","08023","08024","08031",
                       "08032","08033","08034","08035","08042"]),
}


def font(p, s): return ImageFont.truetype(p, s)
def mont(s, w=600):
    f = ImageFont.truetype(F_MONT, s); f.set_variation_by_axes([w]); return f
def tw(d, t, f):
    b = d.textbbox((0, 0), t, font=f); return b[2]-b[0], b[3]-b[1], b[1]


def cline(d, y, t, f, fill, ls=0):
    if ls:
        total = sum(tw(d, ch, f)[0]+ls for ch in t)-ls; x = (W-total)//2
        for ch in t:
            d.text((x, y), ch, font=f, fill=fill); x += tw(d, ch, f)[0]+ls
        return
    w, h, oy = tw(d, t, f); d.text(((W-w)//2, y), t, font=f, fill=fill)


def destello(d, cx, cy, r, color):
    iw = r*0.32
    d.polygon([(cx,cy-r),(cx+iw,cy-iw),(cx+r,cy),(cx+iw,cy+iw),
               (cx,cy+r),(cx-iw,cy+iw),(cx-r,cy),(cx-iw,cy-iw)], fill=color)


def divider(d, cy):
    d.line([(W//2-210,cy),(W//2-52,cy)], fill=CARAMELO, width=3)
    d.line([(W//2+52,cy),(W//2+210,cy)], fill=CARAMELO, width=3)
    destello(d, W//2, cy, 16, BORDO)


def frame(img):
    d = ImageDraw.Draw(img); m, L, wd = 40, 80, 4
    for (px, py, dx, dy) in [(m,m,1,1),(W-m,m,-1,1),(m,H-m,1,-1),(W-m,H-m,-1,-1)]:
        d.line([(px,py),(px+dx*L,py)], fill=BORDO, width=wd)
        d.line([(px,py),(px,py+dy*L)], fill=BORDO, width=wd)


def pill(d, cy, text, f, fbg, ftx, pad=58, h=66):
    w = d.textlength(text, font=f); pw = w+pad*2; px = (W-pw)//2
    d.rounded_rectangle([px,cy,px+pw,cy+h], radius=h//2, fill=fbg)
    b = d.textbbox((0,0), text, font=f)
    d.text(((W-(b[2]-b[0]))//2, cy+(h-(b[3]-b[1]))//2-b[1]), text, font=f, fill=ftx)


def zone_block(d, y0, num, lab, fest, cps):
    pill(d, y0, f"ZONA {num}", mont(34, 800), BORDO, CREMA, pad=50, h=62)
    cline(d, y0+78, f"{lab} laborables  ·  {fest} festivos", mont(30, 700), CACAO)
    half = (len(cps)+1)//2; cols = [cps[:half], cps[half:]]
    fcp = mont(29, 500); rowh = 40; colx = [W//2-145, W//2+145]
    for ci, col in enumerate(cols):
        yy = y0+136
        for cp in col:
            w = d.textlength(cp, font=fcp); d.text((colx[ci]-w//2, yy), cp, font=fcp, fill=BORDO); yy += rowh


def header(img, sub):
    d = ImageDraw.Draw(img)
    lg = Image.open(LOGO).convert("RGBA"); s = 80/lg.height
    lg = lg.resize((int(lg.width*s), 80), Image.LANCZOS); img.paste(lg, ((W-lg.width)//2, 26), lg)
    cline(d, 116, "ENVÍO A DOMICILIO", font(F_RYE, 42), BORDO)
    cline(d, 178, sub, font(F_PLAY, 28), CACAO)


def slide1():
    img = Image.new("RGB", (W, H), CREMA); frame(img); d = ImageDraw.Draw(img)
    lg = Image.open(LOGO).convert("RGBA"); s = 122/lg.height
    lg = lg.resize((int(lg.width*s), 122), Image.LANCZOS); img.paste(lg, ((W-lg.width)//2, 38), lg)
    cline(d, 182, "PASTELERÍA ARGENTINA · BARCELONA", mont(22, 600), CARAMELO, ls=3)
    cline(d, 220, "PEDIDOS Y ENVÍOS", font(F_RYE, 52), BORDO)
    divider(d, 322)
    cline(d, 356, "CÓMO PEDIR", mont(26, 700), MOSTAZA, ls=5)
    cline(d, 410, "Encargá con 24h de antelación", mont(36, 600), BORDO)
    cline(d, 470, "Pedí por WhatsApp", mont(30, 500), CACAO)
    cline(d, 512, "696 98 53 85", font(F_RYE, 56), BORDO)
    cline(d, 604, "Pago por anticipado", mont(34, 700), BORDO)
    cline(d, 652, "Bizum o transferencia inmediata", mont(30, 600), CACAO)
    divider(d, 726)
    cline(d, 760, "ENVÍOS", mont(26, 700), MOSTAZA, ls=5)
    cline(d, 812, "A domicilio según tu zona", mont(36, 600), BORDO)
    cline(d, 866, "o retirá en tienda · Mallorca 517, BCN", mont(30, 600), BORDO)
    pill(d, 932, "Deslizá para ver tu zona y precio  →", mont(28, 700), MOSTAZA, CACAO, pad=40, h=62)
    cline(d, 1018, "@pasteleriamendieta", mont(30, 700), BORDO)
    return img


def slide_zones(za, zb, last=False):
    img = Image.new("RGB", (W, H), CREMA); frame(img); header(img, "Precio según tu código postal")
    d = ImageDraw.Draw(img)
    zone_block(d, 232, za, *ZONAS[za])
    divider(d, max(232+136+((len(ZONAS[za][2])+1)//2)*40+22, 600))
    zb_y = max(232+136+((len(ZONAS[za][2])+1)//2)*40+58, 636)
    zone_block(d, zb_y, zb, *ZONAS[zb])
    foot = "¿No ves tu código? Escribinos por WhatsApp" if last else "Seguí deslizando  →"
    cline(d, 1024, foot, mont(26, 600), CARAMELO)
    return img


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    outs = [("envios-1.png", slide1()),
            ("envios-2.png", slide_zones(1, 2)),
            ("envios-3.png", slide_zones(3, 4, last=True))]
    for name, im in outs:
        tname = "envios1x1-" + name.split("-")[1]
        im.save(TPL / tname, quality=96)
        try:
            shutil.copyfile(TPL / tname, OUTDIR / name)
        except Exception as e:
            print("  (no se pudo copiar a cliente:", e, ")")
        print("OK:", TPL / tname)


if __name__ == "__main__":
    main()
