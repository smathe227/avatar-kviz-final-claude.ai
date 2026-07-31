---
name: vyvojovy-stack
description: Vrstvený postup práce na tomto projekte — poradie krokov od kontextu cez plán a implementáciu až po dizajnový audit. Použi vždy, keď ide o nový feature, väčšiu úpravu Avatar Kvízu, zásah do vzhľadu alebo rozhodnutie o architektúre. Použi aj vtedy, keď sa má inštalovať akákoľvek nová zručnosť, plugin alebo knižnica — obsahuje povinné bezpečnostné kontroly. Nepoužívaj pri triviálnych jednoriadkových opravách.
---

# Vývojový stack: poradie pred rýchlosťou

Destilát guidu *„5 Claude Code Skills"* (Synvii AI, 29. 7. 2026), prispôsobený tomuto projektu.

**Základná myšlienka guidu:** problém zvyčajne nie je v modeli, ale v tom, že sa od neho čaká konzistentný výsledok bez konzistentného procesu. Zručnosti nezvyšujú inteligenciu — znižujú improvizáciu.

---

## Deľba práce medzi zručnosťami

Tieto zručnosti sa **nesmú prekrývať**. Každá vlastní inú fázu:

| Fáza | Zručnosť | Čo vlastní |
|---|---|---|
| PRED | **`rozhovor-pred-stavanim`** | Zisťovanie zadania. Jedna otázka naraz, cieľ, obmedzenia, hraničné prípady, slepé miesta, zhrnutie a čakanie na OK. |
| POČAS | **`vyvojovy-stack`** (táto) | Poradie vrstiev, dizajnová disciplína, hygiena kontextu, bezpečnosť pri inštalácii. |
| PO | **`kontrolovana-slucka`** | Dokazovanie hotovosti. Návrh slučky, merateľný dôkaz, rozpočet kôl, priznanie neovereného. |

**Táto zručnosť nezisťuje zadanie ani nedokazuje hotovosť.** Keď treba vyjasniť, čo sa vlastne stavia, odovzdaj slovo `rozhovoru-pred-stavaním`. Keď treba overiť výsledok, odovzdaj ho `kontrolovanej-slučke`. Nevymýšľaj vlastnú verziu ani jedného.

---

## Poradie vrstiev

```
ROZHOVOR → KONTEXT → PLÁN → (medzera?) → IMPLEMENTÁCIA → DÔKAZ → DIZAJN → POZOROVANIE
```

1. **Rozhovor** — patrí `rozhovoru-pred-stavaním`. Bez jasného zadania nepokračuj.
2. **Kontext** — načítaj len fakty, ktoré menia toto rozhodnutie. Nie celú históriu projektu.
3. **Plán** — kroky v poradí a acceptance criteria. Vychádza zo zhrnutia odsúhlaseného v rozhovore.
4. **Medzera** — ak plán odhalí odbornú dieru, hľadaj zručnosť. Inštaluj až po kontrole (viď nižšie).
5. **Implementácia** — po malých úlohách, každá ukončená dôkazom.
6. **Dôkaz** — odovzdaj `kontrolovanej-slučke`.
7. **Dizajn** — až keď funkčnosť a informačná architektúra sedia. Nikdy namiesto nich.
8. **Pozorovanie** — čo si opakovane opravoval? Navrhni najviac **jednu** testovateľnú zmenu.

### Kedy vrstvy preskočiť

| Situácia | Postup |
|---|---|
| Malá úprava | Krátky plán + dôkaz. Discovery a dizajn preskoč. |
| Nový feature | Celý reťazec. |
| Zmena vzhľadu | Brief → informačná architektúra → funkčnosť → až potom dizajnový audit. |
| Opakovaná chyba | Nájdi koreň, nie symptóm. Zaznamenaj vzor. |

---

## Dizajnová disciplína

