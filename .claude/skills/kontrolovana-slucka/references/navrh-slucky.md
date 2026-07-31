# Návrh slučky — šablóna a ukážky

Vyplň skôr, než sa dotkneš prvého súboru. Ak niektorý riadok nevieš vyplniť dvomi vetami, úloha ešte nie je pripravená a treba sa pýtať.

---

## Šablóna

```
CIEĽ      Čo má po skončení platiť. Jedna overiteľná veta.
ROZSAH    Čoho sa smiem dotknúť. Čoho sa určite nesmiem.
AKCIA     Kroky v poradí. Konkrétne, nie „vylepši to".
DÔKAZ     Príkaz alebo kontrola, ktorá vráti áno/nie.
ROZPOČET  Max. počet kôl.
REPORT    Čo sa zmenilo, čo prešlo, čo overené nebolo.
```

Návrh **ukáž používateľovi** pred zmenou súborov. Pri rozsiahlom alebo nevratnom zásahu si vyžiadaj výslovné OK.

---

## Ako vyzerá dobrý dôkaz

Dôkaz musí byť niečo, čo sa nedá „ukecať" — príkaz s návratovým kódom, počet, porovnanie dvoch zoznamov.

| Slabý dôkaz | Silný dôkaz |
|---|---|
| „Skontroloval som odkazy" | `over_html_appku.py` vráti kód 0 |
| „Otázky sú v poriadku" | 40 z 40 otázok prečítaných, zoznam problémových priložený |
| „Opravil som rod" | `grep -c "aby si mal"` vráti 0 |
| „Appka funguje" | *(nedokázateľné z môjho miesta — nechaj na používateľa)* |

Keď dôkaz vymyslieť nevieš, **zúž úlohu**, kým sa dá odmerať. Alebo otvorene napíš, že táto časť overená nebude.

---

## Ukážka 1 — dobré zadanie

```
CIEĽ      Žiadny asset v repozitári nie je mŕtvy: každý .jpg a .svg
          je odkazovaný z index.html alebo service-worker.js.
ROZSAH    Len mazanie nepoužitých súborov a úprava zoznamu v
          service-worker.js. Do hernej logiky v index.html nesiaham.
AKCIA     1. Spustiť over_html_appku.py, zapísať zoznam mŕtvych assetov
          2. Overiť pri každom, či naozaj nie je použitý (grep)
          3. Ukázať zoznam na schválenie
          4. Po OK zmazať a zvýšiť verziu cache
DÔKAZ     over_html_appku.py má 0 varovaní typu MRTVY ASSET
ROZPOČET  3 kolá
REPORT    Zoznam zmazaných súborov, ušetrené miesto, čo zostalo neisté
```

Prečo je dobré: cieľ sa dá odmerať jedným príkazom, rozsah výslovne vylučuje hernú logiku, a mazanie je nevratné, takže má vlastný krok na schválenie.

---

## Ukážka 2 — zlé zadanie

```
CIEĽ      Vylepšiť kvíz.
ROZSAH    index.html
AKCIA     Prejsť to a opraviť čo treba.
DÔKAZ     Skontrolujem to.
```

Čo je zle:

- **Cieľ** sa nedá overiť. Kedy je „vylepšený"? Nikdy.
- **Rozsah** je celý súbor, čiže žiadne obmedzenie.
- **Akcia** je „oprav čo treba" — to je presne to hádanie, ktorému sa slučka vyhýba.
- **Dôkaz** je sebahodnotenie. Zakázané.
- **Rozpočet** chýba, slučka môže bežať donekonečna.

---

## Ukážka 3 — úloha, ktorú treba najprv zúžiť

Zadanie: *„Skontroluj otázky v kvíze, či sú v poriadku."*

„V poriadku" nie je merateľné. Rozpadni to na vlastnosti, z ktorých každá dôkaz má:

| Vlastnosť | Dôkaz |
|---|---|
| Otázka neobsahuje vlastnú odpoveď | skript hľadá koreň odpovede v texte otázky |
| Ikona neprezrádza správnu odpoveď | porovnanie ikon správnej vs. nesprávnych možností |
| Každý distraktor je jednoznačne nesprávny | **prečítanie očami**, skript to nezistí |
| Žiadne duplicity | počet unikátnych textov = počet položiek |
| Všetky úrovne obsadené v každej kategórii | súčet podľa kategórie a úrovne |

Posledný riadok je dôvod, prečo skript nikdy nestačí. Podrobný zoznam takýchto chýb je v `kontrolny-zoznam.md`.

---

## Kedy slučku zastaviť

- dôkaz prejde **úplne** — nie „skoro", nie „až na jednu vec"
- minie sa rozpočet kôl
- dve kolá po sebe neprinesú žiadnu zmenu

Po vyčerpaní rozpočtu neklam o výsledku. Napíš, čo zostáva nevyriešené a prečo.
