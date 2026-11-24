#!/usr/bin/env python3
"""Génère une page par leçon + une page par niveau + sitemap, à partir de catalogue.json.
Usage : python3 build_pages.py <dossier_site>"""
import hashlib
import glob, json, sys, re, unicodedata, html, datetime, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "interactif"))
import interactive as IX
import cours as CO
from sims import SIMS, SIM_CSS, SIM_COMMON_JS

SITE = sys.argv[1] if len(sys.argv) > 1 else "static"
BASE = "https://yh-physiquechimie.pages.dev"
TODAY = datetime.date.today().isoformat()
WA = "212652236922"
FB = "https://www.facebook.com/profile.php?id=61596309328709"

LEVELS = {
    "1ac": dict(short="1AC", long="1re année collège", alt="1APIC", ar="الأولى إعدادي"),
    "2ac": dict(short="2AC", long="2e année collège", alt="2APIC", ar="الثانية إعدادي"),
    "3ac": dict(short="3AC", long="3e année collège", alt="3APIC", ar="الثالثة إعدادي"),
    "tc": dict(short="TCS", long="Tronc commun scientifique", alt="TCSF", ar="الجذع المشترك العلمي"),
    "1bac": dict(short="1BAC", long="1re année Baccalauréat", alt="1BAC", ar="الأولى بكالوريا"),
    "2bac": dict(short="2BAC", long="2e année Baccalauréat", alt="2BAC", ar="الثانية بكالوريا"),
}
ORDER = list(LEVELS)
MAT = {"phys": "Physique", "chim": "Chimie", "pc": "Physique-Chimie"}
TYPES = {"cours": "Cours", "exo": "Série d'exercices", "corrige": "Corrigé", "video": "Vidéo", "controle": "Devoir surveillé"}

# Nom arabe + court résumé de chaque leçon (texte utile pour Google et pour l'élève)
INFO = {
    "L'air qui nous entoure": ("الهواء من حولنا",
        "La composition de l'air (dioxygène et diazote), ses propriétés (compressibilité, expansibilité), la masse d'un litre d'air et la pression."),
    "Les molécules et les atomes": ("الجزيئات والذرات",
        "Le modèle moléculaire, les atomes et leurs symboles, les molécules et les formules chimiques, corps purs simples et composés."),
    "Les combustions": ("الاحتراقات",
        "La combustion du carbone, du butane et du méthane : réactifs, produits, combustion complète et incomplète, dangers et tests d'identification."),
    "Les matériaux dans la vie quotidienne": ("المواد في حياتنا اليومية",
        "Les familles de matériaux (métaux, plastiques, verre…), leurs propriétés et le tri pour le recyclage."),
    "Les atomes et les ions": ("الذرات والأيونات",
        "La structure de l'atome (noyau, électrons), l'électroneutralité, la formation des ions, ions monoatomiques et polyatomiques."),
    "Réaction de quelques matériaux avec l'air": ("تفاعل بعض المواد مع الهواء",
        "L'oxydation du fer, du cuivre, du zinc et de l'aluminium dans l'air, la rouille, les équations de réaction et la protection des métaux."),
    "La gravitation universelle": ("التجاذب الكوني",
        "La loi de la gravitation universelle de Newton, l'intensité de la pesanteur, le poids d'un corps et son calcul sur la Terre et la Lune."),
    "Exemples d'actions mécaniques": ("أمثلة لتأثيرات ميكانيكية",
        "Actions de contact et à distance, représentation d'une force par un vecteur, force pressante, tension d'un ressort, poussée d'Archimède."),
    "Les espèces chimiques": ("الأنواع الكيميائية",
        "Espèces chimiques naturelles et synthétiques, identification par les sens et par des tests chimiques, pictogrammes de sécurité."),
    "Extraction, séparation et identification": ("استخراج وفصل وتحديد الأنواع الكيميائية",
        "Les techniques d'extraction (hydrodistillation, extraction par solvant), la séparation par ampoule à décanter et l'identification par chromatographie (CCM)."),
    "Contrôles surveillés – Semestre 1": ("الفروض المحروسة – الدورة الأولى",
        "Les devoirs surveillés du semestre 1 avec leurs corrigés et barèmes, pour s'entraîner dans les conditions du contrôle."),
    "Révision — Devoir n°1": ("مراجعة الفرض المحروس رقم 1",
        "Une série de révision pour préparer le devoir surveillé n°1, avec des exercices types des premières leçons."),
}

def slug(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s

def lesson_slug(niv, unite):
    return f"{niv}-{slug(unite)}"

E = html.escape

GTM = """<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-P9DXGPJ4"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());</script>"""

ICONS = {
  "cours":'<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h11l5 5v11H4z"/><path d="M15 4v5h5M8 13h8M8 17h6"/></svg>',
  "exo":'<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>',
  "corrige":'<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 4h6v3H9z"/><path d="M6 6H5v15h14V6h-1"/><path d="m8.5 14 2 2 4-4"/></svg>',
  "controle":'<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/><circle cx="17" cy="17" r="3" fill="currentColor"/></svg>',
  "video":'<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="3"/><path d="m10 9 5 3-5 3z" fill="currentColor"/></svg>',
}
WA_SVG = '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.4-.7-2.8-1.1-4.6-4-4.8-4.2-.1-.2-1.1-1.5-1.1-2.9s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.3.5-.4.4c-.1.1-.3.3-.1.6.2.3.7 1.2 1.6 2 1.1 1 2 1.3 2.3 1.4.3.1.4.1.6-.1l.8-1c.2-.3.4-.2.6-.1l1.9.9c.3.1.5.2.5.3.1.2.1.7-.1 1.3Z"/></svg>'
FB_SVG = '<svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M14 8h3V4h-3c-2.8 0-4 1.8-4 4.3V10H7v4h3v8h4v-8h3l1-4h-4V8.6c0-.4.3-.6.6-.6Z"/></svg>'

CSS = """
:root{--navy:#0f2350;--navy2:#1a3a7c;--ink:#14213d;--ink2:#3d4a66;--muted:#565f74;--bg:#f6f4ef;--card:#fff;--line:#e4dfd3;
--blue:#1f4e9c;--blue-soft:#e8effb;--gold:#d4a017;--gold-soft:#fbf3dc;--red:#c0392b;--green:#2e7d4f;--wa:#25d366;--fb:#1460c9;--r:14px}
*{box-sizing:border-box}html,body{margin:0}
body{font-family:Inter,system-ui,sans-serif;color:var(--ink);background:var(--bg);line-height:1.55}
h1,h2,h3{font-family:Fraunces,Georgia,serif;margin:0;letter-spacing:-.01em}
a{color:inherit}.wrap{max-width:980px;margin:0 auto;padding:0 20px}
.top{background:var(--navy);color:#fff}
.top .wrap{display:flex;align-items:center;gap:12px;padding:12px 20px}
.top img{width:42px;height:42px;border-radius:50%;border:2px solid var(--gold);background:#fff}
.top .brand{font-family:Fraunces,serif;font-weight:800;font-size:18px;text-decoration:none}
.top .brand small{display:block;font-family:Inter,sans-serif;font-weight:500;font-size:12px;color:#c9d5ef}
.head{background:linear-gradient(135deg,var(--navy),var(--navy2));color:#fff;padding:26px 0 30px}
.crumbs{font-size:13px;color:#c9d5ef;margin-bottom:10px}.crumbs a{text-decoration:none}.crumbs a:hover{text-decoration:underline}
.head h1{font-size:clamp(25px,4.4vw,38px);font-weight:800;line-height:1.15}
.head .ar{font-family:"Noto Naskh Arabic",Tahoma,serif;direction:rtl;font-size:20px;color:var(--gold);margin-top:8px}
.tags{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}
.tag{font-size:12.5px;font-weight:600;padding:4px 10px;border-radius:99px;background:rgba(255,255,255,.14)}
.tag.g{background:var(--gold);color:#2b1f00}
main{padding:24px 0 40px}
.intro{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:16px 18px;margin-bottom:20px}
.intro p{margin:0}.intro p+p{margin-top:8px}
.intro .ar{direction:rtl;text-align:right;font-family:"Noto Naskh Arabic",Tahoma,serif;color:var(--ink2)}
h2.sec{font-size:21px;color:var(--navy2);margin:26px 0 12px;display:flex;align-items:center;gap:8px}
h2.sec::before{content:"";width:6px;height:20px;border-radius:3px;background:var(--gold)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}
.card{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:14px;display:flex;gap:12px;align-items:flex-start;text-decoration:none;transition:transform .12s,box-shadow .12s}
.card:hover{transform:translateY(-2px);box-shadow:0 8px 22px rgba(20,33,61,.08)}
.icon{width:42px;height:42px;border-radius:10px;display:grid;place-items:center;flex:none}
.icon.cours{background:var(--blue-soft);color:var(--blue)}.icon.exo{background:var(--gold-soft);color:#9a7200}
.icon.corrige{background:#e5f3ea;color:var(--green)}.icon.video{background:#fbe9e7;color:var(--red)}
.card h3{font-family:Inter,sans-serif;font-size:15px;font-weight:600;line-height:1.35}
.card .sub{font-size:12.5px;color:var(--muted);margin-top:3px}
.card .go{font-size:12.5px;font-weight:700;color:var(--blue);margin-top:6px}
.tip{font-size:13.5px;color:var(--muted);margin-top:10px}
.share{display:flex;gap:10px;flex-wrap:wrap;margin:22px 0 4px}
.btn{display:inline-flex;align-items:center;gap:8px;text-decoration:none;font-weight:600;font-size:14.5px;padding:10px 16px;border-radius:12px;border:1px solid var(--line);background:#fff;cursor:pointer}
.btn.wa{background:var(--wa);border-color:var(--wa);color:#05361a}.btn.fb{background:var(--fb);border-color:var(--fb);color:#fff}
.lcards{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:16px;margin:10px 0 20px}
.lc{display:flex;flex-direction:column;gap:6px;text-decoration:none;background:#fff;border:1px solid var(--line);border-radius:18px;padding:20px 16px 16px;min-height:170px;position:relative;overflow:hidden;transition:transform .15s,box-shadow .15s;color:inherit}
.lc::before{content:"";position:absolute;inset:0 0 auto 0;height:6px;background:var(--c)}
.lc:hover{transform:translateY(-3px);box-shadow:0 12px 28px rgba(20,33,61,.12)}
.exbs{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}.exb{flex:1;min-width:120px;text-align:center;padding:10px 12px;border-radius:10px;background:#eef2fb;color:#1f3a8a;font-weight:700;text-decoration:none}.exb.exc{background:var(--c);color:#fff}.exb:hover{filter:brightness(.95)}.exk{cursor:default}.dv{position:fixed;inset:0;z-index:80;background:#0e1424;display:flex;flex-direction:column}.dv[hidden]{display:none}.dv-bar{display:flex;align-items:center;gap:10px;padding:10px 14px;background:#0f2350;color:#fff}.dv-t{flex:1;font-size:15px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.dv-x{border:0;background:#fff;color:#0f2350;border-radius:10px;width:42px;height:38px;font-size:18px;font-weight:800;cursor:pointer}.dv-pages{flex:1;overflow:auto;padding:12px 8px;-webkit-overflow-scrolling:touch}.dv-p{position:relative;max-width:960px;margin:0 auto 12px;background:#fff;box-shadow:0 4px 18px rgba(0,0,0,.4);aspect-ratio:210/297}.dv-p img{display:block;width:100%;height:100%;object-fit:contain;user-select:none;-webkit-user-drag:none;pointer-events:none}.dv-wm{position:absolute;right:10px;bottom:8px;font:600 11px Inter,sans-serif;color:rgba(15,35,80,.35)}
.cats{grid-template-columns:repeat(auto-fit,minmax(200px,1fr))}.cat{min-height:150px}.cat.on,[data-sub].on{box-shadow:0 0 0 3px var(--c);}
.catp{scroll-margin-top:80px}
.lc-code{font-family:Fraunces,Georgia,serif;font-size:28px;font-weight:800;color:var(--c);line-height:1}
.lc-t{font-weight:700;font-size:17px;color:var(--ink);line-height:1.3}
.lc-m{font-size:14px;color:var(--muted)}
.lc-f{font-size:12.5px;color:#475066;line-height:1.5}
.lc-go{margin-top:auto;font-size:13px;font-weight:700;color:var(--blue)}
.list{list-style:none;padding:0;margin:0;display:grid;gap:8px}
.list a{display:flex;justify-content:space-between;gap:10px;background:#fff;border:1px solid var(--line);border-radius:12px;padding:11px 14px;text-decoration:none;font-weight:600}
.list a:hover{border-color:var(--blue)}.list a span{font-weight:500;color:var(--muted);font-size:13px;white-space:nowrap}
.soutien{background:var(--gold-soft);border:1px solid #efd99a;border-radius:var(--r);padding:16px 18px;margin-top:28px}
.soutien b{color:#7a5a00}
footer{background:#0a1838;color:#9fb0d4;padding:22px 0;font-size:14px}
footer .wrap{display:flex;gap:14px;flex-wrap:wrap;justify-content:space-between}footer a{color:#fff}
.icon.controle{background:#efe7fb;color:#7a3fa8}
.vgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.vid{margin:0;background:#fff;border:1px solid var(--line);border-radius:16px;overflow:hidden}
.vid video{width:100%;aspect-ratio:16/9;background:#0f2350;display:block;object-fit:contain}
.dsh{margin:26px 0 10px;font-size:19px;color:#0f2350;border-left:5px solid #d4a017;padding-left:10px}.dsh a{font-size:13.5px;font-weight:600;margin-left:6px}
.vid figcaption{padding:10px 12px;font-weight:700;font-size:14.5px}
.menu{margin-left:auto;display:flex;gap:4px;align-items:center}
.menu>a,.menu .dd>button{all:unset;cursor:pointer;font-size:14px;font-weight:600;color:#dfe6f5;padding:8px 10px;border-radius:8px}
.menu>a:hover,.menu .dd>button:hover,.menu>a.on{color:#fff;background:rgba(255,255,255,.1)}
.menu>a.on{box-shadow:inset 0 -2px 0 var(--gold)}
.dd{position:relative}.dd>button::after{content:"";display:inline-block;margin-left:6px;width:6px;height:6px;border-right:2px solid currentColor;border-bottom:2px solid currentColor;transform:rotate(45deg) translateY(-3px)}
.dd .dm{display:none;position:absolute;right:0;top:calc(100% + 6px);background:#fff;color:var(--ink);border-radius:12px;box-shadow:0 14px 34px rgba(0,0,0,.25);min-width:250px;padding:6px;z-index:50}
.dd.open .dm,.dd:hover .dm{display:block}
.dm a{display:flex;justify-content:space-between;gap:10px;text-decoration:none;padding:9px 12px;border-radius:8px;font-size:14px;font-weight:600}
.dm a:hover{background:var(--blue-soft);color:var(--blue)}
.dm a small{font-weight:500;color:var(--muted)} .dm a.soon{opacity:.75} .dm a.soon small{color:#7a5a00;background:var(--gold-soft);padding:1px 7px;border-radius:99px}
.burger{all:unset;display:none;margin-left:auto;cursor:pointer;color:#fff;font-weight:700;padding:8px 12px;border-radius:8px;background:rgba(255,255,255,.12)}
@media(max-width:760px){.burger{display:block;margin-left:auto}.menu{display:none;position:absolute;left:0;right:0;top:100%;flex-direction:column;align-items:stretch;background:#0f2350;padding:8px 14px 14px;z-index:60}
 .menu.open{display:flex}.top .wrap{position:relative}.dd .dm{position:static;box-shadow:none;margin-top:4px}.dd:hover .dm{display:none}.dd.open .dm{display:block}}
.wa-float{position:fixed;right:18px;bottom:18px;z-index:40;width:56px;height:56px;border-radius:50%;background:var(--wa);display:grid;place-items:center;box-shadow:0 8px 24px rgba(0,0,0,.25);color:#fff}

"""

def nav_html(active=""):
    lv = "".join(
        (f'<a href="/niveau/{k}/">{LEVELS[k]["short"]} <small>{LEVELS[k]["long"]}</small></a>' if k in USED_LEVELS
         else f'<a class="soon" href="/niveau/{k}/">{LEVELS[k]["short"]} <small>Bientôt · قريبا</small></a>') for k in ORDER)
    on = lambda k: ' class="on"' if active == k else ''
    return f"""<button class="burger" type="button" onclick="this.nextElementSibling.classList.toggle('open')">☰ Menu</button>
<nav class="menu" aria-label="Menu principal"><a href="/"{on('home')}>Accueil</a>
<div class="dd"><button type="button" onclick="this.parentElement.classList.toggle('open')">Niveaux</button><div class="dm">{lv}</div></div>
<a href="/lecons/"{on('lecons')}>Leçons</a><a href="/a-propos/"{on('apropos')}>À propos</a><a href="/contact/"{on('contact')}>Contact</a></nav>"""

_AR_EL = re.compile(r'<(span|div|p|small|td|th|li|h[1-6])\b[^>]*\blang="ar"[^>]*>.*?</\1>', re.S)
def strip_ar(h):
    """Site sans arabe : retire les éléments en arabe et les mentions « قريبا »."""
    h = _AR_EL.sub("", h)
    h = h.replace("Bientôt · قريبا", "Bientôt").replace(" · قريبا", "").replace("قريبا بإذن الله", "Bientôt")
    h = h.replace('"inLanguage": ["fr", "ar"]', '"inLanguage": "fr"')
    return h

def page(title, desc, canonical, body, jsonld, active="", extra_css="", extra_js=""):
    nav = nav_html(active)
    return strip_ar(_page(title, desc, canonical, body, jsonld, nav, extra_css, extra_js))

def _page(title, desc, canonical, body, jsonld, nav, extra_css, extra_js):
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
{GTM}
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{canonical}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
<meta name="theme-color" content="#0f2350">
<meta property="og:type" content="website">
<meta property="og:site_name" content="YH Physique-Chimie">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}/banniere-yh.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700;9..144,800&family=Inter:wght@400;500;600;700&family=Noto+Naskh+Arabic:wght@500;700&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
<style>{CSS}{IX.CSS}{extra_css}</style>
</head>
<body>
<header class="top"><div class="wrap">
  <a href="/"><img src="/logo.jpg" alt="Logo YH Physique-Chimie"></a>
  <a class="brand" href="/">YH Physique-Chimie<small>Pr. Youness HAFIDI</small></a>
  {nav}
