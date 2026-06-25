
  // header scroll state
  const header = document.getElementById('header');
  const onScroll = () => {
    if (window.scrollY > 8) header.classList.add('is-scrolled');
    else header.classList.remove('is-scrolled');
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // mega menu: hover + click (supports data-mega and legacy data-dropdown)
  document.querySelectorAll('.nav-item[data-mega], .nav-item[data-dropdown]').forEach((el) => {
    let timer;
    const open = () => {
      clearTimeout(timer);
      // close siblings, open this
      document.querySelectorAll('.nav-item.open').forEach(n => { if (n !== el) n.classList.remove('open'); });
      el.classList.add('open');
    };
    const close = () => { timer = setTimeout(() => el.classList.remove('open'), 180); };
    el.addEventListener('mouseenter', open);
    el.addEventListener('mouseleave', close);
    el.querySelector('.nav-link').addEventListener('click', (e) => {
      const href = el.querySelector('.nav-link').getAttribute('href') || '';
      // If the nav-link points to a real page, let the browser navigate.
      const isRealHref = href && href !== '#' && !href.startsWith('#');
      if (isRealHref) return;
      e.preventDefault();
      const wasOpen = el.classList.contains('open');
      document.querySelectorAll('.nav-item.open').forEach(n => n.classList.remove('open'));
      if (!wasOpen) el.classList.add('open');
    });
  });
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.nav-item[data-mega], .nav-item[data-dropdown]')) {
      document.querySelectorAll('.nav-item.open').forEach(n => n.classList.remove('open'));
    }
  });

  // capability tiles: cursor-follow spotlight
  document.querySelectorAll('#capabilitiesGrid .block').forEach((tile) => {
    tile.addEventListener('pointermove', (e) => {
      const r = tile.getBoundingClientRect();
      tile.style.setProperty('--mx', `${e.clientX - r.left}px`);
      tile.style.setProperty('--my', `${e.clientY - r.top}px`);
    });
  });
