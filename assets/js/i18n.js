/* ============================================================
   I18N — Mendieta · Español / Inglés
   ------------------------------------------------------------
   USO en HTML:
     <h1 data-i18n="hero.title">Mendieta a casa.</h1>
       → el textContent se reemplaza con la traducción
     <input data-i18n-attr="placeholder:form.namePh" />
       → reemplaza el atributo según la key
     <span data-i18n-html="hero.title">…</span>
       → permite HTML dentro del valor (cuidado: solo strings confiables)

   USO en JS:
     window.MendietaI18n.t('cart.empty')   → string traducido
     window.MendietaI18n.lang              → 'es' | 'en'
     window.MendietaI18n.on(cb)            → callback al cambiar idioma

   PERSISTE: localStorage.mendieta-lang
   DEFAULT: 'es'

   PARA AGREGAR UN STRING NUEVO:
     1. Agregar la key en DICT.es y DICT.en
     2. Marcar el elemento HTML con data-i18n="grupo.key"

   PARA AGREGAR UN IDIOMA NUEVO (ej. catalán):
     1. Agregar entrada en DICT (ej. ca: { ... })
     2. Agregar el botón en el toggle (HTML del header)
============================================================ */

(function () {
  'use strict';

  const STORAGE_KEY = 'mendieta-lang';
  const DEFAULT_LANG = 'es';
  const SUPPORTED = ['es', 'en'];

  const DICT = {
    es: {
      /* ========== NAV / HEADER ========== */
      'nav.order': 'Pedir',
      'nav.history': 'Historia',
      'nav.local': 'Local',
      'nav.contact': 'Contacto',
      'nav.cart': 'Carrito',
      'nav.brandSub': 'Pastelería Argentina',
      'nav.openMenu': 'Abrir menú',
      'nav.viewCart': 'Ver carrito',

      /* ========== HERO ========== */
      'hero.eyebrow': 'Pastelería argentina · Barcelona',
      'hero.title1': 'Mendieta',
      'hero.title2': 'a casa.',
      'hero.lead': 'Medialunas hojaldradas, alfajores como en casa, empanadas al horno y café que acompaña. Pedí online y te lo llevamos.',
      'hero.ctaStart': 'Empezar pedido',
      'hero.ctaHow': 'Cómo funciona',

      /* ========== BENEFICIOS ========== */
      'benefit.fresh.title': 'Recién horneado',
      'benefit.fresh.desc': 'Todo lo del día se prepara la noche/madrugada anterior.',
      'benefit.time.title': '24 h de antelación',
      'benefit.time.desc': 'El tiempo justo para que todo salga del horno para vos.',
      'benefit.pay.title': 'Tarjeta o efectivo',
      'benefit.pay.desc': 'Pagás al recibir, sin trámites online.',

      /* ========== DESTACADOS ========== */
      'featured.eyebrow': 'Lo más buscado',
      'featured.title.before': 'Los favoritos de los ',
      'featured.title.em': 'mendieteros',
      'featured.title.after': '.',
      'featured.lead.before': 'Tocá ',
      'featured.lead.em': '+',
      'featured.lead.after': ' y van directo a tu pedido.',
      'featured.ask': 'a consultar',

      /* ========== CATÁLOGO ========== */
      'catalog.eyebrow': 'Toda la carta',
      'catalog.title.before': 'Elegí por ',
      'catalog.title.em': 'categoría',
      'catalog.title.after': '.',

      /* ========== CÓMO FUNCIONA ========== */
      'how.eyebrow': 'En 3 pasos',
      'how.title.before': 'Pedir es ',
      'how.title.em': 'simple',
      'how.title.after': '.',
      'how.step1.title': 'Elegí lo que querés',
      'how.step1.desc': 'Recorré las categorías o sumá los destacados con un toque.',
      'how.step2.title': 'Confirmá por WhatsApp',
      'how.step2.desc': 'Pedido con 24h de antelación. Te respondemos en minutos.',
      'how.step3.title': 'Te lo llevamos a casa',
      'how.step3.desc': 'Pagás al recibir, en tarjeta o efectivo. Sin trámites online.',

      /* ========== CLOSING ========== */
      'closing.eyebrow': '¿Listo?',
      'closing.title.before': 'Lo de siempre, pero ',
      'closing.title.em': 'a casa',
      'closing.title.after': '.',
      'closing.lead': 'Pedí lo que se te antoje y lo llevamos directo a tu mesa. No hace falta esperar el sábado para una merienda con facturas.',
      'closing.cta': 'Hacer pedido',

      /* ========== CARRITO / DRAWER ========== */
      'cart.title': 'Tu pedido',
      'cart.close': 'Cerrar carrito',
      'cart.empty.line1': 'Tu carrito todavía está vacío.',
      'cart.empty.line2': 'Elegí algo del catálogo.',
      'cart.total': 'Total estimado',
      'cart.priceAsk': 'precio a consultar',
      'cart.subtotal': 'subtotal',
      'cart.send': 'Enviar pedido por WhatsApp',
      'cart.sendNote': 'Abrimos un chat con el pedido ya escrito.',
      'cart.notice.title': '24 h de antelación.',
      'cart.notice.body1': 'Para preparar todo recién hecho.',
      'cart.notice.body2': 'Pago en tarjeta o efectivo al recibir.',
      'cart.qtyMinus': 'Restar uno',
      'cart.qtyPlus': 'Sumar uno',
      'cart.add': 'Agregar al pedido',

      /* ========== FORM CHECKOUT ========== */
      'form.name': 'Nombre',
      'form.namePh': 'Tu nombre',
      'form.nameErr': 'Hace falta tu nombre.',
      'form.phone': 'Teléfono',
      'form.phonePh': '+34 …',
      'form.phoneErr': 'Hace falta un teléfono.',
      'form.address': 'Dirección de entrega',
      'form.addressPh': 'Calle, número, piso · barrio',
      'form.addressErr': 'Necesitamos tu dirección.',
      'form.notes': 'Notas (opcional)',
      'form.notesPh': 'Alergias, hora preferida, indicaciones…',

      /* ========== MOBILE CART BAR ========== */
      'mcb.view': 'Ver pedido',

      /* ========== ORDER BAR PILLS (legacy si quedan) ========== */
      'pill.open': 'Abierto · entrega por WhatsApp',

      /* ========== PÁGINA HISTORIA ========== */
      'history.eyebrow': 'Quiénes somos',
      'history.title.before': 'Pastelería argentina ',
      'history.title.em': 'de barrio',
      'history.title.after': '.',
      'history.lead': "En el Camp de l'Arpa hace años que se cocina lo de siempre: medialunas hojaldradas, alfajores como en casa, café que acompaña.",
      'history.p1': "Mendieta es una pastelería argentina ubicada en el barrio del Camp de l'Arpa del Clot, en Barcelona. Trabajamos con elaboración artesanal cada día: masas levantadas a primera hora, dulce de leche pastelero hecho en casa, atención de la que se acuerda de tu pedido del día anterior.",
      'history.p2': 'No somos una franquicia. No somos un concepto. Somos lo que se entiende cuando se dice "una pastelería de barrio", pero con la voz argentina: la merienda como evento, el café como excusa, la factura recién hecha como motivo legítimo para postergar lo demás un rato.',
      'history.h3a': 'Lo que hacemos',
      'history.p3': 'Medialunas de manteca y de grasa. Alfajores de maicena y de chocolate. Empanadas al horno, tartas caseras, sándwiches de miga, milhojas, chajá. Café propio, mate cocido para quien lo pida. Todo recién hecho, todos los días, desde antes de las siete de la mañana.',
      'history.h3b': 'Dónde encontrarnos',
      'history.p4Strong': 'Carrer de Mallorca, 517, Barcelona.',
      'history.p4Rest': ' Abrimos de lunes a viernes desde las 7 y los fines de semana desde las 7:30, hasta las 9 de la noche todos los días. Tenemos mesa para sentarse y pedido por WhatsApp para llevarlo a casa.',
      'history.ctaOrder': 'Hacer pedido',
      'history.ctaLocal': 'Ver el local',

      /* ========== PÁGINA LOCAL ========== */
      'local.eyebrow': 'Cómo llegar',
      'local.title.before': 'El local ',
      'local.title.em': 'en persona',
      'local.title.after': '.',
      'local.lead': 'Mallorca, 517 — entre Lepant y Padilla, a dos cuadras del metro Sagrada Família. Mesas para sentarse, mostrador para llevar.',
      'local.lblAddress': 'Dirección',
      'local.lblHours': 'Horario',
      'local.lblPhone': 'Teléfono',
      'local.lblWhatsapp': 'WhatsApp',
      'local.lblEmail': 'Email',
      'local.lblMetro': 'Metro',
      'local.ctaDirections': 'Cómo llegar',
      'local.ctaOrder': 'Hacer pedido',
      'local.hoursMon': 'L–V · 07:00 – 21:00',
      'local.hoursWeek': 'S–D · 07:30 – 21:00',

      /* ========== PÁGINA CONTACTO ========== */
      'contact.eyebrow': 'Contacto',
      'contact.title.before': 'Estamos ',
      'contact.title.em': 'a un mensaje',
      'contact.title.after': '.',
      'contact.lead': 'Pedidos, consultas, encargos grandes, eventos. Lo más rápido es WhatsApp; si preferís teléfono o email, también.',
      'contact.wa.title': 'WhatsApp',
      'contact.wa.desc': 'El canal preferido para pedidos. Te respondemos en minutos.',
      'contact.wa.cta': 'Abrir WhatsApp',
      'contact.phone.title': 'Teléfono',
      'contact.phone.desc': '+34 934 33 57 45 — para llamar al local directamente.',
      'contact.phone.cta': 'Llamar al local',
      'contact.email.title': 'Email',
      'contact.email.desc': 'Para encargos grandes, presupuestos o consultas que requieran detalle.',
      'contact.ig.title': 'Instagram',
      'contact.ig.desc': '@pasteleriamendieta — vitrina, novedades, lo que sale del horno.',
      'contact.ig.cta': 'Seguir en Instagram',
      'contact.visit.title': 'Pasar por el local',
      'contact.visit.desc': 'Carrer de Mallorca, 517 · Barcelona. L–V 7:00–21:00, S–D 7:30–21:00.',
      'contact.visit.cta': 'Ver mapa y horarios',
      'contact.order.title': 'Hacer pedido online',
      'contact.order.desc': 'El catálogo completo, sumando al carrito y enviando por WhatsApp.',
      'contact.order.cta': 'Ir al pedido',

      /* ========== PÁGINAS DE CATEGORÍA ========== */
      'catpage.back': 'Volver al pedido',

      /* ========== FOOTER ========== */
      'footer.brand': 'Mendieta',
      'footer.claim': 'Pastelería argentina en Barcelona. Recién hecho, cada día. Pasá por la vitrina o pedí por WhatsApp.',
      'footer.h.menu': 'Mendieta',
      'footer.h.social': 'Redes',
      'footer.copyright': 'Mendieta · Roupag S.L',
      'footer.madeBy': 'Hecho con Vantia · Marketing Digital',

      /* ========== LANG TOGGLE ========== */
      'lang.es': 'ES',
      'lang.en': 'EN',
      'lang.aria': 'Cambiar idioma',
    },

    en: {
      /* ========== NAV / HEADER ========== */
      'nav.order': 'Order',
      'nav.history': 'About',
      'nav.local': 'Find us',
      'nav.contact': 'Contact',
      'nav.cart': 'Cart',
      'nav.brandSub': 'Argentine Bakery',
      'nav.openMenu': 'Open menu',
      'nav.viewCart': 'View cart',

      /* ========== HERO ========== */
      'hero.eyebrow': 'Argentine bakery · Barcelona',
      'hero.title1': 'Mendieta',
      'hero.title2': 'at home.',
      'hero.lead': 'Buttery croissants, classic alfajores, oven-baked empanadas and proper coffee. Order online and we bring it to you.',
      'hero.ctaStart': 'Start your order',
      'hero.ctaHow': 'How it works',

      /* ========== BENEFICIOS ========== */
      'benefit.fresh.title': 'Freshly baked',
      'benefit.fresh.desc': 'Everything is made fresh the night/early morning before delivery.',
      'benefit.time.title': '24 h notice',
      'benefit.time.desc': 'Just enough time so it all comes straight out of the oven for you.',
      'benefit.pay.title': 'Card or cash',
      'benefit.pay.desc': 'Pay on delivery, no online forms.',

      /* ========== DESTACADOS ========== */
      'featured.eyebrow': 'Most loved',
      'featured.title.before': 'Favourites from our ',
      'featured.title.em': 'regulars',
      'featured.title.after': '.',
      'featured.lead.before': 'Tap ',
      'featured.lead.em': '+',
      'featured.lead.after': ' and they go straight to your order.',
      'featured.ask': 'on request',

      /* ========== CATÁLOGO ========== */
      'catalog.eyebrow': 'Full menu',
      'catalog.title.before': 'Pick by ',
      'catalog.title.em': 'category',
      'catalog.title.after': '.',

      /* ========== CÓMO FUNCIONA ========== */
      'how.eyebrow': 'In 3 steps',
      'how.title.before': 'Ordering is ',
      'how.title.em': 'simple',
      'how.title.after': '.',
      'how.step1.title': 'Pick what you want',
      'how.step1.desc': 'Browse the categories or add the featured items with one tap.',
      'how.step2.title': 'Confirm by WhatsApp',
      'how.step2.desc': '24 hours notice. We get back to you in minutes.',
      'how.step3.title': 'We bring it to your home',
      'how.step3.desc': 'Pay on delivery — card or cash. No online checkout.',

      /* ========== CLOSING ========== */
      'closing.eyebrow': 'Ready?',
      'closing.title.before': 'The usual, ',
      'closing.title.em': 'at home',
      'closing.title.after': '.',
      'closing.lead': "Order whatever you fancy and we bring it straight to your table. You don't have to wait for Saturday to enjoy pastries with coffee.",
      'closing.cta': 'Place order',

      /* ========== CARRITO / DRAWER ========== */
      'cart.title': 'Your order',
      'cart.close': 'Close cart',
      'cart.empty.line1': 'Your cart is empty.',
      'cart.empty.line2': 'Pick something from the menu.',
      'cart.total': 'Estimated total',
      'cart.priceAsk': 'price on request',
      'cart.subtotal': 'subtotal',
      'cart.send': 'Send order by WhatsApp',
      'cart.sendNote': 'We open a chat with your order ready to send.',
      'cart.notice.title': '24 h notice required.',
      'cart.notice.body1': 'So everything is freshly baked for you.',
      'cart.notice.body2': 'Pay on delivery — card or cash.',
      'cart.qtyMinus': 'Remove one',
      'cart.qtyPlus': 'Add one',
      'cart.add': 'Add to order',

      /* ========== FORM CHECKOUT ========== */
      'form.name': 'Name',
      'form.namePh': 'Your name',
      'form.nameErr': 'We need your name.',
      'form.phone': 'Phone',
      'form.phonePh': '+34 …',
      'form.phoneErr': 'We need a phone number.',
      'form.address': 'Delivery address',
      'form.addressPh': 'Street, number, floor · neighborhood',
      'form.addressErr': 'We need your address.',
      'form.notes': 'Notes (optional)',
      'form.notesPh': 'Allergies, preferred time, directions…',

      /* ========== MOBILE CART BAR ========== */
      'mcb.view': 'View order',

      /* ========== ORDER BAR PILLS ========== */
      'pill.open': 'Open · delivery via WhatsApp',

      /* ========== PÁGINA HISTORIA ========== */
      'history.eyebrow': 'About us',
      'history.title.before': 'A neighborhood ',
      'history.title.em': 'Argentine bakery',
      'history.title.after': '.',
      'history.lead': "In Camp de l'Arpa we've been baking the same thing for years: buttery croissants, classic alfajores and coffee that goes with everything.",
      'history.p1': "Mendieta is an Argentine bakery in the Camp de l'Arpa del Clot neighborhood of Barcelona. We bake everything by hand, every day: doughs proofed at dawn, dulce de leche made in house, and the kind of attention that remembers your order from yesterday.",
      'history.p2': 'We are not a franchise. We are not a concept. We are what people mean when they say "a neighborhood bakery", but with the Argentine voice: la merienda as an event, coffee as an excuse, a freshly baked pastry as a legitimate reason to postpone everything else for a while.',
      'history.h3a': 'What we make',
      'history.p3': 'Butter and lard croissants. Maicena and chocolate alfajores. Oven-baked empanadas, homemade pies, miga sandwiches, milhojas, chajá. Our own coffee, mate cocido on request. All freshly made, every day, from before 7 in the morning.',
      'history.h3b': 'Where to find us',
      'history.p4Strong': 'Carrer de Mallorca, 517, Barcelona.',
      'history.p4Rest': ' Open Monday to Friday from 7am and weekends from 7:30am, until 9pm every day. We have tables to sit at and WhatsApp ordering to take home.',
      'history.ctaOrder': 'Place order',
      'history.ctaLocal': 'See the shop',

      /* ========== PÁGINA LOCAL ========== */
      'local.eyebrow': 'How to find us',
      'local.title.before': 'The shop ',
      'local.title.em': 'in person',
      'local.title.after': '.',
      'local.lead': 'Mallorca 517 — between Lepant and Padilla, two blocks from Sagrada Família metro. Tables to sit, counter to take away.',
      'local.lblAddress': 'Address',
      'local.lblHours': 'Hours',
      'local.lblPhone': 'Phone',
      'local.lblWhatsapp': 'WhatsApp',
      'local.lblEmail': 'Email',
      'local.lblMetro': 'Metro',
      'local.ctaDirections': 'Get directions',
      'local.ctaOrder': 'Place order',
      'local.hoursMon': 'Mon–Fri · 07:00 – 21:00',
      'local.hoursWeek': 'Sat–Sun · 07:30 – 21:00',

      /* ========== PÁGINA CONTACTO ========== */
      'contact.eyebrow': 'Contact',
      'contact.title.before': "We're ",
      'contact.title.em': 'a message away',
      'contact.title.after': '.',
      'contact.lead': 'Orders, questions, large orders, events. The fastest is WhatsApp; phone or email work too.',
      'contact.wa.title': 'WhatsApp',
      'contact.wa.desc': 'Our preferred channel for orders. We reply in minutes.',
      'contact.wa.cta': 'Open WhatsApp',
      'contact.phone.title': 'Phone',
      'contact.phone.desc': '+34 934 33 57 45 — to call the shop directly.',
      'contact.phone.cta': 'Call the shop',
      'contact.email.title': 'Email',
      'contact.email.desc': 'For large orders, quotes or questions that need detail.',
      'contact.ig.title': 'Instagram',
      'contact.ig.desc': '@pasteleriamendieta — display case, news, what comes out of the oven.',
      'contact.ig.cta': 'Follow on Instagram',
      'contact.visit.title': 'Visit the shop',
      'contact.visit.desc': 'Carrer de Mallorca, 517 · Barcelona. Mon–Fri 7:00–21:00, Sat–Sun 7:30–21:00.',
      'contact.visit.cta': 'See map and hours',
      'contact.order.title': 'Order online',
      'contact.order.desc': 'The full menu, add to cart and send via WhatsApp.',
      'contact.order.cta': 'Go to ordering',

      /* ========== PÁGINAS DE CATEGORÍA ========== */
      'catpage.back': 'Back to ordering',

      /* ========== FOOTER ========== */
      'footer.brand': 'Mendieta',
      'footer.claim': 'Argentine bakery in Barcelona. Freshly made, every day. Drop by the shop or order via WhatsApp.',
      'footer.h.menu': 'Mendieta',
      'footer.h.social': 'Social',
      'footer.copyright': 'Mendieta · Roupag S.L',
      'footer.madeBy': 'Made with Vantia · Digital Marketing',

      /* ========== LANG TOGGLE ========== */
      'lang.es': 'ES',
      'lang.en': 'EN',
      'lang.aria': 'Change language',
    },
  };

  /* ---------------------------------------------------------- */

  function getLang() {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved && SUPPORTED.includes(saved)) return saved;
    } catch {}
    return DEFAULT_LANG;
  }

  function setLang(lang) {
    if (!SUPPORTED.includes(lang)) return;
    try { localStorage.setItem(STORAGE_KEY, lang); } catch {}
    state.lang = lang;
    document.documentElement.setAttribute('lang', lang);
    applyAll();
    listeners.forEach((cb) => { try { cb(lang); } catch {} });
  }

  function t(key) {
    const d = DICT[state.lang] || DICT[DEFAULT_LANG];
    return d[key] !== undefined ? d[key] : key;
  }

  /* Recorre todos los nodos con data-i18n* y aplica las traducciones */
  function applyAll(root) {
    root = root || document;

    // textContent
    root.querySelectorAll('[data-i18n]').forEach((el) => {
      const key = el.getAttribute('data-i18n');
      el.textContent = t(key);
    });

    // innerHTML (cuidado: solo para strings confiables del dict)
    root.querySelectorAll('[data-i18n-html]').forEach((el) => {
      const key = el.getAttribute('data-i18n-html');
      el.innerHTML = t(key);
    });

    // Atributos: data-i18n-attr="attr1:key1,attr2:key2"
    root.querySelectorAll('[data-i18n-attr]').forEach((el) => {
      const spec = el.getAttribute('data-i18n-attr');
      spec.split(',').forEach((pair) => {
        const [attr, key] = pair.trim().split(':');
        if (attr && key) el.setAttribute(attr.trim(), t(key.trim()));
      });
    });

    // data-product-i18n="product-id:field" → busca producto en menu-data
    root.querySelectorAll('[data-product-i18n]').forEach((el) => {
      const [pid, field] = el.getAttribute('data-product-i18n').split(':');
      const product = findProduct(pid);
      if (product && window.MENDIETA_MENU_T) {
        el.textContent = window.MENDIETA_MENU_T(product, field);
      }
    });

    // data-category-i18n="cat-id:field" → busca categoría en menu-data
    root.querySelectorAll('[data-category-i18n]').forEach((el) => {
      const [cid, field] = el.getAttribute('data-category-i18n').split(':');
      const cat = findCategory(cid);
      if (cat && window.MENDIETA_MENU_T) {
        el.textContent = window.MENDIETA_MENU_T(cat, field);
      }
    });

    // Pintar el botón toggle (resaltar idioma actual)
    root.querySelectorAll('.lang-toggle__btn[data-lang]').forEach((btn) => {
      btn.classList.toggle('is-active', btn.dataset.lang === state.lang);
      btn.setAttribute('aria-pressed', btn.dataset.lang === state.lang ? 'true' : 'false');
    });
  }

  function findProduct(id) {
    if (!window.MENDIETA_MENU) return null;
    for (const cat of window.MENDIETA_MENU.categories) {
      for (const it of cat.items) if (it.id === id) return it;
    }
    return null;
  }
  function findCategory(id) {
    if (!window.MENDIETA_MENU) return null;
    return window.MENDIETA_MENU.categories.find((c) => c.id === id) || null;
  }

  /* Listeners para reaccionar al cambio de idioma (ej. cart.js) */
  const listeners = [];
  function on(cb) { if (typeof cb === 'function') listeners.push(cb); }

  /* Wire up del toggle de idioma (delegado en document) */
  function wireToggle() {
    document.addEventListener('click', (ev) => {
      const btn = ev.target.closest('.lang-toggle__btn[data-lang]');
      if (!btn) return;
      setLang(btn.dataset.lang);
    });
  }

  /* ---------------------------------------------------------- */

  const state = { lang: getLang() };

  // Aplicar lang al <html> antes del render para evitar flash de idioma
  document.documentElement.setAttribute('lang', state.lang);

  // Aplicar traducciones al DOM cuando esté listo
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => { applyAll(); wireToggle(); });
  } else {
    applyAll();
    wireToggle();
  }

  // API global
  window.MendietaI18n = { t, setLang, on, applyAll, get lang() { return state.lang; } };
})();
