#!/usr/bin/env python3
"""
Genera las 4 páginas de categoría restantes (dulces, tartas, salados, bebidas)
copiando la plantilla de facturas.html y sustituyendo los strings clave.

Si se cambia el HTML base, regenerar con: python scripts/gen_category_pages.py
"""

from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
TPL = (BASE / "pages" / "pedido" / "facturas.html").read_text(encoding="utf-8")

CATEGORIES = [
    # (slug, name, caption, meta_description)
    ("dulces", "Dulces y alfajores",
     "Lo que se lleva con el café, lo que regala alegría.",
     "Alfajores, palmeritas, conos de dulce de leche, chajá. La vitrina dulce de Mendieta."),
    ("tartas", "Tartas y tortas",
     "Caseras, para llevarse entera o por porción.",
     "Tartas de ricota, milhojas, pastel de dulce de leche y coco. Caseras, en Mendieta Barcelona."),
    ("salados", "Salados",
     "Para la pausa del mediodía o cuando el café trae hambre.",
     "Empanadas argentinas, sándwiches de miga, tostados, prepizzas. En Mendieta."),
    ("bebidas", "Bebidas",
     "El café que acompaña, y el resto también.",
     "Café argentino, mate cocido, té, refrescos. En Mendieta, Barcelona."),
]

REPLACEMENTS = {
    "facturas": "{slug}",
    "Facturas": "{name}",
    "Las clásicas argentinas, recién horneadas cada mañana.": "{caption}",
    "Facturas argentinas en Mendieta — Barcelona. Medialunas, vigilantes, cremonas. Recién horneadas todas las mañanas.": "{meta}",
    "<title>Facturas · Mendieta</title>": "<title>{name} · Mendieta</title>",
}


def generate(slug, name, caption, meta):
    html = TPL
    # Orden de reemplazos importa: del más específico al más genérico
    html = html.replace(
        "<title>Facturas · Mendieta</title>",
        f"<title>{name} · Mendieta</title>",
    )
    html = html.replace(
        "Facturas argentinas en Mendieta — Barcelona. Medialunas, vigilantes, cremonas. Recién horneadas todas las mañanas.",
        meta,
    )
    html = html.replace(
        "Las clásicas argentinas, recién horneadas cada mañana.",
        caption,
    )
    # Title visible h1 + el caption-anchor (cuidado: 'Facturas' aparece varias veces)
    html = html.replace(
        '<h1 class="cat-page-title">Facturas</h1>',
        f'<h1 class="cat-page-title">{name}</h1>',
    )
    # window.MENDIETA_CATEGORY
    html = html.replace(
        "window.MENDIETA_CATEGORY = 'facturas';",
        f"window.MENDIETA_CATEGORY = '{slug}';",
    )
    dst = BASE / "pages" / "pedido" / f"{slug}.html"
    dst.write_text(html, encoding="utf-8")
    print(f"  -> {dst.relative_to(BASE)}")


def main():
    print("Generando paginas de categoria:")
    for slug, name, caption, meta in CATEGORIES:
        generate(slug, name, caption, meta)
    print(f"\nListo. {len(CATEGORIES)} paginas generadas.")


if __name__ == "__main__":
    main()
