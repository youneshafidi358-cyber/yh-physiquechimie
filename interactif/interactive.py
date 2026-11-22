# -*- coding: utf-8 -*-
"""Blocs interactifs des pages de leçon : carte mentale, exercices (énoncé | corrigé), quiz, simulation."""
import json, html, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from content import ERREURS, QUIZ, RESUMES, PROGRAMME
from sims import SIMS
E = html.escape
EXTRACT = json.load(open(os.path.join(os.path.dirname(__file__), "extract.json"), encoding="utf-8"))
COLORS = ["#1f4e9c", "#c0392b", "#2e7d4f", "#8a5a10", "#7a3fa8", "#0e7c86"]

CSS = r"""
.pills{display:flex;gap:8px;flex-wrap:wrap;margin:4px 0 6px;position:sticky;top:0;z-index:6;background:rgba(246,244,239,.96);padding:10px 0;backdrop-filter:blur(6px)}
@media(max-width:640px){.pills{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none}.pills::-webkit-scrollbar{display:none}}
.pills a{white-space:nowrap;text-decoration:none;font-weight:700;font-size:13.5px;padding:7px 13px;border-radius:99px;background:#fff;border:1px solid var(--line)}
.pills a:hover{border-color:var(--blue);color:var(--blue)}
/* Carte mentale */
.mm{position:relative;background:#fff;border:1px solid var(--line);border-radius:18px;padding:22px 16px;overflow:hidden}
.mm svg.wires{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
.mm-grid{position:relative;display:grid;grid-template-columns:1fr minmax(170px,.8fr) 1fr;gap:18px 40px;align-items:center}
.mm-col{display:flex;flex-direction:column;gap:14px}
.mm-center{background:linear-gradient(135deg,#0f2350,#1a3a7c);color:#fff;border-radius:20px;padding:18px 14px;text-align:center;box-shadow:0 10px 26px rgba(15,35,80,.25)}
.mm-center img{width:46px;height:46px;border-radius:50%;border:2px solid var(--gold);background:#fff;margin:0 auto 8px}
.mm-center b{font-family:Fraunces,serif;font-size:19px;display:block;line-height:1.2}
.mm-center small{color:#d4a017;font-size:12px}
.br{border:2px solid var(--c);border-radius:14px;background:#fff;overflow:hidden}
.br>button{all:unset;cursor:pointer;display:flex;align-items:center;gap:8px;width:100%;box-sizing:border-box;padding:9px 12px;background:var(--c);color:#fff;font-weight:700;font-size:14.5px}
.br>button::after{content:"＋";margin-left:auto;font-size:15px}
.br.open>button::after{content:"－"}
.br ul{list-style:none;margin:0;padding:0 10px;max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s}
.br.open ul{max-height:900px;padding:8px 10px 10px}
.br li{font-size:13.5px;padding:4px 0 4px 14px;position:relative;line-height:1.4}
.br li::before{content:"";position:absolute;left:2px;top:11px;width:6px;height:6px;border-radius:50%;background:var(--c)}
.br li b{color:var(--c)}
.br li ul{max-height:none;padding:2px 0 0 4px!important}
.br li li{font-size:13px;color:var(--ink2)}
.mm-tools{display:flex;gap:8px;justify-content:center;margin-top:14px}
.mm-tools button{border:1px solid var(--line);background:#fff;border-radius:99px;padding:6px 12px;font:inherit;font-size:13px;font-weight:600;cursor:pointer}
@media(max-width:820px){.mm-grid{grid-template-columns:1fr;gap:12px}.mm svg.wires{display:none}.mm-center{order:-1}}
/* Exercices : énoncé | corrigé côte à côte */
.ex{background:#fff;border:1px solid var(--line);border-radius:16px;margin-bottom:16px;overflow:hidden}
.ex-h{display:flex;align-items:center;gap:10px;padding:10px 14px;border-bottom:1px solid var(--line);background:#fafbfe;flex-wrap:wrap}
.ex-h b{font-family:Fraunces,serif;font-size:17px;color:var(--navy)}
.ex-h .sp{margin-left:auto;display:flex;gap:6px;flex-wrap:wrap}
.ex-h button{border:1px solid var(--line);background:#fff;border-radius:99px;padding:6px 12px;font:inherit;font-size:13px;font-weight:700;cursor:pointer}
.ex-h button.rep{background:var(--blue);color:#fff;border-color:var(--blue)}
.ex-h button.err{background:#fdecea;color:var(--red);border-color:#f5c6c0}
.ex-b{display:grid;grid-template-columns:1fr 1fr;gap:0}
.ex-b>div{position:relative;padding:10px;min-width:0}
.ex-b .cor{border-left:1px dashed var(--line);background:#f8fbf8}
.ex-b .lbl{font-size:11.5px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:0 0 6px 2px}
.ex-b .cor .lbl{color:var(--green)}
.ex-b img{width:100%;height:auto;display:block;border-radius:8px;-webkit-user-drag:none;user-select:none;pointer-events:none}
.ex-b img+img{margin-top:6px}
.veil{position:absolute;inset:32px 10px 10px;border-radius:10px;background:repeating-linear-gradient(45deg,#eef4ee,#eef4ee 12px,#e4ede4 12px,#e4ede4 24px);display:grid;place-items:center;text-align:center;color:var(--green);font-weight:700;cursor:pointer;padding:12px}
.ex.shown .veil{display:none}
.errbox{display:none;margin:0 14px 12px;background:#fdecea;border-left:4px solid var(--red);border-radius:8px;padding:10px 12px;font-size:14px}
.ex.err .errbox{display:block}
.wmk{position:absolute;inset:0;pointer-events:none;display:flex;align-items:center;justify-content:center;overflow:hidden}
.wmk span{transform:rotate(-25deg);font-family:Fraunces,serif;font-size:22px;color:rgba(31,78,156,.09);white-space:nowrap;font-weight:700}
@media(max-width:820px){.ex-b{grid-template-columns:1fr}.ex-b .cor{border-left:0;border-top:1px dashed var(--line)}}
/* Quiz */
.qz{background:#fff;border:1px solid var(--line);border-radius:16px;padding:16px}
.qz .q{margin-bottom:16px}.qz .q p{font-weight:700;margin:0 0 8px}
.qz .opts{display:grid;gap:6px}
.qz .opts button{text-align:left;border:1px solid var(--line);background:#fafbfe;border-radius:10px;padding:9px 12px;font:inherit;cursor:pointer}
.qz .opts button.good{background:#e5f3ea;border-color:#2e7d4f;color:#1d5c37;font-weight:700}
.qz .opts button.bad{background:#fdecea;border-color:#c0392b;color:#8f2a20}
.qz .ex2{display:none;font-size:13.5px;color:var(--ink2);margin-top:6px;background:var(--blue-soft);border-radius:8px;padding:7px 10px}
.qz .q.done .ex2{display:block}
.qz .score{font-family:Fraunces,serif;font-size:20px;color:var(--navy);text-align:center;padding:8px;border-top:1px solid var(--line)}
/* Bloc simulation */
.simcard{display:flex;gap:14px;align-items:center;background:linear-gradient(135deg,#0f2350,#1a3a7c);color:#fff;border-radius:16px;padding:16px;text-decoration:none}
.simcard .ic{font-size:34px}.simcard b{font-family:Fraunces,serif;font-size:18px;display:block}.simcard span{color:#c9d5ef;font-size:13.5px}
.simcard .go2{margin-left:auto;background:var(--gold);color:#2b1f00;font-weight:800;padding:9px 14px;border-radius:12px;white-space:nowrap}
"""

