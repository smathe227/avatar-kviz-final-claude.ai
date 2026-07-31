# Kontrolný zoznam — chyby, ktoré sa reálne opakujú

Zostavené z konkrétnych chýb nájdených pri stavbe detského kvízu, mzdovej kalkulačky
a textového korektora. **Nie sú vymyslené — každá z nich sa skutočne stala** a väčšinu
z nich odhalil až používateľ, nie automatická kontrola.

Prejdi tento zoznam **skôr**, než vyhlásiš čokoľvek za hotové.

---

## A · Kvízy a databázy otázok

### A1 · Ikona prezrádza odpoveď ⚠️ najzávažnejšie
Správna odpoveď má výstižnú ikonku, nesprávne majú otáznik alebo výplň.
Dieťa uhádne bez znalosti.

**Kontrola:** má správna odpoveď inú ikonu než *všetky* nesprávne?
**Pravidlo:** buď rovnaká ikona na všetkých možnostiach, alebo každá ikona
zodpovedá **svojmu vlastnému textu** (mačka pri „Mačka", krava pri „Krava").

Varianty tej istej chyby:
- číslica nad rovnakou číslicou v texte (`7️⃣` nad „7 dní")
- ikona napovedá poradie (`2️⃣` pri odpovedi „Utorok")
- ikona doslova zobrazuje odpoveď (🌈 pri „veľa farieb")

### A2 · Otázka obsahuje vlastnú odpoveď
„Čo robíme, keď niekomu povieme **ďakujem**?" → „Poďakujeme"
Používateľ sa nič nenaučí.

**Kontrola:** obsahuje text otázky koreň správnej odpovede?
Pozor na falošné poplachy pri formáte „A alebo B?" — tam je to v poriadku.

### A3 · Nesprávna odpoveď je tiež správna
Napr. „Čo poháňa bicykel?" → „Batériu" označené ako nesprávne (elektrobicykle existujú).

**Kontrola:** je každý distraktor **jednoznačne** nesprávny?

### A4 · Rozbité vysvetlenie kvôli zlému formátu poľa
Pri poli s pevným poradím stačí jeden prvok navyše a namiesto poučenia
sa zobrazí názov kategórie („bezpečnosť").

**Kontrola:** má každá položka rovnaký počet prvkov? Je vysvetlenie skutočná veta?

### A5 · Umelé nafukovanie počtu otázok
Tá istá otázka s iným koncom („Vyber správne." / „Premysli si odpoveď.")
vyzerá ako tri otázky, ale je to jedna.

**Kontrola:** koľko je **skutočne unikátnych** položiek po odstránení šablónových prívlastkov?

### A6 · Neexistujúca úroveň náročnosti
Kód mieša tri úrovne, ale jedna sa nikde nepriradí — vyvažovanie ticho nefunguje.

**Kontrola:** vyskytujú sa všetky úrovne v každej kategórii?

### A7 · Duplicitná položka
Tá istá otázka pridaná dvakrát, jedna z nich navyše v zlom formáte.

**Kontrola:** počet unikátnych textov = počet položiek?

---

## B · Jazyk a rod

### B1 · Mužské tvary tam, kde má byť ženský (alebo naopak)
Nestačí hľadať samostatné slová. **Slovné spojenia unikajú:**
- `aby si mal` → `aby si mala`
- `keď si nie si istý` → `istá`
- `si doma sám` → `sama`
- `nie si pripútaný` → `pripútaná`

**Kontrola:** hľadaj aj viacslovné vzory, nielen `\bsám\b`.

### B2 · Rod v pomenovaniach a odznakoch
„Znalec" → „Znalkyňa", „Fanúšik" → „Fanúšička", „Ochranca" → „Ochrankyňa",
„hráč" → „hráčka", „učeň" → „učenka".

### B3 · Nesúlad osoby v jednej otázke
Možnosti „Maľujeme" / „Behám" — raz množné číslo, raz jednotné.

### B4 · Hlas číta iný text, než vidíš
Ak appka číta nahlas, opravou textu sa mení aj zvuk. Skontroluj, čo sa reálne prečíta:
- `3:00` → „tri dvojbodka nula nula" → radšej „3 hodiny"
- `2 €` → „dva euro" → radšej „2 eurá" (skloňovanie 1/2–4/5+)
- `1, 2, 3, ...?` → „bodka bodka bodka" → vypusti výpustku

---

## C · Zobrazenie a znaky

### C1 · Znak, ktorý sa na cieľovom zariadení nezobrazí
Zriedkavé Unicode symboly (`⬠`, `⬣`, `🟰`) sa na mnohých Androidoch vykreslia
ako prázdny štvorček. Používateľ vidí otázku o päťuholníku bez päťuholníka.

**Pravidlo:** pre tvary a symboly použi **vlastné SVG**, nie exotické znaky.
Emoji staršie než ~2018 sú bezpečné, novšie nie.

### C2 · Nesprávny symbol pre daný pojem
`⬣` je šesťuholník, nie osemuholník — no použil sa pri otázke o značke STOP.

### C3 · Pomer strán obrázka vs. kontajnera
Pri `contain` v kontajneri s pevným pomerom zostávajú prázdne pásy.
Pri puzzle to znamená, že dielik odkryje **prázdno namiesto obrázka**.

**Kontrola:** zmeraj pomery všetkých obrázkov a porovnaj s kontajnerom.
**Riešenie:** prispôsob pomer kontajnera načítanému obrázku.

---

## D · Webové aplikácie a PWA

### D1 · Zdvojená cesta v zozname súborov
`avatar-assets/avatar-assets/subor.png` → offline cache ticho zlyhá.

**Kontrola:** porovnaj odkazované cesty so skutočnými súbormi na disku (obojsmerne).

### D2 · Cache drží starú verziu
Stratégia „najprv cache" znamená, že po nahratí aktualizácie používateľ
naďalej vidí starú appku.

**Riešenie:** HTML zo siete, obrázky z cache. Zvýš číslo verzie pri každom nasadení.

### D3 · Súbory v cache, ktoré sa už nepoužívajú
Pozostatky po starších verziách sa zbytočne sťahujú.

### D4 · Chýbajúci `index.html`
GitHub Pages hľadá presne tento názov. Iný názov = stránka nefunguje na hlavnej adrese.

### D5 · Názov appky bez diakritiky
`short_name` v manifeste sa zobrazuje pod ikonkou. „Mzda 2026" namiesto
„Mzdová kalkulačka".

### D6 · Interakcia pred načítaním
Kliknutie na tlačidlo v prvej pol sekunde → `pole[index]` je `undefined` → appka spadne.

**Kontrola:** má každá funkcia pracujúca s dátami poistku na prázdny stav?

### D7 · Tlačidlo zostane v dočasnom stave
Pri potvrdzovaní dvojklikom sa nezruší čakajúci časovač → tlačidlo ukazuje
„Klikni ešte raz!" aj po vykonaní akcie.

---

## E · Výpočty a dáta

### E1 · Overuj aritmetiku skriptom, nie okom
Pri generovaných príkladoch prepočítaj **každý** — sčítanie, odčítanie, skloňovanie
jednotiek, rozsah hodnôt.

### E2 · Sadzby a legislatíva sa menia
Pri mzdových, daňových a podobných výpočtoch **over aktuálne čísla vyhľadávaním**,
nespoliehaj sa na pamäť. Urob ich upraviteľné používateľom.

### E3 · Strop poolu odreže nové položky
`slice(0, N)` na konci môže ticho zahodiť práve pridané kategórie.

**Kontrola:** vypíš rozdelenie podľa kategórie **po** orezaní.

---

## F · Čo overiť nakoniec, vždy

- [ ] Syntax všetkých súborov (JS, JSON, XML/SVG)
- [ ] Každé `getElementById` má svoj prvok v HTML
- [ ] Každá funkcia volaná z `onclick` existuje
- [ ] Odkazované súbory existujú **a** existujúce sú odkazované
- [ ] Simulácia reálneho použitia (nie len jednotlivé funkcie)
- [ ] Prečítanie obsahu očami, nielen skriptom
- [ ] **Zoznam toho, čo overené nebolo**
