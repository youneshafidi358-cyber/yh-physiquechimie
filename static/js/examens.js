/* Examens nationaux : visionneuse rapide, mode examen chronométré, notes de l'élève (gardées sur son appareil) */
(function () {
  var LS = { get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
             set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} },
             del: function (k) { try { localStorage.removeItem(k); } catch (e) {} } };
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function notes() { try { return JSON.parse(LS.get('yh_notes') || '{}'); } catch (e) { return {}; } }
  function hms(s) { s = Math.max(0, Math.round(s)); var h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60), x = s % 60; return h + ':' + (m < 10 ? '0' : '') + m + ':' + (x < 10 ? '0' : '') + x; }
  function beacon(o) { try { o.vid = LS.get('yh_vid') || ''; o.src = 'site'; fetch('https://script.google.com/macros/s/AKfycbxta1pz0xrqrIa9RiENIXd_CQwiQpkvcwtm_sWBH15-UfBTCN4clgsdmtc3HXZtXh4I/exec', { method: 'POST', mode: 'no-cors', body: JSON.stringify(o), headers: { 'Content-Type': 'text/plain;charset=utf-8' }, keepalive: true }).catch(function () {}); } catch (e) {} }

  /* ---------- visionneuse ---------- */
  var ov = document.createElement('div'); ov.className = 'dv'; ov.hidden = true; ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-modal', 'true');
  ov.innerHTML = '<div class="dv-bar"><b class="dv-t"></b><span class="dv-tm" hidden></span><button type="button" class="dv-end" hidden>Terminer</button><button type="button" class="dv-x" aria-label="Fermer">✕</button></div><div class="dv-fin" hidden></div><div class="dv-pages"></div>';
  document.body.appendChild(ov);
  var pg = $('.dv-pages', ov), tm = $('.dv-tm', ov), fin = $('.dv-fin', ov), endB = $('.dv-end', ov), tick = null, cur = null;
  ov.addEventListener('contextmenu', function (e) { e.preventDefault(); });
  function show(imgs, title, start) {
    $('.dv-t', ov).textContent = title || '';
    pg.innerHTML = imgs.split(',').map(function (u, i) { return '<div class="dv-p"><img src="' + u + '" alt="Page ' + (i + 1) + '" ' + (Math.abs(i - (start || 0)) < 2 ? 'fetchpriority="high"' : 'loading="lazy"') + ' draggable="false"><span class="dv-wm">YH Physique-Chimie</span></div>'; }).join('');
    if (ov.hidden) { ov.hidden = false; document.body.style.overflow = 'hidden'; history.pushState(null, '', '#doc'); }
    var p = pg.children[start || 0]; pg.scrollTop = p ? p.offsetTop - 8 : 0;
  }
  function close() { ov.hidden = true; pg.innerHTML = ''; fin.hidden = true; document.body.style.overflow = ''; clearInterval(tick); tick = null; tm.hidden = endB.hidden = true; cur = null; if (location.hash === '#doc') history.back(); refresh(); }
  $('.dv-x', ov).onclick = close;
  addEventListener('keydown', function (e) { if (e.key === 'Escape' && !ov.hidden) close(); });
  addEventListener('popstate', function () { if (!ov.hidden && location.hash !== '#doc') { location.hash = ''; close(); } });

  function row(k) { return $('tr[data-k="' + k + '"]'); }
  function imgsOf(k, w) { var r = row(k); var b = r && $(w === 'c' ? '.xc' : '.xs', r); return b ? b.dataset.imgs : ''; }

  $$('.xs,.xc').forEach(function (b) { b.addEventListener('click', function (e) { e.preventDefault(); show(b.dataset.imgs, b.dataset.t, 0); beacon({ ev: 'ouverture_document', titre: b.dataset.t, type: b.classList.contains('xc') ? 'Corrigé' : 'Examen', niveau: '2BAC' }); }); });
  $$('.xth').forEach(function (a) { a.addEventListener('click', function (e) { e.preventDefault(); var im = imgsOf(a.dataset.k, a.dataset.w); if (im) show(im, a.dataset.t, +a.dataset.p || 0); }); });

  /* ---------- mode examen chronométré ---------- */
  function key(k) { return 'yh_exam_' + k; }
  function finish(k, timeout) {
    clearInterval(tick); tick = null; tm.hidden = endB.hidden = true; LS.del(key(k));
    var n = notes()[k];
    fin.hidden = false;
    fin.innerHTML = '<b>' + (timeout ? '⏰ Temps écoulé !' : '✅ Examen terminé.') + '</b> Corrige-toi avec le corrigé, puis note-toi sur 20.' +
      '<span class="dv-fr"><button type="button" class="dv-c">✅ Voir le corrigé</button><label>Ma note : <input type="number" min="0" max="20" step="0.25" inputmode="decimal" value="' + (n != null ? n : '') + '" class="dv-n"> /20</label><button type="button" class="dv-s">Enregistrer</button></span>';
    $('.dv-c', fin).onclick = function () { show(imgsOf(k, 'c'), 'Corrigé – ' + $('.dv-t', ov).textContent.replace(/^⏱ /, ''), 0); };
    $('.dv-s', fin).onclick = function () { var v = parseFloat(($('.dv-n', fin).value || '').replace(',', '.')); if (isNaN(v) || v < 0 || v > 20) return; var o = notes(); o[k] = v; LS.set('yh_notes', JSON.stringify(o)); this.textContent = '✔ Enregistré'; refresh(); };
    beacon({ ev: 'fin_mode_examen', titre: k, type: timeout ? 'temps écoulé' : 'terminé', niveau: '2BAC' });
  }
  function run(k) {
    var st = +LS.get(key(k)), dur = (+row(k).dataset.dur) * 60;
    function upd() { var left = dur - (Date.now() - st) / 1000; if (left <= 0) return finish(k, true); tm.textContent = '⏱ ' + hms(left); tm.classList.toggle('dv-warn', left < 900); }
    tm.hidden = endB.hidden = false; fin.hidden = true; upd(); clearInterval(tick); tick = setInterval(upd, 1000);
    endB.onclick = function () { if (confirmEnd()) finish(k, false); };
  }
  function confirmEnd() { if (endB.dataset.sure) { delete endB.dataset.sure; endB.textContent = 'Terminer'; return true; } endB.dataset.sure = 1; endB.textContent = 'Sûr ? Terminer'; setTimeout(function () { delete endB.dataset.sure; endB.textContent = 'Terminer'; }, 3000); return false; }
  $$('.xt').forEach(function (b) {
    b.addEventListener('click', function (e) {
      e.preventDefault(); var k = b.dataset.k, r = row(k);
      if (!LS.get(key(k))) { LS.set(key(k), Date.now()); beacon({ ev: 'debut_mode_examen', titre: k, niveau: '2BAC' }); }
      cur = k; show(imgsOf(k, 's'), '⏱ ' + $('.xs', r).dataset.t, 0); run(k);
    });
  });

  /* ---------- notes de l'élève ---------- */
  $$('.xn').forEach(function (inp) {
    var k = inp.closest('tr').dataset.k, n = notes()[k]; if (n != null) inp.value = n;
    inp.addEventListener('change', function () { var o = notes(), v = parseFloat((inp.value || '').replace(',', '.')); if (isNaN(v)) delete o[k]; else o[k] = Math.max(0, Math.min(20, v)); LS.set('yh_notes', JSON.stringify(o)); refresh(); });
  });
  function refresh() {
    var o = notes(), ks = Object.keys(o).filter(function (k) { return row(k); });
    $$('.xn').forEach(function (inp) { var k = inp.closest('tr').dataset.k; inp.value = o[k] != null ? o[k] : ''; });
    $$('.xt').forEach(function (b) { var st = +LS.get(key(b.dataset.k)), r = row(b.dataset.k); if (!st) { b.textContent = '⏱ Mode examen'; return; } var left = (+r.dataset.dur) * 60 - (Date.now() - st) / 1000; b.textContent = left > 0 ? '▶ Reprendre (' + hms(left) + ')' : '⏰ Terminé'; });
    var box = $('#mesres'); if (!box) return;
    if (!ks.length) { box.innerHTML = '<p class="tip">Fais un examen en <b>mode examen</b> ou écris ta note dans le tableau : ta progression apparaîtra ici (elle reste sur ton appareil).</p>'; return; }
    var v = ks.map(function (k) { return o[k]; }), moy = v.reduce(function (a, b) { return a + b; }, 0) / v.length, best = Math.max.apply(null, v);
    box.innerHTML = '<div class="mr"><div><b>' + ks.length + '</b><span>examen' + (ks.length > 1 ? 's' : '') + ' faits</span></div><div><b>' + moy.toFixed(2).replace('.', ',') + '</b><span>moyenne /20</span></div><div><b>' + String(best).replace('.', ',') + '</b><span>meilleure note</span></div></div>' +
      '<ul class="mrl">' + ks.sort().reverse().map(function (k) { var p = k.split('-'); return '<li><span>' + p[0] + ' ' + p[1] + ' – ' + (p[2] === 'N' ? 'normale' : 'rattrapage') + '</span><i style="width:' + (o[k] * 5) + '%"></i><b>' + String(o[k]).replace('.', ',') + '/20</b></li>'; }).join('') + '</ul>';
  }
  refresh();

  /* ---------- onglets SM / PC ---------- */
  $$('[data-fil]').forEach(function (t) { t.addEventListener('click', function () { $$('[data-fil]').forEach(function (x) { x.classList.toggle('on', x === t); }); $$('.xfil').forEach(function (p) { p.hidden = p.id !== 'fil-' + t.dataset.fil; }); }); });
})();
