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

def render(unite, sim_html=""):
    """Renvoie (sommaire, corps) ou ('','') si pas de cours."""
    if unite not in COURS:
        return "", ""
    secs, trad = COURS[unite]
    toc, body, placed = [], [], False
    for num, title, html in secs:
        sid = "c-" + _slug(title)[:40]
        lab = f"{num}. {title}" if num else title
        toc.append(f'<li><a href="#{sid}">{E(lab)}</a></li>')
        if "%%SIM%%" in html:
            html = html.replace("%%SIM%%", sim_html, 1); placed = True
        body.append(f'<section class="csec" id="{sid}"><h3 class="cs"><span>{E(num)}</span>{E(title)}</h3>{html}</section>')
    if sim_html and not placed:
        body.append(sim_html)
    if False and trad:
        toc.append('<li><a href="#c-traduction">Traduction</a></li>')
        body.append(f'<section class="csec" id="c-traduction"><h3 class="cs"><span>🌐</span>Traduction <span lang="ar" dir="rtl" style="background:none;color:inherit;margin:0 6px;min-width:0">الترجمة</span></h3>{TRAD(trad)}</section>')
    return "<ol>" + "".join(toc) + "</ol>", "".join(body)

CSS = r"""
.wrap{max-width:1400px}
.coursewrap{display:grid;grid-template-columns:230px minmax(0,1fr);gap:20px;align-items:start}
.ctoc{position:sticky;top:76px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:12px 12px 8px;font-size:14px;max-height:calc(100vh - 100px);overflow:auto}
.ctoc b{display:block;color:#0f2350;margin-bottom:6px}
.ctoc ol{margin:0;padding-left:0;list-style:none}.ctoc li{margin:0 0 4px}
.ctoc a{display:block;padding:6px 8px;border-radius:8px;color:#334;text-decoration:none;line-height:1.3}
.ctoc a:hover,.ctoc a.on{background:#eef3fc;color:#123c8c;font-weight:600}
.cbody{min-width:0;overflow-wrap:break-word;background:#fff;border:1px solid var(--line);border-radius:16px;padding:8px 22px 18px;line-height:1.65;font-size:16.5px}
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

JS = r"""
<link rel="stylesheet" href="/js/katex/katex.min.css">
<script defer src="/js/katex/katex.min.js"></script>
<script defer src="/js/katex/auto-render.min.js" onload="renderMathInElement(document.querySelector('.cbody')||document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false});document.querySelectorAll('.katex-display').forEach(e=>{if(e.scrollWidth>e.clientWidth){e.tabIndex=0}})"></script>
<script>
document.addEventListener('click',e=>{const o=e.target.closest('.qcm-o button');if(o){const q=o.closest('.qcm');q.querySelectorAll('button').forEach(x=>{x.classList.remove('good','bad');if(x.dataset.ok=='1'&&o.dataset.ok=='1')x.classList.add('good')});o.classList.add(o.dataset.ok=='1'?'good':'bad');const ex=q.querySelector('.qcm-e');if(o.dataset.ok=='1'){ex.hidden=false}else{ex.hidden=true}return;}
const b=e.target.closest('.qa-btn');if(!b)return;const a=b.nextElementSibling;const op=a.hidden;a.hidden=!op;b.setAttribute('aria-expanded',op);b.textContent=op?'Masquer la réponse':'Voir la réponse';});
(()=>{const ls=[...document.querySelectorAll('.ctoc a')];if(!ls.length||!('IntersectionObserver' in window))return;
const io=new IntersectionObserver(es=>{es.forEach(x=>{if(x.isIntersecting){ls.forEach(a=>a.classList.toggle('on',a.getAttribute('href')=='#'+x.target.id));}})},{rootMargin:'-30% 0px -60% 0px'});
document.querySelectorAll('.csec').forEach(s=>io.observe(s));})();
</script>"""
