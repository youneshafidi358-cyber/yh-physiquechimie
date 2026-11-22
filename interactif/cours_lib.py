# -*- coding: utf-8 -*-
"""Petits outils pour écrire les cours en HTML (encadrés, figures, questions à révéler, molécules)."""
import html as _h
E = lambda s: _h.escape(s, quote=True)

KINDS = {  # classe, icône, titre par défaut
    "sit": ("k-sit", "🤔", "Situation-problème"), "act": ("k-act", "🔬", "Activité expérimentale"),
    "doc": ("k-act", "📄", "Activité documentaire"), "obs": ("k-obs", "👀", "Observation"),
    "int": ("k-obs", "💡", "Interprétation"), "conc": ("k-conc", "✅", "Conclusion"),
    "def": ("k-def", "📘", "Définition"), "ret": ("k-ret", "⭐", "À retenir"),
    "rem": ("k-rem", "📝", "Remarque"), "meth": ("k-meth", "🧭", "Méthode"),
    "rule": ("k-rule", "📏", "Règle"), "ex": ("k-ex", "✏️", "Exemple"), "att": ("k-rule", "⚠️", "Attention"),
    "app": ("k-app", "🎯", "Application"),
}

def B(kind, body, title=None):
    c, ic, t = KINDS[kind]
    return f'<div class="bx {c}"><div class="bx-t"><span aria-hidden="true">{ic}</span> {title or t}</div><div class="bx-b">{body}</div></div>'

_q = [0]
def Q(q, a):
    _q[0] += 1
    return (f'<div class="qa"><p class="qa-q">{q}</p><button type="button" class="qa-btn" aria-expanded="false">Voir la réponse</button>'
            f'<div class="qa-a" hidden>{a}</div></div>')

def QS(*pairs):
    return "".join(Q(q, a) for q, a in pairs)

def FIG(src, cap="", w=None):
    st = f' style="max-width:{w}px"' if w else ""
    return f'<figure class="cfig"{st}><img loading="lazy" src="/cours-img/{src}" alt="{E(cap)}" draggable="false">{f"<figcaption>{cap}</figcaption>" if cap else ""}</figure>'

def FIGS(*figs):
    return '<div class="cfigs">' + "".join(figs) + "</div>"

def TAB(head, rows, cls=""):
    h = "".join(f"<th>{x}</th>" for x in head)
    b = "".join((f'<tr class="grp"><td colspan="{len(r)}">{r[0]}</td></tr>' if len(r) > 2 and r[0].startswith("<b>Cas") and not any(r[1:]) else
                 "<tr>" + "".join(f"<td>{x}</td>" for x in r) + "</tr>") for r in rows)
    return f'<div class="ctab {cls}" tabindex="0" role="region" aria-label="Tableau"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'

def UL(*items):
    return "<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"

def OL(*items):
    return "<ol>" + "".join(f"<li>{x}</li>" for x in items) + "</ol>"

def TRAD(pairs):
    rows = "".join(f'<tr><td>{fr}</td><td lang="ar" dir="rtl">{ar}</td></tr>' for fr, ar in pairs)
    return f'<div class="ctab trad"><table><thead><tr><th>Français</th><th lang="ar">العربية</th></tr></thead><tbody>{rows}</tbody></table></div>'

SIM = "%%SIM%%"   # emplacement de la simulation dans le cours

# ---------- molécules (modèles éclatés en SVG) ----------
COL = {"H": ("#f4f4f4", 9), "O": ("#d62828", 12), "N": ("#1d4ed8", 12), "C": ("#2b2b2b", 12), "Cl": ("#2f9e44", 14), "S": ("#e6c200", 14)}
LAY = {
    "H2": [("H", 0, 0), ("H", 16, 0)], "O2": [("O", 0, 0), ("O", 20, 0)], "N2": [("N", 0, 0), ("N", 20, 0)], "Cl2": [("Cl", 0, 0), ("Cl", 24, 0)],
    "CO2": [("O", 0, 0), ("C", 21, 0), ("O", 42, 0)], "NO2": [("O", 0, 6), ("N", 19, -4), ("O", 38, 6)],
    "H2O": [("H", 0, 12), ("O", 14, 0), ("H", 28, 12)], "CH4": [("C", 18, 12), ("H", 18, -3), ("H", 3, 20), ("H", 33, 20), ("H", 18, 27)],
    "CO": [("C", 0, 0), ("O", 20, 0)], "O3": [("O", 0, 8), ("O", 19, 0), ("O", 38, 8)], "NH3": [("N", 16, 4), ("H", 0, 16), ("H", 16, 22), ("H", 32, 16)],
    "SO2": [("O", 0, 8), ("S", 21, 0), ("O", 42, 8)], "H": [("H", 0, 0)], "O": [("O", 0, 0)], "N": [("N", 0, 0)], "C": [("C", 0, 0)], "Cl": [("Cl", 0, 0)], "S": [("S", 0, 0)],
}
def MOL(f, label=True):
    at = LAY[f]
    xs = [x for _, x, _ in at]; ys = [y for _, _, y in at]
    pad = 16; w = max(xs) - min(xs) + 2 * pad; h = max(ys) - min(ys) + 2 * pad
    g = ""
    for a, x, y in sorted(at, key=lambda t: COL[t[0]][1]):
        c, r = COL[a]
        cx, cy = x - min(xs) + pad, y - min(ys) + pad
        g += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}" stroke="#555" stroke-width=".8"/><circle cx="{cx-r/3:.1f}" cy="{cy-r/3:.1f}" r="{r/3:.1f}" fill="#fff" opacity=".45"/>'
    return f'<svg class="mol" viewBox="0 0 {w} {h}" width="{w*1.4:.0f}" height="{h*1.4:.0f}" role="img" aria-label="Modèle de {f}">{g}</svg>'


def QCM(q, opts, ok, expl=""):
    """Question à choix : clic -> vert/rouge + explication. ok = index de la bonne réponse."""
    import re as _re
    def _plain(x):
        x = _re.sub(r"<[^>]+>", "", x); x = x.replace("\\dfrac", "").replace("\\frac", "").replace("$", "")
        x = _re.sub(r"\^\{([^}]*)\}", r" puissance \1", x); x = _re.sub(r"\\[a-zA-Z]+", " ", x)
        return _re.sub(r"[{}\\]", "", x).strip()
    bt = "".join(f'<button type="button" aria-label="{E(_plain(o))}" data-ok="{1 if i == ok else 0}">{o}</button>' for i, o in enumerate(opts))
    return f'<div class="qcm"><p class="qa-q">{q}</p><div class="qcm-o">{bt}</div><div class="qcm-e" hidden>{expl}</div></div>'

def VF(q, vrai, expl=""):
    return QCM(q, ["Vrai", "Faux"], 0 if vrai else 1, expl)

def APP(*items, title="Applications interactives"):
    return B("app", "".join(items), title)


def EC(txt):
    """Petite phrase « en clair » qui explique une relation ou une définition."""
    return f'<p class="enclair">{txt}</p>'
