#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plantillas repetibles de Instagram para Mendieta.
Genera (en assets/brand/templates/):
  - Busqueda laboral: pastelero + camarero, en historia (1080x1920) y post (1080x1350)
  - Datos de pedido: historia + post

REPETIBLE: cambiá los textos en la seccion CONFIG y regenera con
  python scripts/make_templates.py

Marca: paleta + fuentes del brand kit (Rye / Playfair / Montserrat).
Tono argentino, neutral (regla de neutralidad del kit).
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import textwrap

# ---------------- PALETA ----------------
CREMA    = (251, 244, 198)
CREMA_2  = (245, 236, 175)   # crema un toque mas oscuro (cards)
BORDO    = (119, 35, 27)
CACAO    = (83, 49, 24)
CARAMELO = (147, 109, 76)
MOSTAZA  = (237, 199, 125)
TINTA    = (27, 22, 19)
BLANCO   = (255, 255, 255)

# ---------------- FUENTES ----------------
TMP = r"C:/Users/facun/AppData/Local/Temp/"
F_RYE = TMP + "Rye.ttf"
F_PLAY = TMP + "PlayfairBlack.ttf"
F_MONT = TMP + "Montserrat.ttf"

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "assets" / "brand" / "templates"
OUT.mkdir(parents=True, exist_ok=True)
LOGO = BASE / "assets" / "brand" / "logos" / "mendieta-perro-tinta.png"

# ---------------- CONFIG (editar aca) ----------------
WHATSAPP = "+34 696 98 53 85"
TELEFONO = "+34 934 33 57 45"
DIRECCION = "Carrer de Mallorca, 517 · Barcelona"
HORARIO = "L–V 7–21h  ·  S–D 7:30–21h"
CONDICIONES = "24h de antelación  ·  Tarjeta o efectivo"

JOBS = [
    {
        "slug": "pastelero",
        "title": "PASTELERO/A",
        "subtitle": "Buscamos manos para el obrador",
        "body": "¿Te gusta amasar, hornear y arrancar el día con olor a factura recién hecha? Sumate a Mendieta.",
        "tags": "Ganas de equipo · Prolijidad · Amor por lo bien hecho",
    },
    {
        "slug": "camarero",
        "title": "CAMARERO/A",
        "subtitle": "Buscamos buena onda para atender",
        "body": "¿Te gusta el trato con la gente y laburar con energía? Sumate al equipo de Mendieta.",
        "tags": "Simpatía · Ganas · Disponibilidad",
    },
]

FORMATS = {"historia": (1080, 1920), "post": (1080, 1350)}


# ---------------- HELPERS ----------------
def font(path, size):
    return ImageFont.truetype(path, size)

def tw(d, text, f):
    b = d.textbbox((0, 0), text, font=f)
    return b[2] - b[0], b[3] - b[1]

def center_text(d, cx, y, text, f, fill, shadow=None):
    w, h = tw(d, text, f)
    x = cx - w / 2
    if shadow:
        d.text((x + shadow[0], y + shadow[1]), text, font=f, fill=shadow[2])
    d.text((x, y), text, font=f, fill=fill)
    return h

def wrap_center(d, cx, y, text, f, fill, max_w, line_gap=14):
    # wrap por ancho real
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(d, t, f)[0] <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    for ln in lines:
        h = center_text(d, cx, y, ln, f, fill)
        y += h + line_gap
    return y

def destello(d, cx, cy, r, color):
    iw = r * 0.30
    pts = [(cx, cy - r), (cx + iw, cy - iw), (cx + r, cy), (cx + iw, cy + iw),
           (cx, cy + r), (cx - iw, cy + iw), (cx - r, cy), (cx - iw, cy - iw)]
    d.polygon(pts, fill=color)

def separador(d, cx, y, w, color):
    d.line([(cx - w / 2, y), (cx - 18, y)], fill=color, width=3)
    d.line([(cx + 18, y), (cx + w / 2, y)], fill=color, width=3)
    d.ellipse([cx - 8, y - 8, cx + 8, y + 8], fill=color)

def eyebrow(d, cx, y, text, color):
    f = font(F_MONT, 30)
    # tracking manual (espaciado entre letras)
    spaced = "   ".join(list(text))
    w, h = tw(d, spaced, f)
    center_text(d, cx, y, spaced, f, color)
    # destellos a los lados
    destello(d, cx - w / 2 - 45, y + h / 2, 16, color)
    destello(d, cx + w / 2 + 45, y + h / 2, 16, color)
    return h

def paste_logo(img, cx, y, h_px, tint=None):
    logo = Image.open(LOGO).convert("RGBA")
    scale = h_px / logo.height
    logo = logo.resize((int(logo.width * scale), h_px), Image.LANCZOS)
    img.paste(logo, (int(cx - logo.width / 2), y), logo)
    return logo.height

