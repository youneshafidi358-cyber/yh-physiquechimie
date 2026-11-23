/* Notifications YH Physique-Chimie */
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (e) => e.waitUntil(self.clients.claim()));
self.addEventListener("push", (e) => {
  e.waitUntil(fetch("/api/push/derniere", { cache: "no-store" }).then((r) => r.json()).catch(() => ({}))
    .then((m) => self.registration.showNotification(m.titre || "YH Physique-Chimie", {
      body: m.corps || "Nouveautés sur le site", icon: "/icon-192.png", badge: "/icon-96.png",
      data: { url: m.url || "/" },
      // Même message reçu deux fois = même tag : il remplace l'ancien sans sonner une deuxième fois.
      tag: "yh-" + (m.t || "nouveau"), renotify: false })));
});
self.addEventListener("notificationclick", (e) => {
  e.notification.close();
  const url = new URL((e.notification.data && e.notification.data.url) || "/", self.location.origin).href;
  e.waitUntil(self.clients.matchAll({ type: "window", includeUncontrolled: true }).then((cs) => {
    for (const c of cs) if (c.url === url && "focus" in c) return c.focus();
    return self.clients.openWindow(url);
  }));
});