**„Urob to krajšie" je slabé zadanie.** Pred zásahom do vzhľadu musí byť jasné: používateľ, kontext použitia, emócia, hustota informácií, zariadenie a **čo musí zostať nezmenené**.

Rozlišuj dva typy povrchu:

- **Brand surface** — landing page, portfólio. Cieľom je dojem.
- **Product surface** — dashboard, nástroj, hra. Cieľom je, aby používateľ rýchlo pochopil ďalší krok.

*Avatar Kvíz je product surface pre 6-ročné dieťa.* Priorita: veľké dotykové ciele, vysoký kontrast, jednoznačná spätná väzba po odpovedi, žiadny text, ktorý dieťa nedokáže prečítať. Dekorácie až na poslednom mieste.

Štyri režimy práce s vizuálom, v tomto poradí:

1. **Audit** — pomenuj problémy a vysvetli, prečo rozhranie nepôsobí dobre.
2. **Critique** — širší pohľad vrátane hierarchie a používateľského toku.
3. **Distill** — odstráň preplnenie a prvky, ktoré robia priveľa naraz.
4. **Polish** — zjednoť spacing, typografiu a detaily. **Až keď je štruktúra správna.**

---

## Pred inštaláciou čohokoľvek: 4 kontroly

Zručnosť je súbor inštrukcií a niekedy aj spustiteľných skriptov. Beží s plnými oprávneniami agenta.

| # | Kontrola |
|---|---|
| 1 | **Autor a reputácia** repozitára |
| 2 | **Dátum poslednej aktualizácie** |
| 3 | **Obsah `SKILL.md` a všetkých priložených skriptov** |
| 4 | **Rozsah oprávnení** — nežiada zbytočne široký prístup, sieť alebo shell? |

Ďalšie pravidlá:
- Nikdy neinštaluj prvý výsledok vyhľadávania bez kontroly.
- Neinštaluj viac vecí naraz — pri chybe nebudeš vedieť ktorá ju spôsobila.
- API kľúče a heslá patria do premenných prostredia. Nikdy do promptov, `CLAUDE.md`, pamäte ani logov.
- Aktualizácie neinštaluj slepo — nová verzia môže zmeniť hooky a správanie.
- **Viac zručností často znamená viac konfliktov.** Malý overený stack je lepší než dvadsať náhodných.

---

## Hygiena kontextu

> Načítaj iba fakty, ktoré menia aktuálne rozhodnutie.

Vkladať celú históriu projektu do jedného promptu zhoršuje rozhodovanie, nie zlepšuje. Postupuj od stručného indexu k plnému detailu len pri záznamoch, ktoré s úlohou naozaj súvisia.

Rozdeľ si zdroje:
- **`CLAUDE.md`** — stabilné pravidlá: stack, architektúra, pomenovania, zakázané postupy. Udržiavaš vedome a stručne.
- **Priebežná pamäť** — čo sa riešilo, aké rozhodnutie padlo, čo sa pokazilo. Rastie sama.

Citlivé údaje do pamäte nepatria.

---

## Kontext tohto projektu

- **Avatar Kvíz** — jednosúborová HTML aplikácia (`index.html`, ~157 kB) + service worker + PWA manifest. Hra pre dcéru Rebeku.
- Žiadny build systém, žiadne závislosti. Zmeny idú priamo do `index.html`.
- **Majiteľ nie je programátor a pracuje výlučne na mobile.** Nenavrhuj riešenia vyžadujúce terminál, Node.js ani lokálny build.
- Komunikuj po slovensky. Vysvetli **prečo**, nielen čo.
- Vizuál overiť nedokážeš — vždy si vyžiadaj screenshot alebo otestovanie.

---

## Realistické očakávanie

Tento postup nespraví z agenta autonómneho vývojára, ktorý nepotrebuje kontrolu. Spraví jeho správanie predvídateľnejším a zníži počet zbytočných opráv. Nič viac sa nesľubuje.
