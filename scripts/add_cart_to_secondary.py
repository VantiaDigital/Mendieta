#!/usr/bin/env python3
"""
Convierte el boton 'Pedir' (link a la home) en boton 'Carrito' (abre drawer)
en las 3 paginas institucionales (historia, local, contacto), e inyecta el
drawer del carrito + los scripts necesarios para que funcione el carrito
en esas paginas tambien.

Idempotente: si la pagina ya tiene cart-button con id='cartFab' y drawer,
no la modifica.
"""

from pathlib import Path
import re

BASE = Path(__file__).resolve().parent.parent

PAGES = [
    "pages/historia.html",
    "pages/local.html",
    "pages/contacto.html",
]

# 1) BLOQUE A REEMPLAZAR: <a href="../index.html" class="cart-button"> ... </a>
OLD_BUTTON = re.compile(
    r'<a href="\.\./index\.html" class="cart-button">\s*'
    r'<svg[^>]*>.*?</svg>\s*'
    r'<span class="cart-button__label">Pedir</span>\s*'
    r'</a>',
    re.DOTALL,
)

NEW_BUTTON = '''<button class="cart-button" id="cartFab" aria-label="Ver carrito" aria-controls="cartDrawer">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 4h2l2.3 12.5a2 2 0 0 0 2 1.5H18a2 2 0 0 0 2-1.6L21.5 8H6"/>
            <circle cx="9.5" cy="20.5" r="1.5"/><circle cx="17" cy="20.5" r="1.5"/>
          </svg>
          <span class="cart-button__label">Carrito</span>
          <span class="cart-button__count" id="cartCount"></span>
        </button>'''

# 2) BLOQUE A INYECTAR: drawer + scripts, justo antes de </body>
DRAWER_BLOCK = '''
  <!-- Drawer del carrito (inyectado para que el carrito sea accesible
       desde cualquier pagina, no solo desde las de pedido) -->
  <div class="drawer-overlay" id="drawerOverlay"></div>
  <aside class="drawer" id="cartDrawer" role="dialog" aria-modal="true" aria-labelledby="drawer-title" aria-hidden="true">
    <div class="drawer__head">
      <h3 id="drawer-title">Tu pedido</h3>
      <button class="drawer__close" id="drawerClose" aria-label="Cerrar carrito">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg>
      </button>
    </div>
    <div class="drawer__body" id="drawerBody"></div>
    <div class="drawer__foot">
      <button class="btn btn-primary" id="checkoutBtn">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 12.5a8 8 0 0 1-12 7l-5 1.5 1.5-4.6A8 8 0 1 1 20 12.5z"/></svg>
        <span>Enviar pedido por WhatsApp</span>
      </button>
      <small>Abrimos un chat con el pedido ya escrito.</small>
    </div>
  </aside>

  <script src="../assets/js/menu-data.js" defer></script>
  <script src="../assets/js/cart.js" defer></script>
'''

OLD_SCRIPTS_BLOCK = '<script src="../assets/js/main.js" defer></script>'
NEW_SCRIPTS_BLOCK = DRAWER_BLOCK.strip() + '\n  <script src="../assets/js/main.js" defer></script>'


def process(rel: str) -> bool:
    fp = BASE / rel
    if not fp.exists():
        print(f"  SKIP: {rel}")
        return False
    html = fp.read_text(encoding="utf-8")
    orig = html
    is_idempotent = 'id="cartFab"' in html and 'id="cartDrawer"' in html

    if is_idempotent:
        print(f"  == {rel} ya tiene cartFab y cartDrawer")
        return False

    # 1) Cambiar el boton
    new_html, n_button = OLD_BUTTON.subn(NEW_BUTTON, html)
    if n_button == 0:
        print(f"  !! {rel}: no encontre el bloque del boton 'Pedir'")
        return False

    # 2) Inyectar drawer + scripts (antes de main.js, que ya esta)
    new_html = new_html.replace(OLD_SCRIPTS_BLOCK, NEW_SCRIPTS_BLOCK, 1)

    fp.write_text(new_html, encoding="utf-8")
    print(f"  -> {rel} actualizado")
    return True


def main():
    print("Inyectando carrito en paginas institucionales:")
    changed = sum(process(p) for p in PAGES)
    print(f"\n{changed} de {len(PAGES)} paginas actualizadas.")


if __name__ == "__main__":
    main()
