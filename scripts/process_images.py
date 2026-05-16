#!/usr/bin/env python3
"""
Procesa el material visual casero de Mendieta para la web.
- Auto-orient via EXIF (las fotos del iPhone vienen rotadas)
- Recorte custom por foto (encuadre manual, no centrado tonto)
- Auto-enhance: contraste suave, color, brillo
- Exporta JPG optimizado en 2 tamaños (lg=1600px, md=800px)

Uso: python scripts/process_images.py
Salida: assets/images/photos/*.jpg
"""

from PIL import Image, ImageOps, ImageEnhance
from pathlib import Path

SRC = Path(r"C:/Users/facun/Documentos/Mendieta")
DST = Path(__file__).resolve().parent.parent / "assets" / "images" / "photos"
DST.mkdir(parents=True, exist_ok=True)

# Mapeo: nombre origen -> (slug destino, recorte deseado, ratio destino)
# crop: (left%, top%, right%, bottom%) sobre la imagen YA orientada por EXIF
# ratio: 'portrait' (4:5), 'square' (1:1), 'landscape' (16:9)
JOBS = [
    # Cartel "Mendieta-Inodoro Pereyra" — IMAGEN DE MARCA principal
    # Foto bien orientada, recorte ajustado al marco del cartel
    {"src": "IMG_9727.JPG", "slug": "cartel-mendieta", "crop": (0.0, 0.0, 1.0, 1.0), "ratio": "natural", "enhance": "strong"},

    # Latte art (café con leche con dibujo de hoja)
    {"src": "IMG_9716.JPG", "slug": "cafe-latte-art-1", "crop": (0.20, 0.05, 0.95, 0.95), "ratio": "square", "enhance": "soft"},
    {"src": "IMG_9717.JPG", "slug": "cafe-latte-art-2", "crop": (0.18, 0.0, 0.92, 0.90), "ratio": "square", "enhance": "soft"},

    # Interior del local
    {"src": "IMG_9729.JPG", "slug": "interior-estantes", "crop": (0.05, 0.05, 0.95, 0.95), "ratio": "landscape", "enhance": "medium"},
    {"src": "IMG_9730.JPG", "slug": "interior-madera", "crop": (0.0, 0.0, 0.95, 0.85), "ratio": "landscape", "enhance": "medium"},
    {"src": "IMG_9731.JPG", "slug": "interior-yerba-te", "crop": (0.05, 0.10, 0.95, 0.95), "ratio": "landscape", "enhance": "medium"},
]

RATIOS = {
    "portrait": (4, 5),
    "square": (1, 1),
    "landscape": (16, 10),  # un poco menos panorámico que 16:9, queda mejor en grilla
    "wide": (5, 4),         # ligeramente horizontal (para piezas tipo cartel)
    "natural": None,        # mantiene el ratio original sin recortar
}

SIZES = [
    ("lg", 1600),   # grande (hero, fullscreen)
    ("md", 800),    # mediano (tarjetas, retina mobile)
]


def crop_to_ratio(img: Image.Image, target_ratio_wh: tuple) -> Image.Image:
    """Recorta a un ratio exacto manteniendo el centro de lo que ya pasamos."""
    w, h = img.size
    tw, th = target_ratio_wh
    target = tw / th
    current = w / h
    if abs(current - target) < 0.001:
        return img
    if current > target:
        # imagen más ancha que el target -> recortar a los lados
        new_w = int(h * target)
        left = (w - new_w) // 2
        return img.crop((left, 0, left + new_w, h))
    else:
        # imagen más alta -> recortar arriba/abajo
        new_h = int(w / target)
        top = (h - new_h) // 2
        return img.crop((0, top, w, top + new_h))


def enhance(img: Image.Image, level: str) -> Image.Image:
    """Auto-ajuste casero pero efectivo. iPhone tiende a quedar plano y frío."""
    presets = {
        "soft":   {"contrast": 1.08, "color": 1.12, "brightness": 1.02, "sharp": 1.10},
        "medium": {"contrast": 1.15, "color": 1.18, "brightness": 1.03, "sharp": 1.15},
        "strong": {"contrast": 1.22, "color": 1.20, "brightness": 1.04, "sharp": 1.20},
    }
    p = presets.get(level, presets["medium"])
    img = ImageEnhance.Contrast(img).enhance(p["contrast"])
    img = ImageEnhance.Color(img).enhance(p["color"])
    img = ImageEnhance.Brightness(img).enhance(p["brightness"])
    img = ImageEnhance.Sharpness(img).enhance(p["sharp"])
    return img


def process_one(job: dict):
    src_path = SRC / job["src"]
    if not src_path.exists():
        print(f"  SKIP — no existe: {src_path}")
        return
    print(f"  * {job['src']} -> {job['slug']}")

    img = Image.open(src_path)
    # Auto-orient via EXIF (fundamental para fotos de iPhone)
    img = ImageOps.exif_transpose(img)

    # Recorte por porcentaje (sobre imagen orientada)
    w, h = img.size
    L, T, R, B = job["crop"]
    img = img.crop((int(w * L), int(h * T), int(w * R), int(h * B)))

    # Forzar el ratio target (a menos que sea 'natural')
    target = RATIOS[job["ratio"]]
    if target is not None:
        img = crop_to_ratio(img, target)

    # Enhance
    img = enhance(img, job["enhance"])

    # Convertir a RGB (por si viniera con perfil/alpha raro)
    if img.mode != "RGB":
        img = img.convert("RGB")

    # Exportar tamaños
    for tag, max_side in SIZES:
        long_side = max(img.size)
        if long_side > max_side:
            scale = max_side / long_side
            new_size = (int(img.size[0] * scale), int(img.size[1] * scale))
            out = img.resize(new_size, Image.LANCZOS)
        else:
            out = img.copy()
        dst = DST / f"{job['slug']}-{tag}.jpg"
        out.save(dst, "JPEG", quality=85, optimize=True, progressive=True)
        kb = dst.stat().st_size / 1024
        print(f"     -> {dst.name}  ({out.size[0]}x{out.size[1]}, {kb:.0f}KB)")


def main():
    print(f"Procesando fotos de Mendieta")
    print(f"  Origen: {SRC}")
    print(f"  Destino: {DST}\n")
    for job in JOBS:
        process_one(job)
    print(f"\nListo. {len(JOBS)} fotos × 2 tamaños procesados.")


if __name__ == "__main__":
    main()
