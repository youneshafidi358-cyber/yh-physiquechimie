# -*- coding: utf-8 -*-
"""Cours structurés (HTML) de chaque leçon, avec la simulation placée dans le cours."""
import re, unicodedata
from cours_lib import TRAD, E
import cours_2ac as A2, cours_3ac as A3, cours_tc as T

COURS = {
    "L'air qui nous entoure": (A2.AIR, A2.AIR_TRAD),
    "Les molécules et les atomes": (A2.MOLA, A2.MOLA_TRAD),
    "Les combustions": (A2.COMB, A2.COMB_TRAD),
    "Les matériaux dans la vie quotidienne": (A3.MAT, A3.MAT_TRAD),
    "Les atomes et les ions": (A3.IONS, A3.IONS_TRAD),
    "Réaction de quelques matériaux avec l'air": (A3.OXY, A3.OXY_TRAD),
    "La gravitation universelle": (T.GRAV, T.GRAV_TRAD),
    "Exemples d'actions mécaniques": (T.MECA, T.MECA_TRAD),
    "Les espèces chimiques": (T.ESP, T.ESP_TRAD),
    "Extraction, séparation et identification": (T.EXT, T.EXT_TRAD),
}

def _slug(s):
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

def _sid(t):
    return "c-" + _slug(t)[:40]

def render(unite, sim_html="", niveau=""):
    """Renvoie (sommaire, corps) ou ('','') si pas de cours."""
    if unite not in COURS:
        return "", ""
    secs, trad = COURS[unite]
    toc, body, placed = [], [], False
    N = len(secs)
    for k, (num, title, html) in enumerate(secs, 1):
        sid = "c-" + _slug(title)[:40]
        lab = f"{num}. {title}" if num else title
        toc.append(f'<li><a href="#{sid}" data-p="{k}"><span class="pg">p.{k}</span> {E(lab)}</a></li>')
        if "%%SIM%%" in html:
            html = html.replace("%%SIM%%", sim_html, 1); placed = True
        if k == N and sim_html and not placed:
            html += sim_html; placed = True
        nav = ('<nav class="pnav" aria-label="Pages du cours">'
               + (f'<a class="pprev" href="#{_sid(secs[k-2][1])}" data-p="{k-1}">← Page {k-1}</a>' if k > 1 else '<span></span>')
               + f'<span class="pnum">Page {k} / {N}</span>'
               + (f'<a class="pnext" href="#{_sid(secs[k][1])}" data-p="{k+1}">Page {k+1} : {E(secs[k][1])} →</a>' if k < N else '<a class="pnext" href="#resume">Résumé et exercices →</a>')
               + '</nav>')
        body.append(f'<section class="csec page" id="{sid}" data-p="{k}"><div class="phead">Page {k} / {N}</div><h3 class="cs"><span>{E(num)}</span>{E(title)}</h3>{html}{nav}</section>')
    head = (f'<div class="chead"><span class="ch-b"><img src="/logo.jpg" alt="" width="34" height="34">'
            f'<span><b>YH Physique-Chimie</b><i>Pr. Youness HAFIDI</i></span></span>'
            f'<span class="ch-t">{E(unite)}</span>' + (f'<span class="ch-n">{E(niveau)}</span>' if niveau else '') + '</div>')
    return "<ol>" + "".join(toc) + "</ol>", head + "".join(body)

