#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mendieta — Reel "triplete" para Argentina vs Austria (lunes 19h).

Gag: "No es lo mismo un triplete (marcador ARGENTINA 3) que un triplete
(3 sándwiches de miga reales cayendo y apilándose)". Cierre con pedido.

Marcador recreado de marca (sin imagen real de TV). Sándwich real recortado
(tile redondeado + sombra), 3 cayendo: uno primero y dos encima.

Salida: Documentos/Mendieta/partido-austria/FINAL/reel-triplete.mp4 (1080x1920)
"""
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

FF = r"C:/Users/facun/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.1-full_build/bin/ffmpeg.exe"
PROD = Path(r"C:/Users/facun/Documentos/Mendieta/reel-mundial/productos")
PA = Path(r"C:/Users/facun/Documentos/Mendieta/partido-austria")
FINAL = PA / "FINAL"; FINAL.mkdir(parents=True, exist_ok=True)
WORK = Path(r"C:/Users/facun/AppData/Local/Temp/mendieta-triplete/frames")
WORK.mkdir(parents=True, exist_ok=True)
OUT = FINAL / "reel-triplete.mp4"

W, H = 1080, 1920
FPS = 30
CREMA = (251, 244, 198); BORDO = (119, 35, 27); CACAO = (83, 49, 24)
MOSTAZA = (237, 199, 125); CELESTE = (117, 170, 219); BLANCO = (245, 247, 249)
TINTA = (27, 22, 19)
F_RYE = r"C:/Users/facun/AppData/Local/Temp/Rye.ttf"
F_PLAY = r"C:/Users/facun/AppData/Local/Temp/PlayfairBlack.ttf"
F_MONT = r"C:/Users/facun/AppData/Local/Temp/Montserrat.ttf"


def mont(s, w=700):
    f = ImageFont.truetype(F_MONT, s); f.set_variation_by_axes([w]); return f


def ctext(d, y, t, f, fill, sh=None):
    w = d.textlength(t, font=f); x = (W - w) // 2
    if sh:
        d.text((x + 3, y + 4), t, font=f, fill=sh)
    d.text((x, y), t, font=f, fill=fill)
    return x, w


def eob(u):  # ease out back (overshoot)
    c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (u - 1) ** 3 + c1 * (u - 1) ** 2


def bounce(u):
    n, d = 7.5625, 2.75
    if u < 1 / d: return n * u * u
    if u < 2 / d: u -= 1.5 / d; return n * u * u + 0.75
    if u < 2.5 / d: u -= 2.25 / d; return n * u * u + 0.9375
    u -= 2.625 / d; return n * u * u + 0.984375


# ---------- sprite del sándwich (tile real redondeado + sombra) ----------
def make_tile():
    im = Image.open(PROD / "IMG_1364.JPG").convert("RGB")
    Wp, Hp = im.size
    t = im.crop((int(.11 * Wp), int(.54 * Hp), int(.73 * Wp), int(.80 * Hp)))
    t = ImageEnhance.Color(t).enhance(1.1); t = ImageEnhance.Contrast(t).enhance(1.06)
    tw = 600; t = t.resize((tw, int(t.height * tw / t.width)), Image.LANCZOS)
    th = t.height
    # esquinas redondeadas
    rad = 34
    mask = Image.new("L", (tw, th), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, tw, th], radius=rad, fill=255)
    tile = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    tile.paste(t, (0, 0), mask)
    # borde crema fino
    ImageDraw.Draw(tile).rounded_rectangle([1, 1, tw - 2, th - 2], radius=rad, outline=(255, 250, 230, 230), width=4)
    return tile


def paste_with_shadow(frame, sprite, cx, cy, angle, alpha=1.0):
    sp = sprite.rotate(angle, expand=True, resample=Image.BICUBIC)
    if alpha < 1.0:
        sp = sp.copy(); sp.putalpha(sp.split()[3].point(lambda v: int(v * alpha)))
    sh = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    a = sp.split()[3].point(lambda v: int(v * 0.45 * alpha))
    shimg = Image.new("RGBA", sp.size, (40, 22, 12, 0)); shimg.putalpha(a)
    px = int(cx - sp.width / 2); py = int(cy - sp.height / 2)
    sh.paste(shimg, (px + 10, py + 16), shimg)
    sh = sh.filter(ImageFilter.GaussianBlur(12))
    frame.alpha_composite(sh)
    frame.alpha_composite(sp, (px, py))


def bg_cream():
    img = Image.new("RGB", (W, H), CREMA)
    d = ImageDraw.Draw(img)
    # vineta suave + acento celeste arriba
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for y in range(300):
        od.line([(0, y), (W, y)], fill=(*CELESTE, int(36 * (1 - y / 300))))
    img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
    return img


def frame_index_writer():
    idx = 0
    def w(img):
        nonlocal idx
        img.convert("RGB").save(WORK / f"f{idx:04d}.png"); idx += 1
        return idx
    return w


def main():
    tile = make_tile()
    th = tile.height
    write = frame_index_writer()

    # ---------- Escena 1: "No es lo mismo un triplete..." ----------
    base1 = bg_cream()
    n = int(2.6 * FPS)
    f_small = ImageFont.truetype(F_PLAY, 70); f_big = ImageFont.truetype(F_RYE, 104)
    for k in range(n):
        t = k / FPS
        fr = base1.copy().convert("RGBA"); d = ImageDraw.Draw(fr)
        a = min(1.0, t / 0.4)
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        ctext(od, 760, "No es lo mismo", f_small, CACAO)
        ctext(od, 880, "un triplete…", f_big, BORDO)
        ov.putalpha(ov.split()[3].point(lambda v: int(v * a)))
        fr = Image.alpha_composite(fr, ov)
        write(fr)

    # ---------- Escena 2: marcador animado (letras caen + goles 0->1->2->3) ----------
    FROM_Y = -220
    f_name = mont(54, 800); f_dig = mont(150, 800); f_eyeb = mont(30, 700); f_trip = mont(64, 800)
    NAMES_Y = 820; SCORE_Y = 940; CX = W // 2
    goals = [1.65, 2.25, 2.85]
    n = int(4.7 * FPS)

    def fy(rest, delay, t, dur=0.5):
        if t <= delay: return FROM_Y
        u = min(1.0, (t - delay) / dur)
        return FROM_Y + (rest - FROM_Y) * bounce(u)

    def word_fall(d, word, x0, rest_y, f, fill, t, t0, per=0.045):
        x = x0
        for i, ch in enumerate(word):
            d.text((x, fy(rest_y, t0 + i * per, t)), ch, font=f, fill=fill)
            x += d.textlength(ch, font=f)

    for k in range(n):
        t = k / FPS
        fr = Image.new("RGBA", (W, H), (*TINTA, 255)); d = ImageDraw.Draw(fr)
        d.rectangle([0, 0, W, 70], fill=CELESTE); d.rectangle([0, H - 70, W, H], fill=CELESTE)
        ctext(d, 700, "EL ÚLTIMO PARTIDO", f_eyeb, MOSTAZA)
        # nombres (caen letra a letra)
        word_fall(d, "ARGENTINA", 150, NAMES_Y, f_name, BLANCO, t, 0.0)
        wadel = sum(d.textlength(c, font=f_name) for c in "ARGELIA")
        word_fall(d, "ARGELIA", int(W - 150 - wadel), NAMES_Y, f_name, BLANCO, t, 0.45)
        # guion + marcador derecha (caen)
        dy = fy(SCORE_Y, 0.75, t); d.text((CX - d.textlength("-", font=f_dig) / 2, dy), "-", font=f_dig, fill=CREMA)
        ry = fy(SCORE_Y, 0.85, t); d.text((CX + 150 - d.textlength("0", font=f_dig) / 2, ry), "0", font=f_dig, fill=CREMA)
        # marcador Argentina: 0 al inicio, luego 1/2/3 (cada gol cae)
        val = sum(1 for g in goals if t >= g)
        last = 0.8
        for g in goals:
            if t >= g: last = g
        ly = fy(SCORE_Y, last, t, dur=0.42)
        ds = str(val); d.text((CX - 150 - d.textlength(ds, font=f_dig) / 2, ly), ds, font=f_dig, fill=CELESTE)
        # ¡TRIPLETE! tras el 3er gol
        if t >= goals[-1] + 0.45:
            a = min(1.0, (t - goals[-1] - 0.45) / 0.4)
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
            ctext(od, 1200, "¡TRIPLETE!", f_trip, MOSTAZA, sh=(0, 0, 0))
            ov.putalpha(ov.split()[3].point(lambda v: int(v * a))); fr = Image.alpha_composite(fr, ov)
        write(fr)

    # ---------- Escena 3: "...que un triplete" + 3 sándwiches cayendo ----------
    base3 = bg_cream()
    n = int(3.6 * FPS)
    f_small = ImageFont.truetype(F_PLAY, 70); f_big = ImageFont.truetype(F_RYE, 104)
    cx = W // 2; base_y = 1360; overlap = int(th * 0.72)
    start_y = 560  # caen desde abajo del título (no lo cruzan)
    # destinos (de abajo hacia arriba): el 1ero abajo, los otros encima
    dests = [(cx - 22, base_y, -5), (cx + 26, base_y - overlap, 4), (cx - 8, base_y - 2 * overlap, -3)]
    starts = [0.25, 0.78, 1.31]; FALLD = 0.60
    for k in range(n):
        t = k / FPS
        fr = base3.copy().convert("RGBA"); d = ImageDraw.Draw(fr)
        # texto arriba
        ta = min(1.0, t / 0.4)
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        ctext(od, 300, "…que un triplete", f_big, BORDO)
        ctext(od, 430, "de Mendieta", f_small, CACAO)
        ov.putalpha(ov.split()[3].point(lambda v: int(v * ta)))
        fr = Image.alpha_composite(fr, ov)
        # sándwiches cayendo (desde start_y, con fade-in rápido)
        for (dx, dy, ang), st in zip(dests, starts):
            if t < st: continue
            u = min(1.0, (t - st) / FALLD)
            y = start_y + (dy - start_y) * bounce(u)
            al = min(1.0, (t - st) / 0.12)
            paste_with_shadow(fr, tile, dx, y, ang, alpha=al)
        write(fr)

    # ---------- Escena 4: CTA pedido ----------
    base4 = bg_cream(); n = int(4.0 * FPS)
    for k in range(n):
        t = k / FPS
        fr = base4.copy().convert("RGBA"); d = ImageDraw.Draw(fr)
        a = min(1.0, t / 0.4)
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        ctext(od, 470, "ARGENTINA VS AUSTRIA · LUNES 19H", mont(32, 700), BORDO)
        ctext(od, 560, "Hacé tu pedido", ImageFont.truetype(F_RYE, 100), BORDO)
        ctext(od, 700, "y viví el Mundial como en casa", ImageFont.truetype(F_PLAY, 52), CACAO)
        # pildora 24h
        tt = "Encargá con 24h de antelación"; fp = mont(38, 700)
        wp = od.textlength(tt, font=fp); pw = wp + 96; pxp = (W - pw) // 2; yp = 860
        od.rounded_rectangle([pxp, yp, pxp + pw, yp + 90], radius=45, fill=MOSTAZA)
        od.text(((W - wp) // 2, yp + 24), tt, font=fp, fill=CACAO)
        ctext(od, 1010, "WhatsApp", mont(40, 700), CACAO)
        ctext(od, 1066, "696 98 53 85", ImageFont.truetype(F_RYE, 96), BORDO)
        ctext(od, 1230, "Pagá con Bizum o transferencia", mont(40, 600), CACAO)
        ctext(od, 1320, "@pasteleriamendieta", mont(38, 700), BORDO)
        ov.putalpha(ov.split()[3].point(lambda v: int(v * a)))
        fr = Image.alpha_composite(fr, ov)
        write(fr)

    r = subprocess.run([FF, "-y", "-framerate", str(FPS), "-i", str(WORK / "f%04d.png"),
                        "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                        "-pix_fmt", "yuv420p", str(OUT)], capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG ERROR\n", r.stderr[-1600:]); raise SystemExit(1)
    nframes = len(list(WORK.glob("f*.png")))
    print(f"OK: {OUT} ({OUT.stat().st_size//1024} KB, {nframes} frames, {nframes/FPS:.1f}s)")


if __name__ == "__main__":
    main()
