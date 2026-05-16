#!/usr/bin/env python3
"""
Cambia la tipografia display en las 9 paginas:
  DM Serif Display  ->  Alfa Slab One (estilo cartel argentino vintage)

Idempotente.
"""

from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

OLD = "family=DM+Serif+Display:ital@0;1"
NEW = "family=Alfa+Slab+One"

PAGES = [
    "index.html",
    "pages/historia.html", "pages/local.html", "pages/contacto.html",
    "pages/pedido/facturas.html", "pages/pedido/dulces.html",
    "pages/pedido/tartas.html", "pages/pedido/salados.html",
    "pages/pedido/bebidas.html",
]

def main():
    changed = 0
    for rel in PAGES:
        fp = BASE / rel
        if not fp.exists():
            print(f"  SKIP: {rel}")
            continue
        html = fp.read_text(encoding="utf-8")
        if OLD in html:
            html = html.replace(OLD, NEW)
            fp.write_text(html, encoding="utf-8")
            print(f"  -> {rel}")
            changed += 1
        else:
            print(f"  == {rel} (sin cambios)")
    print(f"\n{changed} de {len(PAGES)} actualizadas.")

if __name__ == "__main__":
    main()