CSS = r"""
.cbody.cahier{position:relative;background-image:linear-gradient(90deg,transparent 46px,#f2b8b8 46px,#f2b8b8 48px,transparent 48px),repeating-linear-gradient(#fff 0 31px,#dfe8f5 31px 32px);padding-left:66px!important;box-shadow:0 2px 0 #e8e2d4,0 4px 14px rgba(20,33,61,.06)}
.screens .scr{display:none}.screens.measuring .scr{display:block;visibility:hidden;position:absolute;left:0;right:0}.screens{position:relative}.screens .scr.on{display:block;animation:pgin .25s ease}.cs.cont::after{content:' (suite)';font-weight:400;color:#8a93a8;font-size:.8em}
.js-cahier .cbody.cahier{font-size:15.5px;line-height:1.55}.js-cahier .cahier .cs{margin:10px 0 8px;font-size:19px}.js-cahier .cahier .bx{margin:8px 0}.js-cahier .cahier .bx-b{padding:8px 12px}.js-cahier .cahier .qa,.js-cahier .cahier .qcm{margin:6px 0;padding:6px 10px}.js-cahier .cahier .cfig img{max-height:42vh;width:auto}.js-cahier .cahier .enclair{margin:6px 0 8px;font-size:15px}
@media (prefers-reduced-motion:reduce){.screens .scr.on{animation:none}}
@keyframes pgin{from{opacity:0;transform:translateX(12px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){.js-cahier .cahier .page.on{animation:none}}
.phead{font-size:12.5px;font-weight:700;color:#8a93a8;text-align:right;margin-top:10px;letter-spacing:.04em;text-transform:uppercase}
.pnav{display:flex;justify-content:space-between;align-items:center;gap:10px;margin:22px 0 6px;padding-top:12px;border-top:2px dashed #e3e8f1;flex-wrap:wrap}
.pnav button{font:inherit;border:0;cursor:pointer;display:inline-flex;align-items:center;min-height:44px;padding:8px 16px;border-radius:12px;font-weight:700;font-size:14.5px}
.pnav a{display:inline-flex;align-items:center;min-height:44px;padding:8px 14px;border-radius:12px;font-weight:700;text-decoration:none;font-size:14.5px}
.pprev{background:#f1f4f9;color:#123c8c}.pnext{background:#123c8c;color:#fff}.pnum{font-size:13px;color:#565f74;font-weight:600}
.ctoc .pg{display:inline-block;min-width:30px;font-size:11.5px;font-weight:800;color:#b42318}
.enclair{display:flex;gap:8px;align-items:flex-start;margin:8px 0 12px;padding:8px 12px;background:#fffbe9;border-left:4px solid #e0b100;border-radius:8px;font-size:15.5px}
.enclair::before{content:"💬";flex:none}
@media (max-width:900px){.cbody.cahier{background-image:linear-gradient(90deg,transparent 18px,#f2b8b8 18px,#f2b8b8 20px,transparent 20px),repeating-linear-gradient(#fff 0 31px,#dfe8f5 31px 32px);padding-left:30px!important}.pnav button{font:inherit;border:0;cursor:pointer;display:inline-flex;align-items:center;min-height:44px;padding:8px 16px;border-radius:12px;font-weight:700;font-size:14.5px}
.pnav a{flex:1 1 100%;justify-content:center}.pnum{order:-1;width:100%;text-align:center}}
.wrap{max-width:1400px}
.coursewrap{display:grid;grid-template-columns:230px minmax(0,1fr);gap:20px;align-items:start}
.ctoc{position:sticky;top:76px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:12px 12px 8px;font-size:14px;max-height:calc(100vh - 100px);overflow:auto}
.ctoc b{display:block;color:#0f2350;margin-bottom:6px}
.ctoc ol{margin:0;padding-left:0;list-style:none}.ctoc li{margin:0 0 4px}
.ctoc a{display:block;padding:6px 8px;border-radius:8px;color:#334;text-decoration:none;line-height:1.3}
.ctoc a:hover,.ctoc a.on{background:#eef3fc;color:#123c8c;font-weight:600}
.cbody{min-width:0;overflow-wrap:break-word;background-color:#fff;border:1px solid var(--line);border-radius:16px;padding:8px 22px 18px;line-height:1.65;font-size:16.5px}
.csec{padding-top:6px;scroll-margin-top:80px}
.cs{display:flex;align-items:center;gap:10px;font-size:21px;color:#0f2350;margin:22px 0 12px;padding-bottom:8px;border-bottom:2px solid #e8edf6}
.cs>span:first-child{background:#0f2350;color:#fff;border-radius:8px;padding:2px 10px;font-size:16px;min-width:22px;text-align:center}
.cs>span:first-child:empty{display:none}
.cbody h4{color:#b8860b;font-size:18px;margin:20px 0 8px}.cbody h5{color:#1f7a3a;font-size:16.5px;margin:16px 0 6px}
.cbody ul,.cbody ol{padding-left:22px;margin:6px 0}.cbody li{margin:3px 0}
.bx{border-radius:12px;margin:12px 0;overflow:hidden;border:1px solid}
.bx-t{font-weight:700;font-size:14.5px;padding:6px 12px;color:#fff}
.bx-b{padding:10px 14px}.bx-b>:first-child{margin-top:0}.bx-b>:last-child{margin-bottom:0}
.k-def{border-color:#c9d6ee;background:#f5f8fd}.k-def .bx-t{background:#1f3f7a}
.k-ret{border-color:#bfe0c9;background:#f2faf4}.k-ret .bx-t{background:#1f7a3a}
.k-conc{border-color:#bfe0c9;background:#f6fbf7}.k-conc .bx-t{background:#2f9e44}
.k-act{border-color:#dccdf0;background:#faf7fe}.k-act .bx-t{background:#6b3fa0}
.k-sit{border-color:#f3d9a6;background:#fffaf0}.k-sit .bx-t{background:#c47f00}
.k-obs{border-color:#cfe3f5;background:#f6fafe}.k-obs .bx-t{background:#2b6cb0}
.k-rem{border-color:#efe0b0;background:#fffcf0}.k-rem .bx-t{background:#a07800}
.k-meth{border-color:#c6e4e7;background:#f3fafb}.k-meth .bx-t{background:#14707a}
.k-rule{border-color:#f0c6c6;background:#fff6f6}.k-rule .bx-t{background:#b42318}
.k-ex{border-color:#e2e6ee;background:#fafbfd}.k-ex .bx-t{background:#5b6475}
.k-app{border-color:#d4d9f5;background:#f7f8ff}.k-app .bx-t{background:#3949ab}
.qa{border:1px dashed #c7d0e2;border-radius:10px;padding:8px 12px;margin:8px 0;background:#fff}
.qa-q{margin:0 0 6px;font-weight:600}
.qa-btn{font:inherit;font-size:13.5px;font-weight:700;color:#123c8c;background:#eef3fc;border:1px solid #c9d6ee;border-radius:999px;padding:6px 12px;min-height:36px;cursor:pointer}
.qa-a{margin-top:8px;padding:8px 10px;border-left:4px solid #2f9e44;background:#f2faf4;border-radius:6px}
.qcm{border:1px dashed #c7d0e2;border-radius:10px;padding:8px 12px;margin:8px 0;background:#fff}
.qcm-o{display:flex;flex-wrap:wrap;gap:8px}.qcm-o button{font:inherit;font-size:14.5px;border:1px solid #c9d6ee;background:#f7f9fd;border-radius:10px;padding:7px 12px;min-height:40px;cursor:pointer}
.qcm-o button.good{background:#2f9e44;color:#fff;border-color:#2f9e44}.qcm-o button.bad{background:#d64545;color:#fff;border-color:#d64545}
.qcm-e{margin-top:8px;padding:8px 10px;border-left:4px solid #2f9e44;background:#f2faf4;border-radius:6px}
.cfig{margin:12px auto;text-align:center}.cfig img{max-width:100%;height:auto;border-radius:10px;border:1px solid #e3e8f0;background:#fff}
.cfig figcaption{font-size:13.5px;color:#5b6475;margin-top:4px}
.cfigs{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;align-items:flex-end}.cfigs .cfig{flex:1 1 140px;max-width:300px;margin:6px 0}
.ctab{overflow-x:auto;margin:10px 0;max-width:100%}.ctab table{border-collapse:collapse;width:100%;font-size:15px;background:#fff}
.ctab th{background:#0f2350;color:#fff;padding:7px 9px;text-align:left;font-weight:600}
.ctab td{padding:7px 9px;border-bottom:1px solid #e8edf6;vertical-align:middle}
.ctab tr:nth-child(even) td{background:#fafbfd}
.ctab.mols td:first-child{width:90px;text-align:center}
.ctab.trad{max-width:480px}.ctab.trad td[lang=ar]{text-align:right;font-size:17px}
.ctab tr.grp td{background:#eef3fc!important;color:#123c8c;text-align:left!important}
.mol{vertical-align:middle;margin:2px 4px}
.pie{display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin:10px 0}
.pie-c{width:120px;height:120px;border-radius:50%;box-shadow:inset 0 0 0 1px rgba(0,0,0,.08)}
.pie ul{list-style:none;padding:0}.pie i{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:6px;vertical-align:-1px}
.labin{margin:18px 0}.labin .lab-k{font-weight:800;color:#6b3fa0;font-size:15px;margin:0 0 6px}
.katex{font-size:1.08em}.katex-display{overflow-x:auto;overflow-y:hidden;padding:4px 0}
@media (max-width:900px){.coursewrap{grid-template-columns:minmax(0,1fr)}.ctoc{position:static;max-height:none}
 .cbody{padding:4px 14px 14px;font-size:16px}.cs{font-size:19px}}
"""

