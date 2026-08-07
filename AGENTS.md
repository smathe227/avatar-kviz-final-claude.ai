# AGENTS.md — Avatar tréningový kvíz

Pokyny pre agentov (Codex CLI, Claude Code a podobne), ktorí pracujú v tomto
repozitári. Čítaj to skôr, než začneš čokoľvek meniť.

## Čo to je

Vzdelávací kvíz pre šesťročné dieťa — matematika, všeobecný prehľad a film
Avatar. Beží ako PWA (dá sa nainštalovať na telefón), celý v slovenčine, s
hlasovým čítaním otázok aj hlasovým odpovedaním.

**Cieľová používateľka je dieťa.** To je najdôležitejší kontext pre každé
rozhodnutie: veľké tlačidlá, žiadne trestanie za chybu, žiadna akcia bez
potvrdenia, texty jednoduché a v ženskom rode (appka oslovuje dievča).

## Rýchly štart

Žiadny build, žiadne závislosti, žiadny `package.json`, žiadne testy.

```bash
python3 -m http.server 8000
# potom http://localhost:8000
```

Cez `file://` to **nefunguje** — service worker aj `localStorage` potrebujú
skutočný origin. Nasadzuje sa cez GitHub Pages z vetvy `main`; push do `main`
je nasadenie.

## Mapa súborov

| Súbor | Čo v ňom je |
|---|---|
| `index.html` | **Celá aplikácia** — 2350 riadkov, štýly + markup + logika |
| `service-worker.js` | Cache stratégia, konštanta `VERSION` |
| `manifest.webmanifest` | PWA metadáta, ikony, `lang: sk` |
| `avatar-assets/avatar_01..39` | Obrázky do puzzle (39 súborov) |
| `avatar-assets/app-icon-*` | Ikony aplikácie (bežné + maskable) |

Nepoužité pozostatky, ktoré na nič neodkazujú: `pandora-01..08.svg` (v koreni
aj v `avatar-assets/`) a `app-icon-192.png` / `app-icon-512.png` **v koreni** —
`index.html` aj manifest berú ikony z `avatar-assets/`. Nemaž ich len tak popri
inej práci; ak ich treba upratať, nech je to samostatná zmena.

## Štruktúra `index.html`

Riadky sú orientačné — po väčšej úprave už sedieť nebudú.

| Riadky | Obsah |
|---|---|
| 17–443 | `<style>` — celá grafika, tmavá paleta, ohnivé pozadie |
| 445–589 | markup — brána, ovládanie, puzzle, otázka, koniec |
| 591–679 | konštanty a stav (`QUIZ_*`, `POINTS`, `STAGES`, `SKIP_LIMIT`) |
| 680–1258 | **banka otázok** — `buildMathQuestions` (757), `buildGeneralQuestions` (924), `buildAvatarQuestions` (1107), `assignDifficulty` (1238) |
| 1260–1297 | zostavenie kvízu — `takeBalanced`, `composeQuiz` |
| 1298–1356 | puzzle a ukazovatele postupu |
| 1357–1552 | hlas von (TTS) — výber hlasu, čísla na slová, `readFull` |
| 1553–1813 | hlas dnu — rozpoznávanie reči, `matchVoiceAnswer` |
| 1814–2018 | vykreslenie otázky, vyhodnotenie, koncová obrazovka |
| 2019–2114 | ukladanie stavu a história úspešnosti |
| 2115–2350 | štart, preskočenie, reset, koniec |

## Banka otázok

500 otázok sa generuje pri načítaní (`buildQuestionBank()`), neexistuje ako
dátový súbor. Rozdelenie: **matematika 272, svet okolo nás 146, Avatar 82**,
naprieč 36 okruhmi (`skill`).

Jeden kvíz má **30 otázok** — 12 matematika, 11 všeobecné, 7 Avatar. Poradie
kategórií určuje pevné pole `pattern` v `composeQuiz()`; jeho dĺžka aj počty
musia sedieť s `QUIZ_MATH` / `QUIZ_GEN` / `QUIZ_AVA`, inak sa kvíz skráti.

Otázky sa pridávajú cez pomocníkov, nie ručným písaním objektov:

```js
addMath(list, "Mala si 3 jabĺčka…", 3, "+", 2, 5, "sčítanie", null, "vysvetlenie");
addPic(list, "gen", "Otázka?", null, "Správna", [[null,"Zlá 1"],[null,"Zlá 2"]], "okruh", null, "vysvetlenie");
```

Náročnosť (`ľahšia` 5 b / `stredná` 10 b / `výzva` 15 b) neurčuješ ručne —
priradí ju `assignDifficulty()` podľa okruhu (`DIFF_BY_SKILL`), s výnimkami
v `DIFF_EASY_HINTS` / `DIFF_HARD_HINTS`. Nový okruh preto **musí** pribudnúť do
`DIFF_BY_SKILL`, inak spadne do „stredná".

