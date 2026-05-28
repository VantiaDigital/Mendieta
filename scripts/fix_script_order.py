#!/usr/bin/env python3
"""
Asegura el orden correcto de scripts en las 9 paginas:
  1) menu-data.js   (define window.MENDIETA_MENU + MENDIETA_MENU_T)
  2) i18n.js        (necesita MENDIETA_MENU para data-product-i18n)
  3) menu.js        (opcional segun pagina; usa MENDIETA_MENU_T)
  4) cart.js
  5) main.js

Idempotente.
"""

import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
PAGES = [
    "index.html",
    "pages/historia.html", "pages/local.html", "pages/contacto.html",
    "pages/pedido/facturas.html", "pages/pedido/dulces.html",
    "pages/pedido/tartas.html", "pages/pedido/salados.html",
    "pages/pedido/bebidas.html",
]


def reorder(html: str, prefix: str) -> str:
    """
    Quita TODOS los <script src='...assets/js/X.js' defer></script> existentes
    y los vuelve a poner en el orden canonico, manteniendo solo los que ya estaban.
    """
    pattern = re.compile(
        r'\s*<script src="' + re.escape(prefix) + r'assets/js/(?P<name>[a-z\-]+)\.js" defer></script>',
        re.IGNORECASE,
    )
    existing = set(m.group('name') for m in pattern.finditer(html))
    if not existing:
        return html

    # Limpiar todos los scripts del proyecto
    html = pattern.sub('', html)

    # Orden canonico (solo agregamos los que ya estaban)
    order = ['menu-data', 'i18n', 'menu', 'cart', 'main']
    canonical_block = '\n  ' + '\n  '.join(
        f'<script src="{prefix}assets/js/{n}.js" defer></script>'
        for n in order if n in existing
    ) + '\n'

    # Si hay un <script> con window.MENDIETA_CATEGORY (categoria), insertar despues
    # Si no, insertar antes del </body>
    if 'window.MENDIETA_CATEGORY' in html:
        html = re.sub(
            r"(<script>window\.MENDIETA_CATEGORY[^<]*</script>)",
            r'\1' + canonical_block,
            html,
            count=1,
        )
    else:
        html = re.sub(r'(\s*</body>)', canonical_block + r'\1', html, count=1)
    return html


def path_prefix(rel):
    if rel == "index.html": return ""
    if rel.startswith("pages/pedido/"): return "../../"
    if rel.startswith("pages/"): return "../"
    return ""


def main():
    print("Reordenando scripts: menu-data > i18n > menu > cart > main")
    changed = 0
    for rel in PAGES:
        fp = BASE / rel
        if not fp.exists(): continue
        html = fp.read_text(encoding="utf-8")
        new = reorder(html, path_prefix(rel))
        if new != html:
            fp.write_text(new, encoding="utf-8")
            print(f"  -> {rel}")
            changed += 1
        else:
            print(f"  == {rel}")
    print(f"\n{changed} de {len(PAGES)} actualizadas.")


if __name__ == "__main__":
    main()