</div></header>
{body}
<footer><div class="wrap">
  <span>© Pr. Youness HAFIDI — Physique-Chimie · Consultation en ligne uniquement</span>
  <span>WhatsApp / Tél. : <a href="https://wa.me/{WA}" target="_blank" rel="noopener">06 52 23 69 22</a> · <a href="{FB}" target="_blank" rel="noopener">Facebook</a> · <a href="https://www.linkedin.com/in/youness-hafidi" target="_blank" rel="noopener">LinkedIn</a></span>
</div></footer>
<a class="wa-float" href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="Discuter sur WhatsApp">{WA_SVG.replace('18','30',2)}</a>
{extra_js}
<script>
document.addEventListener('click',e=>{{const a=e.target.closest('a[data-ev]');if(!a)return;try{{gtag('event',a.dataset.ev,{{titre:a.dataset.t||'',lecon:document.title}})}}catch(x){{}}}});
</script>
<script defer src="/js/soutien.js"></script>
<script defer src="/js/avis.js"></script>
<script defer src="/js/suivre.js"></script>
</body>
</html>"""

def share_block(url, text):
    from urllib.parse import quote
    wa = f"https://wa.me/?text={quote(text + ' ' + url)}"
    fb = f"https://www.facebook.com/sharer/sharer.php?u={quote(url)}"
    return f"""<div class="share">
  <a class="btn wa" href="{wa}" target="_blank" rel="noopener" data-ev="partage_whatsapp">{WA_SVG} Partager sur WhatsApp</a>
  <a class="btn fb" href="{fb}" target="_blank" rel="noopener" data-ev="partage_facebook">{FB_SVG} Partager sur Facebook</a>
  <button class="btn" onclick="navigator.clipboard&&navigator.clipboard.writeText('{url}').then(()=>{{this.textContent='Lien copié ✓'}})">🔗 Copier le lien</button>
</div>"""

CTRL = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "interactif", "controles.json"), encoding="utf-8"))
def controles_html(niv, unite):
    from urllib.parse import quote
    D = CTRL.get(f"{niv}|{unite}")
    if not D: return ""
    out = ['<p class="tip" style="margin:0 0 10px">Lis l\'énoncé, cherche seul, puis touche <b>Voir la correction</b> : le corrigé détaillé de l\'exercice s\'affiche à côté'
           + (', avec sa <b>vidéo</b>' if any(x.get("video") for d in D for x in d["ex"]) else '') + '.</p>']
    if len(D) > 1:
        out.append('<nav class="pills">' + "".join(f'<a href="#ds{i}">{E(d["titre"].split("– ")[-1])}</a>' for i, d in enumerate(D)) + '</nav>')
    for i, d in enumerate(D):
        out.append(f'<h3 class="dsh" id="ds{i}">{E(d["titre"])} <a href="/?doc={quote(d["sujet"], safe="/")}">sujet PDF</a> · <a href="/?doc={quote(d["corrige"], safe="/")}">corrigé PDF</a></h3>')
        for x in d["ex"]:
            en = "".join(f'<img loading="lazy" src="/exos/{f}" alt="Énoncé – {E(x["lab"])}" draggable="false">' for f in x["en"])
            co = "".join(f'<img loading="lazy" src="/exos/{f}" alt="Correction détaillée – {E(x["lab"])}" draggable="false">' for f in x["co"])
            vid = (f'<figure class="vid" style="margin:10px 0 0"><video controls preload="none" controlslist="nodownload noplaybackrate" disablepictureinpicture oncontextmenu="return false" poster="/logo.jpg" src="/videos/{x["video"]}"></video><figcaption>🎬 Correction en vidéo – {E(x["lab"])}</figcaption></figure>') if x.get("video") else ''
            out.append(f"""<div class="ex"><div class="ex-h"><b>{E(x['lab'])}</b><div class="sp">{'<button type="button" class="rep">Voir la correction</button>' if co else ''}</div></div>
