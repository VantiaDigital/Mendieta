/* ============================================================
   MAIN — Mendieta
   ------------------------------------------------------------
   Header sticky, mobile nav, reveals on scroll, current year.
============================================================ */

(function () {
  'use strict';

  /* ---- Año actual en el footer ---- */
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---- Header shadow on scroll ---- */
  const header = document.getElementById('siteHeader');
  let lastY = 0;
  const onScroll = () => {
    const y = window.scrollY;
    if (header) header.classList.toggle('is-scrolled', y > 8);
    lastY = y;
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---- Mobile nav toggle ---- */
  const toggle = document.getElementById('navToggle');
  const mobileNav = document.getElementById('mobileNav');
  let mobileOpen = false;
  const closeMobile = () => {
    mobileOpen = false;
    mobileNav?.classList.remove('is-open');
    toggle?.setAttribute('aria-expanded', 'false');
    mobileNav?.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  };
  const openMobile = () => {
    mobileOpen = true;
    mobileNav?.classList.add('is-open');
    toggle?.setAttribute('aria-expanded', 'true');
    mobileNav?.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  };
  toggle?.addEventListener('click', () => (mobileOpen ? closeMobile() : openMobile()));
  mobileNav?.querySelectorAll('a').forEach((a) => a.addEventListener('click', closeMobile));

  document.addEventListener('keydown', (ev) => {
    if (ev.key === 'Escape' && mobileOpen) closeMobile();
  });

  /* ---- Reveals on scroll ---- */
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add('is-visible');
            io.unobserve(e.target);
          }
        });
      },
      { rootMargin: '0px 0px -10% 0px', threshold: 0.05 }
    );

    const observeAll = () => {
      document
        .querySelectorAll('[data-reveal]:not(.is-visible), [data-reveal-stagger]:not(.is-visible)')
        .forEach((el) => io.observe(el));
    };
    observeAll();

    // Observamos también lo que añade menu.js / cart.js después
    const mo = new MutationObserver(observeAll);
    mo.observe(document.body, { childList: true, subtree: true });
  } else {
    // Sin IO, mostrar todo
    document.querySelectorAll('[data-reveal], [data-reveal-stagger]').forEach((el) =>
      el.classList.add('is-visible')
    );
  }

  /* ---- Smooth scroll para anclas internas ---- */
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener('click', (ev) => {
      const href = a.getAttribute('href');
      if (!href || href === '#' || href.length < 2) return;
      const target = document.querySelector(href);
      if (!target) return;
      ev.preventDefault();
      const headerH = header ? header.offsetHeight + 8 : 80;
      const top = target.getBoundingClientRect().top + window.scrollY - headerH;
      window.scrollTo({ top, behavior: 'smooth' });
    });
  });
})();
