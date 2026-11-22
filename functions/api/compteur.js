// Compteur public de visites par jour (KV ABONNES, clé « j:AAAA-MM-JJ »).
// POST : une visite (envoyée une fois par session) ; GET : résumé des 8 derniers jours + avis + abonnés.
const J = (o, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" } });
const jour = (d = new Date()) => new Date(d.getTime()).toISOString().slice(0, 10);

export async function onRequestPost({ env, request }) {
  const kv = env.ABONNES; if (!kv) return J({ ok: false }, 503);
  const d = await request.json().catch(() => ({}));
  const k = "j:" + jour(), cf = request.cf || {};
  const o = (await kv.get(k, "json")) || { visites: 0, nouveaux: 0, villes: {}, sources: {} };
  o.visites++; if (d.nouveau) o.nouveaux++;
  const v = String(cf.city || "?").slice(0, 40); o.villes[v] = (o.villes[v] || 0) + 1;
  const s = String(d.src || "direct").slice(0, 30); o.sources[s] = (o.sources[s] || 0) + 1;
  try { await kv.put(k, JSON.stringify(o), { expirationTtl: 60 * 60 * 24 * 120 }); } catch (_) {}
  return J({ ok: true });
}

export async function onRequestGet({ env }) {
  const kv = env.ABONNES; if (!kv) return J({ actif: false });
  const jours = [];
  for (let i = 0; i < 8; i++) { const d = jour(new Date(Date.now() - i * 864e5)); jours.push({ jour: d, ...((await kv.get("j:" + d, "json")) || { visites: 0, nouveaux: 0, villes: {}, sources: {} }) }); }
  let ab = 0, cur; for (let i = 0; i < 10; i++) { const l = await kv.list({ prefix: "s:", cursor: cur }); ab += l.keys.length; if (l.list_complete) break; cur = l.cursor; }
  return J({ jours, abonnes: ab });
}
