/* Avis des visiteurs (étoiles + commentaire) — YH Physique-Chimie
   Les avis sont envoyés au Google Sheet « Statistiques YH » (même script que les statistiques). */
(function () {
  var URL_SCRIPT = "https://script.google.com/macros/s/AKfycbxta1pz0xrqrIa9RiENIXd_CQwiQpkvcwtm_sWBH15-UfBTCN4clgsdmtc3HXZtXh4I/exec";
  var LABELS = ["", "Pas du tout", "Bof", "Correct", "Très bien", "Excellent !"];
  function ls(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  var vid = ls("yh_vid"); if (!vid) { vid = Math.random().toString(36).slice(2, 10) + Date.now().toString(36); ls("yh_vid", vid); }
  var done = ls("yh_avis") === "1";
  var views = +(ls("yh_pv") || 0) + 1; ls("yh_pv", String(views));

  var css = ".av-fab{position:fixed;left:16px;bottom:18px;z-index:60;display:inline-flex;align-items:center;gap:6px;min-height:46px;padding:10px 16px;border-radius:999px;border:0;background:#0f2350;color:#fff;font:700 14.5px/1 Inter,system-ui,sans-serif;box-shadow:0 8px 22px rgba(15,35,80,.3);cursor:pointer}" +
    ".av-fab b{color:#f5c542;font-size:17px}.av-fab.done{background:#2e7d4f}" +
    ".av-back{position:fixed;inset:0;z-index:70;background:rgba(10,20,45,.55);display:flex;align-items:center;justify-content:center;padding:16px}" +
    ".av-box{background:#fff;border-radius:20px;max-width:440px;width:100%;padding:22px 20px 18px;box-shadow:0 20px 60px rgba(0,0,0,.3);font-family:Inter,system-ui,sans-serif;color:#14213d;position:relative;animation:avin .25s ease}" +
    "@keyframes avin{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}@media (prefers-reduced-motion:reduce){.av-box{animation:none}}" +
    ".av-box h2{margin:0 0 4px;font:800 21px/1.25 Fraunces,Georgia,serif;color:#0f2350}.av-box p{margin:0 0 12px;color:#565f74;font-size:14.5px}" +
    ".av-x{position:absolute;top:8px;right:8px;width:44px;height:44px;border:0;background:none;font-size:24px;color:#565f74;cursor:pointer;border-radius:12px}" +
    ".av-stars{display:flex;gap:4px;justify-content:center;margin:6px 0 2px;border:0;padding:0}.av-stars legend{position:absolute;left:-9999px}" +
    ".av-stars input{position:absolute;opacity:0;width:1px;height:1px}.av-stars label{font-size:40px;line-height:1;cursor:pointer;color:#d5dbe6;padding:2px 3px;transition:transform .1s}" +
    ".av-stars label.on{color:#f5b400}.av-stars label:hover{transform:scale(1.12)}.av-stars input:focus-visible+label{outline:3px solid #123c8c;border-radius:8px}" +
    ".av-lab{text-align:center;font-weight:700;color:#8a5a10;min-height:22px;margin-bottom:10px}" +
    ".av-box textarea{width:100%;min-height:84px;border:1px solid #c9d6ee;border-radius:12px;padding:10px 12px;font:15px/1.4 Inter,system-ui,sans-serif;resize:vertical;box-sizing:border-box}" +
    ".av-box textarea:focus{outline:3px solid #123c8c33;border-color:#123c8c}" +
    ".av-row{display:flex;gap:10px;justify-content:flex-end;margin-top:12px;flex-wrap:wrap}" +
    ".av-row button{min-height:44px;padding:10px 18px;border-radius:12px;border:0;font:700 15px Inter,system-ui,sans-serif;cursor:pointer}" +
    ".av-send{background:#123c8c;color:#fff}.av-send:disabled{opacity:.45;cursor:not-allowed}.av-later{background:#f1f4f9;color:#123c8c}" +
    ".av-ok{text-align:center;padding:10px 0}.av-ok div{font-size:46px}" +
    ".av-small{font-size:12.5px;color:#6b7590;margin-top:8px}" +
    "@media print{.av-fab{display:none}}";
  var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);

  var fab = document.createElement("button");
  fab.type = "button"; fab.className = "av-fab" + (done ? " done" : "");
  fab.innerHTML = done ? "<b>★</b> Merci pour ton avis" : "<b>★</b> Noter le site";
  fab.setAttribute("aria-haspopup", "dialog");
  document.body.appendChild(fab);

  function send(stars, comment) {
    var body = JSON.stringify({ ev: "avis", vid: vid, src: "site", dev: /Mobi|Android|iPhone/i.test(navigator.userAgent) ? "téléphone" : "ordinateur",
      br: "", niveau: String(stars), titre: (comment || "").slice(0, 600), type: location.pathname, canal: document.title.slice(0, 120), nouveau: 0 });
    try { if (navigator.sendBeacon && navigator.sendBeacon(URL_SCRIPT, new Blob([body], { type: "text/plain;charset=utf-8" }))) return; } catch (e) {}
    try { fetch(URL_SCRIPT, { method: "POST", mode: "no-cors", body: body, headers: { "Content-Type": "text/plain;charset=utf-8" }, keepalive: true }); } catch (e) {}
  }

  function open(auto) {
    if (document.querySelector(".av-back")) return;
    var last = document.activeElement;
    var back = document.createElement("div"); back.className = "av-back";
    back.innerHTML = '<div class="av-box" role="dialog" aria-modal="true" aria-labelledby="avT">' +
      '<button type="button" class="av-x" aria-label="Fermer">×</button>' +
      '<h2 id="avT">' + (done ? "Tu peux modifier ton avis" : "Ton avis compte !") + '</h2>' +
      '<p>Combien d\'étoiles donnes-tu au site YH Physique-Chimie ?</p>' +
      '<fieldset class="av-stars"><legend>Note sur 5</legend>' +
      [1, 2, 3, 4, 5].map(function (n) { return '<input type="radio" name="avn" id="av' + n + '" value="' + n + '"><label for="av' + n + '" title="' + n + ' étoile' + (n > 1 ? "s" : "") + '" aria-label="' + n + ' étoile' + (n > 1 ? "s" : "") + ' : ' + LABELS[n] + '">★</label>'; }).join("") +
      '</fieldset><div class="av-lab" aria-live="polite"></div>' +
      '<label for="avC" style="font-weight:600;font-size:14px">Un commentaire ? (facultatif)</label>' +
      '<textarea id="avC" maxlength="600" placeholder="Ce que tu aimes, ce qu\'il faut améliorer, une leçon que tu veux…"></textarea>' +
      '<div class="av-row"><button type="button" class="av-later">' + (auto ? "Plus tard" : "Annuler") + '</button><button type="button" class="av-send" disabled>Envoyer</button></div>' +
      '<div class="av-small">Ne mets pas ton nom ni ton numéro : l\'avis est anonyme.</div></div>';
    document.body.appendChild(back);
    var box = back.querySelector(".av-box"), lab = back.querySelector(".av-lab"), btn = back.querySelector(".av-send");
    var labels = back.querySelectorAll(".av-stars label"), val = 0;
    function paint(n) { labels.forEach(function (l, i) { l.classList.toggle("on", i < n); }); lab.textContent = n ? LABELS[n] : ""; }
    back.querySelectorAll(".av-stars input").forEach(function (r) {
      r.addEventListener("change", function () { val = +r.value; paint(val); btn.disabled = false; });
    });
    labels.forEach(function (l, i) { l.addEventListener("mouseenter", function () { paint(i + 1); }); l.addEventListener("mouseleave", function () { paint(val); }); });
    function close() { back.remove(); document.removeEventListener("keydown", esc); if (last && last.focus) last.focus(); }
    function esc(e) { if (e.key === "Escape") { later(); } }
    function later() { ls("yh_avis_later", String(Date.now())); close(); }
    document.addEventListener("keydown", esc);
    back.addEventListener("click", function (e) { if (e.target === back) later(); });
    back.querySelector(".av-x").onclick = later;
    back.querySelector(".av-later").onclick = later;
    btn.onclick = function () {
      if (!val) return;
      send(val, back.querySelector("#avC").value.trim());
      ls("yh_avis", "1"); ls("yh_avis_note", String(val)); done = true;
      fab.className = "av-fab done"; fab.innerHTML = "<b>★</b> Merci pour ton avis";
      box.innerHTML = '<div class="av-ok"><div>🙏</div><h2>Merci beaucoup !</h2><p>Ton avis aide à améliorer le site pour tous les élèves.</p><div class="av-row" style="justify-content:center"><button type="button" class="av-send">Fermer</button></div></div>';
      box.querySelector(".av-send").onclick = close; box.querySelector(".av-send").focus();
    };
    setTimeout(function () { back.querySelector("#av5").focus(); }, 30);
  }
  fab.addEventListener("click", function () { open(false); });

  /* Invitation automatique : une seule fois par visiteur, après 3 pages vues ou 75 s sur une page,
     puis de nouveau 7 jours après « Plus tard ». */
  if (!done) {
    var lt = +(ls("yh_avis_later") || 0);
    if (Date.now() - lt > 7 * 86400000) {
      var shown = false;
      var ask = function () { if (shown || document.querySelector("#viewer.open")) return; shown = true; open(true); };
      if (views >= 3) setTimeout(ask, 20000); else setTimeout(ask, 75000);
    }
  }
})();
