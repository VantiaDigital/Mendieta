#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mendieta — Video de la torre de sanguches estilo "studio build" (fondo blanco).

El video original (IMG_9688.MOV) tiene fondo de cocina y manos que tapan la
torre — el recorte IA por frame parpadea. En su lugar: BUILD SINTÉTICO con el
frame final limpio (t7.10, recortado con BiRefNet): la torre aparece por
bloques (base → medio → tope) con caída suave + sombra de contacto, y termina
con push-in lento. 1080x1920, 30fps, sin audio.

Requiere: %TEMP%/mendieta-mundial/vidtest/stages/t7.10_cut.png
Salida:   Documentos/Mendieta/reel-mundial/editados/torre-sanguches-pro.mp4
"""
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
from scipy import ndimage

FF = r"C:/Users/facun/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.1-full_build/bin/ffmpeg.exe"
CUT = Path(r"C:/Users/facun/AppData/Local/Temp/mendieta-mundial/vidtest/stages/t7.10_cut.png")
WORK = Path(r"C:/Users/facun/AppData/Local/Temp/mendieta-mundial/torrebuild/frames")
WORK.mkdir(parents=True, exist_ok=True)
OUT = Path(r"C:/Users/facun/Documentos/Mendieta/reel-mundial/editados/torre-sanguches-pro.mp4")

W, H = 1080, 1920
FPS = 30
DUR = 4.2
N = int(DUR * FPS)

# líneas de corte entre bloques, en coords del frame original (ver guides.jpg)
CUT_Y = [630, 880]          # top < 630 <= mid < 880 <= base
# timeline de caída de cada bloque (start_s, dur_s) — orden: base, mid, top
DROPS = [(0.00, 0.32), (0.34, 0.32), (0.68, 0.32)]
ZOOM_START, ZOOM_END, Z_MAX = 1.15, 4.2, 1.085   # push-in del hold final


def ease_out_cubic(u):
    return 1 - (1 - u) ** 3


def load_blocks():
    cut = Image.open(CUT).convert("RGBA")
    arr = np.array(cut)
    a = arr[:, :, 3]
    # limpiar componentes chicos (migas/bordes sueltos)
    mask = a > 120
    lbl, n = ndimage.label(mask)
    if n:
        sizes = ndimage.sum(mask, lbl, range(1, n + 1))
        keep = [i + 1 for i, s in enumerate(sizes) if s >= 0.10 * sizes.max()]
        mask = np.isin(lbl, keep)
    arr[:, :, 3] = np.where(mask, a, 0)
    cut = Image.fromarray(arr)
    bb = cut.getbbox()
    cut = cut.crop(bb)
    y0 = bb[1]

    # grade apetitoso
    rgb = Image.merge("RGB", cut.split()[:3])
    rgb = ImageEnhance.Contrast(rgb).enhance(1.05)
    rgb = ImageEnhance.Color(rgb).enhance(1.06)
    rgb = ImageEnhance.Sharpness(rgb).enhance(1.4)
    rgb = rgb.point(lambda p: min(255, int(p * 1.02)))
    cut = Image.merge("RGBA", (*rgb.split(), cut.split()[3]))

    # escalar a 960px de ancho y ubicar en lienzo
    tw = 960
    s = tw / cut.width
    cut = cut.resize((tw, int(cut.height * s)), Image.LANCZOS)
    px = (W - cut.width) // 2
    py = int(H * 0.47) - cut.height // 2

    # cortar en 3 bloques por las líneas guía (coords frame -> coords cutout)
    cuts = [max(0, min(cut.height, int((cy - y0) * s))) for cy in CUT_Y]
    # bandas con SOLAPE: cada bloque lleva OV px extra del contenido de abajo
    # (difuminados) para que nunca se vea hueco durante la caída; al aterrizar
    # el solape coincide píxel a píxel con el bloque inferior -> invisible.
    OV, FEATH = 18, 8
    bands = [(cuts[1], cut.height),
             (cuts[0], min(cut.height, cuts[1] + OV)),
             (0, min(cut.height, cuts[0] + OV))]   # base, mid, top
    blocks = []
    for (b0, b1) in bands:
        blk = Image.new("RGBA", cut.size, (0, 0, 0, 0))
        blk.paste(cut.crop((0, b0, cut.width, b1)), (0, b0))
        if b1 < cut.height:  # difuminar el borde inferior del solape
            a = np.array(blk.split()[3], dtype=np.float32)
            for k in range(FEATH):
                row = b1 - 1 - k
                if 0 <= row < a.shape[0]:
                    a[row, :] *= (k + 1) / (FEATH + 1)
            blk.putalpha(Image.fromarray(a.astype("uint8")))
        blocks.append(blk)
    return blocks, cut.split()[3], px, py, cut.height


def main():
    blocks, full_alpha, px, py, ch = load_blocks()

    # sombra de suelo estilo estudio: silueta aplastada bajo la torre, muy difusa
    squash = full_alpha.resize((full_alpha.width, max(1, int(ch * 0.22))), Image.LANCZOS)
    sm = Image.new("L", (W, H), 0)
    sm.paste(squash, (px, py + int(ch * 0.86)))
    sm = sm.filter(ImageFilter.GaussianBlur(ch * 0.035)).point(lambda p: int(p * 0.40))
    shadow_full = Image.composite(Image.new("RGBA", (W, H), (70, 45, 30, 255)),
                                  Image.new("RGBA", (W, H), (0, 0, 0, 0)), sm)

    cx, cy = W // 2, py + ch // 2   # centro del push-in

    for f in range(N):
        t = f / FPS
        frame = Image.new("RGBA", (W, H), (255, 255, 255, 255))

        # sombra ligada a la caída de la base
        s0, sd = DROPS[0]
        sprog = ease_out_cubic(min(1.0, max(0.0, (t - s0) / sd)))
        if sprog > 0:
            sh = shadow_full.copy()
            sa = sh.split()[3].point(lambda p: int(p * sprog))
            sh.putalpha(sa)
            frame = Image.alpha_composite(frame, sh)

        for blk, (d0, dd) in zip(blocks, DROPS):
            u = (t - d0) / dd
            if u <= 0:
                continue
            u = min(1.0, u)
            e = ease_out_cubic(u)
            yoff = int(-60 * (1 - e))
            alpha = min(1.0, u / 0.4)
            b = blk if alpha >= 1.0 else Image.merge(
                "RGBA", (*blk.split()[:3], blk.split()[3].point(lambda p: int(p * alpha))))
            frame.alpha_composite(b, (px, py + yoff))

        out = frame.convert("RGB")

        # push-in del hold
        if t > ZOOM_START:
            z = 1.0 + (Z_MAX - 1.0) * min(1.0, (t - ZOOM_START) / (ZOOM_END - ZOOM_START))
            cw, chh = int(W / z), int(H / z)
            x0 = min(max(0, cx - cw // 2), W - cw)
            y0 = min(max(0, cy - chh // 2), H - chh)
            out = out.crop((x0, y0, x0 + cw, y0 + chh)).resize((W, H), Image.LANCZOS)

        out.save(WORK / f"f{f:04d}.png")

    r = subprocess.run([FF, "-y", "-framerate", str(FPS), "-i", str(WORK / "f%04d.png"),
                        "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                        "-pix_fmt", "yuv420p", str(OUT)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG ERROR\n", r.stderr[-1500:])
        raise SystemExit(1)
    print(f"OK: {OUT}  ({OUT.stat().st_size // 1024} KB, {DUR}s)")


if __name__ == "__main__":
    main()
