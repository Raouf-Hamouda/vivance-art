/* VIVANCE · site.js: smooth scroll, reveals, nav state, menu, work filters, mail forms */
(() => {
  const root = document.documentElement; root.classList.remove('no-js');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let lenis = null;
  if (window.Lenis && !reduce) { lenis = new Lenis({ lerp: 0.11, smoothWheel: true }); if (window.gsap) { gsap.ticker.add(t => lenis.raf(t * 1000)); gsap.ticker.lagSmoothing(0); } }
  const reveals = [...document.querySelectorAll('[data-reveal]')];
  if (window.gsap && window.ScrollTrigger && !reduce) { gsap.registerPlugin(ScrollTrigger); if (lenis) lenis.on('scroll', ScrollTrigger.update);
    reveals.forEach(el => gsap.to(el, { opacity: 1, y: 0, duration: 0.8, delay: parseFloat(el.dataset.reveal) || 0, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 92%', once: true } })); }
  else reveals.forEach(el => { el.style.opacity = 1; el.style.transform = 'none'; });
  /* nav: solid after the hero (or after 40px on inner pages) */
  const nav = document.querySelector('[data-nav]'), hero = document.querySelector('.hero');
  const solid = () => { const on = scrollY > (hero ? hero.offsetHeight - nav.offsetHeight : 40); nav.classList.toggle('scrolled', on); if (hero) nav.classList.toggle('on-dark', !on); };
  addEventListener('scroll', solid, { passive: true }); solid();
  /* menu */
  const burger = document.querySelector('.burger'), menu = document.querySelector('.menu');
  if (burger && menu) burger.addEventListener('click', () => { const open = menu.classList.toggle('open'); burger.textContent = open ? 'Close' : 'Menu'; burger.setAttribute('aria-expanded', open); root.classList.toggle('menu-open', open); nav.classList.toggle('scrolled', open || nav.classList.contains('scrolled')); if (lenis) open ? lenis.stop() : lenis.start(); });
  /* work filters */
  const filters = document.querySelector('.filters'), works = [...document.querySelectorAll('#works .work, #works .product')];
  if (filters && works.length) { const state = { artist: 'all', avail: 'all' };
    const apply = () => { let n = 0; works.forEach(w => { const ok = (state.artist === 'all' || w.dataset.artist === state.artist) && (state.avail === 'all' || w.dataset.avail === state.avail); w.classList.toggle('hidden', !ok); if (ok) n++; }); const e = document.getElementById('empty'); if (e) e.hidden = n > 0; if (window.ScrollTrigger) ScrollTrigger.refresh(); };
    filters.addEventListener('click', e => { const b = e.target.closest('.tab'); if (!b) return; state[b.dataset.f] = b.dataset.v; filters.querySelectorAll(`.tab[data-f="${b.dataset.f}"]`).forEach(t => t.setAttribute('aria-selected', t === b)); apply(); });
    const q = new URLSearchParams(location.search).get('artist'); if (q) { const b = filters.querySelector(`.tab[data-v="${q}"]`); if (b) b.click(); } }
  /* forms -> email app */
  document.querySelectorAll('form[data-mailto]').forEach(f => f.addEventListener('submit', e => { e.preventDefault(); const d = new FormData(f); if (d.get('website')) return;
    const subject = f.dataset.subject || 'Contact via vivanceart'; const body = [d.get('name') ? 'Name: ' + d.get('name') : '', 'Email: ' + d.get('email'), '', d.get('message') || ''].filter(x => x !== '').join('\n');
    location.href = `mailto:${f.dataset.mailto}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`; }));
  /* shop panel */
  const panel = document.getElementById('shop'), dataEl = document.getElementById('shop-data');
  if (panel && dataEl) {
    const S = JSON.parse(dataEl.textContent); const grid = panel.querySelector('[data-shop-grid]'), fl = panel.querySelector('[data-shop-filters]'); let built = false; const st = { artist: 'all', avail: 'all' };
    panel.querySelector('[data-shop-count]').textContent = S.items.filter(i => !i.sold).length;
    const card = i => `<article class="product${i.sold ? '' : ''}" data-artist="${i.as}" data-avail="${i.sold ? 'sold' : 'available'}"><a class="frame" href="${i.url}"><img src="${i.img}" alt="${i.t}" loading="lazy">${i.sold ? '<span class="pill sold">Sold</span>' : ''}</a><p class="a">${i.a}</p><p class="t"><i>${i.t}</i>${i.y ? ', ' + i.y : ''}</p><p class="p${i.sold ? ' sold' : ''}">${i.sold ? 'Sold' : i.p}</p><div class="buy">${i.sold ? '<span class="btn is-sold">Sold</span>' : (i.direct ? `<a class="btn btn-accent" href="${i.buy}">Buy now</a>` : `<a class="btn btn-accent" href="${i.buy}" target="_blank" rel="noopener">Add to cart ↗</a>`)}<a class="btn btn-ghost" href="${i.url}">Details</a></div></article>`;
    const build = () => { if (built) return; built = true;
      fl.innerHTML = `<button class="tab" data-f="artist" data-v="all" aria-selected="true">All artists</button>` + S.artists.map(a => `<button class="tab" data-f="artist" data-v="${a.s}" aria-selected="false">${a.n}</button>`).join('') + `<span class="sep"></span><button class="tab" data-f="avail" data-v="all" aria-selected="true">All</button><button class="tab" data-f="avail" data-v="available" aria-selected="false">Available</button>`;
      grid.innerHTML = S.items.map(card).join('');
      fl.addEventListener('click', e => { const b = e.target.closest('.tab'); if (!b) return; st[b.dataset.f] = b.dataset.v; fl.querySelectorAll(`.tab[data-f="${b.dataset.f}"]`).forEach(x => x.setAttribute('aria-selected', x === b)); grid.querySelectorAll('.product').forEach(p => p.classList.toggle('hidden', !((st.artist === 'all' || p.dataset.artist === st.artist) && (st.avail === 'all' || p.dataset.avail === st.avail)))); }); };
    const open = () => { build(); panel.hidden = false; void panel.offsetHeight; panel.classList.add('open'); panel.scrollTop = 0; root.classList.add('shop-open'); if (lenis) lenis.stop(); if (menu && menu.classList.contains('open')) burger.click(); history.replaceState(null, '', '#shop'); };
    const close = () => { panel.classList.remove('open'); root.classList.remove('shop-open'); if (lenis) lenis.start(); setTimeout(() => { panel.hidden = true; }, 320); if (location.hash === '#shop') history.replaceState(null, '', location.pathname); };
    document.querySelectorAll('[data-shop-open]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); open(); }));
    panel.querySelector('[data-shop-close]').addEventListener('click', close);
    addEventListener('keydown', e => { if (e.key === 'Escape' && !panel.hidden) close(); });
    if (location.hash === '#shop') open();
  }
  window.VIVANCE = { lenis };
})();