<div class="ex-b"><div><div class="lbl">Énoncé</div>{en}<div class="wmk" aria-hidden="true"><span>Pr. Youness HAFIDI</span></div></div>
<div class="cor"><div class="lbl">Correction détaillée</div>{co}{vid}{'<div class="veil">🔒 Essaie d’abord seul…<br>puis touche ici pour voir la correction</div>' if co else ''}<div class="wmk" aria-hidden="true"><span>Pr. Youness HAFIDI</span></div></div></div></div>""")
    return "\n".join(out)

LCOLS = {"1ac":"#0e7c86","2ac":"#1f4e9c","3ac":"#7a3fa8","tc":"#c0392b","1bac":"#8a5a10","2bac":"#2e7d4f"}
def lesson_cards(niv, lessons, full=None):
    out = []
    num = {}; n = 0
    for l in (full or lessons):
        if not (l["unite"].startswith("Contrôles") or l["unite"].startswith("Révision")):
            n += 1; num[l["unite"]] = n
    for l in lessons:
        u = l["unite"]; ctl = u not in num
        code = "📝" if ctl else f"{num[u]:02d}"
        feats = []
        if u in CO.COURS: feats.append("📖 Cours")
        if IX.sim_for(u): feats.append("🧪 Simulation")
        if IX.exercices_html(niv, u) or ctl: feats.append("✍️ Exercices corrigés")
        if IX.quiz_html(u): feats.append("✅ Quiz")
        out.append(f'''<a class="lc" style="--c:{LCOLS.get(niv,'#1f4e9c')}" href="/lecons/{lesson_slug(niv,u)}/"><span class="lc-code">{code}</span><span class="lc-t">{E(u)}</span>
<span class="lc-m">{E(MAT.get(l["mat"],"Physique-Chimie"))}</span><span class="lc-f">{" · ".join(feats)}</span><span class="lc-go">{len(l["items"])} documents →</span></a>''')
    return '<div class="lcards">' + "".join(out) + "</div>"

def level_hub(niv, lv):
    col = LCOLS.get(niv, "#1f4e9c")
    lessons = [l for l in lv if not (l["unite"].startswith("Contrôles") or l["unite"].startswith("Révision") or l["unite"].startswith("Examens"))]
    exos = [l for l in lv if IX.exercices_html(niv, l["unite"]) or any(i["type"] == "exo" for i in l["items"])]
    exos = [l for l in exos if not (l["unite"].startswith("Contrôles") or l["unite"].startswith("Examens"))]
    exams = {}
    for l in lv:
        if l["unite"].startswith("Examens"):
            for it in l["items"]:
                m = re.search(r"(\d{4}).*?[Ss]ujet\s+(\w)", it["titre"])
                fil = "PC" if ("Physiques" in l["unite"] or " PC" in l["unite"]) else "SM"
                if m: exams.setdefault((fil, m.group(1), m.group(2)), {})["corr" if it["type"] in ("corrige", "corr") else "sujet"] = it
    ds = []
    for l in lv:
        if l["unite"].startswith("Contrôles"):
            for i, d in enumerate(CTRL.get(f"{niv}|{l['unite']}", [])):
                ds.append((d["titre"], f"/lecons/{lesson_slug(niv, l['unite'])}/#ds{i}", f"{len(d['ex'])} exercices · corrigé détaillé" + (" · vidéos" if any(x.get("video") for x in d["ex"]) else "")))
    def card(code, t, m, f, go, href, extra=""):
        return f'''<a class="lc" style="--c:{col}" href="{href}"{extra}><span class="lc-code">{code}</span><span class="lc-t">{t}</span><span class="lc-m">{m}</span><span class="lc-f">{f}</span><span class="lc-go">{go}</span></a>'''
    num = {l["unite"]: k + 1 for k, l in enumerate(lessons)}
    p_cours = "".join(card(f"{num[l['unite']]:02d}", E(l["unite"]), E(MAT.get(l["mat"], "")), "Cours · simulation · quiz", "Lire le cours →", f"/lecons/{lesson_slug(niv, l['unite'])}/#cours") for l in lessons)
    p_exos = "".join(card(f"{num.get(l['unite'], 0):02d}" if l["unite"] in num else "📝", E(l["unite"]), E(MAT.get(l["mat"], "")), "Série d'exercices + corrigé côte à côte", "S'entraîner →", f"/lecons/{lesson_slug(niv, l['unite'])}/#exercices") for l in exos)
    groups = {}
    for t, h, f in ds:
        m = re.search(r"n°\s*(\d+)", t); n = m.group(1) if m else "1"
        sj = re.search(r"Sujet\s+(\w)", t)
        groups.setdefault(n, []).append((sj.group(1) if sj else "", t, h, f))
    p_ds = ""; subs = ""
    for n, vs in sorted(groups.items(), key=lambda x: int(x[0])):
        if len(vs) == 1:
            _, t, h, f = vs[0]
            p_ds += card(f"DS{n}", f"Devoir surveillé n°{n}", "Semestre 1", E(f), "Voir la correction →", h)
        else:
            letters = ", ".join(v[0] for v in vs)
            p_ds += card(f"DS{n}", f"Devoir surveillé n°{n}", f"{len(vs)} versions : {letters}", "Chaque version corrigée en détail, exercice par exercice", "Choisir la version →", f"#ds{n}", f' data-sub="dsg{n}"')
            vcards = "".join(card(f"Version {L}", E(t), f"DS{n}", E(f), "Voir la correction →", h) for L, t, h, f in vs)
            subs += f'''<section class="subp" id="dsg{n}" hidden><h3 class="sec" style="font-size:19px">📁 DS{n} – choisis ta version</h3><div class="lcards">{vcards}</div></section>'''
    p_ex = '<a class="lc" href="/examens-locaux-3ac/" style="--c:#7b3fb0"><span class="lc-code">📚</span><span class="lc-t">Tous les examens locaux 3AC</span><span class="lc-m">Page dédiée · sujets + corrigés</span><span class="lc-f">Liste complète par année</span><span class="lc-go">Ouvrir →</span></a>' if niv == "3ac" else ""
    ex_fil = {"SM": "", "PC": ""}
    for (fil, an, L), d in sorted(exams.items(), key=lambda x: (x[0][0], -int(x[0][1]), x[0][2])):
        def imgs(u):
            stem = os.path.basename(u)[:-4]
            fs = sorted(glob.glob(os.path.join(SITE, "docimg", stem + "-*.webp")), key=lambda f: int(re.search(r"-(\d+)\.webp$", f).group(1)))
            return ",".join("/docimg/" + os.path.basename(f) + "?v=" + hashlib.md5(open(f, "rb").read()).hexdigest()[:8] for f in fs)
        def btn(it, cls, lab, tt):
            im = imgs(it["url"])
            return f'<a class="exb{cls}" href="/?doc={E(it["url"])}"' + (f' data-imgs="{im}" data-t="{E(tt)}"' if im else "") + f'>{lab}</a>'
        bt = ""
        if "sujet" in d: bt += btn(d["sujet"], "", "📄 Sujet", f"Examen local {an} – sujet {L}")
        if "corr" in d: bt += btn(d["corr"], " exc", "✅ Corrigé détaillé", f"Corrigé détaillé – sujet {L}")
        if niv == "2bac":
            ses = "normale" if L == "N" else "de rattrapage"
            ex_fil[fil] += f'''<div class="lc exk" style="--c:{col}"><span class="lc-code">{an} · {"Normale" if L == "N" else "Rattrapage"}</span><span class="lc-t">Examen national {an} – session {ses}</span><span class="lc-m">{"2BAC Sciences Mathématiques · 4 heures" if fil == "SM" else "2BAC Sciences Physiques · 3 heures"}</span><span class="lc-f">Énoncé + corrigé détaillé</span><span class="exbs">{bt}</span></div>'''
            continue
        p_ex += f'''<div class="lc exk" style="--c:{col}"><span class="lc-code">Sujet {L}</span><span class="lc-t">Examen normalisé local {an}</span><span class="lc-m">{E((d.get("sujet") or d.get("corr")).get("lieu", "Session janvier"))} · 1 heure</span><span class="lc-f">Énoncé + corrigé pas à pas</span><span class="exbs">{bt}</span></div>'''
    if niv == "2bac":
        nb = {f: ex_fil[f].count('class="lc exk"') for f in ex_fil}
        def fcard(f, ic, t):
            n = nb[f]
            return card(ic, t, (f"{n} examen{'s' if n > 1 else ''} corrigé{'s' if n > 1 else ''}" if n else "Bientôt disponible"), "Sessions normale et rattrapage · sujet + corrigé", "Voir les examens →" if n else "Bientôt", f"#ex{f.lower()}", f' data-sub="ex{f.lower()}"')
        def fsec(f, ic, t):
            return f'''<section class="subp" id="ex{f.lower()}" hidden><h3 class="sec" style="font-size:19px">{ic} {t} – examens nationaux</h3>''' + (f'<div class="lcards">{ex_fil[f]}</div>' if ex_fil[f] else '<p class="tip">Bientôt disponible.</p>') + "</section>"
        p_ex = card("⏱", "Examens nationaux : tableau, mode examen et mes notes", "Tous les examens SM et PC", "Chronomètre 4 h / 3 h · exercices par thème · calcul de la note du bac", "Ouvrir →", "/examens-nationaux-2bac/") + fcard("SM", "📐", "Sciences Mathématiques (SM A et B)") + fcard("PC", "🔬", "Sciences Physiques (PC)") \
             + "</div>" + fsec("SM", "📐", "Sciences Mathématiques") + fsec("PC", "🔬", "Sciences Physiques") + '<div class="lcards" hidden>'
    p_ds += "</div>" + subs + '<div class="lcards" hidden>'
    cats = [("cours", "📖", "Cours", f"{len(lessons)} leçon{'s' if len(lessons) > 1 else ''}", p_cours),
            ("exercices", "✍️", "Exercices", f"{len(exos)} série{'s' if len(exos) > 1 else ''} corrigée{'s' if len(exos) > 1 else ''}", p_exos),
            ("devoirs", "📝", "Devoirs", f"{len(groups)} devoir{'s' if len(groups) > 1 else ''} corrigé{'s' if len(groups) > 1 else ''}" + (f" ({len(ds)} versions)" if len(ds) > len(groups) else ""), p_ds)]
    if exams:
        cats.append(("examens", "🎓", "Examens", (f"{len(exams)} examen{'s' if len(exams) > 1 else ''} national{'aux' if len(exams) > 1 else ''} corrigé{'s' if len(exams) > 1 else ''}" if niv == "2bac" else f"{len(exams)} examen{'s' if len(exams) > 1 else ''} {'locaux' if len(exams) > 1 else 'local'} corrigé{'s' if len(exams) > 1 else ''}"), p_ex))
    top = "".join(f'''<a class="lc cat" style="--c:{col}" href="#{k}" data-cat="{k}"><span class="lc-code">{ic}</span><span class="lc-t">{t}</span><span class="lc-m">{n}</span><span class="lc-go">{'Ouvrir →' if p else 'Bientôt'}</span></a>''' for k, ic, t, n, p in cats)
    panels = "".join(f'''<section class="catp" id="{k}" hidden><h2 class="sec">{ic} {t} – {LEVELS[niv]['short']}</h2>{'<div class="lcards">' + p + '</div>' if p else '<p class="tip">Bientôt disponible.</p>'}</section>''' for k, ic, t, n, p in cats)
    js = """<script>(function(){const cs=[...document.querySelectorAll('.cat')];function show(k){document.querySelectorAll('.catp').forEach(p=>p.hidden=p.id!==k);cs.forEach(c=>c.classList.toggle('on',c.dataset.cat===k));}
cs.forEach(c=>c.addEventListener('click',e=>{e.preventDefault();show(c.dataset.cat);history.replaceState(null,'','#'+c.dataset.cat);document.getElementById(c.dataset.cat).scrollIntoView({behavior:'smooth'});}));
(function(){const bs=[...document.querySelectorAll('[data-imgs]')];if(!bs.length)return;
const pre=new Set();function warm(b){b.dataset.imgs.split(',').forEach((u,i)=>{if(pre.has(u))return;pre.add(u);const im=new Image();im.decoding='async';if(i<2)im.fetchPriority='high';im.src=u;});}
document.querySelector('[data-cat=examens]')&&document.querySelector('[data-cat=examens]').addEventListener('click',()=>bs.forEach(warm));
const ov=document.createElement('div');ov.className='dv';ov.setAttribute('role','dialog');ov.setAttribute('aria-modal','true');ov.hidden=true;
ov.innerHTML='<div class="dv-bar"><b class="dv-t"></b><button type="button" class="dv-x" aria-label="Fermer">✕</button></div><div class="dv-pages"></div>';document.body.appendChild(ov);
const pg=ov.querySelector('.dv-pages');let last=null;
function close(){ov.hidden=true;pg.innerHTML='';document.body.style.overflow='';if(location.hash==='#doc')history.back();if(last)last.focus();}
ov.querySelector('.dv-x').onclick=close;addEventListener('keydown',e=>{if(e.key==='Escape'&&!ov.hidden)close();});
addEventListener('popstate',()=>{if(!ov.hidden&&location.hash!=='#doc'){ov.hidden=true;pg.innerHTML='';document.body.style.overflow='';}});
ov.addEventListener('contextmenu',e=>e.preventDefault());
bs.forEach(b=>{b.addEventListener('pointerenter',()=>warm(b));b.addEventListener('touchstart',()=>warm(b),{passive:true});
b.addEventListener('click',e=>{e.preventDefault();last=b;ov.querySelector('.dv-t').textContent=b.dataset.t||'';
pg.innerHTML=b.dataset.imgs.split(',').map((u,i)=>'<div class="dv-p"><img src="'+u+'" alt="Page '+(i+1)+'" '+(i<2?'fetchpriority="high"':'loading="lazy"')+' draggable="false"><span class="dv-wm">YH Physique-Chimie</span></div>').join('');
ov.hidden=false;document.body.style.overflow='hidden';pg.scrollTop=0;history.pushState(null,'','#doc');ov.querySelector('.dv-x').focus();
try{fetch('https://script.google.com/macros/s/AKfycbxta1pz0xrqrIa9RiENIXd_CQwiQpkvcwtm_sWBH15-UfBTCN4clgsdmtc3HXZtXh4I/exec',{method:'POST',mode:'no-cors',body:JSON.stringify({ev:'ouverture_document',vid:localStorage.getItem('yh_vid')||'',src:'site',dev:/Mobi|Android|iPhone/i.test(navigator.userAgent)?'téléphone':'ordinateur',br:'',niveau:document.title.split(' – ')[0].replace('Physique-Chimie ',''),titre:b.dataset.t,type:b.classList.contains('exc')?'Corrigé':'Examen',canal:'',nouveau:0}),headers:{'Content-Type':'text/plain;charset=utf-8'},keepalive:true}).catch(()=>{});}catch(_){}
});});})();
document.querySelectorAll('[data-sub]').forEach(c=>c.addEventListener('click',e=>{e.preventDefault();const id=c.dataset.sub;document.querySelectorAll('.subp').forEach(p=>p.hidden=p.id!==id);document.querySelectorAll('[data-sub]').forEach(x=>x.classList.toggle('on',x===c));document.getElementById(id).scrollIntoView({behavior:'smooth'});}));
const h=location.hash.slice(1);if(['cours','exercices','devoirs'].includes(h))show(h);if(h==='examens'||h==='exsm'||h==='expc'){show('examens');if(h!=='examens'){const c=document.querySelector('[data-sub="'+h+'"]');if(c)c.click();}}if(/^ds\\d+$/.test(h)){show('devoirs');const c=document.querySelector('[data-sub="dsg'+h.slice(2)+'"]');if(c)c.click();}})();</script>"""
    return f'<div class="lcards cats">{top}</div>{panels}', js

def build():
    global USED_LEVELS
    items = json.load(open(os.path.join(SITE, "catalogue.json"), encoding="utf-8"))
    try:  # ressources ajoutées depuis la page d'administration (extras.json)
        _seen = {i["url"] for i in items}
        for _x in json.load(open(os.path.join(SITE, "extras.json"), encoding="utf-8")):
            if _x.get("url") and _x["url"] not in _seen:
                _x.setdefault("matiere", "pc"); _x.setdefault("id", "x" + str(abs(hash(_x["url"])) % 10**6)); _x.setdefault("ordre", 500)
                items.append(_x); _seen.add(_x["url"])
    except FileNotFoundError:
        pass
    lessons = {}
    for it in items:
        key = (it["niveau"], it["unite"])
        L = lessons.setdefault(key, dict(niveau=it["niveau"], unite=it["unite"], mat=it.get("matiere", "pc"),
                                         ord=it.get("ordreUnite", 99), items=[]))
        L["items"].append(it)
        L["ord"] = min(L["ord"], it.get("ordreUnite", 99))
    USED_LEVELS = [k for k in ORDER if any(l["niveau"] == k for l in lessons.values())]
    rank = {"cours": 0, "video": 1, "controle": 2, "exo": 2, "corrige": 3}
    urls = [(f"{BASE}/", "1.0")]
    index_map = {}

    by_level = {}
    for L in lessons.values():
        by_level.setdefault(L["niveau"], []).append(L)
    for L in lessons.values():
        L["ord"] = IX.order_of(L["niveau"], L["unite"])
    for k in by_level:
        by_level[k].sort(key=lambda l: (l["ord"], l["unite"]))

    for L in lessons.values():
        niv, lv = L["niveau"], LEVELS[L["niveau"]]
        s = lesson_slug(niv, L["unite"])
        url = f"{BASE}/lecons/{s}/"
        index_map[f'{niv}|{L["unite"]}'] = f"/lecons/{s}/"
        ar, resume = INFO.get(L["unite"], ("", ""))
        types = sorted({it["type"] for it in L["items"]}, key=lambda t: rank.get(t, 9))
        kinds = " et ".join({"exo": "exercices", "corrige": "corrigés", "cours": "cours", "video": "vidéos", "controle": "devoirs surveillés"}[t] for t in types)
        if L["unite"] in CO.COURS:
            kinds = "cours, simulation, " + kinds
        _u = L["unite"]
        if _u.startswith("Contrôles"):
            title = f"Devoirs surveillés {lv['short']} semestre 1 corrigés en détail"
            desc = f"Devoirs surveillés de physique-chimie {lv['short']} ({lv['long']}) avec corrigé détaillé exercice par exercice" + (" et vidéos" if VIDEOS_LECON.get((niv, _u)) else "") + ". Gratuit, par Pr. Youness HAFIDI."
        elif _u.startswith("Révision"):
            title = f"{_u} – {lv['short']} : corrigé détaillé"
            desc = f"{_u} en physique-chimie {lv['short']} ({lv['long']}) : exercices de préparation avec corrigé détaillé. Gratuit, par Pr. Youness HAFIDI."
        elif _u in CO.COURS:
            title = f"{_u} – {lv['short']} : cours et exercices corrigés"
            desc = f"{_u} ({MAT.get(L['mat'],'Physique-Chimie')}, {lv['long']}) : cours résumé, simulation interactive, exercices corrigés et quiz. Gratuit, par Pr. Youness HAFIDI."
        else:
            title = f"{_u} – {lv['short']} : exercices corrigés"
            desc = f"{_u} ({lv['long']}) : séries d'exercices et corrigés en ligne. Gratuit, par Pr. Youness HAFIDI."
        if len(title) > 65:
            title = title.replace(" : cours et exercices corrigés", " : cours et exercices")
        if len(title) > 65:
            title = title.replace(" : cours et exercices", " : cours")
        if len(desc) > 160:
            desc = desc.replace(" Gratuit, par Pr. Youness HAFIDI.", " Gratuit.")
        if len(title) + 21 <= 70:
            title += " | YH Physique-Chimie"
        cards = ""
        for it in sorted(L["items"], key=lambda i: (i.get("ordre", 0), rank.get(i["type"], 9)) if L["unite"].startswith("Contrôles") else (rank.get(i["type"], 9), i.get("ordre", 0))):
            from urllib.parse import quote
            href = "/?doc=" + quote(it["url"], safe="/")
            cards += f"""<a class="card" href="{href}" data-ev="ouverture_depuis_page_lecon" data-t="{E(it['titre'])}">
  <div class="icon {it['type']}">{ICONS.get(it['type'], ICONS['cours'])}</div>
  <div><h3>{E(it['titre'])}</h3><div class="sub">{E(it.get('sousType') or TYPES.get(it['type'],''))}</div><div class="go">Ouvrir en ligne →</div></div>