JS = r"""
<script>
(function(){
 // Carte mentale : ouvrir/fermer + fils
 document.querySelectorAll('.br>button').forEach(b=>b.onclick=()=>{b.parentElement.classList.toggle('open');setTimeout(wires,380)});
 const all=document.getElementById('mmAll'), none=document.getElementById('mmNone');
 if(all) all.onclick=()=>{document.querySelectorAll('.br').forEach(x=>x.classList.add('open'));setTimeout(wires,380)};
 if(none) none.onclick=()=>{document.querySelectorAll('.br').forEach(x=>x.classList.remove('open'));setTimeout(wires,380)};
 function wires(){ const mm=document.querySelector('.mm'); if(!mm) return; const sv=mm.querySelector('svg.wires'); const c=mm.querySelector('.mm-center'); if(!sv||!c) return;
  const R=mm.getBoundingClientRect(), cr=c.getBoundingClientRect(); let h='';
  mm.querySelectorAll('.br').forEach(b=>{ const r=b.getBoundingClientRect(); const left=r.right<cr.left;
   const x1=(left?cr.left:cr.right)-R.left, y1=cr.top+cr.height/2-R.top, x2=(left?r.right:r.left)-R.left, y2=r.top+18-R.top, mx=(x1+x2)/2;
   h+=`<path d="M${x1} ${y1} C${mx} ${y1} ${mx} ${y2} ${x2} ${y2}" fill="none" stroke="${getComputedStyle(b).getPropertyValue('--c')}" stroke-width="3" opacity=".55"/>`; });
  sv.innerHTML=h; }
 addEventListener('resize',wires); addEventListener('load',wires); setTimeout(wires,300);
 // Exercices
 document.querySelectorAll('.ex').forEach(ex=>{
  const r=ex.querySelector('.rep'), e=ex.querySelector('.err'), v=ex.querySelector('.veil');
  const show=()=>{ex.classList.toggle('shown'); r.textContent=ex.classList.contains('shown')?'Masquer la réponse':'Voir la réponse'; try{gtag('event','voir_reponse',{lecon:document.title,exercice:ex.dataset.n})}catch(x){}};
  if(r) r.onclick=show; if(v) v.onclick=show;
  if(e) e.onclick=()=>{ex.classList.toggle('err'); try{gtag('event','erreur_frequente',{lecon:document.title,exercice:ex.dataset.n})}catch(x){}};
 });
 const sa=document.getElementById('showAll'); if(sa) sa.onclick=()=>{const on=sa.dataset.on!=='1'; sa.dataset.on=on?'1':'0'; sa.textContent=on?'Masquer toutes les réponses':'Afficher toutes les réponses';
  document.querySelectorAll('.ex').forEach(x=>{x.classList.toggle('shown',on); const r=x.querySelector('.rep'); if(r) r.textContent=on?'Masquer la réponse':'Voir la réponse';})};
 // Quiz
 const qs=document.querySelectorAll('.qz .q'); let ok=0, done=0;
 qs.forEach(q=>{ const good=+q.dataset.a; q.querySelectorAll('.opts button').forEach((b,i)=>b.onclick=()=>{ if(q.classList.contains('done')) return; q.classList.add('done'); done++;
   if(i===good){ b.classList.add('good'); ok++; } else { b.classList.add('bad'); q.querySelectorAll('.opts button')[good].classList.add('good'); }
   const s=document.getElementById('qscore'); s.textContent='Score : '+ok+' / '+qs.length+(done===qs.length?(ok===qs.length?' — Parfait ! 🎉':ok>=qs.length/2?' — Bien, continue !':' — Relis le résumé et réessaie.'):'');
   if(done===qs.length){ try{gtag('event','quiz_termine',{lecon:document.title,score:ok})}catch(x){} } }); });
 const rq=document.getElementById('qreset'); if(rq) rq.onclick=()=>{ ok=0;done=0; qs.forEach(q=>{q.classList.remove('done');q.querySelectorAll('button').forEach(b=>b.classList.remove('good','bad'))}); document.getElementById('qscore').textContent='Score : 0 / '+qs.length; };
 ['contextmenu','dragstart'].forEach(ev=>document.addEventListener(ev,e=>{ if(e.target.closest('.ex-b')) e.preventDefault(); }));
})();
</script>"""


