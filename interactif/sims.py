# -*- coding: utf-8 -*-
"""Simulations interactives YH Physique-Chimie (une page autonome par simulation)."""

SIM_CSS = r"""
.lab{background:#fff;border:1px solid var(--line);border-radius:16px;overflow:hidden;box-shadow:0 6px 24px rgba(20,33,61,.06)}
.labhead{display:flex;align-items:center;gap:10px;background:linear-gradient(135deg,#0f2350,#1a3a7c);color:#fff;padding:10px 14px}
.labhead img{width:34px;height:34px;border-radius:50%;border:2px solid #d4a017;background:#fff}
.labhead b{font-family:Fraunces,serif;font-size:16px}.labhead span{font-size:12px;color:#c9d5ef;display:block}
.labhead .sig{margin-left:auto;font-size:11.5px;color:#d4a017;text-align:right}
.labbody{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:0}
.scene{background:#f4f7fc;position:relative;min-height:300px;border-right:1px solid var(--line)}
.scene svg{width:100%;height:auto;display:block}
.ctrl{padding:14px 16px;display:flex;flex-direction:column;gap:12px}
.ctrl[hidden]{display:none}
.ctrl label{font-size:13px;font-weight:600;color:var(--ink2);display:flex;justify-content:space-between;gap:8px}
.ctrl label b{color:var(--blue);font-variant-numeric:tabular-nums}
.ctrl input[type=range]{width:100%;accent-color:#1f4e9c}
.ctrl select{border:1px solid var(--line);border-radius:10px;padding:8px;background:#fff;font:inherit}
.res{background:#0f2350;color:#fff;border-radius:12px;padding:10px 12px;font-size:14px;line-height:1.6}
.res .big{font-family:Fraunces,serif;font-size:22px;color:#ffd666}
.res small{color:#c9d5ef}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chips button,.bt{border:1px solid var(--line);background:#fff;border-radius:99px;padding:7px 12px;font:inherit;font-size:13.5px;font-weight:600;cursor:pointer}
.chips button[aria-pressed=true]{background:#1f4e9c;color:#fff;border-color:#1f4e9c}
.bt.pri{background:#d4a017;border-color:#d4a017;color:#2b1f00}
.note{font-size:13px;color:var(--muted);background:var(--gold-soft);border-radius:10px;padding:8px 10px}
.tabs{display:flex;gap:6px;padding:10px 14px;border-bottom:1px solid var(--line);background:#fafbfe;flex-wrap:wrap}
.ok{color:#2e7d4f;font-weight:700}.ko{color:#c0392b;font-weight:700}
@media(max-width:760px){.labbody{grid-template-columns:1fr}.scene{border-right:0;border-bottom:1px solid var(--line)}}
"""

SIM_COMMON_JS = r"""
const $=s=>document.querySelector(s);
function sci(x,d=3){ if(x===0) return "0"; const e=Math.floor(Math.log10(Math.abs(x))); const m=x/Math.pow(10,e);
  if(e>=-2&&e<=4) return (+x.toPrecision(d)).toLocaleString('fr-FR');
  return m.toFixed(d-1).replace('.',',')+" × 10<sup>"+e+"</sup>"; }
function fr(x,d=2){ return (+x.toFixed(d)).toLocaleString('fr-FR'); }
function bind(id,cb){ const el=$(id); el.addEventListener('input',cb); return el; }
function ns(t,a){ const e=document.createElementNS('http://www.w3.org/2000/svg',t); for(const k in a) e.setAttribute(k,a[k]); return e; }
"""

SIMS = []

def sim(slug, lesson, niv, title, intro, body, js):
    SIMS.append(dict(slug=slug, lesson=lesson, niv=niv, title=title, intro=intro, body=body, js=js))

# ---------------------------------------------------------------- 1. Air / seringue
sim("compressibilite-air", "L'air qui nous entoure", "2ac", "Compressibilité et expansibilité de l'air",
 "Pousse ou tire le piston de la seringue bouchée : observe les molécules et la pression.",
 """<div class="scene"><svg id="sv" viewBox="0 0 560 300"></svg></div>
<div class="ctrl">
 <label>Volume de l'air <b id="vV">60 mL</b></label><input id="V" type="range" min="15" max="100" value="60">
 <div class="res">Pression : <span class="big" id="vP">1013 hPa</span><br><small id="vT"></small></div>
 <div class="note">💡 Le nombre et la taille des molécules ne changent pas : seule la distance entre elles change.</div>
 <div class="chips"><button class="bt" id="b1">Comprimer</button><button class="bt" id="b2">Détendre</button></div>
</div>""",
 r"""
const sv=$('#sv'); const V0=60,P0=1013; const N=34; let mol=[];
for(let i=0;i<N;i++) mol.push({x:Math.random(),y:Math.random(),vx:(Math.random()-.5)*.012,vy:(Math.random()-.5)*.012,o:i<Math.round(N*.22)});
function draw(){ const V=+$('#V').value; const x0=60,x1=60+V*4,y0=95,y1=205;
 sv.innerHTML='';
 sv.append(ns('rect',{x:40,y:85,width:440,height:130,rx:10,fill:'#e8eef8',stroke:'#1a3a7c','stroke-width':3}));
 sv.append(ns('rect',{x:20,y:135,width:22,height:30,fill:'#1a3a7c',rx:4}));
 sv.append(ns('rect',{x:x1,y:88,width:14,height:124,fill:'#d4a017',rx:3}));
 sv.append(ns('rect',{x:x1+14,y:143,width:520-x1,height:14,fill:'#9aa7c0'}));
 sv.append(ns('rect',{x:530,y:120,width:14,height:60,rx:4,fill:'#9aa7c0'}));
 for(let k=0;k<=10;k++){ const gx=60+k*40; sv.append(ns('line',{x1:gx,y1:85,x2:gx,y2:95,stroke:'#1a3a7c'})); const t=ns('text',{x:gx,y:78,'font-size':11,'text-anchor':'middle',fill:'#1a3a7c'}); t.textContent=k*10; sv.append(t); }
 mol.forEach(m=>{ m.x+=m.vx*(60/V); m.y+=m.vy; if(m.x<0||m.x>1) m.vx*=-1; if(m.y<0||m.y>1) m.vy*=-1; m.x=Math.min(1,Math.max(0,m.x)); m.y=Math.min(1,Math.max(0,m.y));
   const cx=x0+8+m.x*(x1-x0-16), cy=y0+8+m.y*(y1-y0-16);
   const c=m.o?'#d93b3b':'#2f6fb8'; sv.append(ns('circle',{cx:cx-4,cy,r:5,fill:c})); sv.append(ns('circle',{cx:cx+4,cy,r:5,fill:c})); });
 const lg=ns('text',{x:40,y:250,'font-size':13,fill:'#14213d'}); lg.innerHTML='<tspan fill="#2f6fb8">●● N₂ (≈78 %)</tspan>   <tspan fill="#d93b3b">●● O₂ (≈21 %)</tspan>'; sv.append(lg);
 const P=P0*V0/V; $('#vV').textContent=V+' mL'; $('#vP').textContent=Math.round(P)+' hPa';
 $('#vT').textContent = V<V0? 'Compression : le volume diminue → la pression augmente (compressibilité).' : V>V0? 'Détente : le volume augmente → la pression diminue (expansibilité).' : 'État initial : pression atmosphérique.';
 requestAnimationFrame(draw); }
$('#b1').onclick=()=>{$('#V').value=Math.max(15,+$('#V').value-15)}; $('#b2').onclick=()=>{$('#V').value=Math.min(100,+$('#V').value+15)};
draw();
""")