</a>"""
        others = [o for o in by_level[niv] if o is not L]
        olist = "".join(
            f'<li><a href="/lecons/{lesson_slug(niv,o["unite"])}/">{E(o["unite"])}<span>{E(MAT.get(o["mat"],""))}</span></a></li>'
            for o in others)
        share_text = f"📚 {L['unite']} ({lv['short']}) – séries et corrigés en ligne :"
        vl = [] if CTRL.get(f"{niv}|{L['unite']}") else VIDEOS_LECON.get((niv, L["unite"]), [])
        ctl = controles_html(niv, L["unite"])
        vids = ('<h2 class="sec" id="videos">Correction en vidéo, exercice par exercice</h2><div class="vgrid">' + "".join(
            f'<figure class="vid"><video controls preload="none" controlslist="nodownload noplaybackrate" disablepictureinpicture oncontextmenu="return false" poster="/logo.jpg" src="/videos/{f}"></video><figcaption>🎬 {E(t)}</figcaption></figure>'
            for t, f in vl) + '</div>') if vl else ''
        rz = IX.resume_html(L["unite"], lv["short"]); exh = IX.exercices_html(niv, L["unite"]); qz = IX.quiz_html(L["unite"])
        smo = IX.sim_for(L["unite"])
        sim_html = (f'''<div class="labin" id="lab"><p class="lab-k">🧪 Simulation : à toi de manipuler !</p><p class="tip" style="margin:0 0 8px">{E(smo['intro'])}</p>
<div class="lab"><div class="labhead"><img src="/logo.jpg" alt=""><div><b>Labo YH Physique-Chimie</b><span>{E(smo['title'])}</span></div><div class="sig">Pr. Youness HAFIDI</div></div>
{('<div class="labbody">' + smo['body'] + '</div>') if not smo['body'].lstrip().startswith('<div class="tabs') else smo['body']}</div></div>''') if smo else ""
        toc, cbody = CO.render(L["unite"], sim_html)
        if not cbody and sim_html:
            cbody = sim_html
        pl = [("#cours", "📖 Cours", cbody), ("#resume", "🧠 Résumé", rz), ("#exercices", "✍️ Exercices corrigés", exh or L["unite"].startswith("Contrôles")), ("#quiz", "✅ Quiz", qz), ("#docs-h", "📄 PDF", True), ("#videos", "🎬 Vidéos", VIDEOS_LECON.get((niv, L["unite"])) and not CTRL.get(f"{niv}|{L['unite']}"))]
        pills = '<nav class="pills sticky-pills">' + "".join(f'<a href="{h}">{t}</a>' for h, t, ok in pl if ok) + '</nav>'
        cours_block = (f'''<h2 class="sec" id="cours">📖 Le cours</h2><div class="coursewrap">{f'<nav class="ctoc" aria-label="Sommaire du cours"><b>Sommaire</b>{toc}</nav>' if toc else '<div></div>'}<div class="cbody cahier">{cbody}</div></div>''') if cbody else ""
        lab_js = ("<script>(function(){" + SIM_COMMON_JS + smo["js"] + "})();</script>") if smo else ""
        if L["unite"].startswith("Contrôles"):
            resume = "Les devoirs surveillés du semestre 1 avec leurs corrigés détaillés, exercice par exercice, pour s'entraîner dans les conditions du contrôle."
        body = f"""<section class="head"><div class="wrap">
  <div class="crumbs"><a href="/">Accueil</a> › <a href="/niveau/{niv}/">{lv['short']} – {lv['long']}</a> › {E(L['unite'])}</div>
  <h1>{E(L['unite'])}</h1>
  {f'<div class="ar" lang="ar">{E(ar)} – {lv["ar"]}</div>' if ar else ''}
  <div class="tags"><span class="tag g">{lv['short']} · {lv['alt']}</span><span class="tag">{E(MAT.get(L['mat'],''))}</span><span class="tag">{kinds.capitalize()}</span><span class="tag">Gratuit · en ligne</span></div>
</div></section>
<main class="wrap">
  <div class="intro">
    <p><b>{E(L['unite'])}</b> ({MAT.get(L['mat'],'Physique-Chimie')}, {lv['long']}) — {E(resume)}</p>
    <p>{'Lis le cours, manipule la simulation, puis entraîne-toi avec les exercices corrigés et le quiz.' if cbody else 'Retrouve ici les documents de Pr. Youness HAFIDI : à faire seul, puis à vérifier avec le corrigé.'}</p>
    {f'<p class="ar" lang="ar" dir="rtl">{E(ar)} – {lv["ar"]} : {'فروض محروسة مع تصحيحها المفصل تمرينا تمرينا' if L['unite'].startswith('Contrôles') else 'سلاسل تمارين مع تصحيحها'}، مجانا وعبر الإنترنت.</p>' if ar else ''}
  </div>
  {pills}
  {cours_block}
  {f'<h2 class="sec" id="resume">🧠 Résumé de la leçon (carte mentale)</h2>{rz}' if rz else ''}
  {f'<h2 class="sec" id="exercices">Correction exercice par exercice{" (avec vidéos)" if "<video" in ctl else ""}</h2>{ctl}' if ctl else ''}
  {f'<h2 class="sec" id="exercices">✍️ Exercices : énoncé et correction côte à côte</h2>{exh}' if exh else ''}
  {f'<h2 class="sec" id="quiz">✅ Quiz : teste-toi !</h2>{qz}' if qz else ''}
  {vids}
  <h2 class="sec" id="docs-h">{'Les devoirs et leurs corrigés (PDF)' if L['unite'].startswith('Contrôles') else '📄 Série et corrigé (PDF)'}</h2>
  <div class="grid" id="docs">{cards}</div>
  {share_block(url, share_text)}
  {f'<h2 class="sec">Autres leçons – {lv["short"]}</h2>{lesson_cards(niv, others, by_level[niv])}' if others else ''}
  <div class="soutien">⭐ <b>Cours de soutien</b> en physique-chimie (en ligne ou à domicile) avec Pr. Hafidi — <a href="https://wa.me/{WA}?text={E('Bonjour Pr. Hafidi, je souhaite des informations sur les cours de soutien.')}" target="_blank" rel="noopener" data-ev="clic_soutien_page_lecon">réserver sur WhatsApp</a> · 06 52 23 69 22</div>
