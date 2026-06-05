#!/usr/bin/env python3
"""
Genera la historia de Instagram 1080x1920 para Mendieta:
'Feriado de la Independencia'.

Diseño:
 - Foto base (mano sosteniendo la tarjeta de visita de Mendieta) escalada
   y ligeramente desenfocada como capa de fondo.
 - Gradiente oscuro vertical que se cubre la mitad superior — borra el
   texto viejo y da contraste para el texto nuevo.
 - Composición editorial:
     · eyebrow: '9 DE JULIO · FERIADO DE LA INDEPENDENCIA'
       (Inter caps, color crema #FEF9C0)
     · titular grande: 'Festejá con\nalgo rico.'
       (Alfa Slab One, blanco roto)
     · subtítulo:
       'Te esperamos con facturas recién hornadas,
        medialunas de manteca y todo lo que extrañás de casa.'
       (Inter regular, blanco con alpha)
     · cierre destacado:
       'Vení a Mendieta y llevate algo rico para festejar.'
       (Inter bold, color crema brand)
 - La tarjeta de visita queda visible abajo (donde ya está en la foto).
 - Margen seguro de Stories: 220px top (UI de cierre), 220px bottom (UI
   de respuesta) → texto entre y=260 y y=1700 aprox.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import textwrap

# --- Config ---
SRC = Path(r"C:/Users/facun/Downloads/Texto promocional Fiesta Independencia ES.png")
OUT_DIR = Path(__file__).resolve().parent.parent / "assets" / "images" / "stories"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT = OUT_DIR / "feriado-independencia.png"

W, H = 1080, 1920

FONT_DISPLAY = r"C:\Users\facun\AppData\Local\Temp\AlfaSlabOne.ttf"
FONT_BODY = r"C:\Users\facun\AppData\Local\Temp\Inter-Regular.ttf"

# Colores de marca (los de la web)
RED_BRAND = (180, 53, 29)        # #B4351D — rojo bordó del feed
CREAM = (254, 249, 192)          # #FEF9C0 — amarillo crema oficial
WHITE = (255, 255, 255)
WHITE_SOFT = (255, 255, 255, 230)
WHITE_FAINT = (255, 255, 255, 170)
INK = (26, 20, 16)


def load_base():
    """Carga la foto base y la lleva a 1080x1920 con cover (recorte centrado)."""
    img = Image.open(SRC).convert("RGB")
    src_w, src_h = img.size
    # Cover: escalar para llenar y recortar
    target_ratio = W / H
    src_ratio = src_w / src_h
    if src_ratio > target_ratio:
        # foto más ancha → recortar a los lados
        new_w = int(src_h * target_ratio)
        offset = (src_w - new_w) // 2
        img = img.crop((offset, 0, offset + new_w, src_h))
    else:
        # foto más alta → recortar arriba/abajo
        new_h = int(src_w / target_ratio)
        offset = (src_h - new_h) // 2
        img = img.crop((0, offset, src_w, offset + new_h))
    img = img.resize((W, H), Image.LANCZOS)
    return img


def apply_overlay(img):
    """Aplica blur sutil + gradiente oscuro vertical (transparente abajo,
    opaco arriba) para que el texto del feed original se 'limpie' y aparezca
    sólo la atmósfera de fondo (ladrillos, planta). La tarjeta de visita
    queda visible abajo."""
    # Blur leve solo en la mitad superior (para borrar texto viejo)
    upper = img.crop((0, 0, W, H * 3 // 5))
    upper_blurred = upper.filter(ImageFilter.GaussianBlur(radius=8))
    img.paste(upper_blurred, (0, 0))

    # Gradiente vertical: oscuro y opaco arriba (donde va el texto),
    # se aclara fuerte abajo para que la TARJETA brille con su amarillo.
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for y in range(H):
        if y < 1100:
            # zona del texto: opaco arriba (235), va bajando a ~180
            alpha = int(235 - (y / 1100) * 55)
        elif y < 1280:
            # transición: se aclara progresivamente
            alpha = int(180 - ((y - 1100) / 180) * 130)
        else:
            # zona de la tarjeta: casi sin overlay (la tarjeta brilla)
            alpha = max(0, int(50 - ((y - 1280) / (H - 1280)) * 50))
        draw.line([(0, y), (W, y)], fill=(0, 0, 0, alpha))
    img.paste(overlay, (0, 0), overlay)

    return img


def draw_text_layer(img):
    """Dibuja la composición editorial sobre el fondo ya oscurecido."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    PAD_X = 90
    text_w = W - 2 * PAD_X

    # === EYEBROW === '9 DE JULIO · FERIADO DE LA INDEPENDENCIA'
    eyebrow_text = "9 DE JULIO · FERIADO DE LA INDEPENDENCIA"
    f_eye = ImageFont.truetype(FONT_BODY, 28)
    bbox = d.textbbox((0, 0), eyebrow_text, font=f_eye, spacing=0)
    w_eye = bbox[2] - bbox[0]
    eye_x = (W - w_eye) // 2
    eye_y = 270

    # Pill amarillo crema con borde sutil rojo + texto rojo bordó
    pill_pad = 30
    pill_h = 64
    pill_w = w_eye + pill_pad * 2
    pill_x = (W - pill_w) // 2
    pill_y = eye_y - 18
    d.rounded_rectangle(
        [pill_x, pill_y, pill_x + pill_w, pill_y + pill_h],
        radius=32,
        fill=CREAM,
        outline=RED_BRAND,
        width=2,
    )
    # Centrar texto verticalmente en el pill
    d.text(
        ((W - w_eye) // 2, pill_y + (pill_h - 32) // 2),
        eyebrow_text,
        font=f_eye,
        fill=RED_BRAND,
    )

    # === TITULAR === 'Festejá con\nalgo rico.'
    f_h1 = ImageFont.truetype(FONT_DISPLAY, 130)
    title_lines = ["Festejá con", "algo rico."]
    y = 410
    for line in title_lines:
        bbox = d.textbbox((0, 0), line, font=f_h1)
        line_w = bbox[2] - bbox[0]
        line_x = (W - line_w) // 2
        # Sombra muy sutil para legibilidad sobre fondos heterogéneos
        d.text((line_x + 3, y + 3), line, font=f_h1, fill=(0, 0, 0, 140))
        d.text((line_x, y), line, font=f_h1, fill=WHITE)
        y += 145

    # === SUBTÍTULO === cuerpo informativo
    body_text = (
        "Te esperamos con facturas recién hornadas, "
        "medialunas de manteca y todo lo que extrañás de casa."
    )
    f_body = ImageFont.truetype(FONT_BODY, 38)
    wrapped = textwrap.wrap(body_text, width=34)
    y = 760
    for line in wrapped:
        bbox = d.textbbox((0, 0), line, font=f_body)
        line_w = bbox[2] - bbox[0]
        line_x = (W - line_w) // 2
        d.text((line_x + 2, y + 2), line, font=f_body, fill=(0, 0, 0, 120))
        d.text((line_x, y), line, font=f_body, fill=WHITE_SOFT)
        y += 54

    # === SEPARADOR DECORATIVO === línea fina + dot rojo
    sep_y = y + 30
    line_w = 240
    line_x = (W - line_w) // 2
    d.line(
        [(line_x, sep_y), (line_x + line_w // 2 - 14, sep_y)],
        fill=CREAM, width=2,
    )
    d.line(
        [(line_x + line_w // 2 + 14, sep_y), (line_x + line_w, sep_y)],
        fill=CREAM, width=2,
    )
    d.ellipse(
        [W // 2 - 7, sep_y - 7, W // 2 + 7, sep_y + 7],
        fill=RED_BRAND,
    )

    # === CIERRE === 'Vení a Mendieta y llevate algo rico para festejar.'
    f_close_brand = ImageFont.truetype(FONT_DISPLAY, 58)
    f_close_body = ImageFont.truetype(FONT_BODY, 34)

    close_brand = "Vení a Mendieta."
    bbox = d.textbbox((0, 0), close_brand, font=f_close_brand)
    cb_w = bbox[2] - bbox[0]
    cb_x = (W - cb_w) // 2
    cb_y = sep_y + 50
    d.text((cb_x + 2, cb_y + 2), close_brand, font=f_close_brand, fill=(0, 0, 0, 140))
    d.text((cb_x, cb_y), close_brand, font=f_close_brand, fill=CREAM)

    close_sub = "Llevate algo rico para festejar."
    bbox = d.textbbox((0, 0), close_sub, font=f_close_body)
    cs_w = bbox[2] - bbox[0]
    cs_x = (W - cs_w) // 2
    cs_y = cb_y + 90
    d.text((cs_x + 2, cs_y + 2), close_sub, font=f_close_body, fill=(0, 0, 0, 120))
    d.text((cs_x, cs_y), close_sub, font=f_close_body, fill=WHITE_FAINT)

    # Componer overlay sobre la imagen base
    img.paste(overlay, (0, 0), overlay)
    return img


def main():
    img = load_base().convert("RGBA")
    img = apply_overlay(img)
    img = draw_text_layer(img)
    img = img.convert("RGB")
    img.save(OUT, "PNG", optimize=True)
    print(f"OK: {OUT}")
    print(f"   tamano: {OUT.stat().st_size / 1024:.0f} KB")
    print(f"   resolucion: {W}x{H} (1080x1920 Instagram Story)")


if __name__ == "__main__":
    main()
