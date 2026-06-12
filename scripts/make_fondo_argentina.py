#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mendieta — Bandera argentina flameando, ALTA CALIDAD (reel del Mundial).

Tela con ondas senoidales + pliegues sombreados + sheen, rotada en diagonal.
Render con supersampling 1.5x y textura dibujada a 2x (sol antialiased).
Generada 100% por código: sin material de terceros, sin escudos/logos.

Salidas (en Documentos/Mendieta/reel-mundial/editados/):
  bandera-argentina.mp4   brillante, calidad máxima (crf 15) — pieza standalone
  fondo-argentina.mp4     oscurecida con viñeta — fondo para overlays
  fondo-argentina.png     frame estático brillante full-res
Todas 1080x1920, 30fps, 6s, loop perfecto, sin audio.
"""
import subprocess
from pathlib import Path
import numpy as np
from scipy.ndimage import map_coordinates
from PIL import Image, ImageDraw, ImageFilter

FF = r"C:/Users/facun/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.1-full_build/bin/ffmpeg.exe"
WORK = Path(r"C:/Users/facun/AppData/Local/Temp/mendieta-mundial/fondo")
BRI = WORK / "bright"; DRK = WORK / "dark"
BRI.mkdir(parents=True, exist_ok=True); DRK.mkdir(parents=True, exist_ok=True)
OUTD = Path(r"C:/Users/facun/Documentos/Mendieta/reel-mundial/editados")
OUT_HQ = OUTD / "bandera-argentina.mp4"
OUT_BG = OUTD / "fondo-argentina.mp4"
OUT_PNG = OUTD / "fondo-argentina.png"

W, H = 1080, 1920
SS = 1.5                              # supersampling
RW, RH = int(W * SS), int(H * SS)
FPS = 30
DUR = 6.0
N = int(DUR * FPS)
ANGLE = np.deg2rad(-14)
DARKEN = 0.50

CELESTE = (117, 170, 219)
BLANCO = (245, 247, 249)
SOL = (236, 184, 92)
SOL_IN = (247, 205, 121)


def flag_texture(tw=4800, th=3000):
    """Bandera a 2x con sol antialiased (se dibuja grande y se baja a la mitad)."""
    img = Image.new("RGB", (tw, th))
    d = ImageDraw.Draw(img)
    f3 = th // 3
    d.rectangle([0, 0, tw, f3], fill=CELESTE)
    d.rectangle([0, f3, tw, 2 * f3], fill=BLANCO)
    d.rectangle([0, 2 * f3, tw, th], fill=CELESTE)
    cx, cy, r = tw // 2, th // 2, int(f3 * 0.42)
    for i in range(24):
        ang = i * (2 * np.pi / 24)
        L = r * (2.1 if i % 2 == 0 else 1.7)
        x2, y2 = cx + L * np.cos(ang), cy + L * np.sin(ang)
        d.line([cx, cy, x2, y2], fill=SOL, width=max(6, r // 9))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SOL)
    d.ellipse([cx - r * .62, cy - r * .62, cx + r * .62, cy + r * .62], fill=SOL_IN)
    img = img.resize((tw // 2, th // 2), Image.LANCZOS)   # antialias del sol
    img = img.filter(ImageFilter.GaussianBlur(0.6))
    return np.asarray(img, dtype=np.float32)


def main():
    tex = flag_texture()
    TH, TW = tex.shape[:2]

    yy, xx = np.mgrid[0:RH, 0:RW].astype(np.float32)
    cxs, cys = RW / 2, RH / 2
    ca, sa = np.cos(ANGLE), np.sin(ANGLE)
    xr = (xx - cxs) * ca - (yy - cys) * sa
    yr = (xx - cxs) * sa + (yy - cys) * ca
    sc = TW / (RW * 1.30)
    u = xr * sc + TW / 2
    v = yr * sc + TH / 2

    # viñeta en res final
    vy, vx = np.mgrid[0:H, 0:W].astype(np.float32)
    dist = np.sqrt(((vx - W / 2) / (W * 0.62)) ** 2 + ((vy - H / 2) / (H * 0.60)) ** 2)
    vign = np.clip(1.0 - 0.55 * np.clip(dist - 0.45, 0, 1.2), 0.35, 1.0)[..., None]
    # viñeta suave para la versión brillante (solo esquinas)
    vign_soft = np.clip(1.0 - 0.22 * np.clip(dist - 0.70, 0, 1.2), 0.72, 1.0)[..., None]

    # frecuencias temporales enteras sobre DUR -> loop perfecto
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

        # pliegues anchos + sheen lento que recorre la tela
        slope = A1 * k1 * np.cos(ph1) + 0.4 * A2 * k2 * np.cos(ph2)
        shade = 1.0 + 0.42 * slope / (A1 * k1 + 0.4 * A2 * k2)
        sheen = 1.0 + 0.06 * np.sin(k1 * 0.5 * u - w3 * t + 2.2)
        shade = np.clip(shade * sheen, 0.68, 1.30)[..., None]

        chans = [map_coordinates(tex[:, :, c], [sv, su], order=1, mode="nearest")
                 for c in range(3)]
        frame = np.stack(chans, axis=-1) * shade
        img = Image.fromarray(np.clip(frame, 0, 255).astype("uint8"))
        img = img.resize((W, H), Image.LANCZOS)           # downsample del supersample
        base = np.asarray(img, dtype=np.float32)

        bright = np.clip(base * 0.92 * vign_soft, 0, 255).astype("uint8")
        dark = np.clip(base * DARKEN * vign, 0, 255).astype("uint8")
        Image.fromarray(bright).save(BRI / f"f{f:04d}.jpg", quality=96)
        Image.fromarray(dark).save(DRK / f"f{f:04d}.jpg", quality=95)
        if f == 45:
            Image.fromarray(bright).save(OUT_PNG)

    for frames, out, crf in [(BRI, OUT_HQ, "15"), (DRK, OUT_BG, "17")]:
        r = subprocess.run([FF, "-y", "-framerate", str(FPS), "-i", str(frames / "f%04d.jpg"),
                            "-an", "-c:v", "libx264", "-preset", "slow", "-crf", crf,
                            "-pix_fmt", "yuv420p", str(out)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print("FFMPEG ERROR\n", r.stderr[-1500:]); raise SystemExit(1)
        print(f"OK: {out}  ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