# ---------------------------------------------------------------- 2. Molécules
sim("construire-molecules", "Les molécules et les atomes", "2ac", "Construis une molécule",
 "Ajoute des atomes pour former une molécule : sa formule, son nombre d'atomes et son type s'affichent.",
 """<div class="scene"><svg id="sv" viewBox="0 0 560 300"></svg></div>
<div class="ctrl" id="ct"></div>""",
 r"""
const A=[['C','carbone','#222'],['H','hydrogène','#fff'],['O','oxygène','#d93b3b'],['N','azote','#2f6fb8']];
const n={C:0,H:0,O:0,N:0};
const KNOWN={'H2O':'Eau','CO2':'Dioxyde de carbone','CH4':'Méthane','O2':'Dioxygène','N2':'Diazote','H2':'Dihydrogène','NH3':'Ammoniac','CO':'Monoxyde de carbone','O3':'Ozone','C4H10':'Butane','C3H8':'Propane','C2H6O':'Éthanol','C6H12':'Cyclohexane','C2H6':'Éthane'};
const ct=$('#ct');
A.forEach(([s,nm])=>{ const l=document.createElement('label'); l.innerHTML=nm+' ('+s+') <b id="c'+s+'">0</b>'; const d=document.createElement('div'); d.className='chips';
 const m=document.createElement('button'); m.className='bt'; m.textContent='− '+s; m.onclick=()=>{n[s]=Math.max(0,n[s]-1);up()};
 const p=document.createElement('button'); p.className='bt pri'; p.textContent='+ '+s; p.onclick=()=>{n[s]=Math.min(12,n[s]+1);up()};
 d.append(m,p); ct.append(l,d); });
const r=document.createElement('div'); r.className='res'; r.id='rs'; ct.append(r);
const ex=document.createElement('div'); ex.className='chips'; ct.append(ex);
[['H2O',{H:2,O:1}],['CO2',{C:1,O:2}],['CH4',{C:1,H:4}],['NH3',{N:1,H:3}],['C4H10',{C:4,H:10}]].forEach(([f,c])=>{const b=document.createElement('button');b.textContent=f.replace(/(\d+)/g,'<sub>$1</sub>');b.innerHTML=f.replace(/(\d+)/g,'<sub>$1</sub>');b.onclick=()=>{Object.keys(n).forEach(k=>n[k]=c[k]||0);up()};ex.append(b)});
function up(){ const sv=$('#sv'); sv.innerHTML=''; let f='',fh='';
 ['C','H','N','O'].forEach(s=>{ if(n[s]){ f+=s+(n[s]>1?n[s]:''); fh+=s+(n[s]>1?'<sub>'+n[s]+'</sub>':''); } });
 if(n.C===0&&f){ f='';fh=''; ['H','N','O'].forEach(s=>{ if(n[s]){ f+=s+(n[s]>1?n[s]:''); fh+=s+(n[s]>1?'<sub>'+n[s]+'</sub>':''); } }); }
 const tot=n.C+n.H+n.O+n.N; const sorts=Object.values(n).filter(v=>v>0).length;
 Object.keys(n).forEach(k=>$('#c'+k).textContent=n[k]);
 // dessin
 let i=0; const cols={C:'#222',H:'#f2f2f2',O:'#d93b3b',N:'#2f6fb8'}, rad={C:22,H:14,O:20,N:20};
 const order=[]; ['C','N','O','H'].forEach(s=>{for(let k=0;k<n[s];k++) order.push(s)});
 const cx=280,cy=140; order.forEach((s,k)=>{ const ang=k*2.399, rr= k===0?0: 26+10*Math.sqrt(k)*2.2;
   const x=cx+Math.cos(ang)*rr, y=cy+Math.sin(ang)*rr*0.8; sv.append(ns('circle',{cx:x,cy:y,r:rad[s],fill:cols[s],stroke:'#14213d','stroke-width':1.5})); });
 let txt, name=KNOWN[f];
 if(!tot) txt='Ajoute des atomes →';
 else if(tot===1) txt='<span class="big">'+fh+'</span><br>Un seul atome : ce n\'est pas une molécule.';
 else txt='Formule : <span class="big">'+fh+'</span>'+(name?' — <b>'+name+'</b>':'')+'<br>Nombre total d\'atomes : <b>'+tot+'</b><br>Corps pur <b>'+(sorts===1?'simple':'composé')+'</b> ('+sorts+' sorte'+(sorts>1?'s':'')+' d\'atomes)';
 $('#rs').innerHTML=txt; }
up();
""")

