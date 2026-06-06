#!/usr/bin/env python3
"""
Genera el documento visual de la paleta de marca de Mendieta a partir de
los colores extraidos del feed real de Instagram.

Salidas:
  - assets/brand/paleta-mendieta.png    → A4 horizontal lista para imprimir/Canva
  - assets/brand/paleta-mendieta.json   → datos estructurados (importar en Canva
                                          Brand Kit > Colores manualmente)
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json

BASE = Path(__file__).resolve().parent.parent
OUT_DIR = BASE / "assets" / "brand"
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_DISPLAY = r"C:\Users\facun\AppData\Local\Temp\AlfaSlabOne.ttf"
FONT_BODY = r"C:\Users\facun\AppData\Local\Temp\Inter-Regular.ttf"

# Paleta REAL extraida del feed (colores y nombres semanticos)
PALETTE = [
    {
        "name": "Crema",
        "role": "FONDO PRINCIPAL",
        "hex": "#FBF4C6",
        "rgb": (251, 244, 198),
        "usage": "Fondo de posts, banners y stories. El amarillo crema del feed.",
        "text_dark": True,
    },
    {
        "name": "Bordó",
        "role": "TIPOGRAFÍA DISPLAY",
        "hex": "#77231B",
        "rgb": (119, 35, 27),
        "usage": "'MENDIETA', 'BINGO', 'Favoritos'. Solo en titulares grandes.",
        "text_dark": False,
    },
    {
        "name": "Cacao",
        "role": "TIPOGRAFÍA SECUNDARIA",
        "hex": "#533118",
        "rgb": (83, 49, 24),
        "usage": "'de Mendieta', 'Año Nuevo'. Subtítulos display.",
        "text_dark": False,
    },
    {
        "name": "Caramelo",
        "role": "ACENTO DECORATIVO",
        "hex": "#936D4C",
        "rgb": (147, 109, 76),
        "usage": "Iconos, líneas, sellos pequeños, ilustraciones.",
        "text_dark": False,
    },
    {
        "name": "Mostaza",
        "role": "ACENTO CÁLIDO",
        "hex": "#EDC77D",
        "rgb": (237, 199, 125),
        "usage": "Bordes de highlights, badges, detalles que destacan.",
        "text_dark": True,
    },
    {
        "name": "Tinta",
        "role": "CUERPO · CAPTIONS",
        "hex": "#1B1613",
        "rgb": (27, 22, 19),
        "usage": "Texto largo, párrafos, captions de IG. No para titulares.",
        "text_dark": False,
    },
]

# A4 horizontal: 297 x 210 mm. A 200 DPI → 2339 x 1654.
# Para Canva ideal va a 1920x1080 o 2480x1748 (A4 @300dpi).
W, H = 2480, 1748


def main():
    img = Image.new("RGB", (W, H), "#FBF4C6")
    d = ImageDraw.Draw(img)

    # Tipografias
    f_h1 = ImageFont.truetype(FONT_DISPLAY, 110)
    f_eye = ImageFont.truetype(FONT_BODY, 30)
    f_swatch_name = ImageFont.truetype(FONT_DISPLAY, 50)
    f_swatch_role = ImageFont.truetype(FONT_BODY, 26)
    f_swatch_hex = ImageFont.truetype(FONT_DISPLAY, 64)
    f_swatch_rgb = ImageFont.truetype(FONT_BODY, 22)
    f_swatch_usage = ImageFont.truetype(FONT_BODY, 22)
    f_foot = ImageFont.truetype(FONT_BODY, 22)

    # === HEADER ===
    pad = 90

    # Eyebrow + titulo
    d.text((pad, pad), "BRAND KIT · CANVA-READY",
           font=f_eye, fill="#77231B")
    d.text((pad, pad + 50), "Mendieta", font=f_h1, fill="#77231B")
    # Subtitulo: pasteleria argentina
    d.text((pad, pad + 175),
           "Paleta extraída del feed real de @pasteleriamendieta",
           font=f_swatch_role, fill="#533118")

    # Linea decorativa derecha
    right_label = "6 COLORES · USO CONTROLADO"
    bbox_lab = d.textbbox((0, 0), right_label, font=f_eye)
    lab_w = bbox_lab[2] - bbox_lab[0]
    lab_x = W - pad - lab_w
    d.line(
        [(lab_x, pad + 60), (W - pad, pad + 60)],
        fill="#77231B", width=3,
    )
    d.text((lab_x, pad + 75), right_label,
           font=f_eye, fill="#533118")

    # === GRID 3x2 DE SWATCHES ===
    grid_top = pad + 290
    grid_h = H - grid_top - pad - 60
    cols = 3
    rows = 2
    gap = 30
    cell_w = (W - 2 * pad - (cols - 1) * gap) // cols
    cell_h = (grid_h - (rows - 1) * gap) // rows

    for i, color in enumerate(PALETTE):
        row = i // cols
        col = i % cols
        x = pad + col * (cell_w + gap)
        y = grid_top + row * (cell_h + gap)

        # Bloque de color (40% del ancho de la celda)
        block_w = int(cell_w * 0.40)
        d.rounded_rectangle(
            [x, y, x + block_w, y + cell_h],
            radius=20, fill=color["hex"],
        )

        # HEX centrado horizontalmente dentro del bloque, en la franja inferior
        text_in_block = "#FBF4C6" if not color["text_dark"] else "#533118"
        hex_str = color["hex"]
        bbox = d.textbbox((0, 0), hex_str, font=f_swatch_hex)
        hex_w = bbox[2] - bbox[0]
        hex_x = x + (block_w - hex_w) // 2
        d.text((hex_x, y + cell_h - 90), hex_str,
               font=f_swatch_hex, fill=text_in_block)

        # Lado derecho: info
        info_x = x + block_w + 40
        info_y = y + 30
        info_w = cell_w - block_w - 60

        # Nombre (display, color de marca rojo)
        d.text((info_x, info_y), color["name"],
               font=f_swatch_name, fill="#77231B")

        # Role (eyebrow)
        d.text((info_x, info_y + 75), color["role"].upper(),
               font=f_eye, fill="#936D4C")

        # RGB
        r, g, b = color["rgb"]
        d.text((info_x, info_y + 130),
               f"R {r:3}  ·  G {g:3}  ·  B {b:3}",
               font=f_swatch_rgb, fill="#533118")

        # Uso recomendado — wrap por ancho real (no chars fijos)
        usage = color["usage"]
        words = usage.split()
        lines = []
        current = ""
        for w in words:
            test = (current + " " + w).strip()
            bbox = d.textbbox((0, 0), test, font=f_swatch_usage)
            if bbox[2] - bbox[0] <= info_w - 20:
                current = test
            else:
                if current:
                    lines.append(current)
                current = w
        if current:
            lines.append(current)
        # Pintar maximo 3 lineas
        for i_l, line in enumerate(lines[:3]):
            d.text((info_x, info_y + 180 + i_l * 32), line,
                   font=f_swatch_usage, fill="#533118")

    # === FOOTER ===
    foot_y = H - pad
    d.line([(pad, foot_y - 30), (W - pad, foot_y - 30)],
           fill="#936D4C", width=1)
    d.text((pad, foot_y - 10),
           "Mendieta · Brand Kit · Para Canva: Brand Kit > Colores > Añadir cada HEX",
           font=f_foot, fill="#533118")
    d.text((W - pad - 400, foot_y - 10),
           "Generado por Vantia · Marketing Digital",
           font=f_foot, fill="#936D4C")

    out_png = OUT_DIR / "paleta-mendieta.png"
    img.save(out_png, "PNG", optimize=True)
    print(f"OK: {out_png} ({out_png.stat().st_size / 1024:.0f} KB · {W}x{H})")

    # JSON estructurado para herramientas
    out_json = OUT_DIR / "paleta-mendieta.json"
    out_json.write_text(json.dumps(PALETTE, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"OK: {out_json}")


if __name__ == "__main__":
    main()
