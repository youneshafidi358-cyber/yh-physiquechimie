/* Bouton « Suivre le site » : notifications des nouveaux documents — YH Physique-Chimie */
(function () {
  try { fetch("/api/push/tick", { keepalive: true }).catch(function () {}); } catch (e) {}
  var ok = "serviceWorker" in navigator && "PushManager" in window && "Notification" in window;
  var ios = /iPhone|iPad|iPod/.test(navigator.userAgent) && !window.MSStream;
  var standalone = window.matchMedia("(display-mode: standalone)").matches || navigator.standalone === true;
  if (!ok && !ios) return;
  var css = ".sv-btn{display:inline-flex;align-items:center;gap:6px;margin:0 4px;padding:7px 14px;min-height:38px;border-radius:999px;border:1px solid rgba(255,255,255,.45);background:rgba(255,255,255,.1);color:#fff;font:800 14px/1 Inter,system-ui,sans-serif;cursor:pointer;white-space:nowrap}" +
    ".sv-btn:hover{background:rgba(255,255,255,.2)}.sv-btn.on{background:#2e7d4f;border-color:#2e7d4f}" +
    ".sv-back{position:fixed;inset:0;z-index:90;background:rgba(10,20,45,.55);display:flex;align-items:center;justify-content:center;padding:16px}" +
    ".sv-box{background:#fff;color:#0f2350;border-radius:18px;max-width:420px;width:100%;padding:22px;font:15px/1.5 Inter,system-ui,sans-serif;box-shadow:0 20px 60px rgba(0,0,0,.3)}" +
    ".sv-box h2{margin:0 0 8px;font-size:20px}.sv-box ol{padding-left:20px;margin:8px 0}.sv-box button{margin-top:12px;border:0;border-radius:10px;padding:10px 18px;background:#0f2350;color:#fff;font-weight:700;cursor:pointer}" +
    "@media (max-width:700px){.sv-btn .t{display:none}.sv-btn{padding:7px 11px}}";
  var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
  var top = document.querySelector("header.top .wrap .av-badge") || document.querySelector("header.top .wrap .brand");
  if (!top) return;
  var b = document.createElement("button"); b.type = "button"; b.className = "sv-btn";
  b.innerHTML = '🔔 <span class="t">Suivre</span>'; b.setAttribute("aria-label", "Suivre le site : recevoir une notification à chaque nouveau document");
  b.hidden = true; top.insertAdjacentElement("afterend", b);
  function etat(on) { b.classList.toggle("on", on); b.innerHTML = on ? '🔔 <span class="t">Abonné ✓</span>' : '🔔 <span class="t">Suivre</span>';
    b.setAttribute("aria-label", on ? "Abonné aux nouveautés. Cliquer pour se désabonner" : "Suivre le site : recevoir une notification à chaque nouveau document"); }
  function boite(html) {
    var bk = document.createElement("div"); bk.className = "sv-back";
    bk.innerHTML = '<div class="sv-box" role="dialog" aria-modal="true">' + html + '<button type="button">OK</button></div>';
    document.body.appendChild(bk); var x = bk.querySelector("button"); x.focus();
    x.onclick = function () { bk.remove(); b.focus(); }; bk.onclick = function (e) { if (e.target === bk) bk.remove(); };
  }
  fetch("/api/push/cle").then(function (r) { return r.json(); }).then(function (d) {
    if (!d || !d.actif) return;
    b.hidden = false;
    if (!ok) { // iPhone dans Safari : il faut d'abord ajouter le site à l'écran d'accueil
      b.onclick = function () { boite('<h2>🔔 Suivre sur iPhone</h2><p>Pour recevoir les nouveautés sur iPhone :</p><ol><li>Appuie sur le bouton <b>Partager</b> (carré avec une flèche).</li><li>Choisis <b>« Sur l\'écran d\'accueil »</b>.</li><li>Ouvre le site depuis la nouvelle icône, puis appuie sur <b>🔔 Suivre</b>.</li></ol>'); };
      return;
    }
    var cle = d.cle;
    navigator.serviceWorker.register("/sw.js").then(function (reg) {
      return reg.pushManager.getSubscription().then(function (s) {
        etat(!!s && Notification.permission === "granted");
        if (s) fetch("/api/push/abonner", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(s) });
        b.onclick = function () {
          reg.pushManager.getSubscription().then(function (s2) {
            if (s2) {
              if (!confirmer()) return;
              fetch("/api/push/desabonner", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(s2) });
              return s2.unsubscribe().then(function () { etat(false); });
            }
            return Notification.requestPermission().then(function (p) {
              if (p !== "granted") { boite("<h2>Notifications bloquées</h2><p>Autorise les notifications pour ce site dans les réglages du navigateur (icône 🔒 à côté de l'adresse), puis réessaie.</p>"); return; }
              var raw = atob(cle.replace(/-/g, "+").replace(/_/g, "/")), key = new Uint8Array(raw.length);
              for (var i = 0; i < raw.length; i++) key[i] = raw.charCodeAt(i);
              return reg.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: key }).then(function (s3) {
                return fetch("/api/push/abonner", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(s3) }).then(function () {
                  etat(true); boite("<h2>Merci, tu es abonné ! 🎉</h2><p>Tu recevras une notification à chaque nouveau cours, série, devoir ou corrigé.</p>");
                });
              });
            });
          }).catch(function () { boite("<h2>Oups</h2><p>L'abonnement n'a pas marché sur ce navigateur. Essaie avec Chrome.</p>"); });
        };
      });
    }).catch(function () { b.hidden = true; });
  }).catch(function () {});
  function confirmer() { return window.confirm ? window.confirm("Ne plus recevoir les notifications des nouveautés ?") : true; }
})();
