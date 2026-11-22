// Notes des visiteurs (publiques) : moyenne, nombre d'avis et répartition 5★…1★.
// Une note par visiteur (la plus récente), stockée dans le KV ABONNES sous « a:<visiteur> ».
const J = (o, s = 200, cache = "no-store") => new Response(JSON.stringify(o), { status: s, headers: { "content-type": "application/json; charset=utf-8", "cache-control": cache } });

// Commentaire public : texte court, sans lien ni adresse, sans mots grossiers courants
const GROS = /(merde|putain|connard|salope|zebi|zabi|9a7ba|qahba|t9owd|tqawed|fuck|shit)/i;
function propre(c) {
  c = String(c || "").replace(/\s+/g, " ").trim().slice(0, 150);
  if (!c || /https?:|www\.|@|\d{6,}/i.test(c) || GROS.test(c)) return "";
  return c;
}
async function bilan(kv) {
  const rep = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
  let cur, n = 0, tot = 0;
  const coms = [];
  for (let i = 0; i < 20; i++) {
    const l = await kv.list({ prefix: "a:", cursor: cur });
    for (const k of l.keys) { const md = k.metadata || {}, v = +md.n; if (v >= 1 && v <= 5) { rep[v]++; n++; tot += v; if (md.c) coms.push({ n: v, c: md.c, v: md.v || "", t: +md.t || 0 }); } }
    if (l.list_complete) break; cur = l.cursor;
  }
  coms.sort((a, b) => b.t - a.t);
  return { moyenne: n ? Math.round((tot / n) * 10) / 10 : 0, nombre: n, repartition: rep, commentaires: coms.slice(0, 200) };
}

export async function onRequestGet({ env, request, waitUntil }) {
  if (!env.ABONNES) return J({ moyenne: 0, nombre: 0, repartition: {} });
  const c = caches.default, key = new Request(new URL("/api/avis?v=1", request.url).toString());
  const hit = await c.match(key); if (hit) return hit;
  const res = J(await bilan(env.ABONNES), 200, "public, max-age=60");
  waitUntil(c.put(key, res.clone()));
  return res;
}

export async function onRequestPost({ env, request }) {
  if (!env.ABONNES) return J({ ok: false }, 503);
  const d = await request.json().catch(() => null);
  // Reprise des anciennes notes du Google Sheet (envoyées par la page Statistiques) : on garde la plus récente par visiteur
  if (d && Array.isArray(d.import)) {
    let k = 0;
    for (const it of d.import.slice(0, 500)) {
      const v = String(it.vid || "").replace(/[^\w-]/g, "").slice(0, 40), n = +it.note, t = +it.t || 0, c = propre(it.c), vi = String(it.v || "").slice(0, 40);
      if (!v || !(n >= 1 && n <= 5)) continue;
      const ex = await env.ABONNES.getWithMetadata("a:" + v);
      if (ex && ex.metadata && +ex.metadata.t >= t) {
        // La note du site est plus récente : on garde sa note mais on récupère le commentaire s'il lui manque
        if (c && ex.metadata.c !== c) { await env.ABONNES.put("a:" + v, String(ex.metadata.n), { metadata: Object.assign({}, ex.metadata, { c, v: ex.metadata.v || vi }) }); k++; }
        continue;
      }
      await env.ABONNES.put("a:" + v, String(n), { metadata: { n, t, c, v: vi } }); k++;
    }
    try { await caches.default.delete(new Request(new URL("/api/avis?v=1", request.url).toString())); } catch (_) {}
    return J({ ok: true, ajoutes: k });
  }
  const n = d && +d.note, vid = d && String(d.vid || "").replace(/[^\w-]/g, "").slice(0, 40);
  if (!vid || !(n >= 1 && n <= 5)) return J({ ok: false }, 400);
  const cf = request.cf || {};
  await env.ABONNES.put("a:" + vid, String(n), { metadata: { n, t: Date.now(), c: propre(d.c), v: String(cf.city || "").slice(0, 40) } });
  try { await caches.default.delete(new Request(new URL("/api/avis?v=1", request.url).toString())); } catch (_) {}
  return J({ ok: true });
}
