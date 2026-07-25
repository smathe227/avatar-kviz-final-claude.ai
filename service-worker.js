// ════════════════════════════════════════════════
// AVATAR KVÍZ — SERVICE WORKER
// Stratégia:
//   • HTML (index.html)  → NAJPRV SIEŤ, cache len ako záloha keď nie je internet.
//     Vďaka tomu sa po nahratí novej verzie na GitHub appka vždy aktualizuje.
//   • Obrázky, ikony     → NAJPRV CACHE (menia sa zriedka, načítajú sa okamžite).
// ════════════════════════════════════════════════
const VERSION = "v8";
const CACHE_NAME = "avatar-kviz-" + VERSION;

const ASSETS = [
  "./",
  "index.html",
  "manifest.webmanifest",
  "avatar-assets/app-icon-192.png",
  "avatar-assets/app-icon-512.png",
  "avatar-assets/avatar_01.jpg",
  "avatar-assets/avatar_02.jpg",
  "avatar-assets/avatar_03.jpg",
  "avatar-assets/avatar_04.jpg",
  "avatar-assets/avatar_05.jpg",
  "avatar-assets/avatar_06.jpg",
  "avatar-assets/avatar_07.jpg",
  "avatar-assets/avatar_08.jpg",
  "avatar-assets/avatar_09.jpg",
  "avatar-assets/avatar_10.jpg",
  "avatar-assets/avatar_11.jpg",
  "avatar-assets/avatar_12.jpg",
  "avatar-assets/avatar_13.jpg",
  "avatar-assets/avatar_14.jpg",
  "avatar-assets/avatar_15.jpg",
  "avatar-assets/avatar_16.webp",
  "avatar-assets/avatar_17.jpg",
  "avatar-assets/avatar_18.jpg",
  "avatar-assets/avatar_19.jpg",
  "avatar-assets/avatar_20.jpg",
  "avatar-assets/avatar_21.jpg",
  "avatar-assets/avatar_22.jpg",
  "avatar-assets/avatar_23.jpg",
  "avatar-assets/avatar_24.jpg",
  "avatar-assets/avatar_25.jpg",
  "avatar-assets/avatar_26.jpg",
  "avatar-assets/avatar_27.jpg",
  "avatar-assets/avatar_28.jpg",
  "avatar-assets/avatar_29.jpg",
  "avatar-assets/avatar_30.jpg",
  "avatar-assets/avatar_31.jpg",
  "avatar-assets/avatar_32.jpg",
  "avatar-assets/avatar_33.jpg",
  "avatar-assets/avatar_34.jpg",
  "avatar-assets/avatar_35.jpg",
  "avatar-assets/avatar_36.jpg",
  "avatar-assets/avatar_37.jpg",
  "avatar-assets/avatar_38.jpg",
  "avatar-assets/avatar_39.jpg",
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
