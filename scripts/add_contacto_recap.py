#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mendieta — Agrega info de contacto/pedidos a la sección de productos del
reel hecho en Canva ("Video para celular recap aesthetic gris.mp4").

La sección de productos va de ~12.2s al final: se superpone un bloque con
scrim inferior (legibilidad sobre fotos), píldora de 24h, WhatsApp grande
y @, todo en fuentes/colores de marca, con fade-in. El audio se conserva.

Salida: editados/recap-mundial-contacto.mp4 (1080x1920, mismo largo)
"""
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FF = r"C:/Users/facun/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.1-full_build/bin/ffmpeg.exe"
D = Path(r"C:/Users/facun/Documentos/Mendieta/reel-mundial/editados")
SRC = D / "Video para celular recap aesthetic gris.mp4"
OUT = D / "recap-mundial-contacto.mp4"
OV = Path(r"C:/Users/facun/AppData/Local/Temp/mendieta-mundial/recap/contacto-ov.png")

W, H = 1080, 1920
T_IN = 12.25          # inicio de la sección de productos
CREMA = (251, 244, 198)
BORDO = (119, 35, 27)
CACAO = (83, 49, 24)
MOSTAZA = (237, 199, 125)
F_RYE = r"C:/Users/facun/AppData/Local/Temp/Rye.ttf"
F_PLAY = r"C:/Users/facun/AppData/Local/Temp/PlayfairBlack.ttf"
F_MONT = r"C:/Users/facun/AppData/Local/Temp/Montserrat.ttf"


def font(p, s):
    return ImageFont.truetype(p, s)


def ctext(d, y, t, f, fill, shadow=True):
    b = d.textbbox((0, 0), t, font=f)
    w = b[2] - b[0]
    x = (W - w) // 2
    if shadow:
        for off in ((3, 4), (2, 2)):
            d.text((x + off[0], y + off[1]), t, font=f, fill=(0, 0, 0, 210))
    d.text((x, y), t, font=f, fill=fill)


def make_overlay():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # scrim inferior fuerte (las fotos de producto son claras)
    for y in range(H - 820, H):
        u = (y - (H - 820)) / 820
        a = int(235 * (u ** 1.4))
        d.line([(0, y), (W, y)], fill=(22, 12, 7, a))

    ctext(d, 1300, "Pedí para el partido", font(F_PLAY, 64), CREMA)

    # píldora 24h
    fp = font(F_MONT, 38)
    t = "Encargá con 24h de antelación"
    b = d.textbbox((0, 0), t, font=fp)
    tw = b[2] - b[0]
    pw = tw + 100
    px, py = (W - pw) // 2, 1415
    d.rounded_rectangle([px + 4, py + 5, px + pw + 4, py + 92 + 5],
                        radius=46, fill=(0, 0, 0, 110))
    d.rounded_rectangle([px, py, px + pw, py + 92], radius=46, fill=MOSTAZA)
    d.text(((W - tw) // 2, py + 25), t, font=fp, fill=CACAO)

    ctext(d, 1555, "WhatsApp", font(F_MONT, 44), CREMA)
    ctext(d, 1615, "696 98 53 85", font(F_RYE, 96), CREMA)
    ctext(d, 1755, "@pasteleriamendieta", font(F_MONT, 40), MOSTAZA)
    img.save(OV)


def main():
    OV.parent.mkdir(parents=True, exist_ok=True)
    make_overlay()
    fc = (f"[1:v]format=rgba,fade=in:st={T_IN}:d=0.55:alpha=1[ov];"
          f"[0:v][ov]overlay=0:0:enable='gte(t,{T_IN})',format=yuv420p[v]")
    r = subprocess.run(
        [FF, "-y", "-i", str(SRC), "-loop", "1", "-i", str(OV),
         "-filter_complex", fc, "-map", "[v]", "-map", "0:a?",
         "-c:v", "libx264", "-preset", "slow", "-crf", "18",
         "-c:a", "copy", "-shortest", str(OUT)],
        capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG ERROR\n", r.stderr[-1500:])
        raise SystemExit(1)
    print(f"OK: {OUT}  ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
