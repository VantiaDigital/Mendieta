#!/usr/bin/env python3
"""
Extrae la paleta de marca de Mendieta analizando los 3 screenshots del feed
de Instagram que el cliente paso.

Estrategia:
  1) Excluir UI de Instagram (la columna izquierda con iconos, el sidebar de
     mensajes/cuenta del lado derecho) → recortar la parte central del feed.
  2) Para cada pixel del area del feed, clasificarlo en una FAMILIA por
     hue/saturation/value (HSV):
       - CREMA          → amarillo claro fondo de posts
       - CREMA_OSCURO   → variante del crema (bordes de highlights)
       - ROJO_BORDO     → tipografia 'MENDIETA', 'BINGO', 'Favoritos'
       - MARRON_OSCURO  → 'de Mendieta', 'Año Nuevo', texto secundario display
       - MARRON_MEDIO   → 'EL DIA PERFECTO', acentos warm
       - VERDE_OK       → toggles iOS (no es de marca pero aparece)
       - NEGRO_TEXTO    → captions del feed (texto IG, no marca)
       - BLANCO         → texto blanco sobre fotos
  3) Por familia, promediar los pixeles y reportar el HEX RGB.
  4) Filtrar familias con menos de N pixeles (descartar ruido).
"""

from PIL import Image
from pathlib import Path
import colorsys
from collections import defaultdict

SHOTS = [
    Path(r"C:/Users/facun/Downloads/ScreenShot Tool -20260606104452.png"),
    Path(r"C:/Users/facun/Downloads/ScreenShot Tool -20260606104509.png"),
    Path(r"C:/Users/facun/Downloads/ScreenShot Tool -20260606104525.png"),
]


def classify(r, g, b):
    """Devuelve (familia, peso) para un pixel RGB(0-255).
       peso=0 → descartado (fuera de las familias de interes)."""
    rf, gf, bf = r/255, g/255, b/255
    h, s, v = colorsys.rgb_to_hsv(rf, gf, bf)
    h_deg = h * 360

    # BLANCO (alta luminosidad, baja saturacion)
    if v > 0.92 and s < 0.08:
        return ("BLANCO_PURO", 1)

    # NEGRO de texto IG (muy oscuro)
    if v < 0.18:
        return ("NEGRO_TEXTO", 1)

    # CREMA / AMARILLO CLARO de fondo (hue 40-60, sat alta, value alto)
    if 35 <= h_deg <= 65 and s > 0.10 and v > 0.85:
        if s > 0.30:
            return ("CREMA_VIVO", 1)        # bordes highlights
        return ("CREMA_BASE", 1)            # fondo principal

    # ROJO BORDO (hue 0-15 o 350-360, sat media-alta, value medio-bajo)
    if (h_deg <= 18 or h_deg >= 348) and s > 0.45 and 0.30 < v < 0.75:
        return ("ROJO_BORDO", 1)

    # MARRON OSCURO (hue 15-35, sat alta, value bajo)
    if 15 <= h_deg <= 35 and s > 0.40 and 0.18 < v < 0.45:
        return ("MARRON_OSCURO", 1)

    # MARRON MEDIO / TERRACOTA (hue 18-32, sat media, value medio)
    if 18 <= h_deg <= 35 and 0.30 < s < 0.65 and 0.45 < v < 0.70:
        return ("MARRON_MEDIO", 1)

    # VERDE iOS toggle (no es marca pero aparece, lo registramos)
    if 80 < h_deg < 150 and s > 0.4 and v > 0.5:
        return ("VERDE_TOGGLE_iOS", 1)

    return (None, 0)


def crop_feed_area(img):
    """Recorta la columna central donde esta el feed del IG.
       Sidebar izquierdo (~120 px) + sidebar derecho (~varia).
       Asumimos resolucion ~1920 ancho. El feed ocupa el ~70% central."""
    w, h = img.size
    left = int(w * 0.06)
    right = int(w * 0.95)
    return img.crop((left, 0, right, h))


def analyze_all():
    fam_counts = defaultdict(int)
    fam_sums = defaultdict(lambda: [0, 0, 0])

    for path in SHOTS:
        img = Image.open(path).convert("RGB")
        img = crop_feed_area(img)
        # Downsample para velocidad (cada N pixeles)
        w, h = img.size
        step = 3
        for y in range(0, h, step):
            for x in range(0, w, step):
                r, g, b = img.getpixel((x, y))
                fam, weight = classify(r, g, b)
                if fam is None or weight == 0:
                    continue
                fam_counts[fam] += weight
                fam_sums[fam][0] += r
                fam_sums[fam][1] += g
                fam_sums[fam][2] += b

    # Promedio por familia, filtrando familias con muy pocos pixeles
    total = sum(fam_counts.values())
    threshold = total * 0.003  # ignorar familias <0.3% del total
    results = []
    for fam, count in fam_counts.items():
        if count < threshold and fam not in ("VERDE_TOGGLE_iOS",):
            continue
        s = fam_sums[fam]
        ar, ag, ab = s[0] // count, s[1] // count, s[2] // count
        hex_ = f"#{ar:02X}{ag:02X}{ab:02X}"
        pct = (count / total) * 100
        results.append((fam, hex_, (ar, ag, ab), count, pct))

    results.sort(key=lambda x: -x[3])
    return results, total


def main():
    print("Analizando 3 screenshots del feed de Mendieta…\n")
    results, total = analyze_all()
    print(f"Pixeles clasificados: {total:,}\n")
    print(f"{'Familia':<24} {'HEX':<10} {'RGB':<22} {'%feed':>7}")
    print("-" * 70)
    for fam, hex_, rgb, count, pct in results:
        print(f"{fam:<24} {hex_:<10} rgb({rgb[0]:3},{rgb[1]:3},{rgb[2]:3})  {pct:6.2f}%")


if __name__ == "__main__":
    main()
