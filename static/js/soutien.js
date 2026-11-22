/* Bandeau « Cours de soutien » en haut de toutes les pages — YH Physique-Chimie */
(function () {
  var WA = "212694194880";
  var msg = "Bonjour Pr. Hafidi, je souhaite des informations sur les cours de soutien (à distance ou à domicile).\nالسلام عليكم أستاذ، أرغب في معلومات حول دروس الدعم والتقوية.";
  var url = "https://wa.me/" + WA + "?text=" + encodeURIComponent(msg);
  var css = ".sb{background:linear-gradient(90deg,#0b7a43,#12a05a);color:#fff;font-family:Inter,system-ui,sans-serif}" +
    ".sb .in{max-width:1200px;margin:0 auto;padding:10px 16px;display:flex;align-items:center;gap:14px;flex-wrap:wrap;justify-content:center}" +
    ".sb .tx{display:flex;flex-direction:column;gap:2px;text-align:center;flex:1 1 380px}" +
    ".sb .fr{font-weight:800;font-size:15.5px;line-height:1.35}.sb .ar{font-weight:700;font-size:15.5px;line-height:1.5;font-family:'Noto Naskh Arabic','Segoe UI',Tahoma,sans-serif}" +
    ".sb a.go{display:inline-flex;align-items:center;gap:8px;background:#fff;color:#0b7a43;border-radius:999px;padding:10px 18px;font-weight:800;font-size:15px;text-decoration:none;box-shadow:0 3px 10px rgba(0,0,0,.18);white-space:nowrap}" +
    ".sb a.go:hover{background:#eafff3}.sb a.go svg{width:20px;height:20px;fill:#0b7a43}" +
    "@media (max-width:640px){.sb .fr,.sb .ar{font-size:14px}.sb .in{padding:8px 12px;gap:8px}.sb a.go{padding:9px 16px;font-size:14px}}";
  var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
  var b = document.createElement("aside"); b.className = "sb"; b.setAttribute("aria-label", "Cours de soutien");
  b.innerHTML = '<div class="in"><div class="tx">' +
    '<span class="fr">📚 Cours de soutien en physique-chimie, à distance ou à domicile, tous niveaux</span>' +
    '<span class="ar" dir="rtl" lang="ar">دروس الدعم والتقوية في الفيزياء والكيمياء عن بعد أو بالمنزل لجميع المستويات</span></div>' +
    '<a class="go" href="' + url + '" target="_blank" rel="noopener"><svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 3C8.8 3 3 8.7 3 15.8c0 2.5.7 4.9 2 7L3 29l6.4-2a13 13 0 0 0 6.6 1.8c7.2 0 13-5.7 13-12.9S23.2 3 16 3zm0 23.6c-2.1 0-4.2-.6-6-1.7l-.4-.3-3.8 1.2 1.2-3.7-.3-.4a10.6 10.6 0 0 1-1.7-5.8C5 9.9 10 5 16 5s11 4.9 11 10.8-4.9 10.8-11 10.8zm6-8.1c-.3-.2-2-1-2.3-1.1-.3-.1-.5-.2-.8.2l-1 1.3c-.2.2-.4.3-.7.1-.3-.2-1.4-.5-2.7-1.7-1-.9-1.7-2-1.9-2.3-.2-.3 0-.5.1-.7l.6-.7.4-.6c.1-.2 0-.4 0-.6l-1-2.5c-.3-.7-.6-.6-.8-.6h-.7c-.2 0-.6.1-.9.4-.3.3-1.2 1.2-1.2 2.9s1.2 3.4 1.4 3.6c.2.2 2.4 3.7 5.9 5.1 2.9 1.1 3.5.9 4.1.8.6-.1 2-.8 2.3-1.6.3-.8.3-1.5.2-1.6-.1-.2-.3-.3-.6-.4z"/></svg>Contactez-moi sur WhatsApp</a></div>';
  var h = document.querySelector("header.top");
  if (h) h.insertAdjacentElement("afterend", b); else document.body.insertAdjacentElement("afterbegin", b);
  b.querySelector("a.go").addEventListener("click", function () {
    try {
      var vid = localStorage.getItem("yh_vid") || "";
      navigator.sendBeacon("https://script.google.com/macros/s/AKfycbxta1pz0xrqrIa9RiENIXd_CQwiQpkvcwtm_sWBH15-UfBTCN4clgsdmtc3HXZtXh4I/exec",
        new Blob([JSON.stringify({ ev: "clic_contact", vid: vid, src: "site", dev: /Mobi|Android|iPhone/i.test(navigator.userAgent) ? "téléphone" : "ordinateur", br: "", niveau: "", titre: "Bandeau soutien", type: location.pathname, canal: "whatsapp", nouveau: 0 })], { type: "text/plain;charset=utf-8" }));
    } catch (e) {}
  });
})();
