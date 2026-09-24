/* ============================================================
   Jianzhik.com — Main Behaviors
   ============================================================ */
(function () {
  'use strict';

  /* Nav scroll state */
  const nav = document.querySelector('.nav');
  if (nav) {
    const onScroll = () => {
      if (window.scrollY > 30) nav.classList.add('scrolled');
      else nav.classList.remove('scrolled');
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* Mobile toggle */
  const toggle = document.querySelector('.nav-mobile-toggle');
  const links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      const open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    links.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
      links.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    }));
  }

  /* Smooth scroll for in-page anchors */
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', (e) => {
      const id = a.getAttribute('href');
      if (id.length > 1) {
        const target = document.querySelector(id);
        if (target) {
          e.preventDefault();
          const top = target.getBoundingClientRect().top + window.scrollY - 80;
          window.scrollTo({ top, behavior: 'smooth' });
        }
      }
    });
  });

  /* Reveal on scroll */
  const reveals = document.querySelectorAll('.reveal, .reveal-scale');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(en => {
        if (en.isIntersecting) {
          en.target.classList.add('in');
          io.unobserve(en.target);
        }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.05 });
    reveals.forEach(el => io.observe(el));
  } else {
    reveals.forEach(el => el.classList.add('in'));
  }

  /* Scroll progress bar */
  const bar = document.querySelector('.scroll-progress');
  if (bar) {
    const updateBar = () => {
      const h = document.documentElement;
      const scrolled = (h.scrollTop || document.body.scrollTop) /
                       ((h.scrollHeight - h.clientHeight) || 1);
      bar.style.width = (scrolled * 100).toFixed(2) + '%';
    };
    updateBar();
    window.addEventListener('scroll', updateBar, { passive: true });
    window.addEventListener('resize', updateBar);
  }
  /* FAQ accordion */
  document.querySelectorAll('.faq-item').forEach(item => {
    const q = item.querySelector('.faq-q');
    if (!q) return;
    q.addEventListener('click', () => {
      const isOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach(o => {
        if (o !== item) o.classList.remove('open');
      });
      item.classList.toggle('open', !isOpen);
    });
  });

  /* Feature tabs */
  document.querySelectorAll('[data-tab-group]').forEach(group => {
    const tabs = group.querySelectorAll('.feature-tab');
    const panels = group.querySelectorAll('.feature-panel');
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const target = tab.dataset.tab;
        tabs.forEach(t => t.classList.toggle('active', t === tab));
        panels.forEach(p => p.classList.toggle('active', p.dataset.panel === target));
      });
    });
  });

  /* News filters */
  const filterGroup = document.querySelector('[data-news-filters]');
  const newsGrid = document.querySelector('[data-news-grid]');
  if (filterGroup && newsGrid) {
    const searchInput = filterGroup.querySelector('input[type=search]');
    const buttons = filterGroup.querySelectorAll('.news-filter');
    const applyFilter = () => {
      const cat = (filterGroup.querySelector('.news-filter.active') || {}).dataset?.cat || 'all';
      const q = (searchInput?.value || '').trim().toLowerCase();
      newsGrid.querySelectorAll('.news-card').forEach(card => {
        const cardCat = card.dataset.cat || '';
        const title = (card.dataset.title || card.textContent).toLowerCase();
        const matchCat = cat === 'all' || cardCat === cat;
        const matchQ = !q || title.includes(q);
        card.style.display = (matchCat && matchQ) ? '' : 'none';
      });
    };
    buttons.forEach(b => b.addEventListener('click', () => {
      buttons.forEach(x => x.classList.remove('active'));
      b.classList.add('active');
      applyFilter();
    }));
    if (searchInput) searchInput.addEventListener('input', applyFilter);
  }

  /* Contact form (no backend) */
  const form = document.querySelector('[data-contact-form]');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const status = form.querySelector('[data-form-status]');
      const btn = form.querySelector('button[type=submit]');
      btn.disabled = true;
      btn.textContent = 'Transmitting...';
      setTimeout(() => {
        if (status) status.textContent = 'OK Message transmitted successfully. We will reply within 24 hours.';
        btn.textContent = 'Sent';
        form.reset();
        setTimeout(() => { btn.disabled = false; btn.innerHTML = '<span>Transmit Message</span><span class=arrow>-></span>'; }, 2400);
      }, 900);
    });
  }

  /* Animated count-up */
  document.querySelectorAll('[data-count]').forEach(el => {
    const target = parseFloat(el.dataset.count);
    const dur = parseInt(el.dataset.dur || '1800', 10);
    const dec = (el.dataset.count.split('.')[1] || '').length;
    const suffix = el.dataset.suffix || '';
    if ('IntersectionObserver' in window) {
      const obs = new IntersectionObserver((entries) => {
        entries.forEach(en => {
          if (en.isIntersecting) {
            const start = performance.now();
            const tick = (t) => {
              const p = Math.min((t - start) / dur, 1);
              const eased = 1 - Math.pow(1 - p, 3);
              el.textContent = (target * eased).toFixed(dec) + suffix;
              if (p < 1) requestAnimationFrame(tick);
            };
            requestAnimationFrame(tick);
            obs.unobserve(el);
          }
        });
      }, { threshold: 0.4 });
      obs.observe(el);
    }
  });

  /* Year in footer */
  document.querySelectorAll('[data-year]').forEach(el => el.textContent = new Date().getFullYear());
})();