</main>
<script>
/* Ajoute automatiquement les nouveaux documents de cette leçon ajoutés dans le Google Sheet */
(async()=>{{try{{
 const U="https://docs.google.com/spreadsheets/d/e/2PACX-1vR719MSv0H2Gjchf9Id3GXEXwcX_G-0EhbAbhYcrYbO2kmYrNVYjAcchKE928Y0c2YcjDNRYTT-Rltf/pub?gid=1662435983&single=true&output=csv";
 const t=await (await fetch(U+"&t="+Date.now())).text();
 const rows=[];let row=[],f="",q=false;for(let i=0;i<t.length;i++){{const c=t[i];if(q){{if(c=='"'){{if(t[i+1]=='"'){{f+='"';i++}}else q=false}}else f+=c}}else if(c=='"')q=true;else if(c==','){{row.push(f);f=""}}else if(c=='\\n'||c=='\\r'){{if(c=='\\r'&&t[i+1]=='\\n')i++;row.push(f);rows.push(row);row=[];f=""}}else f+=c}}if(f||row.length){{row.push(f);rows.push(row)}}
 const n=x=>(x||"").trim().toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g,"");
 const h=rows[0].map(n),ci=k=>h.indexOf(k),NIV={{"2ac":"2ac","2apic":"2ac","3ac":"3ac","3apic":"3ac","1ac":"1ac","1apic":"1ac","tcs":"tc","tc":"tc","tcsf":"tc","1bac":"1bac","2bac":"2bac"}};
 const have=new Set([...document.querySelectorAll('#docs a')].map(a=>decodeURIComponent(a.getAttribute('href').slice(6))));
 const box=document.getElementById('docs');
 rows.slice(1).forEach(r=>{{const g=k=>(r[ci(k)]||"").trim();
  if(NIV[n(g("niveau")).replace(/\\s/g,"")]!=={json.dumps(niv)}||n(g("lecon"))!==n({json.dumps(L['unite'])}))return;
  const u=g("lien");if(!u||have.has(u))return;
  const a=document.createElement('a');a.className='card';a.href='/?doc='+encodeURIComponent(u);
  a.innerHTML='<div class="icon exo">{ICONS["exo"]}</div><div><h3></h3><div class="sub"></div><div class="go">Nouveau · Ouvrir en ligne →</div></div>';
  a.querySelector('h3').textContent=g("titre");a.querySelector('.sub').textContent=g("format");box.appendChild(a);}});
}}catch(e){{}}}})();
</script>"""
        jsonld = {"@context": "https://schema.org", "@graph": [
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Accueil", "item": f"{BASE}/"},
                {"@type": "ListItem", "position": 2, "name": f"{lv['short']} – {lv['long']}", "item": f"{BASE}/niveau/{niv}/"},
                {"@type": "ListItem", "position": 3, "name": L["unite"], "item": url}]},
            {"@type": "LearningResource", "name": f"{L['unite']} – {lv['short']}", "description": desc, "url": url,
             "inLanguage": "fr", "learningResourceType": (["Cours", "Simulation", "Exercices", "Corrigés", "Quiz"] if L["unite"] in CO.COURS else ["Exercices", "Corrigés"]), "isAccessibleForFree": True,
             "educationalLevel": lv["long"], "about": MAT.get(L["mat"], "Physique-Chimie"),
             "author": {"@type": "Person", "name": "Youness HAFIDI", "url": f"{BASE}/"}}]}
        d = os.path.join(SITE, "lecons", s)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(title, desc, url, body, jsonld, niv, extra_css=(SIM_CSS + CO.CSS) if cbody else "", extra_js=IX.JS + (CO.JS if cbody else "") + lab_js))
        urls.append((url, "0.8"))

    for niv in USED_LEVELS:
        lv = by_level[niv]; info = LEVELS[niv]
        url = f"{BASE}/niveau/{niv}/"
        title = f"Physique-Chimie {info['short']} : cours, exercices et devoirs corrigés" if niv not in ("3ac", "2bac") else ("Physique-Chimie 3AC : cours, exercices, devoirs et examens locaux corrigés" if niv == "3ac" else "Examens nationaux Physique-Chimie 2BAC SM corrigés | Bac Sciences Maths")
        desc = (f"Physique-chimie {info['short']} ({info['long']}) : cours, simulations, exercices et devoirs corrigés, gratuits. Leçons : "
                + ", ".join(l["unite"] for l in lv if not l["unite"].startswith(("Contrôles", "Révision"))) + ".")[:300]
        hub_html, hub_js = level_hub(niv, lv)
        li = ""
        for l in lv:
            ar = INFO.get(l["unite"], ("", ""))[0]
            li += f'<li><a href="/lecons/{lesson_slug(niv,l["unite"])}/">{E(l["unite"])}<span>{E(MAT.get(l["mat"],""))} · {len(l["items"])} doc.{" · " + E(ar) if ar else ""}</span></a></li>'
        body = f"""<section class="head"><div class="wrap">
  <div class="crumbs"><a href="/">Accueil</a> › {info['short']}</div>
  <h1>Physique-Chimie – {info['long']}</h1>
  <div class="ar" lang="ar">الفيزياء والكيمياء – {info['ar']}</div>
  <div class="tags"><span class="tag g">{info['short']} · {info['alt']}</span><span class="tag">{len(lv)} leçons</span><span class="tag">Gratuit · en ligne</span></div>
</div></section>
<main class="wrap">
  <div class="intro"><p>Que veux-tu faire ? Choisis : <b>Cours</b>, <b>Exercices</b>, <b>Devoirs</b>{" ou <b>Examens</b>" if any(l["unite"].startswith("Examens") for l in lv) else ""}.</p>
  <p class="ar" lang="ar" dir="rtl">اختر الدرس لتصفح سلاسل التمارين وتصحيحها.</p></div>
  {hub_html}
  {share_block(url, f"📚 Physique-Chimie {info['short']} – séries et corrigés en ligne :")}
  <div class="soutien">⭐ <b>Cours de soutien</b> {info['short']} (en ligne ou à domicile) — <a href="https://wa.me/{WA}" target="_blank" rel="noopener" data-ev="clic_soutien_page_niveau">WhatsApp 06 52 23 69 22</a></div>
</main>"""
        jsonld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "url": url, "description": desc,
                  "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
                      {"@type": "ListItem", "position": 1, "name": "Accueil", "item": f"{BASE}/"},
                      {"@type": "ListItem", "position": 2, "name": info["short"], "item": url}]}}
        d = os.path.join(SITE, "niveau", niv)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(title, desc, url, body, jsonld, niv, extra_js=hub_js))
        urls.insert(1, (url, "0.9"))

    for niv in ORDER:
        if niv in USED_LEVELS: continue
        info = LEVELS[niv]; url = f"{BASE}/niveau/{niv}/"
        body = f"""<section class="head"><div class="wrap"><div class="crumbs"><a href="/">Accueil</a> › {info['short']}</div>
<h1>Physique-Chimie – {info['long']}</h1><div class="ar" lang="ar">الفيزياء والكيمياء – {info['ar']}</div></div></section>
<main class="wrap"><div class="intro" style="text-align:center;padding:30px"><div style="font-size:40px">⏳</div><h2 style="color:var(--navy)">Bientôt disponible</h2>
<p class="ar" lang="ar" style="font-size:22px;color:#7a5a00">قريبا بإذن الله</p><p>Les séries, corrigés et résumés de ce niveau arrivent très prochainement.</p></div>
<div class="soutien">⭐ <b>Cours de soutien</b> {info['short']} dès maintenant — <a href="https://wa.me/{WA}" target="_blank" rel="noopener">WhatsApp 06 52 23 69 22</a></div></main>"""
        d = os.path.join(SITE, "niveau", niv); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(f"Physique-Chimie {info['short']} – bientôt | YH Physique-Chimie", f"Physique-chimie {info['long']} : bientôt disponible.", url, body,
            {"@context": "https://schema.org", "@type": "WebPage", "url": url}, niv).replace('<meta name="viewport"', '<meta name="robots" content="noindex">\n<meta name="viewport"', 1))

    # Page dédiée « Examens locaux 3AC » (référencement : mots-clés recherchés par les élèves)
    ex3 = [it for l in by_level.get("3ac", []) if l["unite"].startswith("Examens") for it in l["items"]]
    if ex3:
        url = f"{BASE}/examens-locaux-3ac/"
        grp = {}
        for it in ex3:
            m = re.search(r"(\d{4}).*?[Ss]ujet\s+(\w)", it["titre"])
            if m: grp.setdefault((m.group(1), m.group(2)), {})["corr" if it["type"] in ("corrige", "corr") else "sujet"] = it
        annees = sorted({a for a, _ in grp}, reverse=True)
        cards = ""
        for (an, L), d in sorted(grp.items(), key=lambda x: (-int(x[0][0]), x[0][1])):
            it0 = d.get("sujet") or d.get("corr"); lieu = it0.get("lieu", "")
            ville = lieu.split(" · ")[0] if lieu else ""
            bt = ""
            if "sujet" in d: bt += f'<a class="exb" href="/?doc={E(d["sujet"]["url"])}">📄 Sujet (PDF)</a>'
            if "corr" in d: bt += f'<a class="exb exc" href="/?doc={E(d["corr"]["url"])}">✅ Corrigé détaillé</a>'
            cards += f'''<article class="lc exk" style="--c:#7b3fb0"><span class="lc-code">{an}</span><h3 class="lc-t" style="margin:0">Examen local Physique-Chimie 3AC {an}{(" – " + E(ville)) if ville else ""} (sujet {L})</h3><span class="lc-m">Examen normalisé local 3APIC · {E(lieu)} · 1 heure</span><span class="lc-f">Sujet + correction détaillée pas à pas</span><span class="exbs">{bt}</span></article>'''
        title = f"Examens locaux 3AC Physique-Chimie corrigés {annees[-1]}–{annees[0]} | 3APIC"
        desc = (f"{len(grp)} examens normalisés locaux de physique-chimie 3ème année collège (3AC / 3APIC) avec corrections détaillées : "
                f"sujets {', '.join(annees)}, semestre 1. Gratuit, en ligne, format officiel.")
        body = f"""<section class="head"><div class="wrap">
  <div class="crumbs"><a href="/">Accueil</a> › <a href="/niveau/3ac/">3AC</a> › Examens locaux</div>
  <h1>Examens locaux Physique-Chimie 3AC avec corrigés</h1>
  <p class="ar" lang="ar-MA" dir="rtl" style="font-size:19px;margin:6px 0">الامتحان المحلي الموحد الفيزياء والكيمياء الثالثة إعدادي مع التصحيح</p>
  <div class="tags"><span class="tag g">3AC · 3APIC</span><span class="tag">{len(grp)} examens corrigés</span><span class="tag">{annees[-1]} – {annees[0]}</span><span class="tag">Gratuit</span></div>
</div></section>
<main class="wrap">
  <div class="intro"><p>Révise l'<b>examen normalisé local de physique-chimie de 3ème année collège</b> (3AC, 3APIC) avec de vrais sujets des années {', '.join(annees)}.
  Chaque <b>examen local 3AC</b> est présenté au <b>format officiel</b> (sujet + barème), avec une <b>correction détaillée</b> : méthode, réponses encadrées et erreurs fréquentes.
  Programme du semestre 1 : les matériaux, l'atome et les ions, l'action de l'air et des solutions acides et basiques sur les métaux, le pH, les tests d'identification des ions, la combustion des matières organiques.</p></div>
  <h2 class="sec">📝 Sujets et corrigés des examens locaux 3AC</h2>
  <div class="lcards">{cards}</div>
  <h2 class="sec">Conseils pour réussir l'examen local de physique-chimie 3AC</h2>
  <div class="intro"><ul>
  <li>Fais d'abord le sujet seul, en <b>1 heure</b>, puis compare avec la correction détaillée.</li>
  <li>Revois les points qui tombent souvent : formule de la rouille Fe<sub>2</sub>O<sub>3</sub>, alumine Al<sub>2</sub>O<sub>3</sub>, charge d'un ion, pH et dilution, tests des ions (Fe<sup>2+</sup>, Fe<sup>3+</sup>, Cu<sup>2+</sup>, Cl<sup>−</sup>), équations équilibrées.</li>
  <li>Retrouve aussi les <a href="/niveau/3ac/">cours, exercices et devoirs corrigés de 3AC</a>.</li></ul></div>
  {share_block(url, "📝 Examens locaux Physique-Chimie 3AC avec corrigés détaillés :")}
  <div class="soutien">⭐ <b>Cours de soutien</b> 3AC (en ligne ou à domicile) pour préparer l'examen — <a href="https://wa.me/{WA}" target="_blank" rel="noopener" data-ev="clic_soutien_examens">WhatsApp 06 52 23 69 22</a></div>