def _items(lst):
    h = ""
    for it in lst:
        if isinstance(it, tuple):
            h += f"<li><b>{E(it[0])}</b><ul>" + "".join(f"<li>{E(x)}</li>" for x in it[1]) + "</ul></li>"
        else:
            h += f"<li>{E(it)}</li>"
    return h


def resume_html(unite, lv_short):
    R = RESUMES.get(unite)
    if not R:
        return ""
    brs = []
    for i, (t, items) in enumerate(R):
        c = COLORS[i % len(COLORS)]
        brs.append(f'<div class="br{" open" if i == 0 else ""}" style="--c:{c}"><button type="button">{E(t)}</button><ul>{_items(items)}</ul></div>')
    left, right = brs[0::2], brs[1::2]
    return f"""<div class="mm"><svg class="wires"></svg><div class="mm-grid">
<div class="mm-col">{''.join(left)}</div>
<div class="mm-center"><img src="/logo.jpg" alt=""><b>{E(unite)}</b><small>Résumé · {lv_short}</small></div>
<div class="mm-col">{''.join(right)}</div></div>
<div class="mm-tools"><button type="button" id="mmAll">Tout ouvrir</button><button type="button" id="mmNone">Tout fermer</button></div></div>"""


def exercices_html(niv, unite):
    X = EXTRACT.get(f"{niv}|{unite}")
    if not X or not X["serie"]:
        return ""
    cor = {e["n"]: e["imgs"] for e in X["corrige"]}
    errs = ERREURS.get(unite, {})
    out = ['<p class="tip" style="margin:0 0 10px">Cherche d\'abord seul, puis clique sur <b>Voir la réponse</b> : la correction s\'affiche à côté de l\'énoncé. <button type="button" id="showAll" class="btn" style="padding:5px 10px;font-size:13px;margin-left:6px">Afficher toutes les réponses</button></p>']
    for e in sorted(X["serie"], key=lambda e: e["n"]):
        n = e["n"]
        en = "".join(f'<img loading="lazy" src="/exos/{f}" alt="Énoncé de l\'exercice {n}" draggable="false">' for f in e["imgs"])
        co = "".join(f'<img loading="lazy" src="/exos/{f}" alt="Correction de l\'exercice {n}" draggable="false">' for f in cor.get(n, []))
        err = errs.get(n)
        out.append(f"""<div class="ex" data-n="{n}"><div class="ex-h"><b>Exercice {n}</b><div class="sp">
{'<button type="button" class="rep">Voir la réponse</button>' if co else ''}{'<button type="button" class="err">⚠ Erreur fréquente</button>' if err else ''}</div></div>
<div class="errbox"><b>Erreur fréquente :</b> {E(err or '')}</div>
<div class="ex-b"><div><div class="lbl">Énoncé</div>{en}<div class="wmk" aria-hidden="true"><span>Pr. Youness HAFIDI</span></div></div>
<div class="cor"><div class="lbl">Correction</div>{co or '<p class="tip">Correction bientôt disponible.</p>'}{'<div class="veil">🔒 Essaie d’abord seul…<br>puis touche ici pour voir la correction</div>' if co else ''}<div class="wmk" aria-hidden="true"><span>Pr. Youness HAFIDI</span></div></div></div></div>""")
    return "\n".join(out)


