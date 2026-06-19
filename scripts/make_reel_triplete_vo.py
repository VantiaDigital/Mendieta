#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mendieta — Reel triplete v2: voz en off + letras cayendo + fondo bandera
argentina + sándwiches cayendo de a uno.

Fondo: bandera argentina flameando (fondo-argentina.mp4, loop).
VO: edge-tts es-AR (Tomás), incrustada. Las letras = el caption, caen en
sync con la voz. Después caen 3 sándwiches de miga reales, individuales.

Salida: Documentos/Mendieta/partido-austria/FINAL/reel-triplete-vo.mp4
"""
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

FF = r"C:/Users/facun/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.1-full_build/bin/ffmpeg.exe"
PROD = Path(r"C:/Users/facun/Documentos/Mendieta/reel-mundial/productos")
PA = Path(r"C:/Users/facun/Documentos/Mendieta/partido-austria")
FLAG = Path(r"C:/Users/facun/Documentos/Mendieta/reel-mundial/editados/fondo-argentina.mp4")
VO = PA / "assets" / "vo_tomas.mp3"
FINAL = PA / "FINAL"; FINAL.mkdir(parents=True, exist_ok=True)
WORK = Path(r"C:/Users/facun/AppData/Local/Temp/mendieta-triplete-vo/ov")
WORK.mkdir(parents=True, exist_ok=True)
OUT = FINAL / "reel-triplete-vo.mp4"

W, H = 1080, 1920
FPS = 30
DUR = 14.0
CREMA = (251, 244, 198); BORDO = (119, 35, 27); CACAO = (83, 49, 24)
MOSTAZA = (237, 199, 125); SHADOW = (8, 5, 3)
F_RYE = r"C:/Users/facun/AppData/Local/Temp/Rye.ttf"
F_PLAY = r"C:/Users/facun/AppData/Local/Temp/PlayfairBlack.ttf"
F_MONT = r"C:/Users/facun/AppData/Local/Temp/Montserrat.ttf"


def mont(s, w=700):
    f = ImageFont.truetype(F_MONT, s); f.set_variation_by_axes([w]); return f
def bounce(u):
    n, d = 7.5625, 2.75
    if u < 1 / d: return n * u * u
    if u < 2 / d: u -= 1.5 / d; return n * u * u + 0.75
    if u < 2.5 / d: u -= 2.25 / d; return n * u * u + 0.9375
    u -= 2.625 / d; return n * u * u + 0.984375


def make_tile():
    im = Image.open(PROD / "IMG_1364.JPG").convert("RGB"); Wp, Hp = im.size
    t = im.crop((int(.11 * Wp), int(.54 * Hp), int(.73 * Wp), int(.80 * Hp)))
    t = ImageEnhance.Color(t).enhance(1.1); t = ImageEnhance.Contrast(t).enhance(1.06)
    tw = 560; t = t.resize((tw, int(t.height * tw / t.width)), Image.LANCZOS); th = t.height
    mask = Image.new("L", (tw, th), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, tw, th], radius=30, fill=255)
    tile = Image.new("RGBA", (tw, th), (0, 0, 0, 0)); tile.paste(t, (0, 0), mask)
    ImageDraw.Draw(tile).rounded_rectangle([1, 1, tw - 2, th - 2], radius=30, outline=(255, 250, 230, 235), width=4)
    return tile


def paste_shadow(frame, sprite, cx, cy, ang, alpha=1.0):
    sp = sprite.rotate(ang, expand=True, resample=Image.BICUBIC)
    if alpha < 1.0:
        sp = sp.copy(); sp.putalpha(sp.split()[3].point(lambda v: int(v * alpha)))
    sh = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    shimg = Image.new("RGBA", sp.size, (10, 6, 3, 0)); shimg.putalpha(sp.split()[3].point(lambda v: int(v * 0.5 * alpha)))
    px = int(cx - sp.width / 2); py = int(cy - sp.height / 2)
    sh.paste(shimg, (px + 8, py + 14), shimg); sh = sh.filter(ImageFilter.GaussianBlur(14))
    frame.alpha_composite(sh); frame.alpha_composite(sp, (px, py))


def fit(text, path, maxw=940, hi=96, lo=46):
    d = ImageDraw.Draw(Image.new("RGB", (4, 4))); s = hi
    while s > lo:
        f = ImageFont.truetype(path, s)
        if d.textlength(text, font=f) <= maxw: return f
        s -= 2
    return ImageFont.truetype(path, lo)


FROM = -200
def draw_caption(layer, lines, cy, fontpath, t, t0, t_end, big=True):
    """Letras cayendo: cada char cae desde arriba con stagger; fade-out al final."""
    d = ImageDraw.Draw(layer)
    fonts = [fit(l, fontpath, hi=(96 if big else 64)) for l in lines]
    hs = [f.getmetrics()[0] + f.getmetrics()[1] for f in fonts]
    gl = 18; total = sum(hs) + gl * (len(lines) - 1); y = cy - total // 2
    # scrim suave detrás
    pad = 40
    sd = ImageDraw.Draw(layer)
    sd.rounded_rectangle([60, y - pad, W - 60, y + total + pad], radius=40, fill=(10, 8, 6, 120))
    ci = 0
    for li, (ln, f, hh) in enumerate(zip(lines, fonts, hs)):
        wln = d.textlength(ln, font=f); x = (W - wln) / 2
        for ch in ln:
            cw = d.textlength(ch, font=f)
            delay = t0 + ci * 0.035
            if t >= delay:
                u = min(1.0, (t - delay) / 0.5); yy = FROM + (y - FROM) * bounce(u)
            else:
                yy = FROM
            d.text((x + 2, yy + 3), ch, font=f, fill=SHADOW, stroke_width=4, stroke_fill=SHADOW)
            d.text((x, yy), ch, font=f, fill=CREMA, stroke_width=4, stroke_fill=SHADOW)
            x += cw; ci += 1
        y += hh + gl


def main():
    tile = make_tile(); th = tile.height
    caps = [
        (0.10, 2.50, ["No es lo mismo", "un triplete"], F_RYE, True),
        (2.55, 4.74, ["Que un triplete", "de Mendieta"], F_RYE, True),
        (4.85, 6.40, ["Pedí tus sanguchitos de miga"], F_PLAY, False),
        (6.45, 7.70, ["para Argentina vs Austria"], F_PLAY, False),
        (7.75, 9.20, ["este lunes a las 19h"], F_PLAY, False),
        (9.25, 12.0, ["y viví el Mundial", "como en casa"], F_PLAY, False),
    ]
    cap_cy = 560
    # sándwiches caen de a uno (en la franja media), durante la parte de pedido
    cx = W // 2
    s_dest = [(cx - 30, 1150, -6), (cx + 46, 1090, 6), (cx - 8, 1035, -3)]
    s_start = [5.1, 6.7, 8.2]; SFALL = 0.6; SFROM = 720

    n = int(DUR * FPS)
    for k in range(n):
        t = k / FPS
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        # captions activos (con fade-out)
        for (t0, te, lines, fp, big) in caps:
            if t0 - 0.6 <= t <= te + 0.35:
                a = 1.0
                if t > te: a = max(0.0, (te + 0.35 - t) / 0.35)
                if t < t0: a = min(1.0, (t - (t0 - 0.6)) / 0.6)
                lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                draw_caption(lay, lines, cap_cy, fp, t, t0, te, big)
                if a < 1.0: lay.putalpha(lay.split()[3].point(lambda v: int(v * a)))
                ov = Image.alpha_composite(ov, lay)
        # sándwiches
        for (dx, dy, ang), st in zip(s_dest, s_start):
            if t < st: continue
            u = min(1.0, (t - st) / SFALL); y = SFROM + (dy - SFROM) * bounce(u)
            al = min(1.0, (t - st) / 0.12)
            paste_shadow(ov, tile, dx, y, ang, alpha=al)
        # CTA abajo (aparece ~10s, se sostiene)
        if t >= 9.8:
            a = min(1.0, (t - 9.8) / 0.5)
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
            d.rounded_rectangle([70, 1470, W - 70, 1800], radius=46, fill=(10, 8, 6, 150))
            def cc(y, tx, f, fill):
                w = d.textlength(tx, font=f); d.text(((W - w) / 2, y), tx, font=f, fill=fill, stroke_width=3, stroke_fill=SHADOW)
            cc(1500, "Encargá con 24h · pago por anticipado", mont(33, 700), CREMA)
            cc(1556, "WhatsApp", mont(38, 700), MOSTAZA)
            cc(1606, "696 98 53 85", ImageFont.truetype(F_RYE, 84), CREMA)
            cc(1726, "Bizum o transferencia · @pasteleriamendieta", mont(30, 600), CREMA)
            if a < 1.0: lay.putalpha(lay.split()[3].point(lambda v: int(v * a)))
            ov = Image.alpha_composite(ov, lay)
        ov.save(WORK / f"f{k:04d}.png")

    fc = (f"[0:v]scale={W}:{H},fps={FPS},setsar=1,eq=brightness=-0.04[bg];"
          f"[bg][1:v]overlay=0:0:format=auto,format=yuv420p[v]")
    r = subprocess.run([FF, "-y", "-stream_loop", "-1", "-i", str(FLAG),
                        "-framerate", str(FPS), "-i", str(WORK / "f%04d.png"),
                        "-i", str(VO), "-filter_complex", fc,
                        "-map", "[v]", "-map", "2:a", "-t", str(DUR),
                        "-c:v", "libx264", "-preset", "slow", "-crf", "17",
                        "-c:a", "aac", "-b:a", "160k", str(OUT)], capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG ERROR\n", r.stderr[-1800:]); raise SystemExit(1)
    print(f"OK: {OUT} ({OUT.stat().st_size//1024} KB, {DUR}s, con VO)")


if __name__ == "__main__":
    main()
