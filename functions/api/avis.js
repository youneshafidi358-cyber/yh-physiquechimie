// Notes des visiteurs (publiques) : moyenne, nombre d'avis et répartition 5★…1★.
// Une note par visiteur (la plus récente), stockée dans le KV ABONNES sous « a:<visiteur> ».
const J = (o, s = 200, cache = "no-store") => new Response(JSON.stringify(o), { status: s, headers: { "content-type": "application/json; charset=utf-8", "cache-control": cache } });

async function bilan(kv) {
  const rep = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
  let cur, n = 0, tot = 0;
  for (let i = 0; i < 20; i++) {
    const l = await kv.list({ prefix: "a:", cursor: cur });
    for (const k of l.keys) { const v = +(k.metadata && k.metadata.n); if (v >= 1 && v <= 5) { rep[v]++; n++; tot += v; } }
    if (l.list_complete) break; cur = l.cursor;
  }
  return { moyenne: n ? Math.round((tot / n) * 10) / 10 : 0, nombre: n, repartition: rep };
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
  const n = d && +d.note, vid = d && String(d.vid || "").replace(/[^\w-]/g, "").slice(0, 40);
  if (!vid || !(n >= 1 && n <= 5)) return J({ ok: false }, 400);
  await env.ABONNES.put("a:" + vid, String(n), { metadata: { n, t: Date.now() } });
  try { await caches.default.delete(new Request(new URL("/api/avis?v=1", request.url).toString())); } catch (_) {}
  return J({ ok: true });
}