</main>"""
        jsonld = {"@context": "https://schema.org", "@graph": [
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Accueil", "item": f"{BASE}/"},
                {"@type": "ListItem", "position": 2, "name": "3AC", "item": f"{BASE}/niveau/3ac/"},
                {"@type": "ListItem", "position": 3, "name": "Examens locaux", "item": url}]},
            {"@type": "CollectionPage", "name": title, "url": url, "description": desc, "inLanguage": "fr", "isAccessibleForFree": True,
             "about": "Physique-Chimie 3ème année collège", "educationalLevel": "3ème année collège (3APIC)",
             "author": {"@type": "Person", "name": "Youness HAFIDI", "url": f"{BASE}/"}}]}
        d = os.path.join(SITE, "examens-locaux-3ac"); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(title, desc, url, body, jsonld, "3ac", extra_css=".exbs{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}.exb{flex:1;min-width:120px;text-align:center;padding:10px 12px;border-radius:10px;background:#eef2fb;color:#1f3a8a;font-weight:700;text-decoration:none}.exb.exc{background:#7b3fb0;color:#fff}.exk{cursor:default}"))
        urls.insert(1, (url, "0.9"))

    # Page « Examens nationaux 2BAC » (tableau, mode examen chronométré, mes notes, exercices par thème) + calculateur de note du bac
    exn = [(l, it) for l in by_level.get("2bac", []) if l["unite"].startswith("Examens") for it in l["items"]]
    if exn:
        def imgs_of(u):
            stem = os.path.basename(u)[:-4]
            fs = sorted(glob.glob(os.path.join(SITE, "docimg", stem + "-*.webp")), key=lambda f: int(re.search(r"-(\d+)\.webp$", f).group(1)))
            return ",".join("/docimg/" + os.path.basename(f) + "?v=" + hashlib.md5(open(f, "rb").read()).hexdigest()[:8] for f in fs)
        tab = {"SM": {}, "PC": {}}
        for l, it in exn:
            fil = "PC" if ("Physiques" in l["unite"] or " PC" in l["unite"]) else "SM"
            m = re.search(r"(\d{4}).*?[Ss]ujet\s+(\w)", it["titre"])
            if m: tab[fil].setdefault((m.group(1), m.group(2)), {})["c" if it["type"] in ("corrige", "corr") else "s"] = it
        FN = {"SM": ("Sciences Mathématiques (A et B)", 240, "4 h"), "PC": ("Sciences Physiques (PC)", 180, "3 h")}
        panes = ""; nb = 0
        for fil, (fnom, dur, dtxt) in FN.items():
            rows = ""
            for (an, L), d in sorted(tab[fil].items(), key=lambda x: (-int(x[0][0]), x[0][1])):
                k = f"{fil}-{an}-{L}"; ses = "Normale" if L == "N" else "Rattrapage"; nb += 1
                tt = f"Examen national {an} – session {ses.lower()} – 2BAC {fil}"
                bs = f'<a class="xb xs" href="/?doc={E(d["s"]["url"])}" data-imgs="{imgs_of(d["s"]["url"])}" data-t="{E(tt)}">📄 Sujet</a>' if "s" in d else "—"
                bc = f'<a class="xb xc" href="/?doc={E(d["c"]["url"])}" data-imgs="{imgs_of(d["c"]["url"])}" data-t="{E("Corrigé – " + tt)}">✅ Corrigé</a>' if "c" in d else "—"
                rows += f'<tr data-k="{k}" data-dur="{dur}"><td data-l="Année"><b>{an}</b></td><td data-l="Session">{ses}</td><td>{bs}</td><td>{bc}</td><td><button type="button" class="xb xt" data-k="{k}">⏱ Mode examen</button></td><td data-l="Ma note"><input class="xn" type="number" min="0" max="20" step="0.25" inputmode="decimal" placeholder="—" aria-label="Ma note sur 20"> /20</td></tr>'
            panes += f'''<div class="xfil" id="fil-{fil.lower()}"{"" if fil == "SM" else " hidden"}>''' + (f'''<table class="xtab"><thead><tr><th>Année</th><th>Session</th><th>Sujet</th><th>Corrigé</th><th>S'entraîner ({dtxt})</th><th>Ma note</th></tr></thead><tbody>{rows}</tbody></table>''' if rows else '<p class="tip">Les examens nationaux de la filière Sciences Physiques arrivent bientôt.</p>') + "</div>"
        th = json.load(open(os.path.join(SITE, "bac_themes.json"), encoding="utf-8"))
        thh = ""
        for tk, tnom in th["themes"].items():
            its = [i for i in th["items"] if i["th"] == tk]
            if not its: continue
            li = "".join(f'''<li><span><b>{i["fil"]} {i["an"]} {"N" if i["s"] == "N" else "R"}</b> · Ex. {i["ex"]}{(" – " + i["part"]) if i["part"] else ""} : {E(i["t"])}</span><span class="thb"><a href="#" class="xth" data-k="{i["fil"]}-{i["an"]}-{i["s"]}" data-w="s" data-p="{i["ps"]}" data-t="{E(i["t"])} – sujet {i["an"]}">Sujet</a><a href="#" class="xth thc" data-k="{i["fil"]}-{i["an"]}-{i["s"]}" data-w="c" data-p="{i["pc"]}" data-t="{E(i["t"])} – corrigé">Corrigé</a></span></li>''' for i in sorted(its, key=lambda i: (-int(i["an"]), i["s"], i["ex"])))
            thh += f'<details class="thm"><summary>{E(tnom)} <small>{len(its)} exercice{"s" if len(its) > 1 else ""}</small></summary><ul>{li}</ul></details>'
        css = """.xtabs{display:flex;gap:8px;flex-wrap:wrap;margin:6px 0 12px}.xtabs button{border:2px solid #2e7d4f;background:#fff;color:#2e7d4f;border-radius:99px;padding:9px 16px;font-weight:800;cursor:pointer;font-size:15px}.xtabs button.on{background:#2e7d4f;color:#fff}
.xtab{width:100%;border-collapse:collapse;background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 2px 10px rgba(15,35,80,.08)}.xtab th{background:#0f2350;color:#fff;padding:10px 8px;font-size:14px;text-align:center}.xtab td{padding:9px 8px;border-top:1px solid #e6eaf2;text-align:center;font-size:15px}
.xb{display:inline-block;padding:8px 12px;border-radius:10px;background:#eef2fb;color:#1f3a8a;font-weight:700;text-decoration:none;border:0;cursor:pointer;font-size:14px;white-space:nowrap}.xb.xc{background:#2e7d4f;color:#fff}.xb.xt{background:#fff4d6;color:#7a5a00}.xn{width:64px;padding:6px;border:1px solid #c9d2e3;border-radius:8px;font-size:15px;text-align:center}
@media(max-width:720px){.xtab thead{display:none}.xtab tr{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:10px;border-top:1px solid #e6eaf2}.xtab td{border:0;padding:2px}.xtab td[data-l]:before{content:attr(data-l)" : ";color:#6b7488;font-size:13px}.xb{width:100%}}
.mr{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:10px}.mr div{background:#fff;border-radius:12px;padding:12px;text-align:center;box-shadow:0 2px 8px rgba(15,35,80,.07)}.mr b{display:block;font-size:26px;color:#0f2350}.mr span{font-size:13px;color:#6b7488}
.mrl{list-style:none;padding:0;margin:0}.mrl li{display:grid;grid-template-columns:170px 1fr 60px;gap:8px;align-items:center;margin:6px 0;font-size:14px}.mrl i{display:block;height:10px;border-radius:9px;background:linear-gradient(90deg,#2e7d4f,#7cc49a)}
.thm{background:#fff;border-radius:12px;margin:8px 0;box-shadow:0 2px 8px rgba(15,35,80,.07)}.thm summary{padding:12px 14px;font-weight:800;color:#0f2350;cursor:pointer}.thm summary small{font-weight:600;color:#6b7488;margin-left:6px}.thm ul{list-style:none;margin:0;padding:0 12px 10px}.thm li{display:flex;justify-content:space-between;gap:10px;align-items:center;padding:7px 0;border-top:1px solid #eef1f6;font-size:14px}.thb{display:flex;gap:6px;flex-shrink:0}.thb a{padding:5px 10px;border-radius:8px;background:#eef2fb;color:#1f3a8a;font-weight:700;text-decoration:none;font-size:13px}.thb a.thc{background:#2e7d4f;color:#fff}
.dv{position:fixed;inset:0;z-index:80;background:#0e1424;display:flex;flex-direction:column}.dv[hidden]{display:none}.dv-bar{display:flex;align-items:center;gap:8px;padding:10px 12px;background:#0f2350;color:#fff}.dv-t{flex:1;font-size:15px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.dv-tm{font:800 18px/1 Inter,monospace;background:#fff4d6;color:#7a5a00;padding:7px 10px;border-radius:9px}.dv-tm.dv-warn{background:#ffd9d9;color:#a40000}.dv-end{border:0;background:#ffcc4d;color:#0f2350;border-radius:10px;padding:9px 12px;font-weight:800;cursor:pointer}.dv-x{border:0;background:#fff;color:#0f2350;border-radius:10px;width:42px;height:38px;font-size:18px;font-weight:800;cursor:pointer}
.dv-fin{background:#e9f7ef;color:#0f2350;padding:10px 14px;font-size:15px}.dv-fr{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:8px}.dv-fr button{border:0;border-radius:9px;padding:8px 12px;font-weight:800;cursor:pointer;background:#2e7d4f;color:#fff}.dv-fr .dv-s{background:#0f2350}.dv-n{width:70px;padding:6px;border-radius:8px;border:1px solid #9fb3c8;font-size:15px}
.dv-pages{flex:1;overflow:auto;padding:12px 8px;-webkit-overflow-scrolling:touch}.dv-p{position:relative;max-width:960px;margin:0 auto 12px;background:#fff;box-shadow:0 4px 18px rgba(0,0,0,.4);aspect-ratio:210/297}.dv-p img{display:block;width:100%;height:100%;object-fit:contain;user-select:none;pointer-events:none}.dv-wm{position:absolute;right:10px;bottom:8px;font:600 11px Inter,sans-serif;color:rgba(15,35,80,.35)}"""
        url = f"{BASE}/examens-nationaux-2bac/"
        title = "Examens nationaux Physique-Chimie 2BAC corrigés 2025–2026 | Bac SM et PC"
        desc = "Examens nationaux de physique-chimie du bac marocain (2BAC Sciences Maths et Sciences Physiques) avec corrections détaillées vérifiées : mode examen chronométré, suivi de tes notes et exercices classés par thème."
        body = f"""<section class="head"><div class="wrap">
  <div class="crumbs"><a href="/">Accueil</a> › <a href="/niveau/2bac/">2BAC</a> › Examens nationaux</div>
  <h1>Examens nationaux Physique-Chimie 2BAC avec corrigés</h1>
  <p class="ar" lang="ar-MA" dir="rtl" style="font-size:19px;margin:6px 0">الامتحانات الوطنية في الفيزياء والكيمياء – الثانية بكالوريا مع التصحيح</p>
  <div class="tags"><span class="tag g">Bac SM · PC</span><span class="tag">{nb} examens corrigés</span><span class="tag">Format officiel</span><span class="tag">Gratuit</span></div>
</div></section>
<main class="wrap">
  <div class="intro"><p>Entraîne-toi avec les <b>examens nationaux du baccalauréat</b> : sujet au <b>format officiel</b> et <b>corrigé détaillé</b> vérifié avec la grille du ministère.
  Lance le <b>⏱ mode examen</b> pour composer en temps réel (4 h en SM, 3 h en PC) : le corrigé s'ouvre quand tu termines, puis tu notes ta copie pour suivre ta progression.</p></div>
  <h2 class="sec">📝 Sujets et corrigés</h2>
  <div class="xtabs"><button type="button" class="on" data-fil="sm">📐 Sciences Maths</button><button type="button" data-fil="pc">🔬 Sciences Physiques</button></div>
  {panes}
  <h2 class="sec">📊 Mes résultats</h2>
  <div id="mesres"></div>
  <h2 class="sec">📚 Exercices par thème</h2>
  <p class="tip">Révise un chapitre précis : chaque lien ouvre directement l'exercice dans le sujet ou dans le corrigé.</p>
  {thh}
  <div class="intro" style="margin-top:18px"><p>🧮 Calcule ta moyenne générale avec le <a href="/calcul-note-bac/"><b>calculateur de note du bac</b></a>.</p></div>
  {share_block(url, "📝 Examens nationaux Physique-Chimie 2BAC avec corrigés, mode examen chronométré :")}
  <div class="soutien">⭐ <b>Cours de soutien</b> 2BAC (en ligne ou à domicile) pour préparer le national — <a href="https://wa.me/{WA}" target="_blank" rel="noopener" data-ev="clic_soutien_examens_bac">WhatsApp 06 52 23 69 22</a></div>
</main>"""
        jsonld = {"@context": "https://schema.org", "@graph": [
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Accueil", "item": f"{BASE}/"},
                {"@type": "ListItem", "position": 2, "name": "2BAC", "item": f"{BASE}/niveau/2bac/"},
                {"@type": "ListItem", "position": 3, "name": "Examens nationaux", "item": url}]},
            {"@type": "CollectionPage", "name": title, "url": url, "description": desc, "inLanguage": "fr", "isAccessibleForFree": True,
             "educationalLevel": "2ème année baccalauréat", "author": {"@type": "Person", "name": "Youness HAFIDI", "url": f"{BASE}/"}}]}
        d = os.path.join(SITE, "examens-nationaux-2bac"); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(title, desc, url, body, jsonld, "2bac", extra_css=css, extra_js='<script src="/js/examens.js" defer></script>'))
        urls.insert(1, (url, "0.9"))

    # Calculateur de la note du bac (formule officielle : 25 % CC + 25 % régional + 50 % national)
    url = f"{BASE}/calcul-note-bac/"
    title = "Calcul note bac Maroc : moyenne générale et note nationale nécessaire | 2BAC"
    desc = "Calculateur gratuit de la moyenne du bac marocain : 25 % contrôle continu, 25 % examen régional, 50 % examen national. Mention obtenue et note nationale nécessaire pour réussir ou avoir une mention."
    body = f"""<section class="head"><div class="wrap"><div class="crumbs"><a href="/">Accueil</a> › <a href="/niveau/2bac/">2BAC</a> › Calcul de la note du bac</div>
<h1>Calcul de la note du bac (Maroc)</h1><p class="ar" lang="ar-MA" dir="rtl" style="font-size:19px;margin:6px 0">حساب معدل البكالوريا</p></div></section>
<main class="wrap"><div class="intro calc">
<p>Formule officielle : <b>Moyenne = 25 % contrôle continu + 25 % examen régional + 50 % examen national</b>.</p>
<label>Contrôle continu (2BAC) <input id="cc" type="number" min="0" max="20" step="0.01" inputmode="decimal"></label>
<label>Examen régional (1BAC) <input id="rg" type="number" min="0" max="20" step="0.01" inputmode="decimal"></label>
<label>Examen national <small>(laisse vide pour savoir la note nécessaire)</small> <input id="nt" type="number" min="0" max="20" step="0.01" inputmode="decimal"></label>
<div id="res" class="cres"></div></div>
<div class="intro"><p>Mentions : <b>Passable</b> de 10 à 12, <b>Assez bien</b> de 12 à 14, <b>Bien</b> de 14 à 16, <b>Très bien</b> à partir de 16.</p>
<p>Prépare l'examen national avec les <a href="/examens-nationaux-2bac/"><b>examens nationaux corrigés</b></a> et le mode examen chronométré.</p></div>
{share_block(url, "🧮 Calcule ta moyenne du bac :")}</main>"""
    calc_css = ".calc label{display:block;margin:10px 0;font-weight:700;color:#0f2350}.calc input{display:block;width:100%;max-width:240px;margin-top:4px;padding:10px;font-size:17px;border:1px solid #c9d2e3;border-radius:10px}.cres{margin-top:14px;padding:14px;border-radius:12px;background:#eef2fb;font-size:16px;line-height:1.6}.cres b.big{font-size:30px;color:#0f2350}"
    calc_js = """<script>(function(){var ids=['cc','rg','nt'],f=function(i){var v=parseFloat((document.getElementById(i).value||'').replace(',','.'));return isNaN(v)?null:Math.max(0,Math.min(20,v));};
function men(m){return m>=16?'Très bien':m>=14?'Bien':m>=12?'Assez bien':m>=10?'Passable':'Non admis (rattrapage si ≥ 9 selon le règlement)';}
function n2(x){return x.toFixed(2).replace('.',',');}
function go(){var cc=f('cc'),rg=f('rg'),nt=f('nt'),r=document.getElementById('res');try{localStorage.setItem('yh_calc',JSON.stringify([cc,rg,nt]));}catch(e){}
if(cc==null||rg==null){r.innerHTML='Écris ta note de contrôle continu et ta note régionale.';return;}
if(nt!=null){var m=0.25*cc+0.25*rg+0.5*nt;r.innerHTML='Moyenne générale : <b class="big">'+n2(m)+'</b> /20<br>Mention : <b>'+men(m)+'</b>';return;}
var s=[[10,'réussir'],[12,'Assez bien'],[14,'Bien'],[16,'Très bien']].map(function(p){var n=(p[0]-0.25*cc-0.25*rg)/0.5;return '<li>Pour <b>'+p[1]+'</b> ('+p[0]+'/20) : '+(n<=0?'déjà assuré':n>20?'impossible':'il te faut <b>'+n2(n)+'</b> au national')+'</li>';}).join('');
r.innerHTML='Note nationale nécessaire :<ul>'+s+'</ul>';}
try{var s=JSON.parse(localStorage.getItem('yh_calc')||'[]');ids.forEach(function(i,k){if(s[k]!=null)document.getElementById(i).value=s[k];});}catch(e){}
ids.forEach(function(i){document.getElementById(i).addEventListener('input',go);});go();})();</script>"""
    d = os.path.join(SITE, "calcul-note-bac"); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(title, desc, url, body, {"@context": "https://schema.org", "@type": "WebApplication", "name": title, "url": url, "applicationCategory": "EducationalApplication", "isAccessibleForFree": True}, "2bac", extra_css=calc_css, extra_js=calc_js))
    urls.insert(1, (url, "0.8"))

    # Page « toutes les leçons » (/lecons/) et page 404
    allli = ""
    for niv in USED_LEVELS:
        info = LEVELS[niv]
        allli += f'<h2 class="sec"><a href="/niveau/{niv}/" style="text-decoration:none">{info["short"]} – {info["long"]}</a></h2>' + lesson_cards(niv, by_level[niv])
    for niv in ORDER:
        if niv not in USED_LEVELS:
            allli += f'<h2 class="sec">{LEVELS[niv]["short"]} – {LEVELS[niv]["long"]} <small style="font-family:Inter;font-size:13px;color:#7a5a00;background:var(--gold-soft);padding:3px 10px;border-radius:99px">Bientôt · قريبا</small></h2>'
    url = f"{BASE}/lecons/"
    t = "Leçons de physique-chimie 2AC, 3AC, TCS | YH Physique-Chimie"
    dsc = "Toutes les leçons de physique-chimie de Pr. Youness HAFIDI : séries d'exercices et corrigés en ligne pour la 2AC, la 3AC et le tronc commun scientifique."
    body = f"""<section class="head"><div class="wrap"><div class="crumbs"><a href="/">Accueil</a> › Toutes les leçons</div>
<h1>Toutes les leçons</h1><div class="ar" lang="ar">جميع الدروس</div></div></section>
<main class="wrap">{allli}</main>"""
    os.makedirs(os.path.join(SITE, "lecons"), exist_ok=True)
    open(os.path.join(SITE, "lecons", "index.html"), "w", encoding="utf-8").write(
        page(t, dsc, url, body, {"@context": "https://schema.org", "@type": "CollectionPage", "name": t, "url": url}, "lecons"))
    urls.insert(1, (url, "0.9"))
    body404 = f"""<section class="head"><div class="wrap"><h1>Page introuvable</h1>
<div class="ar" lang="ar">هذه الصفحة غير موجودة</div></div></section>
<main class="wrap"><div class="intro"><p>L'adresse tapée n'existe pas (vérifie l'orthographe, sans majuscules). Choisis une leçon ci-dessous ou <a href="/">reviens à l'accueil</a>.</p></div>{allli}</main>"""
    html404 = page("Page introuvable | YH Physique-Chimie", dsc, f"{BASE}/", body404, {"@context": "https://schema.org", "@type": "WebPage"})
    html404 = html404.replace('<meta name="viewport"', '<meta name="robots" content="noindex">\n<meta name="viewport"', 1)
    open(os.path.join(SITE, "404.html"), "w", encoding="utf-8").write(html404)

    # ---------- Simulations : intégrées dans les cours -> redirections ----------
    simcards = ""
    for sm_ in SIMS:
        lvs = LEVELS[sm_["niv"]]
        lpath = index_map.get(f'{sm_["niv"]}|{sm_["lesson"]}', "/") + "#lab"
        d = os.path.join(SITE, "simulations", sm_["slug"]); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(
            f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><meta name="robots" content="noindex"><link rel="canonical" href="{BASE}{lpath.split("#")[0]}">'
            f'<meta http-equiv="refresh" content="0;url={lpath}"><title>{E(sm_["title"])}</title></head><body><a href="{lpath}">Ouvrir la simulation dans le cours</a>'
            f'<script>location.replace({json.dumps(lpath)})</script></body></html>')
        simcards += f'''<a class="lc" style="--c:{LCOLS.get(sm_["niv"],'#1f4e9c')}" href="{lpath}"><span class="lc-code">🧪 {lvs["short"]}</span><span class="lc-t">{E(sm_["title"])}</span>
<span class="lc-m">{E(sm_["lesson"])}</span><span class="lc-f">{E(sm_["intro"])}</span><span class="lc-go">Ouvrir dans le cours →</span></a>'''
    d = os.path.join(SITE, "simulations"); os.makedirs(d, exist_ok=True)
    surl = f"{BASE}/simulations/"
    body = f"""<section class="head"><div class="wrap"><div class="crumbs"><a href="/">Accueil</a> › Simulations</div><h1>Les simulations</h1>
<div class="ar" lang="ar">المختبر الافتراضي</div></div></section>
<main class="wrap"><div class="intro"><p>Chaque simulation se trouve maintenant <b>dans son cours</b>, à l'endroit où on en a besoin. Choisis-en une :</p></div><div class="lcards">{simcards}</div></main>"""
    html_s = page("Simulations interactives de physique-chimie | YH Physique-Chimie", "Les simulations de Pr. Youness HAFIDI, intégrées dans les cours.", surl, body,
                  {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Simulations", "url": surl}, "sim")
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(html_s.replace('<meta name="viewport"', '<meta name="robots" content="noindex">\n<meta name="viewport"', 1))

    # ---------- À propos / Contact ----------
    ab = f"""<section class="head"><div class="wrap"><div class="crumbs"><a href="/">Accueil</a> › À propos</div><h1>À propos</h1><div class="ar" lang="ar">من أنا</div></div></section>
<main class="wrap"><div class="intro" style="display:flex;gap:22px;align-items:center;flex-wrap:wrap"><div style="position:relative;flex-shrink:0;margin:auto"><img src="/prof-lg.webp" alt="Pr. Youness HAFIDI, professeur de physique-chimie" width="220" height="239" style="width:220px;height:239px;object-fit:cover;border-radius:18px;border:3px solid var(--gold);display:block"><img src="/logo.jpg" alt="Logo YH Physique-Chimie" style="position:absolute;right:-12px;bottom:-12px;width:64px;height:64px;border-radius:50%;border:3px solid var(--gold);background:#fff"></div>
<div style="flex:1;min-width:240px"><p><b>Pr. Youness HAFIDI</b> — professeur de physique-chimie au cycle secondaire.</p>
<p>YH Physique-Chimie rassemble mes ressources pour les élèves : séries d'exercices et corrigés, devoirs surveillés, résumés en cartes mentales, quiz et simulations interactives, du collège au baccalauréat (examens nationaux 2BAC SM corrigés).</p>
<p class="ar" lang="ar" dir="rtl">أستاذ الفيزياء والكيمياء بالسلك الثانوي. يضم هذا الموقع سلاسل تمارين مع تصحيحها، وفروضا محروسة، وملخصات، وتمارين تفاعلية، مجانا.</p></div></div>
<h2 class="sec">Comment utiliser le site</h2>
<div class="lcards"><a class="lc" style="--c:#1f4e9c" href="/lecons/"><span class="lc-code">01</span><span class="lc-t">📖 Lis le cours</span><span class="lc-m">Définitions, relations et simulation, directement dans la leçon.</span><span class="lc-go">Choisir une leçon →</span></a><a class="lc" style="--c:#1f4e9c" href="/lecons/"><span class="lc-code">02</span><span class="lc-t">✍️ Cherche les exercices</span><span class="lc-m">Seul, sur ta feuille, avant de regarder la correction.</span><span class="lc-go">Choisir une leçon →</span></a><a class="lc" style="--c:#1f4e9c" href="/lecons/"><span class="lc-code">03</span><span class="lc-t">✅ Vérifie</span><span class="lc-m">Clique sur « Voir la réponse » et lis l'erreur fréquente.</span><span class="lc-go">Choisir une leçon →</span></a><a class="lc" style="--c:#1f4e9c" href="/lecons/"><span class="lc-code">04</span><span class="lc-t">🎯 Teste-toi</span><span class="lc-m">Fais le quiz et les applications interactives.</span><span class="lc-go">Choisir une leçon →</span></a></div>
<div class="soutien">⭐ <b>Cours de soutien</b> (en ligne ou à domicile) : <a href="https://wa.me/{WA}" target="_blank" rel="noopener">WhatsApp 06 52 23 69 22</a></div></main>"""
    os.makedirs(os.path.join(SITE, "a-propos"), exist_ok=True)
    open(os.path.join(SITE, "a-propos", "index.html"), "w", encoding="utf-8").write(page("À propos – Pr. Youness HAFIDI | YH Physique-Chimie", "Pr. Youness HAFIDI, professeur de physique-chimie au cycle secondaire : ressources gratuites pour les élèves.", f"{BASE}/a-propos/", ab,
        {"@context": "https://schema.org", "@type": "AboutPage", "url": f"{BASE}/a-propos/"}, "apropos"))
    ct = f"""<section class="head"><div class="wrap"><div class="crumbs"><a href="/">Accueil</a> › Contact</div><h1>Contact</h1><div class="ar" lang="ar">تواصل معي</div></div></section>
<main class="wrap"><div class="intro" style="display:flex;gap:16px;align-items:center;flex-wrap:wrap"><img src="/prof.webp" alt="Pr. Youness HAFIDI" width="96" height="96" style="width:96px;height:96px;border-radius:50%;border:3px solid var(--gold);object-fit:cover"><div style="flex:1;min-width:220px"><p><b>Pr. Youness HAFIDI</b> — professeur de physique-chimie</p><p>Une question sur un exercice, une remarque, ou un cours de soutien ? Écris-moi :</p></div></div>
<div class="share"><a class="btn wa" href="https://wa.me/{WA}?text={E('Bonjour Pr. Hafidi,')}" target="_blank" rel="noopener" data-ev="clic_contact_page">{WA_SVG} WhatsApp : 06 52 23 69 22</a>
<a class="btn" href="tel:+{WA}">📞 Appeler</a><a class="btn fb" href="{FB}" target="_blank" rel="noopener">{FB_SVG} Facebook</a>
<a class="btn" href="https://www.linkedin.com/in/youness-hafidi" target="_blank" rel="noopener">in LinkedIn</a></div>
<h2 class="sec">Envoyer un message rapide</h2>
<div class="intro"><p><input id="nm" placeholder="Ton prénom et ta classe" style="width:100%;padding:10px;border:1px solid var(--line);border-radius:10px;font:inherit;margin-bottom:8px">
<textarea id="ms" rows="4" placeholder="Ton message…" style="width:100%;padding:10px;border:1px solid var(--line);border-radius:10px;font:inherit"></textarea></p>
<p><button class="btn wa" type="button" onclick="location.href='https://wa.me/{WA}?text='+encodeURIComponent('Bonjour Pr. Hafidi, je suis '+document.getElementById('nm').value+'.\\n'+document.getElementById('ms').value)">Envoyer sur WhatsApp</button></p></div></main>"""
    os.makedirs(os.path.join(SITE, "contact"), exist_ok=True)
    open(os.path.join(SITE, "contact", "index.html"), "w", encoding="utf-8").write(page("Contact – Pr. Youness HAFIDI | YH Physique-Chimie", "Contacter Pr. Youness HAFIDI : WhatsApp 06 52 23 69 22, Facebook, LinkedIn.", f"{BASE}/contact/", ct,
        {"@context": "https://schema.org", "@type": "ContactPage", "url": f"{BASE}/contact/"}, "contact"))
    urls += [(f"{BASE}/a-propos/", "0.5"), (f"{BASE}/contact/", "0.5")]

    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><priority>{p}</priority></url>\n" for u, p in urls)
    sm += "</urlset>\n"
    open(os.path.join(SITE, "sitemap.xml"), "w").write(sm)
    json.dump(index_map, open(os.path.join(SITE, "lecons", "index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # Bloc statique (lisible par Google) inséré dans index.html
    blk = ""
    for niv in ORDER:
        info = LEVELS[niv]
        if niv in USED_LEVELS:
            links = " ".join(f'<a href="/lecons/{lesson_slug(niv,l["unite"])}/">{E(l["unite"])}</a>' for l in by_level[niv])
            blk += f'<div class="ix-lvl"><a class="ix-h" href="/niveau/{niv}/">{info["short"]} – {info["long"]}</a><div class="ix-links">{links}</div></div>\n'
        else:
            blk += f'<div class="ix-lvl"><span class="ix-h">{info["short"]} – {info["long"]}</span><span class="ix-soon">Bientôt · قريبا</span></div>\n'
    ix = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
    ix = re.sub(r"<!--NAV-->.*?<!--/NAV-->", lambda m: '<!--NAV--><header class="top"><div class="wrap"><a class="brand" href="/"><img src="/logo.jpg" alt="">YH Physique-Chimie</a>' + nav_html("home") + '</div></header><!--/NAV-->', ix, flags=re.S)
    COLS = {"1ac":"#0e7c86","2ac":"#1f4e9c","3ac":"#7a3fa8","tc":"#c0392b","1bac":"#8a5a10","2bac":"#2e7d4f"}
    nv = ""
    for niv in ORDER:
        info = LEVELS[niv]
        if niv in USED_LEVELS:
            n = len(by_level[niv]); d = sum(len(l["items"]) for l in by_level[niv])
            nv += f'<a class="lv" style="--c:{COLS[niv]}" href="/niveau/{niv}/"><span class="code">{info["short"]}</span><span class="nm">{info["long"]}</span><span class="ar" lang="ar">{info["ar"]}</span><span class="ct">{n} leçons · {d} documents →</span></a>\n'
        else:
            nv += f'<a class="lv soon" style="--c:{COLS[niv]}" href="/niveau/{niv}/"><span class="code">{info["short"]}</span><span class="nm">{info["long"]}</span><span class="ar" lang="ar">{info["ar"]}</span><span class="ct">Bientôt · قريبا</span></a>\n'
    ix = re.sub(r"<!--NIVEAUX-->.*?<!--/NIVEAUX-->", lambda m: "<!--NIVEAUX-->\n" + nv + "<!--/NIVEAUX-->", ix, flags=re.S)
    EMO = ["💨","⚛️","🔥","🔍","🧲","🔩","🪐","📐","🧪","⚗️"]
    sm2 = "".join(f'<a class="sim" href="{index_map.get(x["niv"]+"|"+x["lesson"], "/")}#lab"><span class="e" aria-hidden="true">{EMO[i%len(EMO)]}</span><span><b>{E(x["title"])}</b><span>{LEVELS[x["niv"]]["short"]} · {E(x["lesson"])}</span></span></a>\n' for i, x in enumerate(SIMS))
    ix = re.sub(r"<!--SIMS-->.*?<!--/SIMS-->", lambda m: "<!--SIMS-->\n" + sm2 + "<!--/SIMS-->", ix, flags=re.S)
    ix = re.sub(r"<!--LECONS-->.*?<!--/LECONS-->", "<!--LECONS-->\n" + blk + "<!--/LECONS-->", ix, flags=re.S)
    open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(strip_ar(ix))
    print(len(urls), "URL dans le sitemap")
    # Pages des PDF pré-rendues en images (docimg/<nom>-<n>.webp) : l'accueil les affiche à la place du PDF (ouverture rapide)
    dm = {}
    for f in sorted(glob.glob(os.path.join(SITE, "cours", "*.pdf"))):
        stem = os.path.splitext(os.path.basename(f))[0]
        fs = sorted(glob.glob(os.path.join(SITE, "docimg", glob.escape(stem) + "-*.webp")), key=lambda x: int(re.search(r"-(\d+)\.webp$", x).group(1)))
        if fs: dm["cours/" + os.path.basename(f)] = ["/docimg/" + os.path.basename(x) + "?v=" + hashlib.md5(open(x, "rb").read()).hexdigest()[:8] for x in fs]
    open(os.path.join(SITE, "docimg", "index.json"), "w", encoding="utf-8").write(json.dumps(dm, ensure_ascii=False, separators=(",", ":")))
    print(len(dm), "PDF disponibles en images")

VIDEOS_LECON = {
    ("tc", "Contrôles surveillés – Semestre 1"): [
        ("Exercice 1 – Gravitation universelle", "Correction_DS1_TCSF_Ex1_Gravitation.mp4"),
        ("Exercice 2 – Actions mécaniques et force pressante", "Correction_DS1_TCSF_Ex2_Actions_mecaniques.mp4"),
        ("Chimie – Espèces chimiques et extraction", "Correction_DS1_TCSF_Chimie.mp4"),
        ("Situation-problème – Les trois bouteilles", "Correction_DS1_TCSF_Situation_probleme.mp4")],
}
USED_LEVELS = []

def version_js():
    """Ajoute ?v=<empreinte> aux scripts du site : chaque mise en ligne force les navigateurs à prendre la nouvelle version."""
    import hashlib
    ver = {}
    for n in ("avis", "soutien", "suivre", "examens", "lang"):
        f = os.path.join(SITE, "js", n + ".js")
        if os.path.exists(f): ver[n] = hashlib.md5(open(f, "rb").read()).hexdigest()[:8]
    pat = re.compile(r'src="/js/(avis|soutien|suivre|examens|lang)\.js(?:\?v=\w+)?"')
    k = 0
    for root, _, files in os.walk(SITE):
        for fn in files:
            if not fn.endswith(".html"): continue
            fp = os.path.join(root, fn); t = open(fp, encoding="utf-8").read()
            if "/js/suivre.js" in t and "/js/lang.js" not in t:
                t = re.sub(r'(<script defer src="/js/suivre\.js[^"]*"></script>)', r'\1\n<script defer src="/js/lang.js"></script>', t, count=1)
            t2 = pat.sub(lambda m: f'src="/js/{m.group(1)}.js?v={ver.get(m.group(1), "1")}"', t)
            if t2 != t: open(fp, "w", encoding="utf-8").write(t2); k += 1
    print(k, "pages : scripts versionnés")

build()
version_js()