# ---------------------------------------------------------------- 3. Bec Bunsen
sim("bec-bunsen", "Les combustions", "2ac", "La combustion du butane – bec Bunsen",
 "Ouvre ou ferme la virole : la quantité d'air change la flamme et les produits de la combustion.",
 """<div class="scene"><svg id="sv" viewBox="0 0 560 320"></svg></div>
<div class="ctrl">
 <label>Ouverture de la virole (arrivée d'air) <b id="vA">80 %</b></label><input id="A" type="range" min="0" max="100" value="80">
 <div class="res" id="rs"></div>
 <div class="chips"><button class="bt" id="tc">Tester avec l'eau de chaux</button><button class="bt" id="tv">Approcher une vitre froide</button><button class="bt" id="ts">Approcher une soucoupe</button></div>
 <div class="note" id="obs">Choisis un test pour identifier les produits.</div>
</div>""",
 r"""
let t=0; function draw(){ t+=0.08; const a=+$('#A').value; const sv=$('#sv'); sv.innerHTML='';
 const comp=a>=55; const h=120+ (100-a)*0.9;
 sv.append(ns('rect',{x:250,y:220,width:60,height:80,fill:'#7d8aa5',rx:4}));
 sv.append(ns('rect',{x:240,y:295,width:80,height:12,fill:'#4a5670',rx:3}));
 sv.append(ns('rect',{x:244,y:250,width:72,height:18,fill:'#d4a017',rx:3}));
 sv.append(ns('rect',{x:244+72*(a/100)*0.5,y:254,width:18,height:10,fill:'#14213d',rx:2,opacity:.8}));
 const w=26+Math.sin(t)*2; const top=220-h;
 const outer=comp?'#5b8cff':'#ffb020', inner=comp?'#1f3fd6':'#ffe27a';
 sv.append(ns('path',{d:`M${280-w} 220 Q${280-w-10} ${220-h*0.5} 280 ${top} Q${280+w+10} ${220-h*0.5} ${280+w} 220 Z`,fill:outer,opacity:.85}));
 sv.append(ns('path',{d:`M${280-w*0.45} 220 Q280 ${220-h*0.55} 280 ${220-h*0.6} Q280 ${220-h*0.55} ${280+w*0.45} 220 Z`,fill:inner,opacity:.9}));
 if(!comp){ for(let k=0;k<6;k++){ sv.append(ns('circle',{cx:280+Math.sin(t*1.3+k)*14,cy:top-10-((t*20+k*18)%70),r:5+k%3,fill:'#333',opacity:.35})); } }
 const lab=ns('text',{x:345,y:250,'font-size':13,fill:'#14213d'}); lab.textContent='virole'; sv.append(lab);
 $('#vA').textContent=a+' %';
 $('#rs').innerHTML = comp
  ? 'Flamme <b>bleue</b> : combustion <span class="big">complète</span><br>Butane + Dioxygène → <b>Dioxyde de carbone + Eau</b>'
  : 'Flamme <b>jaune</b> : combustion <span class="big">incomplète</span><br>Butane + Dioxygène → Dioxyde de carbone + Eau + <b>Carbone</b> (fumée noire) + <b>Monoxyde de carbone</b> ⚠️ toxique';
 requestAnimationFrame(draw); }
$('#tc').onclick=()=>$('#obs').innerHTML='L\'eau de chaux <b>se trouble</b> ⇒ il se forme du <b>dioxyde de carbone CO₂</b>.';
$('#tv').onclick=()=>$('#obs').innerHTML='De la <b>buée</b> apparaît sur la vitre ⇒ il se forme de l\'<b>eau</b>.';
$('#ts').onclick=()=>$('#obs').innerHTML= +$('#A').value>=55 ? 'La soucoupe reste <b>propre</b> : pas de carbone (combustion complète).' : 'Un <b>dépôt noir</b> se forme ⇒ il se forme du <b>carbone</b> (combustion incomplète).';
draw();
""")

