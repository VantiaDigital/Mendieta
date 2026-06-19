#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mendieta — Reel triplete PRO (sin voz, solo música).

Estructura:
  - Resultado (0-3.4s): fondo BANDERA real + marcador ARGENTINA 0-0 ARGELIA -> 3-0 ¡TRIPLETE!
  - Transición (crossfade) a un fondo premium oscuro cálido.
  - "Que un triplete de Mendieta": caen 3 sándwiches de a uno sobre ese fondo.
  - CTA: Argentina vs Austria · lunes 19h · 24h · WhatsApp · Bizum.
Audio: SOLO la canción de la carpeta (Spring). La voz la pone Facu después.
Las letras marcan el ritmo (Facu lee siguiendo las letras).

Salida: 6 partido-austria/FINAL/reel-triplete-pro.mp4
"""
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

FF = r"C:/Users/facun/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.1-full_build/bin/ffmpeg.exe"
M = Path(r"C:/Users/facun/Documentos/Vantia Digital/Clientes/Mendieta")
FLAG = M / "6 partido-austria" / "assets" / "bandera-recap.mp4"
TILESRC = M / "1 material-bruto" / "IMG_1364.JPG"
SONG = M / "6 partido-austria" / "assets" / "Spring (From The Four Seasons By Vivaldi).mp4"
FINAL = M / "6 partido-austria" / "FINAL"; FINAL.mkdir(parents=True, exist_ok=True)
TMP = Path(r"C:/Users/facun/AppData/Local/Temp/mendieta-triplete-pro")
WORK = TMP / "frames"; FLAGF = TMP / "flag"
WORK.mkdir(parents=True, exist_ok=True); FLAGF.mkdir(parents=True, exist_ok=True)
OUT = FINAL / "reel-triplete-pro.mp4"

W, H = 1080, 1920
FPS = 30; DUR = 12.0
CREMA = (251, 244, 198); BORDO = (119, 35, 27); CACAO = (83, 49, 24)
MOSTAZA = (237, 199, 125); CELESTE = (130, 180, 226); SHADOW = (8, 5, 3)
F_RYE = r"C:/Users/facun/AppData/Local/Temp/Rye.ttf"
F_PLAY = r"C:/Users/facun/AppData/Local/Temp/PlayfairBlack.ttf"
F_MONT = r"C:/Users/facun/AppData/Local/Temp/Montserrat.ttf"

T1 = 3.4; XF = 0.5  # fin del resultado / crossfade a fondo oscuro


def mont(s, w=700):
    f = ImageFont.truetype(F_MONT, s); f.set_variation_by_axes([w]); return f
def bounce(u):
    n, d = 7.5625, 2.75
    if u < 1/d: return n*u*u
    if u < 2/d: u -= 1.5/d; return n*u*u+0.75
    if u < 2.5/d: u -= 2.25/d; return n*u*u+0.9375
    u -= 2.625/d; return n*u*u+0.984375
def eoc(u): return 1-(1-u)**3


def extract_flag():
    if not any(FLAGF.glob("*.png")):
        subprocess.run([FF, "-y", "-i", str(FLAG), "-vf", f"fps={FPS}",
                        str(FLAGF / "f%03d.png")], capture_output=True)
    return sorted(FLAGF.glob("*.png"))


def dark_bg():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = W/2, 1180
    d = np.sqrt(((xx-cx)/(W*0.72))**2 + ((yy-cy)/(H*0.52))**2)
    glow = np.clip(1.0-d, 0, 1)[..., None]
    warm = np.array([74, 50, 30]); dark = np.array([15, 10, 7])
    bg = dark + glow*(warm-dark)
    return Image.fromarray(np.clip(bg, 0, 255).astype("uint8"))


def make_tile():
    im = Image.open(TILESRC).convert("RGB"); Wp, Hp = im.size
    t = im.crop((int(.11*Wp), int(.54*Hp), int(.73*Wp), int(.80*Hp)))
    t = ImageEnhance.Color(t).enhance(1.12); t = ImageEnhance.Contrast(t).enhance(1.08)
    tw = 580; t = t.resize((tw, int(t.height*tw/t.width)), Image.LANCZOS); th = t.height
    mask = Image.new("L", (tw, th), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, tw, th], radius=32, fill=255)
    tile = Image.new("RGBA", (tw, th), (0, 0, 0, 0)); tile.paste(t, (0, 0), mask)
    ImageDraw.Draw(tile).rounded_rectangle([1, 1, tw-2, th-2], radius=32, outline=(255, 250, 232, 240), width=4)
    return tile


def paste_shadow(frame, sprite, cx, cy, ang, alpha=1.0):
    sp = sprite.rotate(ang, expand=True, resample=Image.BICUBIC)
    if alpha < 1.0: sp = sp.copy(); sp.putalpha(sp.split()[3].point(lambda v: int(v*alpha)))
    sh = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    shimg = Image.new("RGBA", sp.size, (0, 0, 0, 0)); shimg.putalpha(sp.split()[3].point(lambda v: int(v*0.55*alpha)))
    px = int(cx-sp.width/2); py = int(cy-sp.height/2)
    sh.paste(shimg, (px+10, py+18), shimg); sh = sh.filter(ImageFilter.GaussianBlur(16))
    frame.alpha_composite(sh); frame.alpha_composite(sp, (px, py))


def fit(text, path, maxw=940, hi=92, lo=48):
    d = ImageDraw.Draw(Image.new("RGB", (4, 4))); s = hi
    while s > lo:
        f = ImageFont.truetype(path, s)
        if d.textlength(text, font=f) <= maxw: return f
        s -= 2
    return ImageFont.truetype(path, lo)


FROM = -200
def caption(layer, lines, cy, fontpath, t, t0, scrim=True):
    d = ImageDraw.Draw(layer)
    fonts = [fit(l, fontpath) for l in lines]
    hs = [f.getmetrics()[0]+f.getmetrics()[1] for f in fonts]
    gl = 16; total = sum(hs)+gl*(len(lines)-1); y = cy-total//2
    if scrim:
        d.rounded_rectangle([60, y-34, W-60, y+total+34], radius=36, fill=(10, 8, 6, 120))
    ci = 0
    for ln, f, hh in zip(lines, fonts, hs):
        wln = d.textlength(ln, font=f); x = (W-wln)/2
        for ch in ln:
            cw = d.textlength(ch, font=f); delay = t0+ci*0.035
            yy = (FROM+(y-FROM)*bounce(min(1.0, (t-delay)/0.5))) if t >= delay else FROM
            d.text((x+2, yy+3), ch, font=f, fill=SHADOW, stroke_width=4, stroke_fill=SHADOW)
            d.text((x, yy), ch, font=f, fill=CREMA, stroke_width=4, stroke_fill=SHADOW)
            x += cw; ci += 1
        y += hh+gl


def scoreboard(layer, t, t0):
    d = ImageDraw.Draw(layer); cy = 940
    d.rounded_rectangle([90, cy-92, W-90, cy+152], radius=40, fill=(10, 8, 6, 185))
    goals = [t0+0.9, t0+1.4, t0+1.9]; val = sum(1 for g in goals if t >= g)
    fn = mont(46, 800); fd = mont(120, 800)
    d.text((150, cy-66), "ARGENTINA", font=fn, fill=CREMA, stroke_width=3, stroke_fill=SHADOW)
    wadel = d.textlength("ARGELIA", font=fn); d.text((W-150-wadel, cy-66), "ARGELIA", font=fn, fill=CREMA, stroke_width=3, stroke_fill=SHADOW)
    cx = W//2
    d.text((cx-d.textlength("-", font=fd)/2, cy-10), "-", font=fd, fill=CREMA, stroke_width=4, stroke_fill=SHADOW)
    d.text((cx+140-d.textlength("0", font=fd)/2, cy-10), "0", font=fd, fill=CREMA, stroke_width=4, stroke_fill=SHADOW)
    last = t0+0.1
    for g in goals:
        if t >= g: last = g
    ly = (cy-10)-60*(1-bounce(min(1.0, (t-last)/0.34)))
    d.text((cx-140-d.textlength(str(val), font=fd)/2, ly), str(val), font=fd, fill=CELESTE, stroke_width=4, stroke_fill=SHADOW)
    if t >= goals[-1]+0.45:
        a = min(1.0, (t-goals[-1]-0.45)/0.4)
        ft = mont(58, 800); tw = d.textlength("¡TRIPLETE!", font=ft)
        # (alpha lo maneja el caller con el fade del bloque resultado)
        d.text(((W-tw)/2, 1110), "¡TRIPLETE!", font=ft, fill=MOSTAZA, stroke_width=3, stroke_fill=SHADOW)


def main():
    flagframes = extract_flag(); nf = len(flagframes)
    flag_cache = [ImageEnhance.Brightness(Image.open(p).convert("RGB")).enhance(0.72) for p in flagframes]
    dbg = dark_bg(); tile = make_tile()
    cx = W//2
    s_dest = [(cx-34, 1240, -6), (cx+50, 1175, 6), (cx-6, 1120, -3)]
    s_start = [4.05, 4.85, 5.65]; SFALL = 0.62; SFROM = 740

    n = int(DUR*FPS)
    for k in range(n):
        t = k/FPS
        # ---- fondo ----
        if t < T1:
            base = flag_cache[k % nf].copy()
        elif t < T1+XF:
            a = (t-T1)/XF
            base = Image.blend(flag_cache[k % nf], dbg, a)
        else:
            base = dbg.copy()
        frame = base.convert("RGBA")

        # ---- resultado (bandera): marcador + caption ----
        if t <= T1+XF:
            a = 1.0
            if t > T1: a = max(0.0, 1.0-(t-T1)/XF)
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            caption(lay, ["No es lo mismo un triplete"], 470, F_PLAY, t, 0.3)
            scoreboard(lay, t, 0.4)
            if a < 1.0: lay.putalpha(lay.split()[3].point(lambda v: int(v*a)))
            frame = Image.alpha_composite(frame, lay)

        # ---- parte sándwiches / Mendieta ----
        if t >= T1+XF-0.1:
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            # caption "Que un triplete de Mendieta" (3.85-6.8)
            if 3.95 <= t <= 7.0:
                fa = 1.0
                if t > 6.6: fa = max(0.0, (7.0-t)/0.4)
                cl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                caption(cl, ["Que un triplete", "de Mendieta"], 470, F_RYE, t, 3.95, scrim=False)
                if fa < 1.0: cl.putalpha(cl.split()[3].point(lambda v: int(v*fa)))
                lay = Image.alpha_composite(lay, cl)
            frame = Image.alpha_composite(frame, lay)
            # sándwiches cayendo de a uno
            for (dx, dy, ang), st in zip(s_dest, s_start):
                if t < st: continue
                u = min(1.0, (t-st)/SFALL); y = SFROM+(dy-SFROM)*bounce(u)
                paste_shadow(frame, tile, dx, y, ang, alpha=min(1.0, (t-st)/0.12))

        # ---- CTA ----
        if t >= 7.2:
            a = min(1.0, (t-7.2)/0.5)
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
            cc = lambda y, tx, f, fl: d.text(((W-d.textlength(tx, font=f))/2, y), tx, font=f, fill=fl, stroke_width=3, stroke_fill=SHADOW)
            cc(360, "Pedí para el partido", mont(40, 700), MOSTAZA)
            cc(420, "Argentina vs Austria · lunes 19h", mont(46, 800), CREMA)
            d.rounded_rectangle([70, 1500, W-70, 1800], radius=44, fill=(10, 8, 6, 150))
            cc(1528, "Encargá con 24h · pago por anticipado", mont(32, 700), CREMA)
            cc(1584, "WhatsApp", mont(36, 700), MOSTAZA)
            cc(1632, "696 98 53 85", ImageFont.truetype(F_RYE, 80), CREMA)
            cc(1742, "Bizum o transferencia · @pasteleriamendieta", mont(29, 600), CREMA)
            if a < 1.0: lay.putalpha(lay.split()[3].point(lambda v: int(v*a)))
            frame = Image.alpha_composite(frame, lay)

        frame.convert("RGB").save(WORK / f"f{k:04d}.png")

    # encode + SOLO musica (Spring), volumen moderado para que entre la voz despues
    r = subprocess.run([FF, "-y", "-framerate", str(FPS), "-i", str(WORK / "f%04d.png"),
                        "-stream_loop", "-1", "-i", str(SONG),
                        "-map", "0:v", "-map", "1:a", "-af", "volume=0.6",
                        "-t", str(DUR), "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", str(OUT)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG ERROR\n", r.stderr[-1800:]); raise SystemExit(1)
    print(f"OK: {OUT} ({OUT.stat().st_size//1024} KB, {DUR}s, solo musica)")


if __name__ == "__main__":
    main()
