#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mendieta — Reel triplete v3: voz en off + fondo bandera + marcador del
resultado SOBRE la bandera + sándwiches cayendo de a uno + música por debajo.

Estructura (sobre fondo bandera argentina todo el tiempo):
  - "No es lo mismo un triplete": marcador ARGENTINA 0-0 ARGELIA -> 3-0 ¡TRIPLETE!
  - "que un triplete de Mendieta": caen 3 sándwiches de miga de a uno.
  - "pedí... vivi el Mundial como en casa": CTA (24h, WhatsApp, Bizum).
Audio: voz en off + canción (Spring) por debajo, a volumen bajo.

Si hay una grabación propia en assets (vo-*.* / voz*.*) la usa; si no, TTS.
Salida: 6 partido-austria/FINAL/reel-triplete-vo.mp4
"""
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

FF = r"C:/Users/facun/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.1-full_build/bin/ffmpeg.exe"
M = Path(r"C:/Users/facun/Documentos/Vantia Digital/Clientes/Mendieta")
FLAG = M / "6 partido-austria" / "assets" / "bandera-recap.mp4"   # bandera real extraida del recap
TILESRC = M / "1 material-bruto" / "IMG_1364.JPG"
ASSETS = M / "6 partido-austria" / "assets"
SONG = ASSETS / "Spring (From The Four Seasons By Vivaldi).mp4"
FINAL = M / "6 partido-austria" / "FINAL"; FINAL.mkdir(parents=True, exist_ok=True)
WORK = Path(r"C:/Users/facun/AppData/Local/Temp/mendieta-triplete-vo/ov")
WORK.mkdir(parents=True, exist_ok=True)
OUT = FINAL / "reel-triplete-vo.mp4"

W, H = 1080, 1920
FPS = 30; DUR = 14.0
CREMA = (251, 244, 198); BORDO = (119, 35, 27); CACAO = (83, 49, 24)
MOSTAZA = (237, 199, 125); CELESTE = (130, 180, 226); SHADOW = (8, 5, 3)
F_RYE = r"C:/Users/facun/AppData/Local/Temp/Rye.ttf"
F_PLAY = r"C:/Users/facun/AppData/Local/Temp/PlayfairBlack.ttf"
F_MONT = r"C:/Users/facun/AppData/Local/Temp/Montserrat.ttf"


def mont(s, w=700):
    f = ImageFont.truetype(F_MONT, s); f.set_variation_by_axes([w]); return f
def bounce(u):
    n, d = 7.5625, 2.75
    if u < 1/d: return n*u*u
    if u < 2/d: u -= 1.5/d; return n*u*u+0.75
    if u < 2.5/d: u -= 2.25/d; return n*u*u+0.9375
    u -= 2.625/d; return n*u*u+0.984375


def find_vo():
    for pat in ("vo-*", "voz*", "VOZ*"):
        for f in ASSETS.glob(pat):
            if f.suffix.lower() in (".mp3", ".m4a", ".wav", ".aac", ".ogg"):
                return f, True
    return ASSETS / "vo_tomas.mp3", False


def make_tile():
    im = Image.open(TILESRC).convert("RGB"); Wp, Hp = im.size
    t = im.crop((int(.11*Wp), int(.54*Hp), int(.73*Wp), int(.80*Hp)))
    t = ImageEnhance.Color(t).enhance(1.1); t = ImageEnhance.Contrast(t).enhance(1.06)
    tw = 560; t = t.resize((tw, int(t.height*tw/t.width)), Image.LANCZOS); th = t.height
    mask = Image.new("L", (tw, th), 0); ImageDraw.Draw(mask).rounded_rectangle([0,0,tw,th], radius=30, fill=255)
    tile = Image.new("RGBA", (tw, th), (0,0,0,0)); tile.paste(t, (0,0), mask)
    ImageDraw.Draw(tile).rounded_rectangle([1,1,tw-2,th-2], radius=30, outline=(255,250,230,235), width=4)
    return tile


def paste_shadow(frame, sprite, cx, cy, ang, alpha=1.0):
    sp = sprite.rotate(ang, expand=True, resample=Image.BICUBIC)
    if alpha < 1.0: sp = sp.copy(); sp.putalpha(sp.split()[3].point(lambda v: int(v*alpha)))
    sh = Image.new("RGBA", frame.size, (0,0,0,0))
    shimg = Image.new("RGBA", sp.size, (10,6,3,0)); shimg.putalpha(sp.split()[3].point(lambda v: int(v*0.5*alpha)))
    px = int(cx-sp.width/2); py = int(cy-sp.height/2)
    sh.paste(shimg, (px+8, py+14), shimg); sh = sh.filter(ImageFilter.GaussianBlur(14))
    frame.alpha_composite(sh); frame.alpha_composite(sp, (px, py))


def fit(text, path, maxw=940, hi=96, lo=46):
    d = ImageDraw.Draw(Image.new("RGB", (4,4))); s = hi
    while s > lo:
        f = ImageFont.truetype(path, s)
        if d.textlength(text, font=f) <= maxw: return f
        s -= 2
    return ImageFont.truetype(path, lo)


FROM = -200
def draw_caption(layer, lines, cy, fontpath, t, t0, big=True):
    d = ImageDraw.Draw(layer)
    fonts = [fit(l, fontpath, hi=(92 if big else 60)) for l in lines]
    hs = [f.getmetrics()[0]+f.getmetrics()[1] for f in fonts]
    gl = 16; total = sum(hs)+gl*(len(lines)-1); y = cy-total//2
    ImageDraw.Draw(layer).rounded_rectangle([60, y-36, W-60, y+total+36], radius=38, fill=(10,8,6,120))
    ci = 0
    for ln, f, hh in zip(lines, fonts, hs):
        wln = d.textlength(ln, font=f); x = (W-wln)/2
        for ch in ln:
            cw = d.textlength(ch, font=f); delay = t0+ci*0.035
            yy = (FROM + (y-FROM)*bounce(min(1.0,(t-delay)/0.5))) if t >= delay else FROM
            d.text((x+2, yy+3), ch, font=f, fill=SHADOW, stroke_width=4, stroke_fill=SHADOW)
            d.text((x, yy), ch, font=f, fill=CREMA, stroke_width=4, stroke_fill=SHADOW)
            x += cw; ci += 1
        y += hh+gl


def draw_scoreboard(layer, t, t0):
    """Marcador sobre la bandera: ARGENTINA [N] - 0 ARGELIA, 0->3, ¡TRIPLETE!"""
    d = ImageDraw.Draw(layer)
    cy = 940
    d.rounded_rectangle([90, cy-90, W-90, cy+150], radius=40, fill=(10,8,6,180))
    goals = [t0+0.9, t0+1.4, t0+1.9]
    val = sum(1 for g in goals if t >= g)
    fn = mont(46, 800); fd = mont(120, 800)
    # nombres
    cline = lambda yy, tx, f, fl: d.text(((W-d.textlength(tx, font=f))/2, yy), tx, font=f, fill=fl, stroke_width=3, stroke_fill=SHADOW)
    d.text((150, cy-66), "ARGENTINA", font=fn, fill=CREMA, stroke_width=3, stroke_fill=SHADOW)
    wadel = d.textlength("ARGELIA", font=fn)
    d.text((W-150-wadel, cy-66), "ARGELIA", font=fn, fill=CREMA, stroke_width=3, stroke_fill=SHADOW)
    # score grande centrado
    cx = W//2
    d.text((cx-d.textlength("-", font=fd)/2, cy-10), "-", font=fd, fill=CREMA, stroke_width=4, stroke_fill=SHADOW)
    d.text((cx+140-d.textlength("0", font=fd)/2, cy-10), "0", font=fd, fill=CREMA, stroke_width=4, stroke_fill=SHADOW)
    last = t0+0.1
    for g in goals:
        if t >= g: last = g
    ly = (cy-10) - 60*(1-bounce(min(1.0,(t-last)/0.34)))
    d.text((cx-140-d.textlength(str(val), font=fd)/2, ly), str(val), font=fd, fill=CELESTE, stroke_width=4, stroke_fill=SHADOW)


def main():
    vo, custom = find_vo()
    tile = make_tile()
    caps = [
        (0.10, 2.50, ["No es lo mismo un triplete"], F_PLAY, False, "score"),
        (2.55, 4.74, ["Que un triplete", "de Mendieta"], F_RYE, True, "sandwich"),
        (4.85, 6.40, ["Pedí tus sanguchitos de miga"], F_PLAY, False, None),
        (6.45, 7.70, ["para Argentina vs Austria"], F_PLAY, False, None),
        (7.75, 9.20, ["este lunes a las 19h"], F_PLAY, False, None),
        (9.25, 12.0, ["y viví el Mundial", "como en casa"], F_PLAY, False, None),
    ]
    cap_cy = 480
    cx = W//2
    s_dest = [(cx-30, 1230, -6), (cx+46, 1170, 6), (cx-8, 1115, -3)]
    s_start = [2.95, 3.65, 4.35]; SFALL = 0.6; SFROM = 760

    n = int(DUR*FPS)
    for k in range(n):
        t = k/FPS
        ov = Image.new("RGBA", (W, H), (0,0,0,0))
        for (t0, te, lines, fp, big, extra) in caps:
            if t0-0.6 <= t <= te+0.35:
                a = 1.0
                if t > te: a = max(0.0, (te+0.35-t)/0.35)
                if t < t0: a = min(1.0, (t-(t0-0.6))/0.6)
                lay = Image.new("RGBA", (W, H), (0,0,0,0))
                draw_caption(lay, lines, cap_cy, fp, t, t0, big)
                if a < 1.0: lay.putalpha(lay.split()[3].point(lambda v: int(v*a)))
                ov = Image.alpha_composite(ov, lay)
        # marcador (sobre la bandera) durante la 1a frase
        if 0.35 <= t <= 2.75:
            a = 1.0
            if t > 2.5: a = max(0.0, (2.75-t)/0.25)
            lay = Image.new("RGBA", (W, H), (0,0,0,0)); draw_scoreboard(lay, t, 0.4)
            if t >= 2.25:
                d2 = ImageDraw.Draw(lay)
                tw2 = d2.textlength("¡TRIPLETE!", font=mont(58, 800))
                d2.text(((W-tw2)/2, 1110), "¡TRIPLETE!", font=mont(58, 800), fill=MOSTAZA, stroke_width=3, stroke_fill=SHADOW)
            if a < 1.0: lay.putalpha(lay.split()[3].point(lambda v: int(v*a)))
            ov = Image.alpha_composite(ov, lay)
        # sándwiches (durante "que un triplete de Mendieta" y resto)
        for (dx, dy, ang), st in zip(s_dest, s_start):
            if t < st: continue
            u = min(1.0, (t-st)/SFALL); y = SFROM + (dy-SFROM)*bounce(u)
            paste_shadow(ov, tile, dx, y, ang, alpha=min(1.0,(t-st)/0.12))
        # CTA abajo
        if t >= 9.8:
            a = min(1.0, (t-9.8)/0.5)
            lay = Image.new("RGBA", (W, H), (0,0,0,0)); d = ImageDraw.Draw(lay)
            d.rounded_rectangle([70, 1470, W-70, 1800], radius=46, fill=(10,8,6,160))
            cc = lambda y, tx, f, fl: d.text(((W-d.textlength(tx, font=f))/2, y), tx, font=f, fill=fl, stroke_width=3, stroke_fill=SHADOW)
            cc(1500, "Encargá con 24h · pago por anticipado", mont(33,700), CREMA)
            cc(1556, "WhatsApp", mont(38,700), MOSTAZA)
            cc(1606, "696 98 53 85", ImageFont.truetype(F_RYE, 84), CREMA)
            cc(1726, "Bizum o transferencia · @pasteleriamendieta", mont(30,600), CREMA)
            if a < 1.0: lay.putalpha(lay.split()[3].point(lambda v: int(v*a)))
            ov = Image.alpha_composite(ov, lay)
        ov.save(WORK / f"f{k:04d}.png")

    fc = (f"[0:v]scale={W}:{H},fps={FPS},setsar=1,eq=brightness=-0.13:saturation=0.96[bg];"
          f"[bg][1:v]overlay=0:0:format=auto,format=yuv420p[v];"
          f"[2:a]volume=1.0[vo];[3:a]volume=0.16[mus];"
          f"[vo][mus]amix=inputs=2:duration=longest:dropout_transition=0[a]")
    r = subprocess.run([FF, "-y", "-stream_loop", "-1", "-i", str(FLAG),
                        "-framerate", str(FPS), "-i", str(WORK / "f%04d.png"),
                        "-i", str(vo), "-stream_loop", "-1", "-i", str(SONG),
                        "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", str(DUR),
                        "-c:v", "libx264", "-preset", "slow", "-crf", "17",
                        "-c:a", "aac", "-b:a", "160k", str(OUT)], capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG ERROR\n", r.stderr[-1800:]); raise SystemExit(1)
    print(f"OK: {OUT} ({OUT.stat().st_size//1024} KB) — voz: {'PROPIA ('+vo.name+')' if custom else 'TTS Tomas (preview)'} + cancion")


if __name__ == "__main__":
    main()