# ---------------------------------------------------------------- 4. Matériaux
sim("identifier-materiaux", "Les matériaux dans la vie quotidienne", "3ac", "Enquête : identifie le matériau",
 "Un échantillon mystère t'est donné. Réalise des tests, puis propose ta réponse.",
 """<div class="scene"><svg id="sv" viewBox="0 0 560 300"></svg></div>
<div class="ctrl">
 <div class="chips" id="tests"></div>
 <div class="note" id="obs">Choisis un test.</div>
 <label>Ta réponse</label><select id="rep"></select>
 <div class="chips"><button class="bt pri" id="val">Valider</button><button class="bt" id="new">Nouvel échantillon</button></div>
 <div class="res" id="rs">Échantillon n°1</div>
</div>""",
 r"""
const M={
 'Fer':{col:'#8a8f98',fam:'métal',aim:1,cond:1,douce:0,salee:0,fl:'—',ac:0},
 'Cuivre':{col:'#b8643a',fam:'métal',aim:0,cond:1,douce:0,salee:0,fl:'—',ac:0},
 'Aluminium':{col:'#c9ced6',fam:'métal',aim:0,cond:1,douce:0,salee:0,fl:'—',ac:0},
 'Polyéthylène (PE)':{col:'#eef3e8',fam:'plastique',aim:0,cond:0,douce:1,salee:1,fl:'jaune',ac:0},
 'Polystyrène (PS)':{col:'#f4f4f4',fam:'plastique',aim:0,cond:0,douce:0,salee:1,fl:'jaune, fumée noire',ac:1},
 'PVC':{col:'#9fb7c9',fam:'plastique',aim:0,cond:0,douce:0,salee:0,fl:'verte',ac:0},
 'Verre':{col:'#bfe3e6',fam:'verre',aim:0,cond:0,douce:0,salee:0,fl:'—',ac:0}};
const K=Object.keys(M); let cur, n=0, score=0;
K.forEach(k=>{const o=document.createElement('option');o.textContent=k;$('#rep').append(o)});
const T=[['Aimant',m=>m.aim?'L\'aimant <b>attire</b> l\'échantillon.':'L\'aimant <b>n\'attire pas</b> l\'échantillon.'],
 ['Circuit électrique',m=>m.cond?'La lampe <b>brille</b> : conducteur électrique.':'La lampe <b>reste éteinte</b> : isolant électrique.'],
 ['Couleur',m=>'Couleur observée : voir le dessin.'],
 ['Eau douce',m=>m.douce?'L\'échantillon <b>flotte</b> dans l\'eau douce.':'L\'échantillon <b>coule</b> dans l\'eau douce.'],
 ['Eau salée',m=>m.salee?'L\'échantillon <b>flotte</b> dans l\'eau salée.':'L\'échantillon <b>coule</b> dans l\'eau salée.'],
 ['Fil de cuivre chauffé',m=>m.fam!=='plastique'?'Test réservé aux plastiques : rien de particulier.':'Flamme <b>'+m.fl+'</b>.'],
 ['Acétone',m=>m.ac?'L\'échantillon <b>se dissout</b> dans l\'acétone.':'Rien ne se passe dans l\'acétone.']];
T.forEach(([nm,f])=>{const b=document.createElement('button');b.textContent=nm;b.onclick=()=>{ $('#obs').innerHTML=f(M[cur]); draw(nm)};$('#tests').append(b)});
function draw(test){ const m=M[cur],sv=$('#sv'); sv.innerHTML='';
 sv.append(ns('rect',{x:0,y:250,width:560,height:50,fill:'#e4dfd3'}));
 if(test==='Eau douce'||test==='Eau salée'){ const fl=test==='Eau douce'?m.douce:m.salee;
   sv.append(ns('rect',{x:190,y:90,width:180,height:160,fill:test==='Eau douce'?'#cfe6ff':'#d7f1ec',stroke:'#1a3a7c','stroke-width':3}));
   sv.append(ns('rect',{x:255,y:fl?80:215,width:50,height:30,fill:m.col,stroke:'#333'})); }
 else { sv.append(ns('rect',{x:230,y:170,width:100,height:80,fill:m.col,stroke:'#333','stroke-width':2,rx:6}));
   const q=ns('text',{x:280,y:218,'font-size':30,'text-anchor':'middle',fill:'#14213d'}); q.textContent='?'; sv.append(q);
   if(test==='Aimant'){ sv.append(ns('path',{d:'M250 60 v60 h20 v-40 h20 v40 h20 v-60 z',fill:'#c0392b'})); }
   if(test==='Fil de cuivre chauffé'&&m.fam==='plastique'){ sv.append(ns('ellipse',{cx:400,cy:150,rx:18,ry:40,fill:m.fl==='verte'?'#3fbf5a':'#ffb020'})); }
   if(test==='Circuit électrique'){ sv.append(ns('circle',{cx:280,cy:80,r:22,fill:m.cond?'#ffe27a':'#ddd',stroke:'#333'})); sv.append(ns('path',{d:'M258 80 H180 V210 H230 M302 80 H380 V210 H330',fill:'none',stroke:'#333','stroke-width':3})); } }
}
function nouveau(){ cur=K[Math.floor(Math.random()*K.length)]; n++; $('#rs').innerHTML='Échantillon n°'+n+' · score '+score+'/'+(n-1); $('#obs').textContent='Choisis un test.'; draw(); }
$('#val').onclick=()=>{ const ok=$('#rep').value===cur; if(ok) score++; $('#rs').innerHTML=(ok?'<span class="ok">Bravo !</span> ':'<span class="ko">Non…</span> ')+'C\'était : <b>'+cur+'</b> (famille des '+M[cur].fam+'s)<br><small>Score : '+score+'/'+n+'</small>'; };
$('#new').onclick=nouveau; nouveau();
""")

# ---------------------------------------------------------------- 5. Atome / ion
sim("atome-et-ion", "Les atomes et les ions", "3ac", "De l'atome à l'ion",
 "Choisis un atome, puis ajoute ou retire des électrons : observe les charges et la formule de l'ion.",
 """<div class="scene"><svg id="sv" viewBox="0 0 560 320"></svg></div>
<div class="ctrl">
 <label>Atome</label><select id="el"></select>
 <div class="chips"><button class="bt" id="m">− retirer un électron</button><button class="bt pri" id="p">+ ajouter un électron</button><button class="bt" id="r">Atome neutre</button></div>
 <div class="res" id="rs"></div>
 <div class="note">e = 1,6 × 10⁻¹⁹ C · Le noyau ne change pas : seul le nombre d'électrons varie.</div>
</div>""",
 r"""
const E=[['H',1,'hydrogène'],['C',6,'carbone'],['N',7,'azote'],['O',8,'oxygène'],['F',9,'fluor'],['Na',11,'sodium'],['Mg',12,'magnésium'],['Al',13,'aluminium'],['S',16,'soufre'],['Cl',17,'chlore'],['K',19,'potassium'],['Ca',20,'calcium'],['Fe',26,'fer'],['Cu',29,'cuivre'],['Zn',30,'zinc']];
E.forEach((e,i)=>{const o=document.createElement('option');o.value=i;o.textContent=e[2]+' ('+e[0]+', Z = '+e[1]+')';$('#el').append(o)}); $('#el').value=5;
let ne; let t=0;
function reset(){ ne=E[$('#el').value][1]; } reset();
$('#el').onchange=reset; $('#m').onclick=()=>{ne=Math.max(0,ne-1)}; $('#p').onclick=()=>{ne=Math.min(E[$('#el').value][1]+3,ne+1)}; $('#r').onclick=reset;
function sup(q){ if(q===0) return ''; const a=Math.abs(q); return (a>1?a:'')+(q>0?'+':'−'); }
function draw(){ t+=0.01; const [s,Z,nm]=E[$('#el').value]; const sv=$('#sv'); sv.innerHTML='';
 const cx=280,cy=160; sv.append(ns('circle',{cx,cy,r:130,fill:'#e8effb',opacity:.7}));
 sv.append(ns('circle',{cx,cy,r:26,fill:'#c0392b'})); const tn=ns('text',{x:cx,y:cy+5,'text-anchor':'middle','font-size':14,fill:'#fff','font-weight':700}); tn.textContent='+'+Z+'e'; sv.append(tn);
 for(let k=0;k<ne;k++){ const sh=k<2?55:k<10?90:120; const per=k<2?2:k<10?8:Math.max(1,ne-10); const idx=k<2?k:k<10?k-2:k-10;
   const a=t*(k<2?2:k<10?1.3:0.9)+idx*2*Math.PI/per; const x=cx+sh*Math.cos(a), y=cy+sh*Math.sin(a)*0.85;
   sv.append(ns('circle',{cx:x,cy:y,r:7,fill:'#1f4e9c'})); const m=ns('text',{x,y:y+4,'text-anchor':'middle','font-size':10,fill:'#fff'}); m.textContent='−'; sv.append(m); }
 const q=Z-ne; const typ=q===0?'Atome neutre':q>0?'Cation (ion positif) : l\'atome a perdu '+q+' électron'+(q>1?'s':''):'Anion (ion négatif) : l\'atome a gagné '+(-q)+' électron'+(-q>1?'s':'');
 $('#rs').innerHTML='Formule : <span class="big">'+s+'<sup>'+sup(q)+'</sup></span><br>'+typ+'<br>Charge du noyau : <b>+'+Z+'e</b> · Électrons : <b>'+ne+'</b> (charge −'+ne+'e)<br>Charge totale : <b>'+(q===0?'0':(q>0?'+':'−')+Math.abs(q)+'e = '+(q>0?'+':'−')+fr(Math.abs(q)*1.6,1)+' × 10⁻¹⁹ C')+'</b>';
 requestAnimationFrame(draw); }
draw();
""")