def quiz_html(unite):
    Q = QUIZ.get(unite)
    if not Q:
        return ""
    h = '<div class="qz">'
    for i, (q, opts, a, ex) in enumerate(Q):
        h += f'<div class="q" data-a="{a}"><p>{i+1}. {E(q)}</p><div class="opts">' + "".join(f'<button type="button">{E(o)}</button>' for o in opts) + f'</div><div class="ex2">💡 {E(ex)}</div></div>'
    h += f'<div class="score" id="qscore">Score : 0 / {len(Q)}</div><div style="text-align:center"><button type="button" id="qreset" class="btn">Recommencer</button></div></div>'
    return h


def sim_for(unite):
    return next((s for s in SIMS if s["lesson"] == unite), None)


def sim_card(unite):
    s = sim_for(unite)
    if not s:
        return ""
    return f"""<a class="simcard" href="/simulations/{s['slug']}/" data-ev="ouverture_simulation" data-t="{E(s['title'])}"><div class="ic">🧪</div>
<div><b>{E(s['title'])}</b><span>{E(s['intro'])}</span></div><div class="go2">Ouvrir le labo →</div></a>"""


def order_of(niv, unite):
    p = PROGRAMME.get(niv, [])
    if unite in p:
        return p.index(unite) + 1
    if unite.startswith("Contrôles"):
        return 90
    return 50
