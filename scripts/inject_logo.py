#!/usr/bin/env python3
"""
Inyecta el logo SVG (assets/images/logo/mendieta-logo.svg) en:
- El brand del header de las 9 páginas (al lado del wordmark "Mendieta")
- El favicon (reemplaza el data-URI por el SVG real)

Idempotente: si ya está el <img class="brand__logo">, no lo duplica.
"""

import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

PAGES = [
    ("index.html", "assets/images/logo/mendieta-logo.svg"),
    ("pages/historia.html", "../assets/images/logo/mendieta-logo.svg"),
    ("pages/local.html", "../assets/images/logo/mendieta-logo.svg"),
    ("pages/contacto.html", "../assets/images/logo/mendieta-logo.svg"),
    ("pages/pedido/facturas.html", "../../assets/images/logo/mendieta-logo.svg"),
    ("pages/pedido/dulces.html", "../../assets/images/logo/mendieta-logo.svg"),
    ("pages/pedido/tartas.html", "../../assets/images/logo/mendieta-logo.svg"),
    ("pages/pedido/salados.html", "../../assets/images/logo/mendieta-logo.svg"),
    ("pages/pedido/bebidas.html", "../../assets/images/logo/mendieta-logo.svg"),
]

# Patrón del brand actual (sin logo): añadimos el <img class="brand__logo"> antes del texto "Mendieta"
BRAND_OLD = re.compile(
    r'<a href="([^"]+)" class="brand" aria-label="Mendieta · inicio">\s*Mendieta'
)
BRAND_NEW_TPL = (
    '<a href="\\1" class="brand" aria-label="Mendieta · inicio">'
    '<img class="brand__logo" src="{logo}" alt="" width="36" height="36" />'
    'Mendieta'
)

# Favicon: reemplazamos el data-URI por el archivo SVG real
FAVICON_OLD = re.compile(
    r'<link rel="icon" type="image/svg\+xml" href="data:image/svg\+xml,[^"]+"\s*/>'
)


def inject(rel_path, logo_path):
    fp = BASE / rel_path
    if not fp.exists():
        print(f"  SKIP (no existe): {rel_path}")
        return False

    html = fp.read_text(encoding="utf-8")
    orig = html

    # 1) Brand: inyectar img.brand__logo si no está ya
    if 'class="brand__logo"' not in html:
        html = BRAND_OLD.sub(BRAND_NEW_TPL.format(logo=logo_path), html, count=1)

    # 2) Favicon: cambiar data-URI por el SVG real
    html = FAVICON_OLD.sub(
        f'<link rel="icon" type="image/svg+xml" href="{logo_path}" />',
        html,
        count=1,
    )

    if html != orig:
        fp.write_text(html, encoding="utf-8")
        print(f"  -> {rel_path} actualizado")
        return True
    else:
        print(f"  == {rel_path} sin cambios")
        return False


def main():
    print("Inyectando logo en headers + favicons:")
    changed = sum(inject(p, l) for p, l in PAGES)
    print(f"\n{changed} de {len(PAGES)} paginas actualizadas.")


if __name__ == "__main__":
    main()