# ---------------------------------------------------------------- 6. Rouille
sim("rouille", "Réaction de quelques matériaux avec l'air", "3ac", "Expérience : quand le fer rouille-t-il ?",
 "Quatre clous en fer sont placés dans des conditions différentes. Fais avancer le temps.",
 """<div class="scene"><svg id="sv" viewBox="0 0 560 300"></svg></div>
<div class="ctrl">
 <label>Temps écoulé <b id="vJ">0 jour</b></label><input id="J" type="range" min="0" max="30" value="0">
 <div class="res" id="rs"></div>
 <div class="note">Conclusion attendue : il faut du <b>dioxygène</b> ET de l'<b>eau</b> ; le <b>sel</b> accélère la rouille.</div>
</div>""",
 r"""
const C=[['Air sec',0,'#fff8e1'],['Eau bouillie + huile (sans air)',0,'#d6ebff'],['Air humide',1,'#e9f4ff'],['Eau salée + air',2,'#d7f1ec']];
function draw(){ const j=+$('#J').value, sv=$('#sv'); sv.innerHTML=''; $('#vJ').textContent=j+' jour'+(j>1?'s':'');
 C.forEach(([nm,v,bg],i)=>{ const x=30+i*135; sv.append(ns('rect',{x,y:50,width:100,height:190,rx:14,fill:bg,stroke:'#1a3a7c','stroke-width':2}));
  if(i===1) sv.append(ns('rect',{x:x+3,y:70,width:94,height:14,fill:'#f2d46b'}));
  const r=Math.min(1,v*j/(v===2?12:22)); const col=`rgb(${Math.round(140+r*40)},${Math.round(143-r*70)},${Math.round(152-r*120)})`;
  sv.append(ns('rect',{x:x+45,y:95,width:10,height:120,fill:col,rx:2})); sv.append(ns('rect',{x:x+38,y:90,width:24,height:8,fill:col,rx:2}));
  if(r>0.2) for(let k=0;k<Math.round(r*8);k++) sv.append(ns('circle',{cx:x+44+((k*7)%12),cy:110+k*12,r:3+r*2,fill:'#a0522d'}));
  const tx=ns('text',{x:x+50,y:262,'text-anchor':'middle','font-size':11.5,fill:'#14213d'}); tx.textContent=nm.length>18?nm.slice(0,18)+'…':nm; sv.append(tx);
  const t2=ns('text',{x:x+50,y:280,'text-anchor':'middle','font-size':12,'font-weight':700,fill:r>0.2?'#c0392b':'#2e7d4f'}); t2.textContent=r>0.2?'rouillé':'intact'; sv.append(t2); });
 $('#rs').innerHTML = j<5 ? 'Observe les quatre tubes…' : 'Le fer rouille seulement avec <b>air + eau</b> ; plus vite avec le <b>sel</b>.<br>4 Fe + 3 O₂ → 2 Fe₂O₃ (rouille poreuse)';
}
$('#J').oninput=draw; draw();
""")

