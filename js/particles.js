/* ============================================================
   Network / Particle Background — pure canvas, no deps
   ============================================================ */
(function () {
  'use strict';

  const canvas = document.querySelector('.network-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let W = 0, H = 0, dpr = Math.max(1, Math.min(2, window.devicePixelRatio || 1));
  let nodes = [];
  let raf = null;
  const mouse = { x: -9999, y: -9999, active: false };

  const PALETTE = {
    line: 'rgba(0, 229, 255, 0.18)',
    lineStrong: 'rgba(0, 229, 255, 0.45)',
    node: 'rgba(0, 229, 255, 0.85)',
    nodeViolet: 'rgba(124, 92, 255, 0.85)',
    glowCyan: 'rgba(0, 229, 255, 0.5)'
  };

  function resize() {
    const parent = canvas.parentElement;
    const rect = parent.getBoundingClientRect();
    W = rect.width;
    H = rect.height;
    canvas.width = W * dpr;
    canvas.height = H * dpr;
    canvas.style.width = W + 'px';
    canvas.style.height = H + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    seed();
  }

  function seed() {
    const density = Math.min(140, Math.floor((W * H) / 12000));
    nodes = [];
    for (let i = 0; i < density; i++) {
      nodes.push({
        x: Math.random() * W,
        y: Math.random() * H,
        vx: (Math.random() - 0.5) * 0.25,
        vy: (Math.random() - 0.5) * 0.25,
        r: Math.random() * 1.5 + 0.6,
        violet: Math.random() < 0.2
      });
    }
  }

  function step() {
    ctx.clearRect(0, 0, W, H);
    // update
    for (const n of nodes) {
      n.x += n.vx;
      n.y += n.vy;
      if (n.x < 0 || n.x > W) n.vx *= -1;
      if (n.y < 0 || n.y > H) n.vy *= -1;
      // mouse repel
      if (mouse.active) {
        const dx = n.x - mouse.x;
        const dy = n.y - mouse.y;
        const d2 = dx*dx + dy*dy;
        if (d2 < 14000) {
          const d = Math.sqrt(d2) || 1;
          n.x += (dx / d) * 1.2;
          n.y += (dy / d) * 1.2;
        }
      }
    }
    // lines
    for (let i = 0; i < nodes.length; i++) {
      const a = nodes[i];
      for (let j = i + 1; j < nodes.length; j++) {
        const b = nodes[j];
        const dx = a.x - b.x;
        const dy = a.y - b.y;
        const d2 = dx*dx + dy*dy;
        if (d2 < 14000) {
          const alpha = 1 - d2 / 14000;
          ctx.strokeStyle = a.violet || b.violet ? PALETTE.lineStrong.replace('0.45', (0.4 * alpha).toFixed(2)) : PALETTE.line.replace('0.18', (0.18 * alpha).toFixed(2));
          ctx.lineWidth = 0.6;
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.stroke();
        }
      }
    }
    // nodes
    for (const n of nodes) {
      ctx.beginPath();
      ctx.fillStyle = n.violet ? PALETTE.nodeViolet : PALETTE.node;
      ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
      ctx.fill();
    }
    raf = requestAnimationFrame(step);
  }

  canvas.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
    mouse.active = true;
  });
  canvas.addEventListener('mouseleave', () => { mouse.active = false; });

  window.addEventListener('resize', resize);

  // pause when offscreen
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      cancelAnimationFrame(raf); raf = null;
    } else if (!raf) {
      step();
    }
  });

  resize();
  step();
})();