CSS += r"""
/* ===== Style « cahier » : papier quadrillé, titres manuscrits, relations encadrées ===== */
@font-face{font-family:Kalam;font-style:normal;font-weight:400;font-display:swap;src:url(/fonts/kalam-latin-400-normal.woff2) format("woff2")}
@font-face{font-family:"Comic Neue";font-style:normal;font-weight:400;font-display:swap;src:url(/fonts/comic-neue-latin-400-normal.woff2) format("woff2")}
@font-face{font-family:"Comic Neue";font-style:normal;font-weight:700;font-display:swap;src:url(/fonts/comic-neue-latin-700-normal.woff2) format("woff2")}
@font-face{font-family:Kalam;font-style:normal;font-weight:700;font-display:swap;src:url(/fonts/kalam-latin-700-normal.woff2) format("woff2")}
.cbody.cahier{--ink:#16306e;--red:#e04848;--grn:#1f8a3b;--blu:#1f4e9c;color:var(--ink);background-color:#fff;
 background-image:linear-gradient(90deg,transparent 44px,#f08a8a 44px,#f08a8a 46px,transparent 46px,transparent 49px,#f08a8a 49px,#f08a8a 50px,transparent 50px),
 linear-gradient(#dbe6f7 1px,transparent 1px),linear-gradient(90deg,#dbe6f7 1px,transparent 1px);
 background-size:100% 100%,22px 22px,22px 22px;padding-left:66px!important;border-radius:6px 16px 16px 6px}
.cahier .chead{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:12px 0 6px;padding-bottom:8px;border-bottom:2px solid #f0b400}
.cahier .ch-b{display:flex;align-items:center;gap:8px;font-family:Kalam,cursive;line-height:1.1}
.cahier .ch-b img{width:34px;height:34px;border-radius:50%;border:2px solid #f0b400}
.cahier .ch-b b{display:block;color:var(--blu);font-size:17px}.cahier .ch-b i{display:block;font-style:normal;font-size:13.5px;color:#5b6475}
.cahier .ch-t{flex:1;text-align:center;font-family:Kalam,cursive;font-weight:700;font-size:21px;color:var(--ink);border:2px solid var(--red);border-radius:999px;padding:2px 18px;background:#fff;min-width:0}
.cahier .ch-n{font-family:Kalam,cursive;font-weight:700;font-size:16px;color:var(--ink);background:#ffe9b8;border:2px solid #f0a020;border-radius:12px;padding:0 12px}
.cahier .cs{font-family:Kalam,cursive;font-weight:700;color:var(--ink);font-size:22px;border:2px solid #e3a300;border-bottom-width:2px;background:linear-gradient(#fff3a8,#ffd84d);border-radius:12px 999px 999px 12px;padding:3px 22px 3px 12px;display:inline-flex;width:auto;max-width:100%;margin:14px 0 10px;box-shadow:0 2px 0 rgba(224,160,0,.25)}
.cahier .cs>span:first-child{background:none;color:var(--ink);padding:0;min-width:0;font-size:inherit}.cahier .cs>span:first-child::after{content:"."}
.cahier .cs.cont::after{color:#7a6a20}
.cahier h4{font-family:Kalam,cursive;font-weight:700;color:var(--blu);font-size:19.5px;display:inline-block;border:2px solid var(--blu);background:#eef4ff;border-radius:10px 999px 999px 10px;padding:1px 22px 1px 12px;margin:14px 0 6px}
.cahier h5{font-family:Kalam,cursive;font-weight:700;color:var(--grn);font-size:17.5px;text-decoration:underline;text-underline-offset:3px}
.cahier .bx-b,.cahier .screens p,.cahier p,.cahier li,.js-cahier .cahier .enclair,.cahier .enclair{font-family:"Comic Neue",Inter,sans-serif;font-size:17.5px;line-height:1.5}.cahier b,.cahier strong{font-weight:700}
.js-cahier .cbody.cahier{font-size:17.5px}.js-cahier .cahier .cs{font-size:22px}
.cahier ul{list-style:none;padding-left:4px}.cahier ul>li{position:relative;padding-left:22px}
.cahier ul>li::before{content:"";position:absolute;left:4px;top:.62em;width:9px;height:9px;border-radius:50%;background:var(--red)}
.cahier ul ul>li::before{content:"➜";background:none;width:auto;height:auto;top:0;left:0;color:var(--red);font-size:.95em}
.cahier .bx{border:2px solid;border-radius:14px;background:rgba(255,255,255,.92);overflow:visible}
.cahier .bx-t{display:inline-block;background:none!important;font-family:Kalam,cursive;font-size:17px;font-weight:700;padding:6px 14px 0}
.cahier .bx-t>span{display:none}
.cahier .bx-b{padding:4px 14px 10px}
.cahier .k-def{border-color:#9fb8e6}.cahier .k-def .bx-t{color:var(--blu)}.cahier .k-def .bx-t::after{content:" :"}
.cahier .k-ret{border:2px dashed #3aa356;background:rgba(240,251,242,.95)}.cahier .k-ret .bx-t{color:var(--grn);text-decoration:underline;text-underline-offset:3px}.cahier .k-ret .bx-t::after{content:" !"}
.cahier .k-conc{border-color:#3aa356;background:rgba(240,251,242,.95)}.cahier .k-conc .bx-t{color:var(--grn)}
.cahier .k-rule{border:2px dashed var(--red);background:rgba(255,244,244,.95)}.cahier .k-rule .bx-t{color:#b42318}
.cahier .k-rem{border:2px dashed #e98a8a;background:rgba(255,250,240,.95)}.cahier .k-rem .bx-t{color:#b45309}
.cahier .k-meth{border-color:#7cc3c9}.cahier .k-meth .bx-t{color:#0e6b74}
.cahier .k-ex{border:0;background:transparent;border-left:3px solid #f3a0a0;border-radius:0}.cahier .k-ex .bx-t{color:#c0262d;background:#ffe1e1!important;border-radius:6px;padding:0 8px;margin:6px 0 0 10px}.cahier .k-ex .bx-t::after{content:" :"}
.cahier .k-app{border-color:#b9c0f0;background:rgba(247,248,255,.95)}.cahier .k-app .bx-t{color:#3949ab}
.cahier .k-act,.cahier .k-obs,.cahier .k-sit{background:rgba(255,255,255,.92)}.cahier .k-act .bx-t{color:#6b3fa0}.cahier .k-obs .bx-t{color:#2b6cb0}.cahier .k-sit .bx-t{color:#c47f00}
.cahier .katex-display{width:fit-content;max-width:100%;margin:10px auto;padding:6px 18px;border:2px solid var(--red);border-radius:14px;background:#fff;box-shadow:0 2px 0 rgba(224,72,72,.15)}
.cahier .katex{color:#10285f}
.cahier .pie ul>li{padding-left:0}.cahier .pie ul>li::before{display:none}
@media (max-width:600px){.cahier .chead{flex-wrap:nowrap;gap:8px}.cahier .ch-b span{display:none}.cahier .ch-t{order:0;flex:1 1 auto;font-size:16px;padding:2px 10px}.cahier .ch-n{margin-left:0;font-size:14px;padding:0 8px}}
.cahier .enclair{background:rgba(255,251,233,.95);border-left:0;border:2px dashed #e0b100;border-radius:12px}
.cahier .ctab table{border:2px solid var(--blu);border-radius:10px;border-collapse:separate;border-spacing:0;overflow:hidden;font-family:"Comic Neue",Inter,sans-serif;font-size:16.5px}
.cahier .ctab th{background:#dbe7fb;color:var(--ink);font-weight:700;text-align:center;border-bottom:2px solid var(--blu)}
.cahier .ctab td{text-align:center;border-bottom:1px solid #b8c9ea;border-right:1px solid #d3def3}.cahier .ctab td:last-child{border-right:0}
.cahier .ctab tr:nth-child(even) td{background:#f7faff}
.cahier .qa,.cahier .qcm{background:rgba(255,255,255,.95);border:2px dashed #9fb8e6;border-radius:12px}
.cahier .qa-q{font-family:"Comic Neue",Inter,sans-serif;font-weight:700}
.cahier .cfig img{border:2px solid #dbe6f7}
.cahier .phead{font-family:Kalam,cursive}
@media (max-width:900px){.cbody.cahier{background-image:linear-gradient(90deg,transparent 16px,#f08a8a 16px,#f08a8a 18px,transparent 18px),linear-gradient(#dbe6f7 1px,transparent 1px),linear-gradient(90deg,#dbe6f7 1px,transparent 1px);padding-left:28px!important}
 .cahier .ch-t{order:3;flex:1 1 100%;font-size:18px}.cahier .ch-n{margin-left:auto}.cahier .cs{font-size:19px!important}.cahier h4{font-size:17.5px}
 .cahier .bx-b,.cahier p,.cahier li,.js-cahier .cahier .enclair,.cahier .enclair{font-size:16.5px}}
"""