# ---------------------------------------------------------------- 7. Gravitation
sim("gravitation", "La gravitation universelle", "tc", "Interaction gravitationnelle et poids",
 "Change les masses et la distance : observe les forces d'attraction. Onglet 2 : le poids sur les planètes.",
 """<div class="tabs chips"><button aria-pressed="true" id="t1">Deux corps</button><button aria-pressed="false" id="t2">Poids sur les astres</button></div>
<div class="labbody"><div class="scene"><svg id="sv" viewBox="0 0 560 300"></svg></div>
<div class="ctrl" id="c1">
 <label>Masse de A <b id="vA">600 kg</b></label><input id="mA" type="range" min="1" max="2000" value="600">
 <label>Masse de B <b id="vB">150 kg</b></label><input id="mB" type="range" min="1" max="2000" value="150">
 <label>Distance d <b id="vD">5 m</b></label><input id="d" type="range" min="1" max="20" step="0.5" value="5">
 <div class="res">F<sub>A/B</sub> = F<sub>B/A</sub> = G·m<sub>A</sub>·m<sub>B</sub> / d²<br><span class="big" id="vF"></span></div>
 <div class="note">Si d double, F est divisée par 4 (loi en 1/d²).</div>
</div>
<div class="ctrl" id="c2" hidden>
 <label>Masse du corps <b id="vm">60 kg</b></label><input id="m" type="range" min="1" max="200" value="60">
 <label>Astre</label><select id="as"><option value="9.8">Terre (g = 9,8 N/kg)</option><option value="1.62">Lune (1,62)</option><option value="3.7">Mars (3,7)</option><option value="24.8">Jupiter (24,8)</option><option value="8.87">Vénus (8,87)</option></select>
 <div class="res">P = m · g<br><span class="big" id="vP"></span><br><small>La masse ne change pas, le poids change.</small></div>
</div></div>""",
 r"""
let tab=1; const G=6.67e-11;
function draw(){ const sv=$('#sv'); sv.innerHTML='';
 if(tab===1){ const a=+$('#mA').value,b=+$('#mB').value,d=+$('#d').value; const F=G*a*b/(d*d);
  $('#vA').textContent=a+' kg'; $('#vB').textContent=b+' kg'; $('#vD').textContent=fr(d,1)+' m'; $('#vF').innerHTML=sci(F)+' N';
  const sep=70+d*21, xA=280-sep/2,xB=280+sep/2, rA=10+Math.cbrt(a)*2.2, rB=10+Math.cbrt(b)*2.2;
  sv.append(ns('line',{x1:20,y1:150,x2:540,y2:150,stroke:'#9aa7c0','stroke-dasharray':'5 5'}));
  sv.append(ns('circle',{cx:xA,cy:150,r:rA,fill:'#d4a017'})); sv.append(ns('circle',{cx:xB,cy:150,r:rB,fill:'#2f9fb8'}));
  const L=Math.max(8,Math.min(sep/2-Math.max(rA,rB)-8,(Math.log10(F)+11)*12));
  const ar=(x1,x2,c)=>{ sv.append(ns('line',{x1,y1:150,x2,y2:150,stroke:c,'stroke-width':4})); const s=x2>x1?1:-1; sv.append(ns('path',{d:`M${x2} 150 l${-10*s} -7 v14 z`,fill:c})); };
  ar(xA,xA+L,'#c0392b'); ar(xB,xB-L,'#1f4e9c');
  const t=(x,y,s,c)=>{const e=ns('text',{x,y,'font-size':14,'text-anchor':'middle',fill:c,'font-weight':700}); e.textContent=s; sv.append(e)};
  t(xA,150-rA-10,'A','#14213d'); t(xB,150-rB-10,'B','#14213d'); t(xA+L/2,130,'F B/A','#c0392b'); t(xB-L/2,178,'F A/B','#1f4e9c');
  const dd=ns('text',{x:280,y:200,'font-size':13,'text-anchor':'middle',fill:'#14213d'}); dd.textContent='d = '+fr(d,1)+' m'; sv.append(dd);
 } else { const m=+$('#m').value,g=+$('#as').value; const P=m*g; $('#vm').textContent=m+' kg'; $('#vP').textContent=fr(P,1)+' N';
  sv.append(ns('circle',{cx:280,cy:420,r:260,fill:{9.8:'#3d7bd9',1.62:'#bbb',3.7:'#c1440e',24.8:'#d9a066',8.87:'#e3bb76'}[g]}));
  sv.append(ns('rect',{x:262,y:120,width:36,height:40,rx:8,fill:'#14213d'})); sv.append(ns('circle',{cx:280,cy:106,r:14,fill:'#14213d'}));
  const L=Math.min(150,P/12); sv.append(ns('line',{x1:280,y1:140,x2:280,y2:140+L,stroke:'#c0392b','stroke-width':5})); sv.append(ns('path',{d:`M280 ${150+L} l-8 -12 h16 z`,fill:'#c0392b'}));
  const e=ns('text',{x:300,y:150+L/2,'font-size':15,fill:'#c0392b','font-weight':700}); e.textContent='P = '+fr(P,1)+' N'; sv.append(e); }
}
['#mA','#mB','#d','#m'].forEach(i=>$(i).oninput=draw); $('#as').onchange=draw;
$('#t1').onclick=()=>{tab=1;$('#c1').hidden=false;$('#c2').hidden=true;$('#t1').setAttribute('aria-pressed',true);$('#t2').setAttribute('aria-pressed',false);draw()};
$('#t2').onclick=()=>{tab=2;$('#c1').hidden=true;$('#c2').hidden=false;$('#t2').setAttribute('aria-pressed',true);$('#t1').setAttribute('aria-pressed',false);draw()};
draw();
""")

