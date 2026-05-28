#!/usr/bin/env python3
"""
Inyecta en las 9 paginas:
  1) El bloque del toggle de idioma (ES | EN) en .header-actions
  2) <script src="assets/js/i18n.js" defer> ANTES de los demas scripts
     (debe cargar primero para tener t() disponible cuando los otros corran)
  3) data-i18n="key" en todos los textos UI principales

Idempotente.
"""

import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

PAGES_HOME = ["index.html"]
PAGES_SEC = ["pages/historia.html", "pages/local.html", "pages/contacto.html"]
PAGES_CAT = [
    "pages/pedido/facturas.html", "pages/pedido/dulces.html",
    "pages/pedido/tartas.html", "pages/pedido/salados.html",
    "pages/pedido/bebidas.html",
]
ALL_PAGES = PAGES_HOME + PAGES_SEC + PAGES_CAT


def path_prefix(rel):
    """Prefijo para llegar al root desde la pagina."""
    if rel == "index.html": return ""
    if rel.startswith("pages/pedido/"): return "../../"
    if rel.startswith("pages/"): return "../"
    return ""


TOGGLE_HTML = '''<div class="lang-toggle" role="group" data-i18n-attr="aria-label:lang.aria">
          <button class="lang-toggle__btn" type="button" data-lang="es" data-i18n="lang.es">ES</button>
          <button class="lang-toggle__btn" type="button" data-lang="en" data-i18n="lang.en">EN</button>
        </div>
        '''


def inject_toggle(html: str) -> str:
    """Inserta el .lang-toggle al inicio de .header-actions si no esta."""
    if 'class="lang-toggle"' in html:
        return html
    # Patron: <div class="header-actions">  → insertar toggle inmediatamente despues
    return re.sub(
        r'(<div class="header-actions">\s*)',
        r'\1' + TOGGLE_HTML,
        html,
        count=1,
    )


def inject_i18n_script(html: str, prefix: str) -> str:
    """Carga i18n.js ANTES del primer script defer del proyecto."""
    src = f'{prefix}assets/js/i18n.js'
    if f'src="{src}"' in html:
        return html
    # Insertar antes del primer <script src="...assets/js/menu-data.js"
    return re.sub(
        r'(<script src="[^"]*assets/js/(menu-data|cart|main)\.js" defer></script>)',
        r'<script src="' + src + r'" defer></script>\n  \1',
        html,
        count=1,
    )


# Mapeos data-i18n a aplicar (selector simple por texto exacto)
# Cada item: (texto_a_buscar, key)
TEXT_REPLACEMENTS_COMMON = [
    # NAV principal (visible)
    ('>Pedir</a>', ' data-i18n="nav.order">Pedir</a>'),
    ('>Historia</a>', ' data-i18n="nav.history">Historia</a>'),
    ('>Local</a>', ' data-i18n="nav.local">Local</a>'),
    ('>Contacto</a>', ' data-i18n="nav.contact">Contacto</a>'),
    # Brand sub
    ('<span class="brand__sub">Pastelería Argentina</span>',
     '<span class="brand__sub" data-i18n="nav.brandSub">Pastelería Argentina</span>'),
    # Cart button label
    ('<span class="cart-button__label">Carrito</span>',
     '<span class="cart-button__label" data-i18n="nav.cart">Carrito</span>'),
    # Footer brand claim (igual en todas)
    ('Pastelería argentina en Barcelona. Recién hecho, cada día.',
     '<span data-i18n="footer.claim">Pastelería argentina en Barcelona. Recién hecho, cada día.</span>'),
    # Footer copyright
    ('© <span id="year"></span> Mendieta · Roupag S.L',
     '© <span id="year"></span> <span data-i18n="footer.copyright">Mendieta · Roupag S.L</span>'),
    # Hecho con Vantia
    ('Hecho con Vantia&nbsp;·&nbsp;Marketing Digital',
     '<span data-i18n="footer.madeBy">Hecho con Vantia · Marketing Digital</span>'),
    # Footer column headers
    ('<h4>Mendieta</h4>',
     '<h4 data-i18n="footer.h.menu">Mendieta</h4>'),
    ('<h4>Redes</h4>',
     '<h4 data-i18n="footer.h.social">Redes</h4>'),
    # Footer links (Pedir/Historia/Local/Contacto ya cubiertos arriba)
    # Aria labels
    ('aria-label="Abrir menú"', 'aria-label="Abrir menú" data-i18n-attr="aria-label:nav.openMenu"'),
    ('aria-label="Ver carrito"', 'aria-label="Ver carrito" data-i18n-attr="aria-label:nav.viewCart"'),
]


def apply_replacements(html: str, replacements):
    for old, new in replacements:
        # Solo reemplazar si no esta ya el data-i18n
        if old in html and 'data-i18n' not in old:
            # Verificar que el texto a sustituir no este ya marcado
            # (los replacements arriba ya tienen data-i18n en el "new",
            #  asi que si "new" ya esta presente no volvemos a reemplazar)
            if new not in html:
                html = html.replace(old, new, 1)
        elif old in html:
            html = html.replace(old, new, 1)
    return html


def process(rel: str) -> bool:
    fp = BASE / rel
    if not fp.exists():
        print(f"  SKIP: {rel}")
        return False
    html = fp.read_text(encoding="utf-8")
    orig = html

    html = inject_toggle(html)
    html = inject_i18n_script(html, path_prefix(rel))
    html = apply_replacements(html, TEXT_REPLACEMENTS_COMMON)

    if html != orig:
        fp.write_text(html, encoding="utf-8")
        print(f"  -> {rel}")
        return True
    print(f"  == {rel} sin cambios")
    return False


def main():
    print("Inyectando i18n en todas las paginas (toggle + script + data-i18n comunes):")
    changed = sum(process(p) for p in ALL_PAGES)
    print(f"\n{changed} de {len(ALL_PAGES)} actualizadas.")
    print("\nIMPORTANTE: los textos especificos de cada pagina (hero, secciones, formularios)")
    print("se marcan en una segunda pasada manual, no via este script generico.")


if __name__ == "__main__":
    main()
