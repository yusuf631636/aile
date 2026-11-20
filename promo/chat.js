// Chat-screen builder for the messaging-style promo videos. A page defines window.CHAT before
// loading this file; it fills the scene #chat, sets its length (data-dur) and its sound cues
// (data-sfx: pop for incoming, tap for sent, ding for notifications).
(() => {
  const C = window.CHAT, $ = id => document.getElementById(id);
  const scene = $('chat');
  const clock = t => { const m = C.clockStart + Math.floor(t / 5); return `${String(Math.floor(m / 60)).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`; };
  scene.innerHTML = `
    <div class="sb"><span>${clock(0)}</span><span>●●●● 5G ▮</span></div>
    <div class="hdr"><div class="back">‹</div><img class="av" src="${C.avatar}"><div class="who"><b>${C.name}</b><span id="st">${C.sub}</span></div>
      <div class="ics">${ic('phone')}${ic('more-vertical')}</div></div>
    <div class="wall"><div class="msgs" id="msgs"><div class="daychip">Bugün</div></div><div class="typing" id="typing"><i></i><i></i><i></i></div>
      ${(C.notifs || []).map((n, i) => `<div class="notifB" id="nb${i}"><img src="assets/logo-mark.svg"><div><div class="h"><b>getirtrend</b><span>şimdi</span></div><div class="t">${n.title}</div><div class="s">${n.body}</div></div></div>`).join('')}
    </div>
    <div class="inbar"><div class="em">${ic('smile')}</div><div class="field ph" id="field">Mesaj</div><div class="send">${ic('send')}</div></div>
    ${C.msgs.map((m, i) => m.zoom ? `<div class="viewer" id="vw${i}"><div class="vh">${ic('arrow-left')}<div><b>${m.s === 'R' ? 'Siz' : (m.from || C.name)}</b><br><span style="opacity:.7">Bugün ${clock(m.t)}</span></div></div><img src="${m.img}"></div>` : '').join('')}`;
  const box = $('msgs');
  C.msgs.forEach((m, i) => {
    const from = C.group && m.s === 'L' ? `<span class="from" style="color:${C.members[m.from]}">${m.from}</span>` : '';
    let inner;
    if (m.img) inner = `<div class="bub img">${from}<img src="${m.img}" style="height:${m.h || 640}px">${m.cap ? `<div class="cap">${m.cap}</div>` : ''}<small style="padding:0 12px">${clock(m.t)}</small></div>`;
    else if (m.link) inner = `<div class="bub" style="padding:12px 12px 12px">${from}<div class="link"><img src="assets/ui/basvur-og.jpg"><div class="tx"><b>Restoranınızı getirtrend Yemek’e ekleyin</b><em>getirtrend.com</em></div></div><div style="padding:0 12px">${m.text ? m.text + '\n' : ''}<span class="url-t">getirtrend.com/restoran-ol</span></div><small>${clock(m.t)}</small></div>`;
    else inner = `<div class="bub">${from}${m.text}<small>${clock(m.t)}</small></div>`;
    box.insertAdjacentHTML('beforeend', `<div class="w" id="m${i}"><div class="${m.s}">${inner}</div></div>`);
  });
  // length + sound cues for the build script
  const cues = [];
  C.msgs.forEach(m => cues.push(`${m.s === 'L' ? 'pop' : 'tap'}:${m.t.toFixed(2)}`));
  (C.notifs || []).forEach(n => cues.push(`ding:${n.t.toFixed(2)}`));
  scene.dataset.sfx = cues.join(';');
  scene.dataset.dur = String(C.end);

  HOOKS.chat = (lt) => {
    scene.querySelector('.sb span').textContent = clock(lt);
    C.msgs.forEach((m, i) => {
      const w = $('m' + i), k = easeOut((lt - m.t) / 0.3);
      w.style.height = (k * w.firstElementChild.offsetHeight) + 'px';
      const b = w.querySelector('.bub');
      b.style.transform = `scale(${0.85 + 0.15 * k})`; b.style.transformOrigin = m.s === 'L' ? 'left bottom' : 'right bottom';
      b.style.opacity = k;
      if (m.zoom) {
        const v = $('vw' + i), z = Math.min(easeOut((lt - m.zoom[0]) / 0.3), 1 - easeOut((lt - m.zoom[1]) / 0.3));
        v.style.opacity = z; v.querySelector('img').style.transform = `scale(${0.8 + 0.2 * z})`;
      }
    });
    const typer = C.msgs.find(m => m.s === 'L' && lt > m.t - 1.0 && lt < m.t);
    const tk = typer ? 1 : 0;
    $('typing').style.opacity = tk;
    [...$('typing').children].forEach((d, i) => d.style.transform = `translateY(${-10 * Math.max(0, Math.sin(lt * 9 - i * .8))}px)`);
    box.style.paddingBottom = (30 + tk * 140) + 'px';
    $('st').textContent = typer ? (C.group ? `${typer.from} yazıyor...` : 'yazıyor...') : C.sub;
    const f = $('field'); let txt = '';
    C.msgs.forEach(m => { if (m.s === 'R' && m.ty !== undefined && lt >= m.ty && lt < m.t) {
      const full = [...(m.typed || m.text)], p = clamp((lt - m.ty) / Math.max(.3, m.t - m.ty - .3));
      txt = full.slice(0, Math.round(p * full.length)).join('');
    } });
    if (txt) { f.classList.remove('ph'); f.innerHTML = txt + '<span class="caret"></span>'; } else { f.classList.add('ph'); f.textContent = 'Mesaj'; }
    (C.notifs || []).forEach((n, i) => {
      const nk = easeOut((lt - n.t) / 0.35) * (1 - easeOut((lt - n.t - (n.d || 2)) / 0.35));
      $('nb' + i).style.transform = `translateY(${-420 + 436 * nk}px)`;
    });
  };
})();