# ---------------------------------------------------------------- 8. Plan incliné + force pressante
sim("plan-incline-pression", "Exemples d'actions mécaniques", "tc", "Plan incliné et force pressante",
 "Onglet 1 : un solide en équilibre sur un plan incliné (poids, réaction, frottement). Onglet 2 : la pression P = F / S.",
 """<div class="tabs chips"><button aria-pressed="true" id="t1">Plan incliné</button><button aria-pressed="false" id="t2">Force pressante</button></div>
<div class="labbody"><div class="scene"><svg id="sv" viewBox="0 0 560 320"></svg></div>
<div class="ctrl" id="c1">
 <label>Angle α <b id="va">30°</b></label><input id="a" type="range" min="0" max="45" value="30">
 <label>Masse m <b id="vm">500 g</b></label><input id="m" type="range" min="100" max="1000" step="50" value="500">
 <div class="res" id="r1"></div>
 <div class="note">À l'équilibre : R⃗ = −P⃗. R<sub>N</sub> = P·cos α ; R<sub>T</sub> = P·sin α ; k = tan φ = R<sub>T</sub>/R<sub>N</sub>.</div>
</div>
<div class="ctrl" id="c2" hidden>
 <label>Force F <b id="vF">30 N</b></label><input id="F" type="range" min="1" max="200" value="30">
 <label>Surface S <b id="vS">2 cm²</b></label><input id="S" type="range" min="0.5" max="20" step="0.5" value="2">
 <div class="res" id="r2"></div>
</div></div>""",
 r"""
let tab=1;
function arrow(sv,x,y,dx,dy,c,lab){ sv.append(ns('line',{x1:x,y1:y,x2:x+dx,y2:y+dy,stroke:c,'stroke-width':4})); const a=Math.atan2(dy,dx);
 sv.append(ns('path',{d:`M${x+dx} ${y+dy} l${-12*Math.cos(a-0.4)} ${-12*Math.sin(a-0.4)} l${12*Math.cos(a-0.4)-12*Math.cos(a+0.4)} ${12*Math.sin(a-0.4)-12*Math.sin(a+0.4)} z`,fill:c}));
 const t=ns('text',{x:x+dx*1.08+6,y:y+dy*1.08,'font-size':14,'font-weight':700,fill:c}); t.textContent=lab; sv.append(t); }
function draw(){ const sv=$('#sv'); sv.innerHTML='';
 if(tab===1){ const a=+$('#a').value, m=+$('#m').value/1000, P=m*10, ar=a*Math.PI/180; const RN=P*Math.cos(ar), RT=P*Math.sin(ar);
  $('#va').textContent=a+'°'; $('#vm').textContent=Math.round(m*1000)+' g';
  const x0=60,y0=280,L=460; const x1=x0+L*Math.cos(ar), y1=y0-L*Math.sin(ar);
  sv.append(ns('path',{d:`M${x0} ${y0} L${x0+L*Math.cos(ar)} ${y0} L${x1} ${y1} Z`,fill:'#e4dfd3',stroke:'#7d6b4a'}));
  const cx=x0+0.55*L*Math.cos(ar), cy=y0-0.55*L*Math.sin(ar);
  const g=ns('g',{transform:`translate(${cx},${cy}) rotate(${-a})`}); g.append(ns('rect',{x:-35,y:-50,width:70,height:50,fill:'#1f4e9c',rx:4})); sv.append(g);
  const Gx=cx-25*Math.sin(ar), Gy=cy-25*Math.cos(ar); const k=20;
  arrow(sv,Gx,Gy,0,P*k,'#c0392b','P'); arrow(sv,Gx,Gy,0,-P*k,'#2e7d4f','R');
  arrow(sv,Gx,Gy,-RN*k*Math.sin(ar),-RN*k*Math.cos(ar),'#7a3fa8','RN'); arrow(sv,Gx,Gy,-RT*k*Math.cos(ar),RT*k*Math.sin(ar),'#d4a017','RT');
  $('#r1').innerHTML='P = m·g = <b>'+fr(P)+' N</b> = R<br>R<sub>N</sub> = <b>'+fr(RN)+' N</b> · R<sub>T</sub> = <b>'+fr(RT)+' N</b><br>Angle de frottement φ = α = <b>'+a+'°</b> · k = tan φ = <b>'+fr(Math.tan(ar))+'</b>';
 } else { const F=+$('#F').value, S=+$('#S').value, P=F/(S*1e-4); $('#vF').textContent=F+' N'; $('#vS').textContent=fr(S,1)+' cm²';
  sv.append(ns('rect',{x:120,y:120,width:320,height:120,fill:'#e8effb',stroke:'#1a3a7c','stroke-width':3,rx:8}));
  const w=Math.sqrt(S)*40; sv.append(ns('rect',{x:280-w/2,y:100,width:w,height:24,fill:'#d4a017'}));
  arrow(sv,280,40,0,Math.min(55,10+F/4),'#c0392b','F');
  for(let i=0;i<Math.min(60,10+P/6000);i++) sv.append(ns('circle',{cx:130+Math.random()*300,cy:130+Math.random()*100,r:3,fill:'#2f6fb8'}));
  $('#r2').innerHTML='P = F / S = '+F+' / ('+fr(S,1)+' × 10⁻⁴)<br><span class="big">'+sci(P)+' Pa</span><br>= '+fr(P/100,0)+' hPa = '+fr(P/1e5,2)+' bar = '+fr(P/1.013e5,2)+' atm<br><small>'+(P>1.013e5?'Supérieure':'Inférieure')+' à la pression atmosphérique (1013 hPa)</small>'; }
}
['#a','#m','#F','#S'].forEach(i=>$(i).oninput=draw);
$('#t1').onclick=()=>{tab=1;$('#c1').hidden=false;$('#c2').hidden=true;$('#t1').setAttribute('aria-pressed',true);$('#t2').setAttribute('aria-pressed',false);draw()};
$('#t2').onclick=()=>{tab=2;$('#c1').hidden=true;$('#c2').hidden=false;$('#t2').setAttribute('aria-pressed',true);$('#t1').setAttribute('aria-pressed',false);draw()};
draw();
""")

# ---------------------------------------------------------------- 9. Tests chimiques
sim("tests-chimiques", "Les espèces chimiques", "tc", "Laboratoire des tests chimiques",
 "Choisis un échantillon et un réactif : observe le résultat et conclus.",
 """<div class="scene"><svg id="sv" viewBox="0 0 560 300"></svg></div>
<div class="ctrl">
 <label>Échantillon</label><select id="ech"></select>
 <label>Test</label><select id="tst"></select>
 <button class="bt pri" id="go">Réaliser le test</button>
 <div class="res" id="rs">Choisis puis réalise le test.</div>
</div>""",
 r"""
const S={'Jus de citron':{eau:1,glu:0,ami:0,ph:3,co2:0},'Eau sucrée (glucose)':{eau:1,glu:1,ami:0,ph:7,co2:0},'Pain mixé dans l\'eau':{eau:1,glu:0,ami:1,ph:6,co2:0},
 'Eau distillée':{eau:1,glu:0,ami:0,ph:7,co2:0},'Coca-Cola':{eau:1,glu:1,ami:0,ph:2.5,co2:1},'Eau savonneuse':{eau:1,glu:0,ami:0,ph:10,co2:0},'Huile':{eau:0,glu:0,ami:0,ph:null,co2:0}};
const T={'Sulfate de cuivre anhydre':['#f4f4f4',s=>s.eau?['#3a7bd5','Le solide blanc <b>bleuit</b> ⇒ présence d\'<b>eau</b>.']:['#f4f4f4','Il reste blanc ⇒ pas d\'eau.']],
 'Liqueur de Fehling (chauffée)':['#2f6fe0',s=>s.glu?['#b5482a','Précipité <b>rouge brique</b> ⇒ présence de <b>glucose</b>.']:['#2f6fe0','Reste bleue ⇒ pas de glucose.']],
 'Eau iodée':['#c8932c',s=>s.ami?['#3b1f6b','Coloration <b>bleu-violet</b> ⇒ présence d\'<b>amidon</b>.']:['#c8932c','Reste jaune-orangé ⇒ pas d\'amidon.']],
 'Papier pH':['#e6c84a',s=>s.ph==null?['#e6c84a','Pas de solution aqueuse : test impossible.']:[s.ph<5?'#d93b3b':s.ph<6.5?'#f08a24':s.ph<=7.5?'#7cb342':'#3f51b5','pH ≈ <b>'+String(s.ph).replace('.',',')+'</b> ⇒ solution <b>'+(s.ph<7?'acide':s.ph>7?'basique':'neutre')+'</b>.']],
 'BBT':['#5aa05a',s=>s.ph==null?['#5aa05a','Pas de solution aqueuse.']:s.ph<6.5?['#e8c21e','Le BBT devient <b>jaune</b> ⇒ milieu <b>acide</b>.']:s.ph>7.5?['#2e5fd6','Le BBT devient <b>bleu</b> ⇒ milieu <b>basique</b>.']:['#4caf50','Le BBT reste <b>vert</b> ⇒ milieu <b>neutre</b>.']],
 'Gaz dans l\'eau de chaux':['#eef6f6',s=>s.co2?['#dcdcdc','L\'eau de chaux <b>se trouble</b> ⇒ <b>dioxyde de carbone</b>.']:['#eef6f6','Pas de gaz dégagé : l\'eau de chaux reste limpide.']]};
Object.keys(S).forEach(k=>{const o=document.createElement('option');o.textContent=k;$('#ech').append(o)});
Object.keys(T).forEach(k=>{const o=document.createElement('option');o.textContent=k;$('#tst').append(o)});
function tube(col,lab){ const sv=$('#sv'); sv.innerHTML='';
 sv.append(ns('path',{d:'M240 40 v190 a40 40 0 0 0 80 0 v-190',fill:'#fff',stroke:'#1a3a7c','stroke-width':3}));
 sv.append(ns('path',{d:'M243 130 v100 a37 37 0 0 0 74 0 v-100 z',fill:col}));
 const t=ns('text',{x:280,y:295,'text-anchor':'middle','font-size':13,fill:'#14213d'}); t.textContent=lab; sv.append(t); }
$('#go').onclick=()=>{ const s=S[$('#ech').value], tt=T[$('#tst').value]; tube(tt[0],'avant'); setTimeout(()=>{ const [c,msg]=tt[1](s); tube(c,'après'); $('#rs').innerHTML=msg; },700); };
tube('#eef2f8','');
""")