Každá skupina končí `uniqueByQ(list).slice(0, N)` — deduplikácia podľa textu
otázky. Stropy (320 / 175 / 125) sú vyššie než reálny výsledok, takže pridané
otázky sa neztratia; keby si sa k stropu priblížil, zdvihni ho.

## Čo sa nesmie rozbiť

Toto sú opravy skutočných chýb. Komentáre v kóde vysvetľujú prečo — nemaž ich.

**Verzia cache.** Pri každej zmene, ktorá sa má dostať k používateľke, zdvihni
`VERSION` v `service-worker.js` (teraz `v12`). Bez toho môže telefón ďalej
servírovať staré súbory.

**Epocha čítania (`ttsEpoch`).** Čítanie otázky je asynchrónny cyklus. Keď
dieťa klikne v polovici čítania, starý cyklus sa musí ticho ukončiť —
inak sa dva cykly navzájom rušia a hlas drmolí. Nepridávaj do čítania `await`
bez kontroly epochy.

**`currentOptions`.** Možnosti sa držia ako objekty. Neskladaj ich späť z HTML —
takto sa kedysi strácal príznak `correct` a hlasom povedaná správna odpoveď sa
vyhodnotila ako chyba.

**`AVATAR_IMAGES`.** Zo 39 súborov je v zozname len 21 — zvyšok sú duplikáty.
Nedopĺňaj tam chýbajúce čísla, puzzle by ukazovalo tú istú fotku dvakrát
po sebe.

**Potvrdzovanie (`confirmClick`).** Reset, Koniec a Preskočiť potrebujú dve
kliknutia do 2 sekúnd. Dieťa si tak nezmaže rozohranú hru. Nové deštruktívne
tlačidlo napoj rovnako.

**Limit preskočení.** `SKIP_LIMIT = 5` na kvíz — bez neho sa dá preklikať celý
kvíz bez odpovedania.

**Prvé spustenie neťahá všetky fotky.** Service worker pri inštalácii sťahuje
len `ZAKLAD` (bez `avatar_*`); puzzle obrázky pribúdajú do cache až keď sa
zobrazia. Nedávaj ich do `install`, na mobilných dátach by to bolo 39 fotiek
naraz.

**HTML ide najprv zo siete**, obrázky najprv z cache. Neprehadzuj to — appka by
sa prestala aktualizovať po nasadení.

## Konvencie

- **Všetko po slovensky** — texty v appke, názvy funkcií (`vyberDvaDistraktory`,
  `vazenyShuffle`, `zavriBranu`), komentáre aj správy commitov. Nepremenúvaj
  existujúce slovenské názvy na anglické.
- Komentáre vysvetľujú **prečo**, nie čo. Väčšina zaznamenáva konkrétnu chybu,
  ktorá sa opravovala. Zachovaj tento štýl.
- Matematické príbehy sú v druhej osobe, minulý čas, ženský rod („Mala si…").
- Štýl je inline v `<style>`, logika v jednom `<script>`. Nepridávaj build
  krok ani externé knižnice — appka musí fungovať offline z jedného súboru.
- `localStorage` kľúče: `avatarQuizStav` (rozohraná hra), `avatarQuizHistoria`
  (úspešnosť podľa okruhov, riadi vážený výber otázok), `avatarQuizBestScore`,
  `avatarQuizAutoMic`. Zmena tvaru uloženého stavu musí zniesť staré dáta —
  `loadState()` je preto v `try/catch`.

## Kontrola pred commitom

Testy neexistujú, takže over ručne:

1. Banka otázok sa poskladá a má očakávaný počet:
   ```bash
   node -e '
     globalThis.localStorage={getItem:()=>null,setItem:()=>{}};
     globalThis.document={getElementById:()=>({style:{},classList:{add(){},remove(){}}})};
     const fs=require("fs");
     const src=fs.readFileSync("index.html","utf8").split("\n").slice(590,1258).join("\n");
     eval(src+";console.log(QUESTIONS.length)");
   '
   ```
   Očakávaj 500 (alebo viac, ak si otázky pridal).
2. Appka nabehne cez `python3 -m http.server`, kvíz sa dá dohrať do konca.
3. Hlas prečíta otázku a rýchle preklikanie ho nezacyklí.
4. Ak si menil súbory, ktoré vidí používateľka — zdvihnutá `VERSION`.

Konzola prehliadača musí zostať bez chýb; appka veľa vecí polyká cez
`try/catch`, takže chyba sa nemusí prejaviť inak.

## Ako pracovať s repozitárom

- Vývoj na vetve, nie priamo do `main` — push do `main` znamená nasadenie.
- Správy commitov po slovensky, vecne, v štýle existujúcej histórie
  („Oprava hlasu, 500 otázok a 17 vylepšení kvízu").
- `index.html` je jeden veľký súbor; rob cielené úpravy a needituj ho ako celok,
  nech sú diffy čitateľné.
