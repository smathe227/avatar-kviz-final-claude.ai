---
name: bezpecny-kod
description: Použi vždy, keď sa píše alebo upravuje kód pre webovú appku (Avatar Kvíz, Mzdová kalkulačka, Korektor SK, Krúpy Alert, alebo čokoľvek nové), a vždy keď Števo žiada bezpečnostnú kontrolu alebo audit kódu. Ide o technický doplnok k všeobecnému pravidlu OWASP-style review; táto zručnosť obsahuje konkrétne kontrolné zoznamy a vzory útokov, ktoré treba blokovať.
---

# Bezpečné programovanie pre webové appky

Prístup bug huntera: kód sa píše tak, aby fungoval, a zároveň tak, aby sa nedal ľahko zneužiť. Nižšie sú kontrolné zoznamy podľa typu zraniteľnosti — technické termíny a názvy hlavičiek zostávajú v angličtine, lebo to sú presné reťazce, ktoré musia sedieť v kóde.

**Kontext:** appky, ktoré Števo stavia, sú väčšinou jednosúborové, bez backendu a bez prihlasovania. Nižšie uvedené sa použije v plnom rozsahu vtedy, keď appka pracuje s dátami používateľa, robí sieťové volania, alebo ukladá niečo citlivé. Pri jednoduchej klientskej appke (napríklad kvíz bez backendu) sa aplikuje len to, čo je relevantné — hlavne XSS, bezpečné zaobchádzanie s dátami v `localStorage`, a validácia vstupov.

---

## Základné zásady

- **Defense in depth** — nikdy sa nespoliehať na jednu jedinú ochranu
- **Fail securely** — keď niečo zlyhá, zlyhať smerom k zamietnutiu prístupu, nie k jeho povoleniu
- **Least privilege** — minimálne potrebné oprávnenia
- **Validácia vstupu** — nikdy never dôverovať vstupu od používateľa, validovať vždy na serveri (ak server existuje)
- **Kódovanie výstupu** — podľa kontextu, v ktorom sa dáta zobrazujú

---

## Prístupové práva

Pre každé dáta a akciu vyžadujúcu prihlásenie:

- Každý používateľ pristupuje len k vlastným dátam — overiť vlastníctvo na úrovni dát, nie len na úrovni cesty/route
- Používať UUID namiesto sekvenčných ID, aby sa dáta nedali uhádnuť
- Pri odobratí prístupu okamžite zneplatniť všetky tokeny a session

**Časté chyby:** IDOR (prístup k cudziemu záznamu cez jeho ID), eskalácia práv cez neoverenú zmenu roly, hromadné priradenie polí (`mass assignment` — appka prijme celé telo požiadavky vrátane polí, ktoré nemal používateľ meniť).

---

## XSS (Cross-Site Scripting)

Každý vstup, ktorý ovplyvňuje používateľ — priamo aj nepriamo — treba sanitizovať.

**Časté aj prehliadané zdroje:** formulárové polia, URL parametre, hlavičky (Referer, User-Agent), dáta z localStorage/sessionStorage ak sa vykresľujú, chybové hlášky, ktoré vracajú vstup späť, SVG súbory (môžu obsahovať JavaScript).

**Ochrana:**
- Kódovanie výstupu podľa kontextu (HTML, JS, URL, CSS) — používať vstavané escapovanie frameworku (React JSX a podobne)
- Content-Security-Policy hlavička, vyhýbať sa `'unsafe-inline'` a `'unsafe-eval'`
- Sanitizácia knižnicou (napríklad DOMPurify) pri HTML vstupe od používateľa
- `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`

---

## CSRF (Cross-Site Request Forgery)

Týka sa to appiek s backendom a prihlásením — pri čisto klientskych appkách bez servera nehrozí.

Každý endpoint, ktorý mení stav (POST, PUT, PATCH, DELETE), musí byť chránený:
- CSRF token viazaný na session, overovaný pri každej požiadavke
- `SameSite=Strict` alebo `Lax` na session cookies, v kombinácii s tokenom
- Validácia Origin/Referer hlavičky aj pri JSON API — content-type sám osebe CSRF nezabráni

---

## Citlivé dáta v klientskom kóde

Nikdy sa nesmie objaviť na strane klienta:
- API kľúče, connection stringy, JWT signing secrets, OAuth client secrets
- Celé čísla platobných kariet, heslá (aj hashované), plné telefónne čísla

**Kde sa citlivé dáta bežne skrývajú a treba to skontrolovať:** JavaScript bundle (vrátane source maps), HTML komentáre, skryté form polia, `data-` atribúty, initial state pri server-side renderingu, premenné typu `NEXT_PUBLIC_*`.

