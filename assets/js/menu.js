/* ============================================================
   MENU RENDERER — Mendieta · catálogo tipo app de pedido
   ------------------------------------------------------------
   Renderiza categorías + filas de producto en #menuRoot, y los
   tabs en #menuTabs. Datos desde window.MENDIETA_MENU.
============================================================ */

(function () {
  'use strict';

  const data = window.MENDIETA_MENU;
  if (!data || !data.categories) return;

  const root = document.getElementById('menuRoot');
  if (!root) return;
  const tabs = document.getElementById('menuTabs'); // opcional (solo en vista todo-en-uno)

  // Si la página declara `window.MENDIETA_CATEGORY = 'facturas'`, filtramos
  const filterCat = window.MENDIETA_CATEGORY || null;
  const categoriesToRender = filterCat
    ? data.categories.filter((c) => c.id === filterCat)
    : data.categories;

  /* ---- helpers ---- */
  const fmt = (price) => {
    if (price == null) return null;
    return new Intl.NumberFormat('es-ES', {
      style: 'currency', currency: 'EUR', minimumFractionDigits: 2,
    }).format(price);
  };
  const shade = (i) => `product--shade-${(i % 5) + 1}`;

  /* ---- icon library (SVG inline, trazo blanco sobre gradiente cálido) ---- */
  const ICONS = {
    medialuna: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M30 22c-12 8-20 22-20 38s8 30 20 38c-5-10-7-22-7-38s2-28 7-38z"/><path d="M30 22c18-4 38 8 46 30-8 22-28 34-46 30 10-7 16-18 16-30s-6-23-16-30z"/></svg>`,
    factura: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.4"><circle cx="50" cy="50" r="32"/><path d="M30 50c0-12 9-22 20-22s20 10 20 22"/><path d="M38 50h24M42 60h16"/></svg>`,
    alfajor: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.4"><circle cx="50" cy="50" r="30"/><path d="M22 50h56"/></svg>`,
    palmer: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M20 32c12-6 30-6 30 18 0-24 18-24 30-18"/><path d="M20 68c12 6 30 6 30-18 0 24 18 24 30 18"/><path d="M50 32v36"/></svg>`,
    cono: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M30 30h40l-15 50h-10z"/><path d="M30 30c0-6 9-12 20-12s20 6 20 12"/></svg>`,
    tarta: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.4"><ellipse cx="50" cy="68" rx="32" ry="10"/><path d="M18 68v-18a32 10 0 0 0 64 0V68"/><path d="M50 46v14"/></svg>`,
    milhoja: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.4"><rect x="18" y="32" width="64" height="9" rx="2"/><rect x="18" y="46" width="64" height="9" rx="2"/><rect x="18" y="60" width="64" height="9" rx="2"/></svg>`,
    chaja: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M22 56c4-12 16-20 28-20s24 8 28 20"/><path d="M22 56h56"/><path d="M30 56v14h40V56"/></svg>`,
    pan: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M22 60c0-16 12-26 28-26s28 10 28 26"/><path d="M18 60h64v10H18z"/></svg>`,
    bola: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.4"><circle cx="50" cy="50" r="28"/><path d="M40 60c4 4 16 4 20 0"/></svg>`,
    empanada: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M18 56c0-14 14-26 32-26s32 12 32 26v6H18z"/><path d="M28 60c2-3 4-3 6 0s4 3 6 0s4-3 6 0s4 3 6 0s4-3 6 0s4 3 6 0s4-3 6 0"/></svg>`,
    sandwich: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.4"><rect x="22" y="32" width="56" height="36" rx="2"/><path d="M22 44h56M22 56h56"/></svg>`,
    tostado: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.4"><rect x="22" y="34" width="56" height="32" rx="3"/><path d="M22 50h56"/></svg>`,
    chapata: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.4"><ellipse cx="50" cy="50" rx="32" ry="14"/><path d="M30 50h40" stroke-dasharray="3 4"/></svg>`,
    pizza: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.4"><circle cx="50" cy="50" r="32"/><circle cx="40" cy="44" r="3" fill="currentColor"/><circle cx="58" cy="48" r="3" fill="currentColor"/><circle cx="46" cy="60" r="3" fill="currentColor"/></svg>`,
    cafe: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M24 38h44v22c0 10-10 18-22 18s-22-8-22-18z"/><path d="M68 44h6c4 0 8 4 8 8s-4 8-8 8h-6"/><path d="M40 26c-2 3-2 6 0 9M52 26c-2 3-2 6 0 9"/></svg>`,
    te: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M28 38h40v24c0 8-9 16-20 16s-20-8-20-16z"/><path d="M68 46h6c4 0 8 4 8 8s-4 8-8 8h-6"/></svg>`,
    mate: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M32 44a18 18 0 0 0 36 0v22a8 8 0 0 1-8 8H40a8 8 0 0 1-8-8z"/><path d="M50 28v18"/><path d="M60 56v22"/></svg>`,
    agua: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M50 18c-10 14-20 26-20 38a20 20 0 0 0 40 0c0-12-10-24-20-38z"/></svg>`,
    refresco: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M34 30h32l-3 50H37z"/><path d="M34 30l2-8h28l2 8"/></svg>`,
    default: `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.4"><circle cx="50" cy="50" r="30"/></svg>`,
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

  /* ---- Render tabs (solo si existe el contenedor) ---- */
  if (tabs) {
    categoriesToRender.forEach((cat, i) => {
      const t = document.createElement('button');
      t.className = 'tab' + (i === 0 ? ' is-active' : '');
      t.type = 'button';
      t.dataset.cat = cat.id;
      t.textContent = cat.name;
      t.setAttribute('role', 'tab');
      tabs.appendChild(t);
    });
  }

  /* ---- Render categorías ---- */
  categoriesToRender.forEach((cat, catIndex) => {
    const section = document.createElement('section');
    section.className = 'cat';
    section.id = `cat-${cat.id}`;
    section.dataset.cat = cat.id;

    section.innerHTML = `
      <header class="cat__head">
        <h2 class="cat__title">${cat.name}</h2>
        ${cat.caption ? `<p class="cat__caption">${cat.caption}</p>` : ''}
      </header>
      <div class="cat__grid"></div>
    `;
    const grid = section.querySelector('.cat__grid');

    cat.items.forEach((item, i) => {
      const article = document.createElement('article');
      article.className = `product ${shade(catIndex + i)}`;
      article.dataset.id = item.id;
      const priceLabel = fmt(item.price);
      const tagHtml = (item.tags || []).slice(0, 1).map((t) => `<span class="product__tag">${t}</span>`).join('');

      // Media: foto si existe, si no SVG ilustrativo
      const mediaInner = item.image
        ? `<img src="${item.image}" alt="${item.name}" loading="lazy" decoding="async" />`
        : iconFor(item.name);

      article.innerHTML = `
        <div class="product__media ${item.image ? 'product__media--photo' : ''}" aria-hidden="true">
          ${tagHtml}
          ${mediaInner}
        </div>
        <div class="product__body">
          <h3 class="product__name">${item.name}</h3>
          <p class="product__desc">${item.description || ''}</p>
          <div class="product__foot">
            ${
              priceLabel
                ? `<span class="product__price">${priceLabel}</span>`
                : `<span class="product__price product__price--ask">a consultar</span>`
            }
            <div class="product__add-slot" data-slot="${item.id}">
              <button class="product__add" data-add="${item.id}" aria-label="Agregar ${item.name}">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
              </button>
            </div>
          </div>
        </div>
      `;
      grid.appendChild(article);
    });

    root.appendChild(section);
  });

  /* ---- Tabs activos según scroll (solo si hay tabs) ---- */
  if (!tabs) {
    // Página de categoría única: no hay tabs, salimos
    return setupRenderApi();
  }
  const tabButtons = Array.from(tabs.querySelectorAll('.tab'));
  const sections = Array.from(root.querySelectorAll('.cat'));
  const setActive = (id) => {
    tabButtons.forEach((t) => {
      const active = t.dataset.cat === id;
      t.classList.toggle('is-active', active);
      if (active) {
        // Auto-scroll de tabs para mantener visible el activo
        t.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
      }
    });
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
      { rootMargin: '-160px 0px -55% 0px', threshold: [0.05, 0.3, 0.6] }
    );
    sections.forEach((s) => io.observe(s));
  }

  // Click en tab → scroll suave
  tabButtons.forEach((tab) => {
    tab.addEventListener('click', () => {
      const id = tab.dataset.cat;
      const target = document.getElementById(`cat-${id}`);
      if (!target) return;
      const offset = 130;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
      setActive(id);
    });
  });

  setupRenderApi();

  // Exponer API para que cart.js pueda re-renderizar el botón ± de un producto
  function setupRenderApi() {
    window.MendietaMenuRender = {
      renderAddSlot(productId, qty) {
        const slot = document.querySelector(`.product__add-slot[data-slot="${productId}"]`);
        if (!slot) return;
        if (qty > 0) {
          slot.innerHTML = `
            <div class="product__add product__add--qty" data-qty-for="${productId}">
              <button type="button" data-dec="${productId}" aria-label="Quitar uno">−</button>
              <span>${qty}</span>
              <button type="button" data-inc="${productId}" aria-label="Sumar uno">+</button>
            </div>
          `;
        } else {
          slot.innerHTML = `
            <button class="product__add" data-add="${productId}" aria-label="Agregar al pedido">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
            </button>
          `;
        }
      },
    };
  }
})();
