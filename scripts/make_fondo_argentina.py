#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mendieta — Fondo "Argentina" para el reel del Mundial.

Bandera argentina flameando (tela con ondas + pliegues sombreados), rotada en
diagonal, oscurecida con viñeta para que los overlays (búsqueda de Google,
chat de WhatsApp) resalten encima. Generada 100% por código: sin material de
terceros, sin escudos/logos (la bandera es símbolo público).

Salidas:
  editados/fondo-argentina.mp4  (1080x1920, 30fps, 6s, loop perfecto, sin audio)
  editados/fondo-argentina.png  (frame estático full-res, para Canva/stories)
"""
import subprocess
from pathlib import Path
import numpy as np
from scipy.ndimage import map_coordinates
from PIL import Image, ImageDraw, ImageFilter

FF = r"C:/Users/facun/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.1-full_build/bin/ffmpeg.exe"
WORK = Path(r"C:/Users/facun/AppData/Local/Temp/mendieta-mundial/fondo/frames")
WORK.mkdir(parents=True, exist_ok=True)
OUTD = Path(r"C:/Users/facun/Documentos/Mendieta/reel-mundial/editados")
OUT_MP4 = OUTD / "fondo-argentina.mp4"
OUT_PNG = OUTD / "fondo-argentina.png"

W, H = 1080, 1920
FPS = 30
DUR = 6.0
N = int(DUR * FPS)
RW, RH = 540, 960          # render a media resolución, upscale x2
ANGLE = np.deg2rad(-14)    # diagonal de la bandera
DARKEN = 0.50              # oscurecido global (fondo, no protagonista)

CELESTE = np.array([117, 170, 219], dtype=np.float32)
BLANCO = np.array([244, 246, 248], dtype=np.float32)
SOL = (236, 184, 92)


def flag_texture(tw=2400, th=1500):
    """Bandera: tres franjas + sol dorado simple (sin escudos oficiales)."""
    img = Image.new("RGB", (tw, th))
    d = ImageDraw.Draw(img)
    f3 = th // 3
    d.rectangle([0, 0, tw, f3], fill=tuple(CELESTE.astype(int)))
    d.rectangle([0, f3, tw, 2 * f3], fill=tuple(BLANCO.astype(int)))
    d.rectangle([0, 2 * f3, tw, th], fill=tuple(CELESTE.astype(int)))
    # sol de mayo simplificado: disco + rayos alternados
    cx, cy, r = tw // 2, th // 2, int(f3 * 0.42)
    for i in range(24):
        ang = i * (2 * np.pi / 24)
        L = r * (2.1 if i % 2 == 0 else 1.7)
        x2, y2 = cx + L * np.cos(ang), cy + L * np.sin(ang)
        d.line([cx, cy, x2, y2], fill=SOL, width=max(4, r // 9))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SOL)
    d.ellipse([cx - r * .62, cy - r * .62, cx + r * .62, cy + r * .62],
              fill=(247, 205, 121))
    img = img.filter(ImageFilter.GaussianBlur(1.2))
    return np.asarray(img, dtype=np.float32)


def main():
    tex = flag_texture()
    TH, TW = tex.shape[:2]

    # grilla de salida (media res) -> coords de bandera (rotación inversa)
    yy, xx = np.mgrid[0:RH, 0:RW].astype(np.float32)
    cxs, cys = RW / 2, RH / 2
    ca, sa = np.cos(ANGLE), np.sin(ANGLE)
    xr = (xx - cxs) * ca - (yy - cys) * sa
    yr = (xx - cxs) * sa + (yy - cys) * ca
    # escalar para que la bandera cubra todo el frame rotado
    sc = TW / (RW * 1.30)
    u = xr * sc + TW / 2
    v = yr * sc + TH / 2

    # viñeta (precalculada, en res final)
    vy, vx = np.mgrid[0:H, 0:W].astype(np.float32)
    dist = np.sqrt(((vx - W / 2) / (W * 0.62)) ** 2 + ((vy - H / 2) / (H * 0.60)) ** 2)
    vign = np.clip(1.0 - 0.55 * np.clip(dist - 0.45, 0, 1.2), 0.35, 1.0)[..., None]

    # ondas: frecuencias temporales enteras sobre DUR -> loop perfecto
    # k3 chico = los pliegues cruzan el frame como lineas largas (sin "manchas")
    w1, w2, w3 = 2 * np.pi * 2 / DUR, 2 * np.pi * 3 / DUR, 2 * np.pi * 1 / DUR
    k1, k2, k3 = 2 * np.pi / (TW * 0.70), 2 * np.pi / (TW * 0.33), 2 * np.pi / (TH * 3.2)
    A1, A2 = TH * 0.038, TH * 0.014

    for f in range(N):
        t = f / FPS
        ph1 = k1 * u + k3 * v - w1 * t
        ph2 = k2 * u - w2 * t + 1.7
        dv = A1 * np.sin(ph1) + A2 * np.sin(ph2)
        du = A2 * 0.6 * np.sin(k2 * u - w3 * t + 0.6)
        su = np.clip(u + du, 0, TW - 1.001)
        sv = np.clip(v + dv, 0, TH - 1.001)

        # sombreado de pliegues: dominado por la onda larga -> pliegues anchos
        slope = A1 * k1 * np.cos(ph1) + 0.4 * A2 * k2 * np.cos(ph2)
        shade = (1.0 + 0.42 * slope / (A1 * k1 + 0.4 * A2 * k2))[..., None]
        shade = np.clip(shade, 0.70, 1.26)

        chans = [map_coordinates(tex[:, :, c], [sv, su], order=1, mode="nearest")
                 for c in range(3)]
        frame = np.stack(chans, axis=-1) * shade
        img = Image.fromarray(np.clip(frame, 0, 255).astype("uint8"))
        img = img.resize((W, H), Image.LANCZOS)

        out = np.asarray(img, dtype=np.float32) * DARKEN * vign
        Image.fromarray(np.clip(out, 0, 255).astype("uint8")).save(
            WORK / f"f{f:04d}.png")
        if f == 45:  # frame estático lindo, también en versión clara
            Image.fromarray(np.clip(np.asarray(img, dtype=np.float32) * 0.85 * vign,
                                    0, 255).astype("uint8")).save(OUT_PNG)

    r = subprocess.run([FF, "-y", "-framerate", str(FPS), "-i", str(WORK / "f%04d.png"),
                        "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
                        "-pix_fmt", "yuv420p", str(OUT_MP4)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG ERROR\n", r.stderr[-1500:])
        raise SystemExit(1)
    print(f"OK: {OUT_MP4}  ({OUT_MP4.stat().st_size // 1024} KB, {DUR}s loop)")
    print(f"OK: {OUT_PNG}")


if __name__ == "__main__":
    main()
