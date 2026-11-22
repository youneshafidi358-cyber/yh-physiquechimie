// Notifications « Suivre le site » (Web Push, sans service extérieur).
// Stockage : espace KV lié sous le nom ABONNES (Cloudflare Pages > Settings > Bindings).
// Les clés VAPID sont créées automatiquement au premier appel et gardées dans le KV.
import { endpointValide, limite, noter } from "../../../lib/securite.js";

const SITE = "https://yh-physiquechimie.pages.dev";
const NIV = { "2ac": "2APIC", "3ac": "3APIC", tc: "TCS", "1bac": "1BAC", "2bac": "2BAC" };
const TYPES = { cours: "Cours", exo: "Série", corr: "Corrigé", ds: "Devoir", video: "Vidéo", resume: "Résumé" };

const b64u = (buf) => btoa(String.fromCharCode(...new Uint8Array(buf))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
const J = (o, s = 200, h = {}) => new Response(JSON.stringify(o), { status: s, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", ...h } });

async function cles(kv) {
  let k = await kv.get("vapid", "json");
  if (!k) {
    const p = await crypto.subtle.generateKey({ name: "ECDSA", namedCurve: "P-256" }, true, ["sign", "verify"]);
    k = { prive: await crypto.subtle.exportKey("jwk", p.privateKey), public: b64u(await crypto.subtle.exportKey("raw", p.publicKey)) };
    await kv.put("vapid", JSON.stringify(k));
  }
  return k;
}
async function jwt(k, aud) {
  const enc = (o) => b64u(new TextEncoder().encode(JSON.stringify(o)));
  const data = enc({ typ: "JWT", alg: "ES256" }) + "." + enc({ aud, exp: Math.floor(Date.now() / 1000) + 12 * 3600, sub: SITE });
  const key = await crypto.subtle.importKey("jwk", k.prive, { name: "ECDSA", namedCurve: "P-256" }, false, ["sign"]);
  const sig = await crypto.subtle.sign({ name: "ECDSA", hash: "SHA-256" }, key, new TextEncoder().encode(data));
  return data + "." + b64u(sig);
}
async function idAb(endpoint) {
  const h = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(endpoint));
  return "s:" + [...new Uint8Array(h)].slice(0, 16).map((x) => x.toString(16).padStart(2, "0")).join("");
}

// Envoie un lot (≤ 40) de notifications « vides » : le téléphone vient ensuite lire /api/push/derniere.
async function lot(kv) {
  const e = await kv.get("envoi", "json");
  if (!e) return 0;
  const k = await cles(kv);
  const l = await kv.list({ prefix: "s:", limit: 40, cursor: e.cursor || undefined });
  const jetons = {};
  let n = 0;
  for (const it of l.keys) {
    const ab = await kv.get(it.name, "json");
    if (!ab || !endpointValide(ab.endpoint)) { await kv.delete(it.name); continue; } // adresse non autorisée : supprimée
    const aud = new URL(ab.endpoint).origin;
    jetons[aud] = jetons[aud] || (await jwt(k, aud));
    try {
      const r = await fetch(ab.endpoint, { method: "POST", headers: { Authorization: `vapid t=${jetons[aud]}, k=${k.public}`, TTL: "172800", Urgency: "normal", "Content-Length": "0" } });
      if (r.status === 404 || r.status === 410) await kv.delete(it.name); else n++;
    } catch (_) {}
  }
  if (l.list_complete) await kv.delete("envoi"); else await kv.put("envoi", JSON.stringify({ cursor: l.cursor }));
  return n;
}

// Regarde s'il y a de nouveaux documents dans le site ; si oui, prépare une notification.
async function verifier(kv, origin) {
  const items = [];
  for (const f of ["/catalogue.json", "/extras.json"]) {
    try { const r = await fetch(origin + f, { cf: { cacheTtl: 60 } }); if (r.ok) (await r.json()).forEach((x) => x && x.url && items.push(x)); } catch (_) {}
  }
  if (!items.length) return;
  const vus = await kv.get("vus", "json");
  const urls = items.map((x) => x.url);
  if (!vus) { await kv.put("vus", JSON.stringify(urls)); return; } // première fois : on n'envoie rien
  const S = new Set(vus), nouv = items.filter((x) => !S.has(x.url));
  if (!nouv.length) return;
  let msg;
  if (nouv.length === 1) {
    const x = nouv[0];
    msg = { titre: "Nouveau : " + x.titre, corps: [x.sousType || TYPES[x.type] || "", NIV[x.niveau] || x.niveau || "", x.unite || ""].filter(Boolean).join(" · "), url: "/?doc=" + encodeURIComponent(x.url) };
  } else {
    msg = { titre: nouv.length + " nouveaux documents sur YH Physique-Chimie", corps: nouv.slice(0, 3).map((x) => "• " + x.titre).join("\n") + (nouv.length > 3 ? "\n…" : ""), url: "/" };
  }
  msg.t = Date.now();
  await kv.put("derniere", JSON.stringify(msg));
  await kv.put("vus", JSON.stringify([...new Set([...vus, ...urls])]));
  await kv.put("envoi", JSON.stringify({ cursor: null }));
}

export async function onRequest({ request, env, params, waitUntil }) {
  const kv = env.ABONNES;
  const route = (params.route || []).join("/");
  if (!kv) return J({ actif: false }, 503);
  const origin = new URL(request.url).origin;

  if (route === "cle") return J({ actif: true, cle: (await cles(kv)).public });

  if ((route === "abonner" || route === "desabonner") && request.method === "POST") {
    if (await limite(request, "push-" + route, 10, 600)) { await noter(kv, request, "trop_de_requetes", route); return J({ ok: false }, 429, { "retry-after": "600" }); }
    if (+(request.headers.get("content-length") || 0) > 4096) { await noter(kv, request, "requete_trop_grosse", route); return J({ ok: false }, 413); }
  }
  if (route === "abonner" && request.method === "POST") {
    const s = await request.json().catch(() => null);
    if (!s || !endpointValide(s.endpoint)) {
      await noter(kv, request, "abonnement_refuse", s && typeof s.endpoint === "string" ? s.endpoint : "corps invalide");
      return J({ ok: false }, 400);
    }
    await kv.put(await idAb(s.endpoint), JSON.stringify({ endpoint: s.endpoint, t: Date.now() }));
    return J({ ok: true });
  }
  if (route === "desabonner" && request.method === "POST") {
    const s = await request.json().catch(() => null);
    if (s && endpointValide(s.endpoint)) await kv.delete(await idAb(s.endpoint));
    return J({ ok: true });
  }
  if (route === "derniere") {
    return J((await kv.get("derniere", "json")) || { titre: "YH Physique-Chimie", corps: "Nouveautés sur le site", url: "/" });
  }
  if (route === "stats") {
    let n = 0, cur;
    for (let i = 0; i < 10; i++) { const l = await kv.list({ prefix: "s:", cursor: cur }); n += l.keys.length; if (l.list_complete) break; cur = l.cursor; }
    return J({ abonnes: n });
  }
  if (route === "tick") {
    // Appelé à chaque visite ; au plus une vérification toutes les 3 minutes (cache, sans écriture KV).
    const c = caches.default, key = new Request(origin + "/__push_tick");
    if (await c.match(key)) return new Response(null, { status: 204 });
    await c.put(key, new Response("1", { headers: { "cache-control": "max-age=180" } }));
    waitUntil((async () => { if (!(await kv.get("envoi"))) await verifier(kv, origin); await lot(kv); })());
    return new Response(null, { status: 204 });
  }
  return J({ erreur: "inconnu" }, 404);
}
