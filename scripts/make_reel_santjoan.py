#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mendieta — Reel cocas de Sant Joan.

Fotos reales de las cocas (recortadas de las capturas) como fondo apenas
oscurecido; texto crema grande al medio que se ESCRIBE (typewriter) y se borra.
Dos líneas por beat: arriba español argentino, abajo catalán. Cierre con
encargo 24h + WhatsApp, para la nit del 23.

Salida: Documentos/Mendieta/sant-joan/FINAL/reel-santjoan.mp4 (1080x1920, sin audio)
Música: se agrega en Instagram (catálogo de empresa).
"""
import subprocess, shutil
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
CPS = 0.045          # segundos por carácter (typewriter)
DARK = 108           # oscurecido del fondo (0-255), "no demasiado"
CREMA = (251, 244, 198); MOSTAZA = (237, 199, 125); SHADOW = (12, 7, 3)
F_PLAY = r"C:/Users/facun/AppData/Local/Temp/PlayfairBlack.ttf"
F_RYE = r"C:/Users/facun/AppData/Local/Temp/Rye.ttf"
F_MONT = r"C:/Users/facun/AppData/Local/Temp/Montserrat.ttf"


def mont(s, w=600):
    f = ImageFont.truetype(F_MONT, s); f.set_variation_by_axes([w]); return f


def fit(text, path, maxw=970, hi=92, lo=46):
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    s = hi
    while s > lo:
        f = ImageFont.truetype(path, s)
        if d.textlength(text, font=f) <= maxw:
            return f
        s -= 2
    return ImageFont.truetype(path, lo)


def bg_for(photo):
    im = Image.open(photo).convert("RGB")
    # cover-crop a 1080x1920
    s = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    x = (im.width - W) // 2; y = (im.height - H) // 2
    im = im.crop((x, y, x + W, y + H))
    im = ImageEnhance.Color(im).enhance(1.08)
    im = ImageEnhance.Contrast(im).enhance(1.04)
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    im = Image.blend(im, dark, DARK / 255.0)
    return im


def draw_line(d, cx_text, y, full, shown, font, fill, cursor=False, blink_on=True):
    """Dibuja 'shown' chars de 'full' anclado a la izquierda en cx_text (calculado
    para que el texto COMPLETO quede centrado). Cursor opcional al final."""
    sub = full[:shown]
    # sombra + contorno
    for ox, oy in ((3, 4), (-2, 2), (2, -2)):
        d.text((cx_text + ox, y + oy), sub, font=font, fill=SHADOW, stroke_width=4, stroke_fill=SHADOW)
    d.text((cx_text, y), sub, font=font, fill=fill, stroke_width=4, stroke_fill=SHADOW)
    if cursor and blink_on:
        cw = d.textlength(sub, font=font)
        asc, desc = font.getmetrics()
        d.rectangle([cx_text + cw + 6, y + 6, cx_text + cw + 6 + max(6, font.size // 14), y + asc],
                    fill=CREMA)


def ensure_crops():
    """Recorta la coca de cada captura (saca el panel de IG). BOX para capturas 1920x912."""
    REC.mkdir(parents=True, exist_ok=True)
    BOX = (305, 28, 980, 886)
    shots = sorted(f for f in (SJ / "fotos").iterdir() if f.suffix.lower() == ".png")
    for i, f in enumerate(shots[:3], 1):
        dst = REC / f"coca{i}.png"
        if not dst.exists():
            Image.open(f).convert("RGB").crop(BOX).save(dst)


def main():
    ensure_crops()
    beats = [
        {"photo": REC / "coca1.png", "es": "Se viene Sant Joan", "cat": "Arriba Sant Joan"},
        {"photo": REC / "coca3.png", "es": "Nuestras cocas ya están", "cat": "Les nostres coques ja hi són"},
        {"photo": REC / "coca2.png", "es": "De crema, llardons o fruta confitada",
         "cat": "De crema, llardons o fruita confitada"},
        {"photo": REC / "coca1.png", "es": "Encargá con 24h de antelación",
         "cat": "Encarrega amb 24h d'antelació",
         "eyebrow": "SANT JOAN · 23 DE JUNIO", "phone": "WhatsApp 696 98 53 85", "last": True},
    ]

    fidx = 0
    for b in beats:
        bg = bg_for(b["photo"])
        fe = fit(b["es"], F_PLAY); fc = fit(b["cat"], F_PLAY)
        d0 = ImageDraw.Draw(bg)
        we = d0.textlength(b["es"], font=fe); wc = d0.textlength(b["cat"], font=fc)
        xe = int((W - we) // 2); xc = int((W - wc) // 2)
        he = fe.getmetrics()[0] + fe.getmetrics()[1]
        hc = fc.getmetrics()[0] + fc.getmetrics()[1]
        gap_lines = 28
        block_h = he + gap_lines + hc
        cy = int(H * 0.50)
        ye = cy - block_h // 2; yc = ye + he + gap_lines

        phone = b.get("phone"); eyebrow = b.get("eyebrow"); last = b.get("last", False)
        fp = ImageFont.truetype(F_RYE, 86) if phone else None
        feb = mont(34, 600) if eyebrow else None

        Tes = len(b["es"]) * CPS
        GAP = 0.30
        Tcat = len(b["cat"]) * CPS
        type_end = Tes + GAP + Tcat
        PHONE_IN = 0.5 if phone else 0.0
        HOLD = 1.5 if last else 1.15
        FADE = 0.0 if last else 0.45
        dur = type_end + PHONE_IN + HOLD + FADE
        n = int(round(dur * FPS))

        for k in range(n):
            t = k / FPS
            es_n = min(len(b["es"]), int(t / CPS)) if t < Tes else len(b["es"])
            if t < Tes + GAP:
                cat_n = 0
            else:
                cat_n = min(len(b["cat"]), int((t - Tes - GAP) / CPS))
            typing_es = t < Tes
            typing_cat = (Tes + GAP) <= t < type_end
            blink = (int(t / 0.5) % 2 == 0)

            # alpha global (fade out al final del beat, salvo el último)
            a = 1.0
            if not last and t > dur - FADE:
                a = max(0.0, (dur - t) / FADE)

            frame = bg.copy()
            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            if eyebrow:
                web = d.textlength(eyebrow, font=feb)
                d.text(((W - web) // 2, ye - 110), eyebrow, font=feb, fill=MOSTAZA,
                       stroke_width=3, stroke_fill=SHADOW)
            draw_line(d, xe, ye, b["es"], es_n, fe, CREMA, cursor=typing_es, blink_on=blink)
            draw_line(d, xc, yc, b["cat"], cat_n, fc, CREMA,
                      cursor=(typing_cat or (t >= type_end and not phone)), blink_on=blink)
            if phone and t >= type_end:
                pa = min(1.0, (t - type_end) / PHONE_IN)
                wp = d.textlength(phone, font=fp)
                yp = yc + hc + 70
                pl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dp = ImageDraw.Draw(pl)
                dp.text(((W - wp) // 2, yp), phone, font=fp, fill=CREMA, stroke_width=5, stroke_fill=SHADOW)
                pl.putalpha(pl.split()[3].point(lambda v: int(v * pa)))
                layer = Image.alpha_composite(layer, pl)
            if a < 1.0:
                layer.putalpha(layer.split()[3].point(lambda v: int(v * a)))
            frame.paste(layer, (0, 0), layer)
            frame.save(WORK / f"f{fidx:04d}.png"); fidx += 1
        print(f"  beat ok ({b['es'][:18]}...) {dur:.1f}s")

    r = subprocess.run([FF, "-y", "-framerate", str(FPS), "-i", str(WORK / "f%04d.png"),
                        "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                        "-pix_fmt", "yuv420p", str(OUT)], capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG ERROR\n", r.stderr[-1500:]); raise SystemExit(1)
    print(f"\nOK: {OUT} ({OUT.stat().st_size//1024} KB, {fidx} frames, {fidx/FPS:.1f}s)")


if __name__ == "__main__":
    main()
