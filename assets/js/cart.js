/* ============================================================
   CART + WHATSAPP CHECKOUT — Mendieta
   ------------------------------------------------------------
   Carrito persistente (localStorage) + envío de pedido por
   WhatsApp con mensaje pre-formateado.

   PARA EL CLIENTE: cambiar WHATSAPP_NUMBER abajo si el número
   del local cambia (formato internacional, sin "+").
============================================================ */

(function () {
  'use strict';

  // ─────────────── CONFIG ───────────────
  const WHATSAPP_NUMBER = '34696985385';   // ← número del local (sin "+")
  const STORE_NAME = 'Mendieta';
  const STORAGE_KEY = 'mendieta-cart-v1';
  const FORM_KEY = 'mendieta-form-v1';
  // ──────────────────────────────────────

  const data = window.MENDIETA_MENU;
  if (!data) return;

  const productById = new Map();
  data.categories.forEach((cat) => cat.items.forEach((it) => productById.set(it.id, it)));

  const fmtPrice = (n) =>
    new Intl.NumberFormat('es-ES', {
      style: 'currency', currency: 'EUR', minimumFractionDigits: 2,
    }).format(n);

  /* ---- State ---- */
  let cart = loadCart();

  function loadCart() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return [];
      const parsed = JSON.parse(raw);
      return parsed.filter((it) => productById.has(it.id) && Number.isFinite(it.qty) && it.qty > 0);
    } catch { return []; }
  }
  function saveCart() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(cart)); } catch {}
  }
  function qtyOf(id) {
    const it = cart.find((x) => x.id === id);
    return it ? it.qty : 0;
  }
  function totalItems() { return cart.reduce((a, x) => a + x.qty, 0); }
  function totalPrice() {
    return cart.reduce((a, x) => {
      const p = productById.get(x.id);
      return a + (p?.price ? p.price * x.qty : 0);
    }, 0);
  }

  /* ---- DOM ---- */
  const cartBtn = document.getElementById('cartFab');
  const countEl = document.getElementById('cartCount');
  const drawer = document.getElementById('cartDrawer');
  const overlay = document.getElementById('drawerOverlay');
  const closeBtn = document.getElementById('drawerClose');
  const body = document.getElementById('drawerBody');
  const checkoutBtn = document.getElementById('checkoutBtn');

  /* ---- Bottom cart bar móvil (se inyecta una sola vez al cargar) ---- */
  let mobileBar = document.getElementById('mobileCartBar');
  if (!mobileBar && drawer) {
    mobileBar = document.createElement('div');
    mobileBar.className = 'mobile-cart-bar';
    mobileBar.id = 'mobileCartBar';
    mobileBar.innerHTML = `
      <button class="mobile-cart-bar__btn" type="button" id="mobileCartBarBtn" data-i18n-attr="aria-label:mcb.view">
        <span class="mobile-cart-bar__count" id="mobileCartBarCount">0</span>
        <span class="mobile-cart-bar__label" data-i18n="mcb.view">Ver pedido</span>
        <span class="mobile-cart-bar__total" id="mobileCartBarTotal">€0,00</span>
        <span class="mobile-cart-bar__arrow" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
        </span>
      </button>
    `;
    document.body.appendChild(mobileBar);
    mobileBar.querySelector('#mobileCartBarBtn').addEventListener('click', () => openDrawer());
  }
  const mobileBarCount = mobileBar?.querySelector('#mobileCartBarCount');
  const mobileBarTotal = mobileBar?.querySelector('#mobileCartBarTotal');

  /* ---- Render del badge en el header + mobile cart bar ---- */
  function renderCounter() {
    const n = totalItems();
    if (countEl) countEl.textContent = n > 0 ? n : '';
    // Mobile cart bar: aparece si hay items, oculta si no
    if (mobileBar) {
      mobileBar.classList.toggle('is-visible', n > 0);
      document.body.classList.toggle('has-cart-bar', n > 0);
      if (n > 0) {
        if (mobileBarCount) mobileBarCount.textContent = n;
        if (mobileBarTotal) mobileBarTotal.textContent = fmtPrice(totalPrice());
      }
    }
  }

  /* ---- Render de los controles +/− en cada producto ---- */
  function renderAddSlots() {
    if (!window.MendietaMenuRender) return;
    const map = new Map(cart.map((it) => [it.id, it.qty]));
    // Re-renderiza todos los slots según cantidad en carrito
    document.querySelectorAll('.product__add-slot[data-slot]').forEach((slot) => {
      const id = slot.dataset.slot;
      if (!productById.has(id)) return;
      window.MendietaMenuRender.renderAddSlot(id, map.get(id) || 0);
    });
  }

  /* ---- Helpers i18n (caen al texto en ES si i18n.js no esta cargado) ---- */
  const I18N = () => window.MendietaI18n;
  const TT = (key, fallback) => (I18N() ? I18N().t(key) : fallback);
  const productName = (p) => (window.MENDIETA_MENU_T ? window.MENDIETA_MENU_T(p, 'name') : p.name);

  /* ---- Render del drawer ---- */
  function renderDrawer() {
    if (cart.length === 0) {
      body.innerHTML = `
        <div class="cart-empty">
          <svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 18h4l6 30h26l4-22H22"/>
            <circle cx="28" cy="54" r="3"/>
            <circle cx="48" cy="54" r="3"/>
          </svg>
          <p>${TT('cart.empty.line1', 'Tu carrito todavía está vacío.')}<br>${TT('cart.empty.line2', 'Elegí algo del catálogo.')}</p>
        </div>
      `;
      checkoutBtn.disabled = true;
      return;
    }
    checkoutBtn.disabled = false;

    const lblSubtotal = TT('cart.subtotal', 'subtotal');
    const lblAsk = TT('cart.priceAsk', 'precio a consultar');
    const lblMinus = TT('cart.qtyMinus', 'Restar uno');
    const lblPlus = TT('cart.qtyPlus', 'Sumar uno');

    const itemsHtml = cart.map((it) => {
      const p = productById.get(it.id);
      if (!p) return '';
      const sub = p.price ? p.price * it.qty : 0;
      const name = productName(p);
      return `
        <div class="cart-item" data-id="${p.id}">
          <div class="cart-item__thumb" aria-hidden="true"></div>
          <div class="cart-item__info">
            <span class="cart-item__name">${name}</span>
            <span class="cart-item__price">${p.price ? `${fmtPrice(p.price)} · ${lblSubtotal} ${fmtPrice(sub)}` : lblAsk}</span>
          </div>
          <div class="cart-item__qty" role="group" aria-label="${name}">
            <button type="button" data-dec="${p.id}" aria-label="${lblMinus}">−</button>
            <span>${it.qty}</span>
            <button type="button" data-inc="${p.id}" aria-label="${lblPlus}">+</button>
          </div>
        </div>
      `;
    }).join('');

    const total = totalPrice();

    body.innerHTML = `
      <div class="cart-items">${itemsHtml}</div>
      <div class="checkout">
        <div class="checkout__totals">
          <span>${TT('cart.total', 'Total estimado')}</span>
          <strong>${fmtPrice(total)}</strong>
        </div>

        <div class="checkout__notice">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>
          <div>
            <strong>${TT('cart.notice.title', '24 h de antelación.')}</strong> ${TT('cart.notice.body1', 'Para preparar todo recién hecho.')}<br>
            <span>${TT('cart.notice.body2', 'Pago en tarjeta o efectivo al recibir.')}</span>
          </div>
        </div>

        <div class="form-field" data-field="name">
          <label for="ck-name">${TT('form.name', 'Nombre')}</label>
          <input id="ck-name" name="name" autocomplete="name" required placeholder="${TT('form.namePh', 'Tu nombre')}" />
          <span class="error-msg">${TT('form.nameErr', 'Hace falta tu nombre.')}</span>
        </div>
        <div class="form-field" data-field="phone">
          <label for="ck-phone">${TT('form.phone', 'Teléfono')}</label>
          <input id="ck-phone" name="phone" type="tel" autocomplete="tel" required placeholder="${TT('form.phonePh', '+34 …')}" />
          <span class="error-msg">${TT('form.phoneErr', 'Hace falta un teléfono.')}</span>
        </div>
        <div class="form-field" data-field="address">
          <label for="ck-address">${TT('form.address', 'Dirección de entrega')}</label>
          <input id="ck-address" name="address" autocomplete="street-address" required placeholder="${TT('form.addressPh', 'Calle, número, piso · barrio')}" />
          <span class="error-msg">${TT('form.addressErr', 'Necesitamos tu dirección.')}</span>
        </div>
        <div class="form-field" data-field="notes">
          <label for="ck-notes">${TT('form.notes', 'Notas (opcional)')}</label>
          <textarea id="ck-notes" name="notes" placeholder="${TT('form.notesPh', 'Alergias, hora preferida, indicaciones…')}"></textarea>
        </div>
      </div>
    `;
    restoreFormValues();
  }

  function render() {
    renderCounter();
    renderAddSlots();
    renderDrawer();
  }

  /* ---- Operations ---- */
  function add(id) {
    const p = productById.get(id);
    if (!p) return;
    // Productos con precio null SÍ se pueden agregar; aparecen en el mensaje
    // de WhatsApp como "a consultar" y el local confirma el precio.
    const existing = cart.find((x) => x.id === id);
    if (existing) existing.qty += 1;
    else cart.push({ id, qty: 1 });
    saveCart();
    render();
    pulseBadge();
  }
  function inc(id) {
    const it = cart.find((x) => x.id === id);
    if (it) { it.qty += 1; saveCart(); render(); }
  }
  function dec(id) {
    const it = cart.find((x) => x.id === id);
    if (!it) return;
    it.qty -= 1;
    if (it.qty <= 0) cart = cart.filter((x) => x.id !== id);
    saveCart();
    render();
  }

  /* ---- Drawer open/close ---- */
  let lastFocus = null;
  function openDrawer() {
    lastFocus = document.activeElement;
    drawer.classList.add('is-open');
    overlay.classList.add('is-open');
    document.body.style.overflow = 'hidden';
    drawer.setAttribute('aria-hidden', 'false');
    const firstInput = drawer.querySelector('input, button');
    setTimeout(() => firstInput?.focus({ preventScroll: true }), 300);
  }
  function closeDrawer() {
    drawer.classList.remove('is-open');
    overlay.classList.remove('is-open');
    document.body.style.overflow = '';
    drawer.setAttribute('aria-hidden', 'true');
    lastFocus?.focus?.();
  }

  /* ---- Form persistence ---- */
  function getFormValues() {
    return {
      name: drawer.querySelector('#ck-name')?.value.trim() || '',
      phone: drawer.querySelector('#ck-phone')?.value.trim() || '',
      address: drawer.querySelector('#ck-address')?.value.trim() || '',
      notes: drawer.querySelector('#ck-notes')?.value.trim() || '',
    };
  }
  function saveFormValues() {
    try { sessionStorage.setItem(FORM_KEY, JSON.stringify(getFormValues())); } catch {}
  }
  function restoreFormValues() {
    try {
      const raw = sessionStorage.getItem(FORM_KEY);
      if (!raw) return;
      const v = JSON.parse(raw);
      const $ = (s) => drawer.querySelector(s);
      if ($('#ck-name')) $('#ck-name').value = v.name || '';
      if ($('#ck-phone')) $('#ck-phone').value = v.phone || '';
      if ($('#ck-address')) $('#ck-address').value = v.address || '';
      if ($('#ck-notes')) $('#ck-notes').value = v.notes || '';
    } catch {}
  }
  function validateAndCollect() {
    const v = getFormValues();
    let ok = true;
    ['name', 'phone', 'address'].forEach((k) => {
      const field = drawer.querySelector(`[data-field="${k}"]`);
      if (!field) return;
      if (!v[k]) { field.classList.add('form-field--error'); ok = false; }
      else field.classList.remove('form-field--error');
    });
    return ok ? v : null;
  }

  /* ---- WhatsApp message ---- */
  function buildWhatsAppMessage(form) {
    const lines = [];
    lines.push(`🥐 *NUEVO PEDIDO — ${STORE_NAME}*`);
    lines.push('');
    lines.push(`👤 Nombre: ${form.name}`);
    lines.push(`📍 Dirección: ${form.address}`);
    lines.push(`📞 Teléfono: ${form.phone}`);
    lines.push('');
    lines.push('🛒 *PEDIDO:*');
    lines.push('');
    cart.forEach((it) => {
      const p = productById.get(it.id);
      if (!p) return;
      const line = `${it.qty}x ${p.name}` + (p.price ? ` — ${fmtPrice(p.price * it.qty)}` : '');
      lines.push(line);
    });
    lines.push('');
    lines.push(`💰 *TOTAL: ${fmtPrice(totalPrice())}*`);
    lines.push('');
    lines.push('⏰ Pedido con 24h de antelación.');
    lines.push('💳 Pago en tarjeta o efectivo al recibir.');
    if (form.notes) {
      lines.push('');
      lines.push(`📝 Notas: ${form.notes}`);
    }
    return lines.join('\n');
  }
  function sendOrder() {
    if (cart.length === 0) return;
    const form = validateAndCollect();
    if (!form) {
      const firstErr = drawer.querySelector('.form-field--error input, .form-field--error textarea');
      firstErr?.focus();
      return;
    }
    saveFormValues();
    const msg = buildWhatsAppMessage(form);
    const url = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(msg)}`;
    window.open(url, '_blank', 'noopener');
  }

  function pulseBadge() {
    if (!cartBtn) return;
    cartBtn.animate(
      [{ transform: 'scale(1)' }, { transform: 'scale(1.08)' }, { transform: 'scale(1)' }],
      { duration: 320, easing: 'cubic-bezier(0.22, 1, 0.36, 1)' }
    );
  }

  /* ---- Eventos ---- */

  // Botones + en producto y +/- en el control inline
  document.addEventListener('click', (ev) => {
    const addBtn = ev.target.closest('[data-add]');
    if (addBtn) { add(addBtn.dataset.add); return; }
    const incBtn = ev.target.closest('.product__add-slot [data-inc]');
    if (incBtn) { inc(incBtn.dataset.inc); return; }
    const decBtn = ev.target.closest('.product__add-slot [data-dec]');
    if (decBtn) { dec(decBtn.dataset.dec); return; }
  });

  cartBtn?.addEventListener('click', openDrawer);
  closeBtn?.addEventListener('click', closeDrawer);
  overlay?.addEventListener('click', closeDrawer);

  // Plus/minus dentro del drawer
  body?.addEventListener('click', (ev) => {
    const incEl = ev.target.closest('.cart-item__qty [data-inc]');
    const decEl = ev.target.closest('.cart-item__qty [data-dec]');
    if (incEl) inc(incEl.dataset.inc);
    else if (decEl) dec(decEl.dataset.dec);
  });
  body?.addEventListener('input', (ev) => {
    if (ev.target.matches('input, textarea')) saveFormValues();
  });

  checkoutBtn?.addEventListener('click', sendOrder);

  document.addEventListener('keydown', (ev) => {
    if (ev.key === 'Escape' && drawer.classList.contains('is-open')) closeDrawer();
  });

  // Cuando menu.js termina de pintar, refrescamos los slots
  // (los scripts cargan en orden con defer, pero el render de menú
  // crea DOM en runtime; usamos un microtask para asegurar el orden)
  Promise.resolve().then(render);
  // Y también en window load por si acaso
  window.addEventListener('load', render);

  // Suscribir al cambio de idioma: re-renderizar drawer (textos cambian)
  if (window.MendietaI18n && window.MendietaI18n.on) {
    window.MendietaI18n.on(() => render());
  }

  window.MendietaCart = { open: openDrawer, close: closeDrawer, add, refresh: render };
})();
