// Protection des API du site + journal des tentatives bloquées.
// Le journal est gardé 30 jours dans l'espace KV ABONNES (clés « sec:… »), et se lit
// dans la page Statistiques (section « Sécurité ») ou via GET /api/securite avec l'en-tête X-Stats-Key.

// Seuls les services de notification des navigateurs sont acceptés comme adresses d'abonnement.
const PUSH_HOTES = [/^fcm\.googleapis\.com$/, /^android\.googleapis\.com$/, /^updates\.push\.services\.mozilla\.com$/,
  /^web\.push\.apple\.com$/, /^[a-z0-9-]+\.push\.apple\.com$/, /^[a-z0-9-]+\.notify\.windows\.com$/];

export function endpointValide(e) {
  if (typeof e !== "string" || e.length > 800) return false;
  let u;
  try { u = new URL(e); } catch (_) { return false; }
  return u.protocol === "https:" && !u.port && !u.username && !u.password && PUSH_HOTES.some((r) => r.test(u.hostname));
}

export const ipDe = (request) => request.headers.get("cf-connecting-ip") || "?";

// Compteur par IP dans le cache de Cloudflare (aucune écriture KV). true = limite dépassée.
export async function limite(request, nom, max, fenetreSec) {
  try {
    const c = caches.default, origin = new URL(request.url).origin;
    const tranche = Math.floor(Date.now() / 1000 / fenetreSec);
    const key = new Request(`${origin}/__rl/${nom}/${encodeURIComponent(ipDe(request))}/${tranche}`);
    const hit = await c.match(key);
    const n = (hit ? +(await hit.text()) || 0 : 0) + 1;
    await c.put(key, new Response(String(n), { headers: { "cache-control": `max-age=${fenetreSec}` } }));
    return n > max;
  } catch (_) { return false; }
}

// Note une tentative bloquée. Une même IP n'est notée qu'une fois toutes les 10 minutes par motif,
// et au plus 60 notes par heure : une attaque ne peut pas remplir le KV ni épuiser son quota d'écritures.
export async function noter(kv, request, motif, detail = "") {
  if (!kv) return;
  try {
    if (await limite(request, "log-" + motif, 1, 600)) return;
    if (await limite(new Request(new URL("/", request.url)), "log-total", 60, 3600)) return;
    const u = new URL(request.url), t = Date.now();
    const meta = {
      t, motif, ip: ipDe(request).slice(0, 45), pays: (request.cf && request.cf.country) || "",
      chemin: (request.method + " " + u.pathname).slice(0, 100),
      ua: (request.headers.get("user-agent") || "").slice(0, 150), detail: String(detail).slice(0, 200),
    };
    // Clé décroissante : les tentatives les plus récentes sortent en premier dans kv.list.
    const key = "sec:" + String(9999999999999 - t).padStart(13, "0") + ":" + Math.random().toString(36).slice(2, 8);
    await kv.put(key, "", { metadata: meta, expirationTtl: 30 * 86400 });
  } catch (_) {}
}

// Comparaison à temps constant du code d'accès.
export function memeCle(a, b) {
  a = String(a || ""); b = String(b || "");
  if (!a || !b) return false;
  let d = a.length ^ b.length;
  for (let i = 0; i < Math.max(a.length, b.length); i++) d |= (a.charCodeAt(i) || 0) ^ (b.charCodeAt(i) || 0);
  return d === 0;
}