# ---- iconos simples (line icons en circulo) ----
def icon_circle(d, cx, cy, r, ring=BORDO):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLANCO, outline=ring, width=3)

def ic_chat(d, cx, cy, r):
    icon_circle(d, cx, cy, r)
    s = r * 0.55
    d.rounded_rectangle([cx - s, cy - s * 0.8, cx + s, cy + s * 0.4], radius=int(s * 0.4),
                        outline=BORDO, width=3)
    d.polygon([(cx - s * 0.3, cy + s * 0.4), (cx - s * 0.1, cy + s * 0.4),
               (cx - s * 0.3, cy + s * 0.85)], fill=BORDO)
    for dx in (-s * 0.4, 0, s * 0.4):
        d.ellipse([cx + dx - 3, cy - s * 0.25 - 3, cx + dx + 3, cy - s * 0.25 + 3], fill=BORDO)

def ic_phone(d, cx, cy, r):
    icon_circle(d, cx, cy, r)
    s = r * 0.5
    d.rounded_rectangle([cx - s * 0.7, cy - s, cx + s * 0.7, cy + s], radius=int(s * 0.35),
                        outline=BORDO, width=3)
    d.ellipse([cx - 3, cy + s * 0.55 - 3, cx + 3, cy + s * 0.55 + 3], fill=BORDO)

def ic_pin(d, cx, cy, r):
    icon_circle(d, cx, cy, r)
    s = r * 0.55
    d.ellipse([cx - s * 0.7, cy - s * 0.8, cx + s * 0.7, cy + s * 0.5], outline=BORDO, width=3)
    d.polygon([(cx - s * 0.4, cy + s * 0.15), (cx + s * 0.4, cy + s * 0.15),
               (cx, cy + s * 0.9)], fill=BORDO)
    d.ellipse([cx - s * 0.22, cy - s * 0.35, cx + s * 0.22, cy + s * 0.1], fill=BLANCO)

def ic_clock(d, cx, cy, r):
    icon_circle(d, cx, cy, r)
    s = r * 0.55
    d.ellipse([cx - s, cy - s, cx + s, cy + s], outline=BORDO, width=3)
    d.line([(cx, cy), (cx, cy - s * 0.55)], fill=BORDO, width=3)
    d.line([(cx, cy), (cx + s * 0.4, cy)], fill=BORDO, width=3)


# ---------------- TEMPLATE: BUSQUEDA LABORAL ----------------
def job_template(job, fmt):
    W, H = FORMATS[fmt]
    img = Image.new("RGB", (W, H), CREMA)
    d = ImageDraw.Draw(img)
    cx = W / 2

    # marco de esquinas (sutil)
    m, L, wd = 50, 90, 3
    for (px, py, dx, dy) in [(m, m, 1, 1), (W - m, m, -1, 1), (m, H - m, 1, -1), (W - m, H - m, -1, -1)]:
        d.line([(px, py), (px + dx * L, py)], fill=BORDO, width=wd)
        d.line([(px, py), (px, py + dy * L)], fill=BORDO, width=wd)

    top = 150 if fmt == "historia" else 110
    # logo
    lh = paste_logo(img, cx, top, 150 if fmt == "historia" else 120)
    y = top + lh + (60 if fmt == "historia" else 40)

    # eyebrow
    y += 0
    eh = eyebrow(d, cx, y, "SUMATE AL EQUIPO", BORDO)
    y += eh + (50 if fmt == "historia" else 35)

    # titulo (Rye) - el puesto
    f_title = font(F_RYE, 120 if fmt == "historia" else 100)
    # achicar si no entra
    while tw(d, job["title"], f_title)[0] > W - 120:
        f_title = font(F_RYE, f_title.size - 6)
    th = center_text(d, cx, y, job["title"], f_title, BORDO, shadow=(3, 3, (0, 0, 0, 60)))
    y += th + (40 if fmt == "historia" else 26)

    # subtitulo (Playfair)
    f_sub = font(F_PLAY, 52 if fmt == "historia" else 44)
    sh = center_text(d, cx, y, job["subtitle"], f_sub, CACAO)
    y += sh + (55 if fmt == "historia" else 38)

    # separador
    separador(d, cx, y, 260, CARAMELO)
    y += (60 if fmt == "historia" else 45)

    # body (Montserrat)
    f_body = font(F_MONT, 40 if fmt == "historia" else 34)
    y = wrap_center(d, cx, y, job["body"], f_body, TINTA, W - 200, line_gap=16)
    y += (45 if fmt == "historia" else 30)

    # tags / lo que buscamos
    f_tags = font(F_MONT, 32 if fmt == "historia" else 28)
    center_text(d, cx, y, job["tags"], f_tags, CARAMELO)
    y += (90 if fmt == "historia" else 60)

    # CTA card
    cta_y = H - (430 if fmt == "historia" else 320)
    card_h = 200 if fmt == "historia" else 170
    pad = 70
    d.rounded_rectangle([pad, cta_y, W - pad, cta_y + card_h], radius=28, fill=BORDO)
    f_cta1 = font(F_MONT, 34 if fmt == "historia" else 30)
    f_cta2 = font(F_PLAY, 46 if fmt == "historia" else 40)
    center_text(d, cx, cta_y + (34 if fmt == "historia" else 26), "Acercá tu CV al local o escribinos", f_cta1, MOSTAZA)
    center_text(d, cx, cta_y + (90 if fmt == "historia" else 74), WHATSAPP, f_cta2, CREMA)

    # bottom: direccion
    f_addr = font(F_MONT, 28 if fmt == "historia" else 24)
    center_text(d, cx, H - (130 if fmt == "historia" else 95), DIRECCION, f_addr, CACAO)

    out = OUT / f"busqueda-{job['slug']}-{fmt}.png"
    img.save(out, "PNG", optimize=True)
    print(f"  -> {out.name}  ({W}x{H})")


