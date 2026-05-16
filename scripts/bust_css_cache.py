#!/usr/bin/env python3
"""
Agrega/actualiza un querystring de version al <link href='main.css'>
en las 9 paginas, para forzar a los navegadores a re-bajar el CSS
despues de cambios visuales fuertes.

Usar cada vez que se haga un cambio CSS importante que el cache de los
clientes pueda romper.
"""

import re
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
PAGES = [
    "index.html",
    "pages/historia.html", "pages/local.html", "pages/contacto.html",
    "pages/pedido/facturas.html", "pages/pedido/dulces.html",
    "pages/pedido/tartas.html", "pages/pedido/salados.html",
    "pages/pedido/bebidas.html",
]

# Version = timestamp YYYYMMDDHHMM
VERSION = datetime.now().strftime("%Y%m%d%H%M")
# Patron: href="...main.css" o href="...main.css?v=XXX"
PAT = re.compile(r'(href="[^"]*assets/css/main\.css)(\?v=\d+)?(")')

def main():
    print(f"Cache-bust version: ?v={VERSION}")
    changed = 0
    for rel in PAGES:
        fp = BASE / rel
        if not fp.exists():
            print(f"  SKIP: {rel}")
            continue
        html = fp.read_text(encoding="utf-8")
        new_html, n = PAT.subn(r'\1?v=' + VERSION + r'\3', html)
        if n > 0 and new_html != html:
            fp.write_text(new_html, encoding="utf-8")
            print(f"  -> {rel}")
            changed += 1
        else:
            print(f"  == {rel} (sin cambios)")
    print(f"\n{changed} de {len(PAGES)} actualizadas.")

if __name__ == "__main__":
    main()
