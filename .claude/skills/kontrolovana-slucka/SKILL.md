---
name: kontrolovana-slucka
description: Pracovná slučka s dôkazom namiesto sebahodnotenia. POVINNE použi túto zručnosť vždy, keď ide o väčšiu alebo zložitejšiu úlohu — tvorbu či úpravu aplikácie, webu, kvízu, kalkulačky, databázy otázok, dokumentu alebo dátovej sady — a vždy, keď používateľ žiada "hĺbkovú kontrolu", "prekontroluj to poriadne", "oprav čo treba", "sprav to poriadne", "finálnu verziu", "deep check", "review", "audit", alebo keď sa v predchádzajúcich kolách opakovane objavovali nové chyby. Použi ju aj vtedy, keď o ňu používateľ nepožiada výslovne, ale úloha má viac než jednu overiteľnú vlastnosť.
---

# Kontrolovaná slučka: dôkaz, nie pocit

Táto zručnosť rieši jediný konkrétny problém: **model si sám skontroluje vlastnú prácu, sám sa vyhlási za úspešného a používateľ potom nájde chyby, ktoré mal nájsť model.**

Nie je to o väčšej snahe. Je to o tom, oddeliť *robenie* od *dokazovania*.

---

## Základné pravidlo

> **Úspech neurčuje moje zhrnutie. Určuje ho dôkaz, ktorý sa nedá „ukecať".**

Keď neviem výsledok odmerať, nesmiem o ňom tvrdiť, že je hotový. Namiesto toho zúžim úlohu, kým ho odmerať neviem — alebo otvorene poviem, čo overené nie je.

---

## Pred prvým krokom navrhni slučku

Nikdy nezačínaj prácou. Najprv nahlas zodpovedz šesť otázok. Ak niektorú nevieš vysvetliť dvomi vetami, úloha ešte nie je pripravená.

| # | Otázka | Čo musí byť jasné |
|---|--------|-------------------|
| 1 | **Cieľ** | Čo má po skončení platiť? Jedna veta, overiteľná. |
| 2 | **Rozsah** | Čoho sa smiem dotknúť a čoho určite nie. |
| 3 | **Akcia** | Konkrétne kroky v poradí. Nikdy „vylepši to". |
| 4 | **Dôkaz** | Príkaz, skript alebo kontrola, ktorá vráti áno/nie. |
| 5 | **Rozpočet** | Max. počet kôl. Bez limitu slučku nespúšťaj. |
| 6 | **Report** | Čo sa zmenilo, čo prešlo, **čo overené nebolo**. |

Návrh ukáž používateľovi **skôr**, než začneš meniť súbory. Pri rozsiahlych alebo nevratných zásahoch si vyžiadaj súhlas.

---

## Cyklus

```
UROB KROK  →  OVER DÔKAZOM  →  ROZHODNI  →  ZOPAKUJ
```

Zastav sa, keď:
- dôkaz prejde **úplne** (nie „skoro"), alebo
- minie sa rozpočet kôl, alebo
- dve kolá po sebe neprinesú žiadnu zmenu.

Po vyčerpaní rozpočtu **neklam o výsledku**. Napíš, čo zostáva nevyriešené.

---

## Tri zakázané vety

Tieto formulácie signalizujú, že hodnotím sám seba. Nepoužívaj ich bez podkladu:

1. ❌ **„Skontroloval som to, je to v poriadku."** → Čím konkrétne? Ukáž výstup.
2. ❌ **„0 chýb, kompletne overené."** → Kompletne podľa akého zoznamu kontrol?
3. ❌ **„Toto je finálna verzia."** → Finálnosť vyhlasuje používateľ, nie ja.

**Namiesto toho vždy uveď dve veci:**
- ✅ **Čo som overil** — menovite, s výsledkom
- ✅ **Čo som neoveril** — a prečo (napr. „appku nevidím, vizuál musíš skontrolovať ty")

Druhá časť je dôležitejšia. Bez nej používateľ netuší, kde ešte hrozí riziko.

---

## Skript nájde len to, čo ťa napadlo hľadať

Toto je najčastejší dôvod, prečo sa chyby objavujú kolo za kolom.

Automatická kontrola je nutná, ale **nikdy nie postačujúca**. Preto pri práci s obsahom (otázky, texty, dáta, preklady) platí:

> **Aspoň raz prejdi všetky položky očami, nielen skriptom.**

Ak je položiek priveľa, prečítaj reprezentatívnu vzorku z **každej** kategórie a povedz, akú časť si čítal.

Typické chyby, ktoré skript neodhalí, ale čítanie áno:
- otázka obsahuje vlastnú odpoveď („Čo robíme, keď povieme ďakujem?" → „Poďakujeme")
- vecná nezmyselnosť pri formálne správnej štruktúre
- nesúlad rodu, osoby alebo štýlu
- odpoveď, ktorá je tiež správna, hoci je označená ako nesprávna

---

## Čo nevidím a musím to priznať

Nevidím vykreslenú stránku. Pracujem s kódom, nie s obrazovkou. **Nikdy netvrď, že vizuál je overený.**

Vždy, keď výsledok obsahuje rozhranie, výslovne napíš:
> „Vizuál a používanie som overiť nemohol — to je na tebe."

A požiadaj o screenshot alebo krátke otestovanie.

---

## Podrobnosti

Pri konkrétnej práci si načítaj podľa potreby:

- **`references/kontrolny-zoznam.md`** — zoznam reálnych chýb, ktoré sa opakovane objavujú vo webových appkách, kvízoch a databázach otázok. Prejdi ho pred vyhlásením akejkoľvek hotovosti.
- **`references/navrh-slucky.md`** — šablóna návrhu slučky na vyplnenie a ukážky dobrých vs. zlých zadaní.
- **`scripts/over_html_appku.py`** — pripravený overovací skript pre jednosúborové HTML aplikácie: syntax, prepojenia ID, odkazy na súbory, funkcie volané z onclick. Spusti ho a **jeho výstup má prednosť pred mojím dojmom**.

---

## Zhrnutie v jednej vete

Navrhni slučku, urob krok, dokáž ho merateľne, priznaj čo si nedokázal, a opakuj len v rámci rozpočtu.
