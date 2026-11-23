/* Interface en arabe (bouton « ع / FR ») : traduit menus, boutons et titres. Les cours, exercices et examens restent en français (BIOF). */
(function () {
  var KEY = 'yh_lang';
  function get() { try { return localStorage.getItem(KEY) || 'fr'; } catch (e) { return 'fr'; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  var D = {
    "Accueil": "الرئيسية", "Niveaux": "المستويات", "Leçons": "الدروس", "À propos": "من أنا", "Contact": "اتصل بي", "☰ Menu": "☰",
    "Noter le site": "قيّم الموقع", "★ Noter le site": "★ قيّم الموقع", "Suivre": "تابع", "🔔 Suivre": "🔔 تابع", "Suivi ✓": "متابَع ✓", "🔔 Suivi ✓": "🔔 متابَع ✓",
    "Aller au contenu": "انتقل إلى المحتوى", "Fermer": "إغلاق", "Rechercher": "بحث", "Rechercher une leçon": "ابحث عن درس", "Populaire :": "الأكثر بحثاً :",
    "Choisir mon niveau": "اختر مستواي", "Choisis ton niveau": "اختر مستواك", "Que veux-tu faire ? Choisis :": "ماذا تريد أن تفعل ؟ اختر :",
    "Comprendre la physique-chimie,": "افهم الفيزياء والكيمياء،", "simplement.": "ببساطة.",
    "Physique-Chimie · Collège et lycée · Gratuit": "الفيزياء والكيمياء · الإعدادي والثانوي · مجاناً",
    "Professeur de Physique-Chimie · Cycle secondaire": "أستاذ الفيزياء والكيمياء · التعليم الثانوي",
    "1re année collège": "الأولى إعدادي", "2e année collège": "الثانية إعدادي", "3e année collège": "الثالثة إعدادي",
    "Tronc commun scientifique": "الجذع المشترك العلمي", "Tronc commun": "الجذع المشترك", "1re année Baccalauréat": "الأولى بكالوريا", "2e année Baccalauréat": "الثانية بكالوريا",
    "Cours": "الدروس", "Exercices": "التمارين", "Devoirs": "الفروض", "Examens": "الامتحانات", "Simulations": "المحاكاة", "Quiz": "اختبار سريع", "Vidéos": "الفيديوهات",
    "Tout": "الكل", "Séries": "السلاسل", "Corrigés": "التصحيحات", "Contrôles": "الفروض",
    "Cours · simulation · quiz": "درس · محاكاة · اختبار", "📖 Cours · 🧪 Simulation · ✍️ Exercices corrigés · ✅ Quiz": "📖 درس · 🧪 محاكاة · ✍️ تمارين مصححة · ✅ اختبار",
    "Lire le cours →": "اقرأ الدرس ←", "S'entraîner →": "تدرّب ←", "Ouvrir →": "افتح ←", "Voir la correction →": "شاهد التصحيح ←", "Voir les examens →": "شاهد الامتحانات ←", "Voir toutes les simulations →": "كل المحاكاة ←",
    "Bientôt": "قريباً", "Bientôt disponible": "قريباً", "Bientôt disponible.": "قريباً.", "Gratuit": "مجاني", "Gratuit · en ligne": "مجاني · عبر الإنترنت",
    "Série d'exercices + corrigé côte à côte": "سلسلة تمارين + التصحيح جنباً إلى جنب", "Énoncé + corrigé pas à pas": "النص + التصحيح خطوة بخطوة", "Énoncé + corrigé détaillé": "النص + تصحيح مفصل",
    "Sujet": "الموضوع", "Corrigé": "التصحيح", "📄 Sujet": "📄 الموضوع", "✅ Corrigé": "✅ التصحيح", "✅ Corrigé détaillé": "✅ تصحيح مفصل", "📄 Sujet (PDF)": "📄 الموضوع",
    "Normale": "عادية", "Rattrapage": "استدراكية", "Semestre 1": "الدورة الأولى", "Physique": "الفيزياء", "Chimie": "الكيمياء",
    "Toutes les leçons": "كل الدروس", "Toutes les leçons par niveau": "كل الدروس حسب المستوى", "Résultats de la recherche": "نتائج البحث",
    "Tout pour réussir, au même endroit": "كل ما تحتاجه للنجاح في مكان واحد", "Résumés interactifs": "ملخصات تفاعلية", "Chaque leçon en carte mentale cliquable.": "كل درس في خريطة ذهنية تفاعلية.",
    "Exercices corrigés": "تمارين مصححة", "✍️ Exercices corrigés": "✍️ تمارين مصححة", "Énoncé et correction côte à côte + erreurs fréquentes.": "النص والتصحيح جنباً إلى جنب + الأخطاء الشائعة.",
    "Teste-toi et obtiens ta note tout de suite.": "اختبر نفسك واحصل على نقطتك فوراً.", "Fais les expériences en ligne, sans danger.": "أنجز التجارب عبر الإنترنت دون خطر.",
    "Devoirs surveillés": "الفروض المحروسة", "Sujets + corrigés + barèmes, pour s'entraîner.": "مواضيع + تصحيحات + سلم التنقيط للتدرب.",
    "Le labo virtuel": "المختبر الافتراضي", "🧪 Labo virtuel": "🧪 المختبر الافتراضي", "Comment réviser avec le site ?": "كيف تراجع بالموقع ؟",
    "Cours de soutien": "دروس الدعم", "Cours de soutien en Physique-Chimie": "دروس الدعم في الفيزياء والكيمياء", "Réserver sur WhatsApp": "احجز عبر واتساب", "Appeler": "اتصل",
    "Suivi personnalisé": "تتبع شخصي", "Niveaux :": "المستويات :", "Programme :": "البرنامج :", "Modes :": "الصيغ :", "Page Facebook": "صفحة فيسبوك",
    "Partager sur WhatsApp": "شارك على واتساب", "Partager sur Facebook": "شارك على فيسبوك", "🔗 Copier le lien": "🔗 انسخ الرابط", "Lien copié ✓": "تم نسخ الرابط ✓",
    "Lecture seule — téléchargement désactivé": "قراءة فقط — التحميل غير متاح", "Le site": "الموقع", "WhatsApp / Tél. :": "واتساب / الهاتف :",
    "Contactez-moi sur WhatsApp": "تواصل معي عبر واتساب",
    "Contrôles surveillés – Semestre 1": "الفروض المحروسة – الدورة الأولى", "Examens locaux – Semestre 1": "الامتحانات المحلية – الدورة الأولى",
    "Tous les examens locaux 3AC": "كل الامتحانات المحلية 3AC", "Page dédiée · sujets + corrigés": "صفحة خاصة · مواضيع + تصحيحات", "Liste complète par année": "اللائحة الكاملة حسب السنة",
    "Sciences Mathématiques (SM A et B)": "العلوم الرياضية (أ و ب)", "Sciences Physiques (PC)": "العلوم الفيزيائية", "Sessions normale et rattrapage · sujet + corrigé": "الدورتان العادية والاستدراكية · موضوع + تصحيح",
    "Tous les examens SM et PC": "كل امتحانات العلوم الرياضية والفيزيائية", "Examens nationaux : tableau, mode examen et mes notes": "الامتحانات الوطنية : الجدول، وضع الامتحان ونقطي",
    "Chronomètre 4 h / 3 h · exercices par thème · calcul de la note du bac": "عداد 4 س / 3 س · تمارين حسب الدرس · حساب معدل الباك",
    "📐 Sciences Maths": "📐 العلوم الرياضية", "🔬 Sciences Physiques": "🔬 العلوم الفيزيائية", "📝 Sujets et corrigés": "📝 المواضيع والتصحيحات", "📊 Mes résultats": "📊 نتائجي", "📚 Exercices par thème": "📚 التمارين حسب الدرس",
    "Année": "السنة", "Session": "الدورة", "Ma note": "نقطتي", "S'entraîner (4 h)": "تدرّب (4 س)", "S'entraîner (3 h)": "تدرّب (3 س)", "⏱ Mode examen": "⏱ وضع الامتحان", "Terminer": "إنهاء", "Sûr ? Terminer": "متأكد ؟ إنهاء",
    "✅ Voir le corrigé": "✅ شاهد التصحيح", "Enregistrer": "حفظ", "✔ Enregistré": "✔ تم الحفظ", "Ma note :": "نقطتي :", "⏰ Temps écoulé !": "⏰ انتهى الوقت !", "✅ Examen terminé.": "✅ انتهى الامتحان.", "⏰ Terminé": "⏰ انتهى",
    "meilleure note": "أحسن نقطة", "moyenne /20": "المعدل /20", "examen faits": "امتحان منجز", "examens faits": "امتحانات منجزة",
    "Bac SM · PC": "باك علوم رياضية · فيزيائية", "Format officiel": "الشكل الرسمي",
    "Calcul de la note du bac (Maroc)": "حساب معدل البكالوريا", "Contrôle continu (2BAC)": "المراقبة المستمرة (2 باك)", "Examen régional (1BAC)": "الامتحان الجهوي (1 باك)", "Examen national": "الامتحان الوطني",
    "💬 Ce que disent les visiteurs": "💬 آراء الزوار", "Envoyer": "إرسال", "Merci !": "شكراً !", "Annuler": "إلغاء"
  };
  var P = [
    [/^(\d+) leçons?$/, "$1 دروس"], [/^(\d+) documents? →$/, "$1 وثيقة ←"], [/^(\d+) leçons? · (\d+) documents →$/, "$1 دروس · $2 وثيقة ←"],
    [/^(\d+) séries? corrigées?$/, "$1 سلسلة مصححة"], [/^(\d+) devoirs? corrigés?$/, "$1 فرض مصحح"], [/^(\d+) exercices?$/, "$1 تمارين"], [/^(\d+) exercices? · corrigé détaillé$/, "$1 تمارين · تصحيح مفصل"],
    [/^(\d+) examens? (?:nationa\w+|locaux|local) corrigés?$/, "$1 امتحانات مصححة"], [/^(\d+) examens? corrigés?$/, "$1 امتحانات مصححة"],
    [/^Examen national (\d{4}) – session normale$/, "الامتحان الوطني $1 – الدورة العادية"], [/^Examen national (\d{4}) – session de rattrapage$/, "الامتحان الوطني $1 – الدورة الاستدراكية"],
    [/^(\d{4}) · Normale$/, "$1 · عادية"], [/^(\d{4}) · Rattrapage$/, "$1 · استدراكية"], [/^Examen normalisé local (\d{4})$/, "الامتحان المحلي الموحد $1"],
    [/^▶ Reprendre \((.+)\)$/, "▶ استئناف ($1)"], [/^(📖|✍️|📝|🎓) (Cours|Exercices|Devoirs|Examens) – (\w+)$/, function (m, e, w, n) { return e + ' ' + D[w] + ' – ' + n; }],
    [/^Devoir surveillé n°(\d+)$/, "الفرض المحروس رقم $1"]
  ];
  var orig = new WeakMap(), lang = get();
  function tr(s) {
    var t = s.trim(); if (!t) return null;
    if (D[t]) return s.replace(t, D[t]);
    for (var i = 0; i < P.length; i++) if (P[i][0].test(t)) return s.replace(t, t.replace(P[i][0], P[i][1]));
    return null;
  }
  function skip(n) { for (var e = n.parentElement; e; e = e.parentElement) { if (e.matches && e.matches('script,style,textarea,.dv-pages,.lesson-body,article.lecon,[data-noar],.katex')) return true; } return false; }
  function walk(root) {
    var w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT), n, list = [];
    while ((n = w.nextNode())) list.push(n);
    list.forEach(function (x) {
      if (skip(x)) return;
      if (lang === 'ar') { var src = orig.has(x) ? orig.get(x) : x.nodeValue, r = tr(src); if (r != null) { if (!orig.has(x)) orig.set(x, x.nodeValue); if (x.nodeValue !== r) x.nodeValue = r; } }
      else if (orig.has(x)) { x.nodeValue = orig.get(x); orig.delete(x); }
    });
    (root.querySelectorAll ? root.querySelectorAll('input[placeholder]') : []).forEach(function (i) {
      if (!i.dataset.phfr) i.dataset.phfr = i.placeholder;
      var r = lang === 'ar' ? tr(i.dataset.phfr) : null; i.placeholder = r != null ? r : i.dataset.phfr;
    });
  }
  var busy = false;
  var mo = new MutationObserver(function (ms) { if (lang !== 'ar' || busy) return; busy = true; ms.forEach(function (m) { if (m.type === 'characterData') { var n = m.target; if (!orig.has(n) || tr(orig.get(n)) !== n.nodeValue) { orig.delete(n); walk(n.parentNode || document.body); } } else m.addedNodes.forEach(function (n) { if (n.nodeType === 1) walk(n); else if (n.nodeType === 3 && n.parentNode) walk(n.parentNode); }); }); busy = false; });
  function apply() {
    document.documentElement.classList.toggle('ui-ar', lang === 'ar');
    walk(document.body);
    if (btn) { btn.textContent = lang === 'ar' ? 'FR' : 'ع'; btn.title = lang === 'ar' ? 'Afficher en français' : 'عرض الواجهة بالعربية'; }
  }
  var st = document.createElement('style');
  st.textContent = '.lang-b{border:2px solid rgba(255,255,255,.55);background:transparent;color:#fff;border-radius:99px;min-width:40px;height:36px;padding:0 10px;font:800 16px/1 Inter,system-ui,sans-serif;cursor:pointer;margin-left:8px;flex-shrink:0}@media(max-width:760px){.lang-b{min-width:34px;height:34px;padding:0 6px;margin-left:0}header.top .wrap{gap:6px;padding:10px}header.top .wrap>a>img{width:38px;height:38px}header.top .brand{font-size:15px;line-height:1.15}header.top .brand small{display:none}header.top .burger{padding:8px 10px;flex-shrink:0}}@media(max-width:400px){header.top .av-badge{font-size:13px;padding:7px 9px}header.top .wrap{gap:4px;padding:8px}.lang-b{min-width:30px;padding:0 4px}}.lang-b:hover{background:rgba(255,255,255,.12)}html.ui-ar body{font-family:Inter,"Noto Sans Arabic","Segoe UI",Tahoma,sans-serif}';
  document.head.appendChild(st);
  var btn = document.createElement('button'); btn.type = 'button'; btn.className = 'lang-b'; btn.setAttribute('aria-label', 'Langue de l’interface / لغة الواجهة');
  btn.onclick = function () { lang = lang === 'ar' ? 'fr' : 'ar'; set(lang); apply(); try { fetch('https://script.google.com/macros/s/AKfycbxta1pz0xrqrIa9RiENIXd_CQwiQpkvcwtm_sWBH15-UfBTCN4clgsdmtc3HXZtXh4I/exec', { method: 'POST', mode: 'no-cors', body: JSON.stringify({ ev: 'langue', titre: lang, vid: localStorage.getItem('yh_vid') || '', src: 'site' }), headers: { 'Content-Type': 'text/plain;charset=utf-8' }, keepalive: true }).catch(function () {}); } catch (e) {} };
  function mount() {
    var anchor = document.querySelector('header.top .wrap .brand'), stop = document.querySelector('header.top .wrap .burger') || document.querySelector('header.top .wrap nav');
    if (anchor) { if (stop && stop.parentNode === anchor.parentNode) stop.parentNode.insertBefore(btn, stop); else anchor.insertAdjacentElement('afterend', btn); }
    else { btn.style.cssText = 'position:fixed;top:10px;right:10px;z-index:90;background:#0f2350'; document.body.appendChild(btn); }
    var bg = document.querySelector('header.top .burger'); if (bg && innerWidth <= 760) { bg.textContent = '☰'; bg.setAttribute('aria-label', 'Menu'); }
    apply(); mo.observe(document.body, { childList: true, subtree: true, characterData: true });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount); else mount();
})();
