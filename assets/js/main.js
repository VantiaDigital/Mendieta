/* ============================================================
   MAIN — Mendieta
   ------------------------------------------------------------
   Mobile nav, reveals on scroll, año en footer.
============================================================ */

(function () {
  'use strict';

  /* Año actual en el footer */
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* Mobile nav toggle */
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

  /* Reveals on scroll */
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
      { rootMargin: '0px 0px -8% 0px', threshold: 0.04 }
    );
    const observeAll = () => {
      document.querySelectorAll('[data-reveal]:not(.is-visible)').forEach((el) => io.observe(el));
    };
    observeAll();
    const mo = new MutationObserver(observeAll);
    mo.observe(document.body, { childList: true, subtree: true });
  } else {
    document.querySelectorAll('[data-reveal]').forEach((el) => el.classList.add('is-visible'));
  }
})();