JS = r"""
<link rel="stylesheet" href="/js/katex/katex.min.css">
<script defer src="/js/katex/katex.min.js"></script>
<script defer src="/js/katex/auto-render.min.js" onload="renderMathInElement(document.querySelector('.cbody')||document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false});document.querySelectorAll('.katex-display').forEach(e=>{if(e.scrollWidth>e.clientWidth){e.tabIndex=0}})"></script>
<script>
(()=>{const cb=document.querySelector('.cbody.cahier');if(!cb)return;document.documentElement.classList.add('js-cahier');
const secs=[...cb.querySelectorAll('section.page')];const toc=[...document.querySelectorAll('.ctoc a')];
const blocks=[];secs.forEach((s,si)=>{const h=s.querySelector('h3.cs');[...s.children].forEach(c=>{if(c.matches('.phead,.pnav,h3.cs'))return;blocks.push({el:c,si,sec:s,h});});});
const chd=cb.querySelector(':scope>.chead');if(chd)chd.remove();const stage=document.createElement('div');stage.className='screens';cb.appendChild(stage);secs.forEach(s=>s.style.display='none');
let screens=[];
function build(){const keep=blocks.map(b=>b.el);stage.innerHTML='';screens=[];
 const H=Math.max(360,window.innerHeight-(window.innerWidth<900?190:210));let cur=null,curSi=-1;
 function newScreen(si,cont){const d=document.createElement('div');d.className='scr';d.dataset.si=si;if(chd)d.appendChild(chd.cloneNode(true));const h=blocks.find(b=>b.si===si).h.cloneNode(true);if(cont)h.classList.add('cont');d.appendChild(h);stage.appendChild(d);screens.push(d);return d;}
 stage.classList.add('measuring');
 blocks.forEach(b=>{if(b.si!==curSi){cur=newScreen(b.si,false);curSi=b.si;}
  cur.appendChild(b.el);if(cur.scrollHeight>H&&cur.children.length>(chd?3:2)){cur.removeChild(b.el);cur=newScreen(b.si,true);cur.appendChild(b.el);}});
 stage.classList.remove('measuring');
 screens.forEach((d,i)=>{const n=document.createElement('nav');n.className='pnav';n.setAttribute('aria-label','Pages du cours');
  n.innerHTML=(i>0?'<button type="button" class="pprev" data-go="'+(i-1)+'">← Précédent</button>':'<span></span>')+'<span class="pnum">Page '+(i+1)+' / '+screens.length+'</span>'+(i<screens.length-1?'<button type="button" class="pnext" data-go="'+(i+1)+'">Suivant →</button>':'<a class="pnext" href="#resume">Résumé et exercices →</a>');d.appendChild(n);});
 toc.forEach(a=>{const si=secs.findIndex(s=>'#'+s.id===a.getAttribute('href'));const k=screens.findIndex(d=>+d.dataset.si===si);a.dataset.go=k;const pg=a.querySelector('.pg');if(pg)pg.textContent='p.'+(k+1);});}
let at=0;function go(k,scroll){k=Math.max(0,Math.min(screens.length-1,k));at=k;screens.forEach((d,i)=>d.classList.toggle('on',i===k));const si=+screens[k].dataset.si;
 toc.forEach(a=>a.classList.toggle('on',+a.dataset.go===screens.findIndex(d=>+d.dataset.si===si)));
 if(scroll){const t=document.getElementById('cours');if(t&&t.getBoundingClientRect().top<0||scroll==='force')t.scrollIntoView({behavior:'smooth',block:'start'});}
 history.replaceState(null,'','#'+secs[si].id);window.dispatchEvent(new Event('resize-sim'));}
build();
document.addEventListener('click',e=>{const a=e.target.closest('[data-go]');if(!a)return;if(!(cb.contains(a)||a.closest('.ctoc')))return;e.preventDefault();go(+a.dataset.go,true);});
const h=location.hash.slice(1);let st=0;const si0=secs.findIndex(s=>s.id===h);if(si0>=0)st=screens.findIndex(d=>+d.dataset.si===si0);
const lab=document.getElementById('lab');if(h==='lab'&&lab){st=screens.findIndex(d=>d.contains(lab));}
go(Math.max(0,st),false);if(h==='lab'&&lab)setTimeout(()=>lab.scrollIntoView(),60);
let rt;window.addEventListener('resize',()=>{clearTimeout(rt);rt=setTimeout(()=>{const el=screens[at]&&screens[at].querySelector(':scope>:not(.chead):not(h3)');build();let k=screens.findIndex(d=>el&&d.contains(el));go(k<0?0:k,false);},300);});
document.addEventListener('keydown',e=>{if(e.target.closest('input,textarea,select'))return;if(e.key==='ArrowRight')go(at+1,true);if(e.key==='ArrowLeft')go(at-1,true);});
let x0=null;cb.addEventListener('touchstart',e=>{x0=e.touches[0].clientX},{passive:true});cb.addEventListener('touchend',e=>{if(x0===null)return;const dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>70&&!e.target.closest('input,.lab,.ctab,.katex-display'))go(at+(dx<0?1:-1),true);x0=null;},{passive:true});})();
document.addEventListener('click',e=>{const o=e.target.closest('.qcm-o button');if(o){const q=o.closest('.qcm');q.querySelectorAll('button').forEach(x=>{x.classList.remove('good','bad');if(x.dataset.ok=='1'&&o.dataset.ok=='1')x.classList.add('good')});o.classList.add(o.dataset.ok=='1'?'good':'bad');const ex=q.querySelector('.qcm-e');if(o.dataset.ok=='1'){ex.hidden=false}else{ex.hidden=true}return;}
const b=e.target.closest('.qa-btn');if(!b)return;const a=b.nextElementSibling;const op=a.hidden;a.hidden=!op;b.setAttribute('aria-expanded',op);b.textContent=op?'Masquer la réponse':'Voir la réponse';});
</script>"""
