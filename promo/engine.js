// Tiny deterministic animation engine. Every frame is a pure function of time t,
// so render.js can capture frames exactly. Scene durations come from the voiceover
// (window.setTimeline), so visuals stay in sync with the narration.
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
  const easeOut = x => 1 - Math.pow(1 - clamp(x), 3);
  const back = x => { x = clamp(x); const c1 = 1.5, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
  const TR = 0.4; // scene transition length
  const H = window.HOOKS = window.HOOKS || {};
  let scenes = [], total = 0;

  function setTimeline(durs) {
    const els = [...document.querySelectorAll('.scene')];
    let s = 0;
    scenes = els.map((el, i) => { const d = durs[i]; const o = { el, start: s, dur: d }; s += d; return o; });
    total = s;
    window.DUR = total;
    return total;
  }

  function animEl(el, lt) {
    const start = parseFloat(el.dataset.in), d = parseFloat(el.dataset.d || 0.55);
    const k = clamp((lt - start) / d), e = easeOut(k), a = el.dataset.anim || 'up';
    let tf = '';
    if (a === 'up') tf = `translateY(${(1 - e) * 70}px)`;
    else if (a === 'down') tf = `translateY(${(e - 1) * 70}px)`;
    else if (a === 'left') tf = `translateX(${(1 - e) * -220}px)`;
    else if (a === 'right') tf = `translateX(${(1 - e) * 220}px)`;
    else if (a === 'pop') tf = `scale(${0.5 + 0.5 * back(k)})`;
    else if (a === 'rise') tf = `translateY(${(1 - e) * 500}px)`;
    el.style.opacity = a === 'pop' ? clamp(k * 2) : e;
    el.style.transform = tf + (el.dataset.base ? ' ' + el.dataset.base : '');
  }

  function render(t) {
    // ambient background
    const b = document.querySelectorAll('.blob');
    if (b[0]) b[0].style.transform = `translate(${-200 + 140 * Math.sin(t * .35)}px, ${-120 + 180 * Math.cos(t * .28)}px)`;
    if (b[1]) b[1].style.transform = `translate(${560 + 120 * Math.cos(t * .3)}px, ${1250 + 160 * Math.sin(t * .4)}px)`;
    if (b[2]) b[2].style.transform = `translate(${700 + 100 * Math.sin(t * .25)}px, ${300 + 120 * Math.cos(t * .33)}px)`;
    document.querySelectorAll('.dot').forEach((d, i) => {
      const sp = 20 + (i * 37) % 40, x = (i * 173) % 1080, y = (1920 + 60 - ((t * sp + i * 311) % 2040));
      d.style.transform = `translate(${x + 20 * Math.sin(t + i)}px, ${y}px)`;
      d.style.opacity = .15 + .25 * ((i * 7) % 5) / 5;
    });
    const pr = $('.progress'); if (pr) pr.style.width = (t / total * 1080) + 'px';

    scenes.forEach((s, i) => {
      const lt = t - s.start, last = i === scenes.length - 1;
      const on = lt >= 0 && lt < s.dur + (last ? 1 : 0);
      s.el.style.display = on ? 'flex' : 'none';
      if (!on) return;
      const inK = i === 0 ? 1 : easeOut(lt / TR), outK = last ? 1 : clamp((s.dur - lt) / TR);
      s.el.style.opacity = Math.min(inK, outK);
      const drift = 1 + 0.025 * (lt / s.dur);
      s.el.style.transform = `scale(${drift * (1 + 0.06 * (1 - outK))}) translateY(${(1 - inK) * 40}px)`;
      s.el.querySelectorAll('[data-in]').forEach(el => animEl(el, lt));
      const hook = H[s.el.id]; if (hook) hook(lt, s.dur, s.el);
    });
  }

  Object.assign(window, { setTimeline, render, clamp, easeOut, back });

  // ambient decoration
  const st = $('#stage');
  for (let i = 0; i < 18; i++) { const d = document.createElement('div'); d.className = 'dot'; const r = 6 + (i * 5) % 12; d.style.width = d.style.height = r + 'px'; st.prepend(d); }

  // live preview with default timings when opened in a browser
  window.addEventListener('load', () => {
    if (location.search.includes('capture')) return;
    setTimeline(window.DEFAULT_DURS);
    const t0 = performance.now();
    (function loop() { render(((performance.now() - t0) / 1000) % (total + 1)); requestAnimationFrame(loop); })();
  });
})();
