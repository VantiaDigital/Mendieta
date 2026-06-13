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
OUT = D / "recap-mundial-final.mp4"          # 9:16 (Reel)
OUT45 = D / "recap-mundial-carrusel.mp4"     # 4:5 (carrusel de feed)
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


def mont(s, w=700):
    """Montserrat es variable (default Thin 100). Forzamos peso real."""
    f = ImageFont.truetype(F_MONT, s)
    f.set_variation_by_axes([w])
    return f


def cline(d, y, t, f, fill, stroke=5, scol=(16, 9, 5)):
    b = d.textbbox((0, 0), t, font=f, stroke_width=stroke)
    x = (W - (b[2] - b[0])) // 2 - b[0]
    # sombra suave + contorno -> legible sobre cualquier foto
    d.text((x + 2, y + 4), t, font=f, fill=(0, 0, 0, 150), stroke_width=stroke, stroke_fill=(0, 0, 0, 150))
    d.text((x, y), t, font=f, fill=fill, stroke_width=stroke, stroke_fill=scol)


def render_sprite(draw_fn):
    """Dibuja el bloque en un lienzo full y lo recorta. Devuelve (sprite, centro)."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(img))
    bb = img.getbbox()
    sp = img.crop(bb)
    cx = (bb[0] + bb[2]) / 2
    cy = (bb[1] + bb[3]) / 2
    return sp, (cx, cy)


def block_header(d):
    cline(d, 368, "·  MENDIETA  ·", mont(36, 700), MOSTAZA, stroke=3)
    cline(d, 430, "PEDÍ PARA", font(F_RYE, 84), CREMA, stroke=6)
    cline(d, 540, "EL PARTIDO", font(F_RYE, 84), CREMA, stroke=6)


def block_24h(d):
    t = "Encargá con 24h de antelación"
    fp = mont(40, 700)
    b = d.textbbox((0, 0), t, font=fp); tw = b[2] - b[0]
    pw = tw + 110; px = (W - pw) // 2; y = 688
    d.rounded_rectangle([px + 4, y + 5, px + pw + 4, y + 99], radius=49, fill=(0, 0, 0, 130))
    d.rounded_rectangle([px, y, px + pw, y + 94], radius=49, fill=MOSTAZA)
    d.text(((W - tw) // 2, y + 25), t, font=fp, fill=CACAO)


def block_wpp(d):
    cline(d, 836, "Pedí por WhatsApp", mont(44, 700), CREMA, stroke=5)
    cline(d, 894, "696 98 53 85", font(F_RYE, 98), CREMA, stroke=6)


def block_pago(d):
    cline(d, 1103, "Pago por Bizum o", mont(48, 700), CREMA, stroke=5)
    cline(d, 1163, "transferencia bancaria", mont(48, 700), CREMA, stroke=5)


def block_comprobante(d):
    cline(d, 1288, "Confirmamos tu pedido", mont(44, 800), CREMA, stroke=5)
    cline(d, 1350, "al recibir el comprobante", mont(40, 700), MOSTAZA, stroke=4)


def block_arroba(d):
    cline(d, 1505, "@pasteleriamendieta", mont(46, 700), MOSTAZA, stroke=4)


def eoc(u):
    return 1 - (1 - u) ** 3


def eob(u):
    c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (u - 1) ** 3 + c1 * (u - 1) ** 2


def src_dur():
    r = subprocess.run([FP, "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", str(SRC)], capture_output=True, text=True)
    return float(r.stdout.strip())


def main():
    sd = src_dur()
    final_dur = CHAT_IN + (CHAT_OUT - CHAT_IN) / SPEED + (sd - CHAT_OUT)
    N = int(round(final_dur * FPS))

    DUR_IN = 0.52
    SCRIM_T0, SCRIM_T1 = 10.2, 14.9
    SCRIM_A0, SCRIM_A1 = 70, 120

    # bloques: t0, draw_fn, efecto, parámetros
    DEFS = [
        (10.35, block_header, "pop", 0.80),
        (11.20, block_24h, "left", -190),
        (12.15, block_wpp, "pop", 0.80),
        (13.30, block_pago, "right", 190),
        (14.40, block_comprobante, "left", -190),
        (15.45, block_arroba, "rise", 70),
    ]
    BLOCKS = []
    for t0, fn, fx, p in DEFS:
        sp, c = render_sprite(fn)
        BLOCKS.append({"t0": t0, "sp": sp, "c": c, "fx": fx, "p": p})

    blank = TDIR / "_blank.png"
    Image.new("RGBA", (W, H), (0, 0, 0, 0)).save(blank)

    for f in range(N):
        t = f / FPS
        if t < SCRIM_T0 - 0.05:
            shutil.copyfile(blank, TDIR / f"f{f:04d}.png")
            continue

        frame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        # panel oscuro que crece -> va cubriendo la pantalla
        sp_ramp = min(1.0, max(0.0, (t - SCRIM_T0) / (SCRIM_T1 - SCRIM_T0)))
        pa = int(SCRIM_A0 + (SCRIM_A1 - SCRIM_A0) * eoc(sp_ramp))
        if pa > 0:
            frame.alpha_composite(Image.new("RGBA", (W, H), (20, 11, 6, pa)))

        for blk in BLOCKS:
            if t < blk["t0"]:
                continue
            u = min(1.0, (t - blk["t0"]) / DUR_IN)
            a = eoc(u)
            ox = oy = 0.0
            sc = 1.0
            if blk["fx"] == "pop":
                sc = blk["p"] + (1 - blk["p"]) * eob(u)
            elif blk["fx"] == "left":
                ox = blk["p"] * (1 - eob(u))
            elif blk["fx"] == "right":
                ox = blk["p"] * (1 - eob(u))
            elif blk["fx"] == "rise":
                oy = blk["p"] * (1 - eob(u))

            sp = blk["sp"]; cx, cy = blk["c"]
            if abs(sc - 1.0) > 0.01:
                nw = max(1, int(sp.width * sc)); nh = max(1, int(sp.height * sc))
                sp = sp.resize((nw, nh), Image.LANCZOS)
            if a < 1.0:
                al = sp.split()[3].point(lambda p: int(p * a))
                sp = Image.merge("RGBA", (*sp.split()[:3], al))
            px = int(round(cx + ox - sp.width / 2))
            py = int(round(cy + oy - sp.height / 2))
            frame.alpha_composite(sp, (px, py))

        frame.save(TDIR / f"f{f:04d}.png")

    # retiming + overlay del track de títulos (image2 sequence)
    retime = (
        f"[0:v]trim=0:{CHAT_IN},setpts=PTS-STARTPTS[a];"
        f"[0:v]trim={CHAT_IN}:{CHAT_OUT},setpts=(PTS-STARTPTS)/{SPEED}[b];"
        f"[0:v]trim={CHAT_OUT},setpts=PTS-STARTPTS[c];"
        f"[a][b][c]concat=n=3:v=1:a=0,fps={FPS},setpts=PTS-STARTPTS[vc];"
    )
    def enc(args, out):
        r = subprocess.run([FF, "-y", *args, "-map", "[v]", "-an",
                            "-c:v", "libx264", "-preset", "slow", "-crf", "15",
                            "-x264-params", "aq-mode=3", str(out)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print("FFMPEG ERROR\n", r.stderr[-1800:])
            raise SystemExit(1)
        print(f"OK: {out}  ({out.stat().st_size // 1024} KB)")

    # 1) 9:16 (Reel, pantalla completa)
    fc916 = retime + "[vc][1:v]overlay=0:0:format=auto,format=yuv420p[v]"
    enc(["-i", str(SRC), "-framerate", str(FPS), "-i", str(TDIR / "f%04d.png"),
         "-filter_complex", fc916], OUT)

    # 2) 4:5 carrusel (desde el 9:16): bandera/buscador y comida a PANTALLA
    #    COMPLETA (crop centrado); solo el chat con relleno DESENFOCADO para que
    #    el movil se vea entero sin barras planas amarillas.
    B0 = CHAT_IN
    B1 = CHAT_IN + (CHAT_OUT - CHAT_IN) / SPEED
    f45 = (
        f"[0:v]trim=0:{B0:.3f},setpts=PTS-STARTPTS,crop=1080:1350:0:285,setsar=1[a];"
        f"[0:v]trim={B0:.3f}:{B1:.3f},setpts=PTS-STARTPTS,split=2[bs][bf];"
        f"[bs]scale=1080:1350:force_original_aspect_ratio=increase,crop=1080:1350,"
        f"boxblur=24:2,eq=brightness=-0.05:saturation=1.05[bb];"
        f"[bf]scale=-2:1350[bfs];"
        f"[bb][bfs]overlay=(W-w)/2:(H-h)/2,setsar=1[b];"
        f"[0:v]trim={B1:.3f}:999,setpts=PTS-STARTPTS,crop=1080:1350:0:285,setsar=1[c];"
        f"[a][b][c]concat=n=3:v=1:a=0,format=yuv420p[v]"
    )
    enc(["-i", str(OUT), "-filter_complex", f45], OUT45)
    print(f"   {final_dur:.2f}s, {N} frames")


if __name__ == "__main__":
    main()
