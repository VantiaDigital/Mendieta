#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mendieta — Reel cocas de Sant Joan (solo español).

Fotos reales de las cocas (recortadas de capturas) como fondo apenas oscurecido;
texto crema grande al medio que se ESCRIBE (typewriter con cursor) y se borra.
Una o dos líneas por beat, en español. Cierre con encargo 24h + WhatsApp.

Salida: Documentos/Mendieta/sant-joan/FINAL/reel-santjoan.mp4 (1080x1920, sin audio)
"""
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

FF = r"C:/Users/facun/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.1-full_build/bin/ffmpeg.exe"
SJ = Path(r"C:/Users/facun/Documentos/Mendieta/sant-joan")
REC = SJ / "recortadas"
FINAL = SJ / "FINAL"; FINAL.mkdir(parents=True, exist_ok=True)
WORK = Path(r"C:/Users/facun/AppData/Local/Temp/mendieta-santjoan/frames")
WORK.mkdir(parents=True, exist_ok=True)
OUT = FINAL / "reel-santjoan.mp4"

W, H = 1080, 1920
FPS = 30
CPS = 0.045
DARK = 108
CREMA = (251, 244, 198); MOSTAZA = (237, 199, 125); SHADOW = (12, 7, 3)
F_PLAY = r"C:/Users/facun/AppData/Local/Temp/PlayfairBlack.ttf"
F_RYE = r"C:/Users/facun/AppData/Local/Temp/Rye.ttf"
F_MONT = r"C:/Users/facun/AppData/Local/Temp/Montserrat.ttf"


def mont(s, w=600):
    f = ImageFont.truetype(F_MONT, s); f.set_variation_by_axes([w]); return f


def fit(text, path, maxw=980, hi=98, lo=52):
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    s = hi
    while s > lo:
        f = ImageFont.truetype(path, s)
        if d.textlength(text, font=f) <= maxw:
            return f
        s -= 2
    return ImageFont.truetype(path, lo)


def ensure_crops():
    REC.mkdir(parents=True, exist_ok=True)
    BOX = (305, 28, 980, 886)
    shots = sorted(f for f in (SJ / "fotos").iterdir() if f.suffix.lower() == ".png")
    for i, f in enumerate(shots[:3], 1):
        dst = REC / f"coca{i}.png"
        if not dst.exists():
            Image.open(f).convert("RGB").crop(BOX).save(dst)


def bg_for(photo):
    im = Image.open(photo).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    x = (im.width - W) // 2; y = (im.height - H) // 2
    im = im.crop((x, y, x + W, y + H))
    im = ImageEnhance.Color(im).enhance(1.08)
    im = ImageEnhance.Contrast(im).enhance(1.04)
    return Image.blend(im, Image.new("RGB", (W, H), (0, 0, 0)), DARK / 255.0)


def draw_text(d, x, y, full, shown, font, fill, cursor=False, blink=True):
    sub = full[:shown]
    d.text((x + 3, y + 4), sub, font=font, fill=SHADOW, stroke_width=4, stroke_fill=SHADOW)
    d.text((x, y), sub, font=font, fill=fill, stroke_width=4, stroke_fill=SHADOW)
    if cursor and blink:
        cw = d.textlength(sub, font=font); asc = font.getmetrics()[0]
        d.rectangle([x + cw + 6, y + 8, x + cw + 6 + max(6, font.size // 14), y + asc], fill=CREMA)


def main():
    ensure_crops()
    beats = [
        {"photo": REC / "coca1.png", "lines": ["Se viene Sant Joan"]},
        {"photo": REC / "coca3.png", "lines": ["Nuestras cocas", "recién hechas"]},
        {"photo": REC / "coca2.png", "lines": ["De crema, llardons", "o fruta confitada"]},
        {"photo": REC / "coca1.png", "lines": ["Hacé tu pedido,", "no te quedes sin la tuya"]},
        {"photo": REC / "coca2.png", "lines": ["Encargá con 24h de antelación"],
         "eyebrow": "SANT JOAN · 23 DE JUNIO", "phone": "WhatsApp 696 98 53 85",
         "note": "Pagá con Bizum o transferencia", "last": True},
    ]

    fidx = 0
    GAP = 0.30
    for b in beats:
        bg = bg_for(b["photo"])
        d0 = ImageDraw.Draw(bg)
        lines = b["lines"]
        fonts = [fit(t, F_PLAY) for t in lines]
        widths = [d0.textlength(t, font=f) for t, f in zip(lines, fonts)]
        xs = [int((W - w) // 2) for w in widths]
        hts = [f.getmetrics()[0] + f.getmetrics()[1] for f in fonts]
        gl = 26
        block = sum(hts) + gl * (len(lines) - 1)
        cy = int(H * 0.50)
        ys = []
        yy = cy - block // 2
        for h in hts:
            ys.append(yy); yy += h + gl

        eyebrow = b.get("eyebrow"); phone = b.get("phone"); last = b.get("last", False)
        note = b.get("note")
        feb = mont(34, 600) if eyebrow else None
        fp = ImageFont.truetype(F_RYE, 84) if phone else None
        fnote = mont(40, 600) if note else None

        # tiempos de tipeo por línea
        starts = []; t_acc = 0.0
        for t in lines:
            starts.append(t_acc); t_acc += len(t) * CPS + GAP
        type_end = t_acc - GAP
        PHONE_IN = 0.5 if phone else 0.0
        HOLD = 1.4 if last else 0.95
        FADE = 0.0 if last else 0.42
        dur = type_end + PHONE_IN + HOLD + FADE
        n = int(round(dur * FPS))

        for k in range(n):
            t = k / FPS
            blink = (int(t / 0.5) % 2 == 0)
            a = 1.0
            if not last and t > dur - FADE:
                a = max(0.0, (dur - t) / FADE)

            frame = bg.copy()
            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
            if eyebrow:
                web = d.textlength(eyebrow, font=feb)
                d.text(((W - web) // 2, ys[0] - 110), eyebrow, font=feb, fill=MOSTAZA,
                       stroke_width=3, stroke_fill=SHADOW)
            for i, (ln, f, x, y) in enumerate(zip(lines, fonts, xs, ys)):
                st = starts[i]
                shown = 0 if t < st else min(len(ln), int((t - st) / CPS))
                typing = st <= t < st + len(ln) * CPS
                # cursor en la última línea durante el hold (si no hay phone)
                cur = typing or (i == len(lines) - 1 and t >= type_end and not phone and not last)
                draw_text(d, x, y, ln, shown, f, CREMA, cursor=cur, blink=blink)
            if phone and t >= type_end:
                pa = min(1.0, (t - type_end) / PHONE_IN)
                wp = d.textlength(phone, font=fp); yp = ys[-1] + hts[-1] + 64
                pl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dp = ImageDraw.Draw(pl)
                dp.text(((W - wp) // 2, yp), phone, font=fp, fill=CREMA, stroke_width=5, stroke_fill=SHADOW)
                if note:
                    wn = dp.textlength(note, font=fnote)
                    yn = yp + fp.getmetrics()[0] + fp.getmetrics()[1] + 28
                    dp.text(((W - wn) // 2, yn), note, font=fnote, fill=CREMA, stroke_width=4, stroke_fill=SHADOW)
                pl.putalpha(pl.split()[3].point(lambda v: int(v * pa)))
                layer = Image.alpha_composite(layer, pl)
            if a < 1.0:
                layer.putalpha(layer.split()[3].point(lambda v: int(v * a)))
            frame.paste(layer, (0, 0), layer)
            frame.save(WORK / f"f{fidx:04d}.png"); fidx += 1
        print(f"  beat ok ({lines[0][:18]}) {dur:.1f}s")

    r = subprocess.run([FF, "-y", "-framerate", str(FPS), "-i", str(WORK / "f%04d.png"),
                        "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                        "-pix_fmt", "yuv420p", str(OUT)], capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG ERROR\n", r.stderr[-1500:]); raise SystemExit(1)
    print(f"\nOK: {OUT} ({OUT.stat().st_size//1024} KB, {fidx} frames, {fidx/FPS:.1f}s)")


if __name__ == "__main__":
    main()
