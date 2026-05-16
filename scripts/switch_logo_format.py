#!/usr/bin/env python3
"""
Cambia las referencias del logo en las 9 paginas:
  mendieta-logo.svg  ->  mendieta-logo.png

Idempotente.
"""

from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

PAGES = [
    "index.html",
    "pages/historia.html", "pages/local.html", "pages/contacto.html",
    "pages/pedido/facturas.html", "pages/pedido/dulces.html",
    "pages/pedido/tartas.html", "pages/pedido/salados.html",
    "pages/pedido/bebidas.html",
]

OLD = "mendieta-logo.svg"
NEW = "mendieta-logo.png"

def main():
    changed = 0
    for rel in PAGES:
        fp = BASE / rel
        if not fp.exists():
            print(f"  SKIP: {rel}")
            continue
        html = fp.read_text(encoding="utf-8")
        if OLD in html:
            # Cambiar tambien el favicon type que pasa de svg+xml a png
            html = html.replace(
                'type="image/svg+xml" href="' + ("../../" if "/pedido/" in rel else "../" if rel.startswith("pages/") else "") + "assets/images/logo/" + OLD + '"',
                'type="image/png" href="' + ("../../" if "/pedido/" in rel else "../" if rel.startswith("pages/") else "") + "assets/images/logo/" + NEW + '"',
            )
            # Cambiar la ref del <img class="brand__logo">
            html = html.replace(OLD, NEW)
            fp.write_text(html, encoding="utf-8")
            print(f"  -> {rel}")
            changed += 1
        else:
            print(f"  == {rel} (sin cambios)")
    print(f"\n{changed} de {len(PAGES)} actualizadas.")

if __name__ == "__main__":
    main()
