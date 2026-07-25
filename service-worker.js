// ════════════════════════════════════════════════
// AVATAR KVÍZ — SERVICE WORKER
// Stratégia:
//   • HTML (index.html)  → NAJPRV SIEŤ, cache len ako záloha keď nie je internet.
//     Vďaka tomu sa po nahratí novej verzie na GitHub appka vždy aktualizuje.
//   • Obrázky, ikony     → NAJPRV CACHE (menia sa zriedka, načítajú sa okamžite).
// ════════════════════════════════════════════════
const VERSION = "v4";
const CACHE_NAME = "avatar-kviz-" + VERSION;

const ASSETS = [
  "./",
  "index.html",
  "manifest.webmanifest",
  "avatar-assets/app-icon.svg",
  "avatar-assets/app-icon-192.png",
  "avatar-assets/app-icon-512.png",
  "avatar-assets/pandora-01.svg",
  "avatar-assets/pandora-02.svg",
  "avatar-assets/pandora-03.svg",
  "avatar-assets/pandora-04.svg",
  "avatar-assets/pandora-05.svg",
  "avatar-assets/pandora-06.svg",
  "avatar-assets/pandora-07.svg",
  "avatar-assets/pandora-08.svg"
];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(ASSETS))
      .catch(() => {})   // keď je jeden súbor nedostupný, inštalácia nespadne
  );
  self.skipWaiting();
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", event => {
  const req = event.request;
  if (req.method !== "GET") return;

  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;   // cudzie domény nechaj tak

  const isHTML = req.mode === "navigate" ||
                 (req.headers.get("accept") || "").includes("text/html");

  if (isHTML) {
    // NAJPRV SIEŤ — vždy najnovšia verzia appky
    event.respondWith(
      fetch(req)
        .then(res => {
          const copy = res.clone();
          caches.open(CACHE_NAME).then(c => c.put(req, copy)).catch(() => {});
          return res;
        })
        .catch(() => caches.match(req).then(r => r || caches.match("index.html")))
    );
    return;
  }

  // NAJPRV CACHE — obrázky a ikony
  event.respondWith(
    caches.match(req).then(cached => {
      if (cached) return cached;
      return fetch(req).then(res => {
        const copy = res.clone();
        caches.open(CACHE_NAME).then(c => c.put(req, copy)).catch(() => {});
        return res;
      });
    })
  );
});
