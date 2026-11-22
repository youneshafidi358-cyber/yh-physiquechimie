// Ville / région approximatives du visiteur (géolocalisation de Cloudflare d'après l'adresse IP). Rien n'est stocké ici.
export async function onRequestGet({ request }) {
  const cf = request.cf || {};
  return new Response(JSON.stringify({ ville: cf.city || "", region: cf.region || "", pays: cf.country || "" }), {
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "private, max-age=3600" },
  });
}
