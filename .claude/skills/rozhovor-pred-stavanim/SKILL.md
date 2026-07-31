---
name: rozhovor-pred-stavanim
description: Rozhovor pred stavaním namiesto hádania zadania. POVINNE použi túto zručnosť skôr, než začneš stavať čokoľvek, čo má viac než jednu overiteľnú vlastnosť — aplikáciu, web, landing page, kalkulačku, kvíz, databázu otázok, dokument, dátovú sadu, skript, workflow, automatizáciu alebo prezentáciu. Použi ju aj vtedy, keď o ňu používateľ nepožiada výslovne. Nepoužívaj ju pri faktických otázkach, vysvetleniach, krátkych úpravách existujúceho kódu ani vtedy, keď používateľ zadanie už sám podrobne rozpísal vrátane obmedzení.
---

# Rozhovor pred stavaním

Táto zručnosť rieši jediný problém: **postavím presne to, čo bolo napísané, a nie to, čo používateľ naozaj chcel** — a zistí sa to až po hodine práce.

Nie je to o opatrnosti. Je to o tom, že zadanie v jednej vete nikdy neobsahuje všetko podstatné.

---

## Základné pravidlo

> **Skôr než sa dotknem prvého súboru, musím vedieť vysvetliť vlastnými slovami, čo staviam a prečo.**

Ak to vysvetliť neviem, ešte nemám dosť informácií. Vtedy sa pýtam, nie kódujem.

---

## Kedy sa spúšťa

**Áno** — čokoľvek s viac než jednou overiteľnou vlastnosťou:
aplikácia, web, landing page, kalkulačka, kvíz, databáza otázok, dokument, dátová sada, skript, workflow, automatizácia, prezentácia, väčšia prepracovaná šablóna.

**Nie** — rozhovor by len zdržoval:
faktické otázky, vysvetlenia, krátke úpravy existujúceho textu či kódu, jednorazové odpovede, príkazy so lomítkom, a prípady, keď používateľ zadanie sám podrobne rozpísal vrátane obmedzení.

Pri pochybnosti sa rozhovor **spúšťa**. Jedna otázka navyše stojí menej než hodina zle postavenej práce.

---

## Ako sa pýtať

**Vždy len jednu otázku naraz. Potom počkaj na odpoveď.**

Zoznam piatich otázok naraz nie je rozhovor, je to dotazník. Používateľ na polovicu neodpovie a zvyšok odpovie povrchne. Jedna otázka dostane skutočnú odpoveď a tá často zmení aj to, na čo sa oplatí pýtať ďalej.

Pýtaj sa na to, čo **reálne zmení výsledok**. Nie na formality, ktoré si vieš domyslieť alebo ktoré sa dajú doladiť neskôr.

Ak odpoveď už zaznela v konverzácii alebo sa dá spoľahlivo odvodiť z projektu, **nepýtaj sa na ňu znova**.

---

## Čo musí byť na konci jasné

| # | Oblasť | Čo potrebujem vedieť |
|---|--------|----------------------|
| 1 | **Cieľ** | Na čo to má slúžiť, kto to bude používať, ako vyzerá úspech |
| 2 | **Obmedzenia** | Mobil či desktop, technológie, čas, kde to pobeží, čo sa nesmie zmeniť |
| 3 | **Hraničné prípady** | Čo sa má stať pri prázdnom, chybnom alebo extrémnom vstupe |
| 4 | **Slepé miesta** | Čo v zadaní chýba a používateľa to zatiaľ nenapadlo |

Štvrtý bod je najcennejší a zároveň sa naň najľahšie zabúda. Je to jediná časť, ktorú používateľ sám doplniť nevie — práve preto, že o nej nevie.

---

## Slepé miesta: hľadaj rozpor medzi formou a cieľom

Najhoršia chyba nie je zle postavená vec. Je to **správne postavená vec, ktorá nesplní cieľ**.

Typické prípady:

- Používateľ si vyžiada formát, ktorý zvolený nástroj nevie spracovať.
- Zadanie počíta s prostredím, ktoré používateľ nemá k dispozícii.
- Riešenie by zverejnilo údaje, ktoré majú zostať súkromné.
- Požadovaná funkcia už v projekte existuje pod iným názvom.
- Zadanie rieši príznak, nie príčinu.

Keď taký rozpor uvidíš, **povedz to hneď a priamo**, ešte pred ďalšími otázkami. Nie je to spochybňovanie zadania, je to jediná vec, ktorú vieš prispieť skôr, než sa začne pracovať.

---

## Záver rozhovoru

Keď máš jasno, **zhrň vlastnými slovami**, čo ideš postaviť:

- čo vznikne a v akej podobe
- čo tam vedome **nebude**
- ako sa výsledok dostane tam, kde ho treba

Potom **počkaj na výslovné OK**. Nie na „hej", ktoré sa dá vyložiť ako súhlas s niečím iným, ale na jasné potvrdenie zhrnutia.

Až potom stavaj.

---

## Nadväznosť

Po dokončení práce nasleduje zručnosť **`kontrolovana-slucka`** — overenie dôkazom namiesto sebahodnotenia.

Rozhovor je **prevencia pred** stavaním.
Kontrolovaná slučka je **overenie po** ňom.

Pri väčšej úlohe patria obe. Jedna bez druhej necháva polovicu rizika neošetrenú.

---

## Zhrnutie v jednej vete

Pýtaj sa po jednej otázke, kým nemáš jasno v cieli, obmedzeniach, hraničných prípadoch a slepých miestach; potom zhrň, počkaj na OK a až vtedy stavaj.