# ---------------------------------------------------------------- 10. Ampoule à décanter
sim("ampoule-a-decanter", "Extraction, séparation et identification", "tc", "Extraction par solvant – ampoule à décanter",
 "Choisis le solvant extracteur : est-il bien choisi ? Où se trouve chaque phase ?",
 """<div class="scene"><svg id="sv" viewBox="0 0 560 340"></svg></div>
<div class="ctrl">
 <label>Espèce à extraire</label><select id="esp"><option>Eugénol (clou de girofle)</option><option>Limonène (orange)</option><option>Menthone (menthe)</option></select>
 <label>Solvant extracteur</label><select id="sol"></select>
 <div class="chips"><button class="bt pri" id="ag">Agiter puis laisser décanter</button></div>
 <div class="res" id="rs"></div>
</div>""",
 r"""
const SOL={'Cyclohexane':{d:0.78,mis:0,sol:'très grande'},'Dichlorométhane':{d:1.33,mis:0,sol:'très grande'},'Éthanol':{d:0.79,mis:1,sol:'très grande'},'Toluène':{d:0.87,mis:0,sol:'grande'},'Eau salée':{d:1.1,mis:1,sol:'faible'}};
Object.keys(SOL).forEach(k=>{const o=document.createElement('option');o.textContent=k;$('#sol').append(o)});
let shake=0;
function draw(){ const s=SOL[$('#sol').value], sv=$('#sv'); sv.innerHTML=''; const dx=shake>0?Math.sin(shake*1.4)*8:0;
 const g=ns('g',{transform:`translate(${dx},0)`}); sv.append(g);
 g.append(ns('path',{d:'M270 20 h20 v30 q90 40 70 140 l-70 70 v60 h-20 v-60 l-70 -70 q-20 -100 70 -140 z',fill:'#fff',stroke:'#1a3a7c','stroke-width':3}));
 g.append(ns('rect',{x:262,y:258,width:36,height:10,fill:'#14213d'}));
 const aq='#bfe0ff', org='#ffcf8a';
 if(shake>0||s.mis){ g.append(ns('path',{d:'M206 120 q-10 60 0 80 l74 74 l74 -74 q10 -20 0 -80 z',fill:s.mis?'#d8ecd2':'#d9c7b0'})); }
 else { const orgDown=s.d>1;
   g.append(ns('path',{d:'M206 120 q-6 30 -2 45 h152 q4 -15 -2 -45 z',fill:orgDown?aq:org}));
   g.append(ns('path',{d:'M204 165 q0 20 2 35 l74 74 l74 -74 q2 -15 2 -35 z',fill:orgDown?org:aq}));
   const t=(y,txt)=>{const e=ns('text',{x:375,y,'font-size':13,fill:'#14213d'}); e.textContent=txt; sv.append(e)};
   t(145,orgDown?'Phase aqueuse (eau, d = 1)':'Phase organique ('+$('#sol').value+')'); t(205,orgDown?'Phase organique ('+$('#sol').value+')':'Phase aqueuse (eau, d = 1)'); }
 if(shake>0){ shake--; requestAnimationFrame(draw); return; }
 const esp=$('#esp').value.split(' (')[0];
 $('#rs').innerHTML = s.mis ? '<span class="ko">Mauvais choix</span> : le '+$('#sol').value.toLowerCase()+' est <b>miscible à l\'eau</b> : une seule phase, impossible de séparer.'
  : '<span class="ok">Bon choix</span> : non miscible à l\'eau, solubilité de l\'espèce '+s.sol+'.<br>d = '+String(s.d).replace('.',',')+(s.d>1?' > 1 : la phase organique est <b>en bas</b>.':' < 1 : la phase organique est <b>en haut</b>.')+'<br>L\''+esp.toLowerCase()+' se trouve dans la <b>phase organique</b>.';
}
$('#ag').onclick=()=>{shake=60;draw()}; $('#sol').onchange=draw; $('#esp').onchange=draw; draw();
""")
