#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mendieta — Versión FINAL del reel recap (Canva) con títulos de pedido
APARECIENDO sobre las fotos de comida (uno por foto), no un bloque al final.

Sobre el export de Canva, en una sola pasada:
  1. DERECHOS: saca el audio incrustado de la plantilla de Canva. La música
     se agrega al publicar, desde el catálogo de Instagram para empresas.
  2. PRODUCCIÓN: acelera la sección de chat (3.4s–11.4s) x1.25.
  3. PRODUCCIÓN: durante las 4 fotos de comida aparece un título de pedido
     por foto (fade in/out), terminando en el WhatsApp grande que se sostiene.
     Todo en zona segura de la UI de Instagram.

Salida: editados/recap-mundial-final.mp4 (1080x1920, ~17.4s, SIN audio)
"""
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FF = r"C:/Users/facun/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.1-full_build/bin/ffmpeg.exe"
FP = r"C:/Users/facun/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.1-full_build/bin/ffprobe.exe"
D = Path(r"C:/Users/facun/Documentos/Mendieta/reel-mundial/editados")
SRC = D / "Video para celular recap aesthetic gris.mp4"
OUT = D / "recap-mundial-final.mp4"
TDIR = Path(r"C:/Users/facun/AppData/Local/Temp/mendieta-mundial/recap/titles")
TDIR.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920
FPS = 30
# retiming del chat
CHAT_IN, CHAT_OUT, SPEED = 3.4, 11.4, 1.25
SHIFT = (CHAT_OUT - CHAT_IN) - (CHAT_OUT - CHAT_IN) / SPEED  # tiempo ahorrado (1.6s)

CREMA = (251, 244, 198)
CACAO = (83, 49, 24)
MOSTAZA = (237, 199, 125)
F_RYE = r"C:/Users/facun/AppData/Local/Temp/Rye.ttf"
F_PLAY = r"C:/Users/facun/AppData/Local/Temp/PlayfairBlack.ttf"
F_MONT = r"C:/Users/facun/AppData/Local/Temp/Montserrat.ttf"


def font(p, s):
    return ImageFont.truetype(p, s)


def ctext(d, y, t, f, fill):
    b = d.textbbox((0, 0), t, font=f)
    w = b[2] - b[0]
    x = (W - w) // 2
    for off in ((3, 4), (2, 2)):
        d.text((x + off[0], y + off[1]), t, font=f, fill=(0, 0, 0, 220))
    d.text((x, y), t, font=f, fill=fill)


def scrim(d):
    for y in range(H - 840, H):
        u = (y - (H - 840)) / 840
        a = int(232 * (u ** 1.45))
        d.line([(0, y), (W, y)], fill=(22, 12, 7, a))


def pill(d, y, t, fs=38):
    fp = font(F_MONT, fs)
    b = d.textbbox((0, 0), t, font=fp)
    tw = b[2] - b[0]
    pw = tw + 104
    px = (W - pw) // 2
    d.rounded_rectangle([px + 4, y + 5, px + pw + 4, y + 97], radius=47, fill=(0, 0, 0, 120))
    d.rounded_rectangle([px, y, px + pw, y + 92], radius=47, fill=MOSTAZA)
    d.text(((W - tw) // 2, y + 25), t, font=fp, fill=CACAO)


# --- contenido de cada título (a opacidad plena; el fade se aplica después) ---
def title_A():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img); scrim(d)
    ctext(d, 1330, "·  MENDIETA  ·", font(F_MONT, 34), MOSTAZA)
    ctext(d, 1400, "Pedí para el partido", font(F_PLAY, 66), CREMA)
    return img


def title_B():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img); scrim(d)
    ctext(d, 1335, "Encargá con tiempo", font(F_PLAY, 60), CREMA)
    pill(d, 1430, "24h de antelación")
    return img


def title_C():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img); scrim(d)
    ctext(d, 1360, "Hacé tu pedido", font(F_PLAY, 60), CREMA)
    ctext(d, 1440, "por WhatsApp", font(F_RYE, 78), MOSTAZA)
    return img


def title_D():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img); scrim(d)
    ctext(d, 1300, "WhatsApp", font(F_MONT, 44), CREMA)
    ctext(d, 1360, "696 98 53 85", font(F_RYE, 104), CREMA)
    ctext(d, 1515, "@pasteleriamendieta", font(F_MONT, 42), MOSTAZA)
    return img


# ventanas en timeline FINAL (source - SHIFT). Source: A 11.7-13.5, B 13.7-15.3,
# C 15.5-17.2, D 17.4-fin
def src_dur():
    r = subprocess.run([FP, "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", str(SRC)], capture_output=True, text=True)
    return float(r.stdout.strip())


def main():
    sd = src_dur()
    final_dur = CHAT_IN + (CHAT_OUT - CHAT_IN) / SPEED + (sd - CHAT_OUT)
    N = int(round(final_dur * FPS))

    def fin(s):  # source time -> final time
        return s - SHIFT

    TITLES = [
        (fin(11.75), fin(13.45), title_A()),
        (fin(13.70), fin(15.30), title_B()),
        (fin(15.55), fin(17.15), title_C()),
        (fin(17.35), final_dur, title_D()),
    ]
    FADE = 0.32

    # frame transparente reutilizable para los tramos sin título
    blank = TDIR / "_blank.png"
    Image.new("RGBA", (W, H), (0, 0, 0, 0)).save(blank)

    for f in range(N):
        t = f / FPS
        active = None
        for (t0, t1, ov) in TITLES:
            if t0 - FADE <= t <= t1 + 0.05:
                fo = FADE if t1 < final_dur - 0.1 else 0.0   # D no hace fade-out
                a_in = min(1.0, max(0.0, (t - t0) / FADE)) if t >= t0 else 0.0
                a_in = min(1.0, max(0.0, (t - (t0 - FADE)) / FADE))
                a_out = 1.0 if fo == 0 else min(1.0, max(0.0, (t1 - t) / fo))
                a = max(0.0, min(a_in, a_out))
                if a > 0:
                    active = (ov, a)
                break
        dst = TDIR / f"f{f:04d}.png"
        if active is None:
            shutil.copyfile(blank, dst)
        else:
            ov, a = active
            al = ov.split()[3].point(lambda p: int(p * a))
            Image.merge("RGBA", (*ov.split()[:3], al)).save(dst)

    # retiming + overlay del track de títulos (image2 sequence)
    fc = (
        f"[0:v]trim=0:{CHAT_IN},setpts=PTS-STARTPTS[a];"
        f"[0:v]trim={CHAT_IN}:{CHAT_OUT},setpts=(PTS-STARTPTS)/{SPEED}[b];"
        f"[0:v]trim={CHAT_OUT},setpts=PTS-STARTPTS[c];"
        f"[a][b][c]concat=n=3:v=1:a=0,fps={FPS},setpts=PTS-STARTPTS[vc];"
        f"[vc][1:v]overlay=0:0:format=auto,format=yuv420p[v]"
    )
    r = subprocess.run(
        [FF, "-y", "-i", str(SRC), "-framerate", str(FPS), "-i", str(TDIR / "f%04d.png"),
         "-filter_complex", fc, "-map", "[v]", "-an",
         "-c:v", "libx264", "-preset", "slow", "-crf", "18", str(OUT)],
        capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG ERROR\n", r.stderr[-1800:])
        raise SystemExit(1)
    print(f"OK: {OUT}  ({OUT.stat().st_size // 1024} KB, {final_dur:.2f}s, {N} frames)")


if __name__ == "__main__":
    main()
