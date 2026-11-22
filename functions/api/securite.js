// Journal de sécurité : liste des tentatives bloquées des 30 derniers jours.
// Accès réservé : en-tête X-Stats-Key = le code des statistiques (variable secrète STATS_CLE).
import { limite, memeCle, noter } from "../../lib/securite.js";

const J = (o, s = 200, h = {}) => new Response(JSON.stringify(o), {
  status: s, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", ...h },
});

export async function onRequestGet({ request, env }) {
  const kv = env.ABONNES;
  if (!kv || !env.STATS_CLE) return J({ erreur: "non configuré" }, 503);
  // Contre les essais de code en série : 20 lectures max par IP et par 15 minutes.
  if (await limite(request, "sec-lecture", 20, 900)) { await noter(kv, request, "code_force_brute"); return J({ erreur: "trop d'essais" }, 429, { "retry-after": "900" }); }
  if (!memeCle(request.headers.get("x-stats-key"), env.STATS_CLE)) {
    await noter(kv, request, "code_incorrect", "lecture du journal de sécurité");
    return J({ erreur: "code incorrect" }, 401);
  }
  const jours = Math.min(30, Math.max(1, +new URL(request.url).searchParams.get("jours") || 30));
  const depuis = Date.now() - jours * 86400000;
  const liste = [];
  let cur;
  for (let i = 0; i < 5 && liste.length < 500; i++) {
    const l = await kv.list({ prefix: "sec:", cursor: cur, limit: 100 });
    for (const k of l.keys) if (k.metadata && k.metadata.t >= depuis) liste.push(k.metadata);
    if (l.list_complete || (l.keys.length && l.keys[l.keys.length - 1].metadata?.t < depuis)) break;
    cur = l.cursor;
  }
  return J({ jours, total: liste.length, tentatives: liste });
}
