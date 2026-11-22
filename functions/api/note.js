// Note moyenne publique du site (calculée à partir des avis du Google Sheet « Statistiques YH »).
// Le code d'accès aux statistiques est lu dans la variable secrète STATS_CLE (Cloudflare Pages > Settings > Variables).
const SCRIPT = "https://script.google.com/macros/s/AKfycbxta1pz0xrqrIa9RiENIXd_CQwiQpkvcwtm_sWBH15-UfBTCN4clgsdmtc3HXZtXh4I/exec";

export async function onRequestGet({ env, request, waitUntil }) {
  const cache = caches.default;
  const key = new Request(new URL("/api/note?v=1", request.url).toString());
  const hit = await cache.match(key);
  if (hit) return hit;
  let out = { moyenne: 0, nombre: 0 };
  const cle = env.STATS_CLE || "";
  if (cle) {
    try {
      const r = await fetch(SCRIPT + "?cle=" + encodeURIComponent(cle) + "&t=" + Date.now(), { redirect: "follow" });
      const d = await r.json();
      const last = {};
      for (const l of d.lignes || []) {
        if (l[1] !== "avis") continue;
        const n = +l[6];
        if (n >= 1 && n <= 5) last[l[2]] = n; // un seul avis par visiteur (le plus récent)
      }
      const notes = Object.values(last);
      if (notes.length) out = { moyenne: Math.round((notes.reduce((a, b) => a + b, 0) / notes.length) * 10) / 10, nombre: notes.length };
    } catch (e) {}
  }
  const res = new Response(JSON.stringify(out), {
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "public, max-age=600" },
  });
  waitUntil(cache.put(key, res.clone()));
  return res;
}
