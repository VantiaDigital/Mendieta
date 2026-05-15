/* ============================================================
   MENU RENDERER — Mendieta
   ------------------------------------------------------------
   Renderiza categorías + productos en #menuRoot y los tabs en #menuTabs.
   Los datos vienen de assets/js/menu-data.js → window.MENDIETA_MENU.

   Iconografía: cada producto recibe un SVG ilustrativo (línea sobre
   gradiente cálido) seleccionado por palabra clave de su nombre.
============================================================ */

(function () {
  'use strict';

  const data = window.MENDIETA_MENU;
  if (!data || !data.categories) return;

  const root = document.getElementById('menuRoot');
  const tabs = document.getElementById('menuTabs');
  if (!root || !tabs) return;

  /* ---- helpers ---- */
  const fmt = (price) => {
    if (price == null) return null;
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'EUR',
      minimumFractionDigits: 2,
    }).format(price);
  };

  const shadeFor = (i) => `product--shade-${(i % 5) + 1}`;

  /* SVG icons inline por keyword del nombre del producto.
     Trazo simple — funcionan en cualquier escala. */
  const ICONS = {
    medialuna: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2"><path d="M30 22c-12 8-20 22-20 38s8 30 20 38c-5-10-7-22-7-38s2-28 7-38z"/><path d="M30 22c18-4 38 8 46 30-8 22-28 34-46 30 10-7 16-18 16-30s-6-23-16-30z"/></svg>`,
    factura: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2"><circle cx="50" cy="50" r="32"/><path d="M30 50c0-12 9-22 20-22s20 10 20 22"/><path d="M38 50h24M42 60h16"/></svg>`,
    alfajor: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2"><circle cx="50" cy="50" r="30"/><path d="M22 50h56"/><path d="M22 42h56M22 58h56" stroke-dasharray="2 3"/></svg>`,
    palmer: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 30c12-6 30-6 30 20 0-26 18-26 30-20"/><path d="M20 70c12 6 30 6 30-20 0 26 18 26 30 20"/><path d="M50 30v40"/></svg>`,
    cono: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2"><path d="M30 30h40l-15 50h-10z"/><path d="M30 30c0-6 9-12 20-12s20 6 20 12"/><path d="M36 45h28M40 60h20"/></svg>`,
    tarta: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2"><ellipse cx="50" cy="68" rx="32" ry="10"/><path d="M18 68v-18a32 10 0 0 0 64 0V68"/><path d="M30 46v14M50 46v14M70 46v14"/></svg>`,
    milhoja: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2"><rect x="18" y="32" width="64" height="9" rx="2"/><rect x="18" y="46" width="64" height="9" rx="2"/><rect x="18" y="60" width="64" height="9" rx="2"/><path d="M20 41c10 2 20-2 30 0s20 2 30 0M20 55c10 2 20-2 30 0s20 2 30 0"/></svg>`,
    chaja: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 56c4-12 16-20 28-20s24 8 28 20"/><path d="M22 56h56"/><path d="M30 56v14h40V56"/><circle cx="38" cy="46" r="3"/><circle cx="50" cy="42" r="3"/><circle cx="62" cy="46" r="3"/></svg>`,
    pan: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 60c0-16 12-26 28-26s28 10 28 26"/><path d="M18 60h64v10H18z"/><path d="M32 50l4-8M50 46v-10M68 50l-4-8"/></svg>`,
    bola: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2"><circle cx="50" cy="50" r="28"/><path d="M40 44c2-2 6-2 8 0M52 44c2-2 6-2 8 0M40 60c4 4 16 4 20 0"/></svg>`,
    empanada: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 56c0-14 14-26 32-26s32 12 32 26v6H18z"/><path d="M28 60c2-2 4-2 6 0s4 2 6 0s4-2 6 0s4 2 6 0s4-2 6 0s4 2 6 0s4-2 6 0"/></svg>`,
    sandwich: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2"><rect x="22" y="32" width="56" height="36" rx="2"/><path d="M22 44h56M22 56h56"/><path d="M28 38l8 6M40 38l8 6M52 38l8 6M64 38l8 6"/></svg>`,
    tostado: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2"><rect x="22" y="34" width="56" height="32" rx="3"/><path d="M22 50h56"/><path d="M30 42c3-3 7-3 10 0M48 42c3-3 7-3 10 0M66 42c3-3 7 3 10 0"/></svg>`,
    chapata: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2"><ellipse cx="50" cy="50" rx="32" ry="14"/><path d="M30 50h40M28 44h44M28 56h44" stroke-dasharray="3 4"/></svg>`,
    pizza: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2"><circle cx="50" cy="50" r="32"/><circle cx="50" cy="50" r="24" stroke-dasharray="3 5"/><circle cx="40" cy="44" r="3"/><circle cx="58" cy="48" r="3"/><circle cx="46" cy="60" r="3"/><circle cx="62" cy="58" r="3"/></svg>`,
    cafe: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2"><path d="M24 38h44v22c0 10-10 18-22 18s-22-8-22-18z"/><path d="M68 44h6c4 0 8 4 8 8s-4 8-8 8h-6"/><path d="M36 24c-2 3-2 6 0 9M48 24c-2 3-2 6 0 9M60 24c-2 3-2 6 0 9"/></svg>`,
    te: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2"><path d="M28 38h40v24c0 8-9 16-20 16s-20-8-20-16z"/><path d="M68 46h6c4 0 8 4 8 8s-4 8-8 8h-6"/><path d="M42 50c4 6 12 6 16 0M44 28c0 4 4 6 4 10"/></svg>`,
    mate: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2"><path d="M32 44a18 18 0 0 0 36 0v22a8 8 0 0 1-8 8H40a8 8 0 0 1-8-8z"/><path d="M50 28v18"/><path d="M58 32l-8 12-8-12"/><path d="M60 56v22"/></svg>`,
    agua: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2"><path d="M50 18c-10 14-20 26-20 38a20 20 0 0 0 40 0c0-12-10-24-20-38z"/><path d="M40 56c0 6 4 10 10 10"/></svg>`,
    refresco: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2"><path d="M34 30h32l-3 50H37z"/><path d="M34 30l2-8h28l2 8"/><path d="M36 44h28M36 56h28"/></svg>`,
    default: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2"><circle cx="50" cy="50" r="30"/><circle cx="50" cy="50" r="18"/><circle cx="50" cy="50" r="6"/></svg>`,
  };

  function iconFor(name) {
    const n = name.toLowerCase();
    if (n.includes('medialuna')) return ICONS.medialuna;
    if (n.includes('factura')) return ICONS.factura;
    if (n.includes('alfajor')) return ICONS.alfajor;
    if (n.includes('palmer')) return ICONS.palmer;
    if (n.includes('cono')) return ICONS.cono;
    if (n.includes('chajá') || n.includes('chaja')) return ICONS.chaja;
    if (n.includes('milhoja')) return ICONS.milhoja;
    if (n.includes('tarta') || n.includes('torta') || n.includes('pastel')) return ICONS.tarta;
    if (n.includes('pan')) return ICONS.pan;
    if (n.includes('bola')) return ICONS.bola;
    if (n.includes('vigilante') || n.includes('cremona')) return ICONS.factura;
    if (n.includes('empanada')) return ICONS.empanada;
    if (n.includes('tostado')) return ICONS.tostado;
    if (n.includes('sándwich') || n.includes('sandwich')) return ICONS.sandwich;
    if (n.includes('chapata')) return ICONS.chapata;
    if (n.includes('pizza')) return ICONS.pizza;
    if (n.includes('café') || n.includes('cafe') || n.includes('latte') || n.includes('cortado')) return ICONS.cafe;
    if (n.includes('té') || n === 'te') return ICONS.te;
    if (n.includes('mate')) return ICONS.mate;
    if (n.includes('agua')) return ICONS.agua;
    if (n.includes('refresco')) return ICONS.refresco;
    return ICONS.default;
  }

  /* ---- Render tabs ---- */
  data.categories.forEach((cat, i) => {
    const t = document.createElement('a');
    t.className = 'menu__tab' + (i === 0 ? ' is-active' : '');
    t.href = `#cat-${cat.id}`;
    t.dataset.cat = cat.id;
    t.textContent = cat.name;
    t.setAttribute('role', 'tab');
    tabs.appendChild(t);
  });

  /* ---- Render categorías ---- */
  data.categories.forEach((cat, catIndex) => {
    const section = document.createElement('section');
    section.className = 'menu__category';
    section.id = `cat-${cat.id}`;
    section.dataset.cat = cat.id;
    section.setAttribute('aria-labelledby', `cat-${cat.id}-title`);

    section.innerHTML = `
      <header class="menu__category-head" data-reveal>
        <h3 id="cat-${cat.id}-title">${cat.name}</h3>
        ${cat.caption ? `<p>${cat.caption}</p>` : ''}
      </header>
      <div class="menu__grid" data-reveal-stagger></div>
    `;

    const grid = section.querySelector('.menu__grid');

    cat.items.forEach((item, i) => {
      const article = document.createElement('article');
      article.className = `product ${shadeFor(catIndex + i)}`;
      article.dataset.id = item.id;

      const priceLabel = fmt(item.price);
      const tagsHtml = (item.tags || []).slice(0, 1)
        .map((t) => `<span class="product__tag">${t}</span>`)
        .join('');

      article.innerHTML = `
        <div class="product__media" aria-hidden="true">
          ${tagsHtml}
          <div class="product__media-art">${iconFor(item.name)}</div>
        </div>
        <div class="product__body">
          <h4 class="product__name">${item.name}</h4>
          <p class="product__desc">${item.description || ''}</p>
          <div class="product__foot">
            ${
              priceLabel
                ? `<span class="product__price">${priceLabel}</span>`
                : `<span class="product__price product__price--ask">consultar</span>`
            }
            ${
              priceLabel
                ? `<button class="product__add" data-add="${item.id}" aria-label="Agregar ${item.name} al pedido">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                    <span>Agregar</span>
                  </button>`
                : `<span class="product__add product__add--disabled" title="Preguntá por mostrador o agregalo desde WhatsApp">consultar</span>`
            }
          </div>
        </div>
      `;
      grid.appendChild(article);
    });

    root.appendChild(section);
  });

  /* ---- Tabs activos según scroll ---- */
  const tabLinks = Array.from(tabs.querySelectorAll('.menu__tab'));
  const sections = Array.from(root.querySelectorAll('.menu__category'));

  const setActive = (id) => {
    tabLinks.forEach((t) => t.classList.toggle('is-active', t.dataset.cat === id));
  };

  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries
          .filter((e) => e.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)
          .slice(0, 1)
          .forEach((e) => setActive(e.target.dataset.cat));
      },
      { rootMargin: '-180px 0px -55% 0px', threshold: [0.05, 0.3, 0.6] }
    );
    sections.forEach((s) => io.observe(s));
  }

  // Tap en tabs hace scroll suave manual (compensa el header sticky)
  tabLinks.forEach((tab) => {
    tab.addEventListener('click', (ev) => {
      const id = tab.dataset.cat;
      const target = document.getElementById(`cat-${id}`);
      if (!target) return;
      ev.preventDefault();
      const offset = 120;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
      setActive(id);
    });
  });
})();