---

## Open Redirect

Ak appka prijíma URL na presmerovanie od používateľa:
- Allowlist povolených domén, alebo len relatívne cesty (nie plné URL)
- Pozor na obchádzky: `@` v URL (`https://legit.com@evil.com`), zdvojené kódovanie, Unicode homograf útoky (cyrilické znaky vyzerajúce ako latinka)

---

## Heslá

- Minimálne 8 znakov (odporúčaných 12+), bez umelého maxima
- Povoliť všetky znaky, nevynucovať konkrétne typy znakov
- Ukladať cez Argon2id, bcrypt alebo scrypt — nikdy MD5, SHA1 alebo čisté SHA256

---

## SSRF (Server-Side Request Forgery)

Ak appka robí požiadavky na URL zadanú alebo ovplyvnenú používateľom (webhooky, náhľady URL, sťahovanie súborov):
- Allowlist povolených domén je preferovaná ochrana
- Blokovať prístup k cloudovým metadata endpointom (`169.254.169.254` a podobné)
- Pri IP adresách si dať pozor na obchádzky — decimálny, oktálový a hexadecimálny zápis IP, IPv6 loopback, DNS rebinding

---

## Nahrávanie súborov

- Kontrolovať príponu AJ magic bytes súboru — nikdy sa nespoliehať len na jedno
- Premenovať súbor na náhodné UUID meno, ukladať mimo webroot
- Nastaviť `Content-Disposition: attachment` a `X-Content-Type-Options: nosniff`
- Pozor na SVG s vloženým JavaScriptom a na dvojité prípony (`shell.php.jpg`)

---

## SQL Injection

Ak appka pracuje s databázou:
- Parametrizované dotazy sú primárna obrana — nikdy neskladať SQL string spájaním s používateľským vstupom
- ORDER BY, názvy tabuliek a stĺpcov sa nedajú parametrizovať — tam nutne whitelist
- Databázový používateľ má mať len minimálne potrebné oprávnenia

---

## XXE a Path Traversal

**XXE** (ak appka parsuje XML, vrátane DOCX/XLSX/SVG, ktoré sú v skutočnosti XML): vypnúť spracovanie DTD a externých entít v XML parseri.

**Path Traversal** (ak appka pracuje s cestami k súborom podľa vstupu): nikdy neskladať cestu priamym spojením s používateľským vstupom, kanonikalizovať a overiť, že výsledná cesta ostáva v rámci povoleného adresára.

---

## Bezpečnostné hlavičky (ak appka beží na serveri)

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Content-Security-Policy: (podľa sekcie XSS vyššie)
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
```

---

## JWT

- Vždy explicitne overiť algoritmus pri verifikácii, nikdy ho nepreberať z hlavičky tokenu
- Odmietnuť `alg: none`
- Secret aspoň 256 bitov náhodných dát, nie heslo ani fráza
- Token v httpOnly, Secure, SameSite=Strict cookie — nikdy v localStorage

---

## Všeobecné zásady pri generovaní kódu

1. Validovať všetok vstup na serveri, nikdy sa nespoliehať len na klientsku validáciu
2. Parametrizované dotazy, nikdy spájanie reťazcov
3. Kódovať výstup podľa kontextu
4. Overovať autentifikáciu na každom endpointe, nielen na úrovni routingu
5. Overovať, že používateľ smie pristupovať práve k tomuto konkrétnemu záznamu
6. Bezpečné predvolené hodnoty
7. Chybové hlášky nesmú prezradiť stack trace ani interné detaily
8. Pri neistote zvoliť reštriktívnejšiu, bezpečnejšiu možnosť a poznačiť to v komentári

## Zdroj

Slovenská adaptácia zručnosti `VibeSec-Skill` (repozitár `BehiSecc/VibeSec-Skill`, licencia **Apache-2.0**, 1,1 tis. hviezdičiek). Prevzatý bol celý obsah bez skrátenia významu, len preložený a doplnený o kontext appiek bez backendu.

Overené 8.8.2026 priamo na GitHube: repozitár existuje, hviezdičky sedia, `SKILL.md` v ňom je. **Licencia je Apache-2.0, nie MIT** — pôvodná verzia tohto textu uvádzala MIT, opravené podľa súboru `LICENSE` v repozitári. Údaj „5+ rokov v bug bounty" pochádza z README samotného autora, nedá sa nezávisle overiť — ber ho ako tvrdenie autora, nie ako fakt.