# ---------------- TEMPLATE: DATOS DE PEDIDO ----------------
def order_template(fmt):
    W, H = FORMATS[fmt]
    img = Image.new("RGB", (W, H), CREMA)
    d = ImageDraw.Draw(img)
    cx = W / 2

    m, L, wd = 50, 90, 3
    for (px, py, dx, dy) in [(m, m, 1, 1), (W - m, m, -1, 1), (m, H - m, 1, -1), (W - m, H - m, -1, -1)]:
        d.line([(px, py), (px + dx * L, py)], fill=BORDO, width=wd)
        d.line([(px, py), (px, py + dy * L)], fill=BORDO, width=wd)

    top = 150 if fmt == "historia" else 110
    lh = paste_logo(img, cx, top, 150 if fmt == "historia" else 120)
    y = top + lh + (55 if fmt == "historia" else 38)

    eh = eyebrow(d, cx, y, "MENDIETA A CASA", BORDO)
    y += eh + (45 if fmt == "historia" else 32)

    # titulo
    f_title = font(F_RYE, 130 if fmt == "historia" else 108)
    th = center_text(d, cx, y, "PEDÍ A CASA", f_title, BORDO, shadow=(3, 3, (0, 0, 0, 60)))
    y += th + (30 if fmt == "historia" else 20)

    f_sub = font(F_PLAY, 50 if fmt == "historia" else 42)
    sh = center_text(d, cx, y, "Te lo llevamos, recién hecho", f_sub, CACAO)
    y += sh + (60 if fmt == "historia" else 42)

    # filas de datos
    rows = [
        (ic_chat,  "WHATSAPP", WHATSAPP),
        (ic_phone, "TELÉFONO", TELEFONO),
        (ic_pin,   "DÓNDE",    DIRECCION),
        (ic_clock, "HORARIO",  HORARIO),
    ]
    row_gap = 150 if fmt == "historia" else 120
    icon_r = 42 if fmt == "historia" else 36
    left = 130 if fmt == "historia" else 120
    f_lbl = font(F_MONT, 26 if fmt == "historia" else 23)
    f_val = font(F_MONT, 38 if fmt == "historia" else 32)
    for ic, lbl, val in rows:
        ic(d, left, y + icon_r, icon_r)
        tx = left + icon_r + 40
        d.text((tx, y + 2), "   ".join(list(lbl)), font=f_lbl, fill=CARAMELO)
        d.text((tx, y + 36 if fmt == "historia" else y + 32), val, font=f_val, fill=TINTA)
        y += row_gap

    y += (10 if fmt == "historia" else 0)
    # condiciones (pill mostaza)
    f_cond = font(F_MONT, 30 if fmt == "historia" else 26)
    cw = tw(d, CONDICIONES, f_cond)[0]
    pill_w = cw + 80
    pill_h = 70 if fmt == "historia" else 60
    d.rounded_rectangle([cx - pill_w / 2, y, cx + pill_w / 2, y + pill_h], radius=35, fill=MOSTAZA)
    center_text(d, cx, y + (pill_h - 36) / 2, CONDICIONES, f_cond, CACAO)
    y += pill_h + (55 if fmt == "historia" else 40)

    # CTA
    f_cta = font(F_PLAY, 46 if fmt == "historia" else 40)
    center_text(d, cx, y, "Escribinos y armamos tu pedido", f_cta, BORDO)

    out = OUT / f"pedidos-datos-{fmt}.png"
    img.save(out, "PNG", optimize=True)
    print(f"  -> {out.name}  ({W}x{H})")


def main():
    print("Generando plantillas Mendieta...")
    print(" Busqueda laboral:")
    for job in JOBS:
        for fmt in FORMATS:
            job_template(job, fmt)
    print(" Datos de pedido:")
    for fmt in FORMATS:
        order_template(fmt)
    print("Listo.")


if __name__ == "__main__":
    main()
