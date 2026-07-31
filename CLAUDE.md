# Pravidlá projektu

## Jazyk a štýl

- Komunikuj **vždy po slovensky**. Kód, názvy premenných a commit správy môžu byť anglicky, ale vysvetlenia, otázky a zhrnutia sú po slovensky.
- Píš stručne a prakticky. Žiadne zdvorilostné úvody typu „Skvelá otázka" ani zhrnutia toho, čo som práve napísal.
- Vyhýbaj sa AI-štýlu písania: bez fráz „je dôležité poznamenať", bez nadužívania pomlčiek, bez povinných trojíc príkladov.
- Formátovanie používaj len tam, kde pomáha čitateľnosti. Nie odrážky na všetko.
- Odpoveď ukonči, keď je myšlienka hotová. Nepridávaj doplňujúce otázky, ak nie sú potrebné.

## Prostredie

- Pracujem **z mobilu (Android)**, cez Claude Code na webe. Nemám bežne k dispozícii lokálny terminál ani počítač.
- Predvolene navrhuj riešenia, ktoré sa dajú dokončiť z prehliadača.
- Ak nejaký krok naozaj vyžaduje počítač alebo lokálny terminál, **výslovne to označ** a napíš prečo. Nepredpokladaj, že ho mám poruke.

## Kód a bezpečnosť

- Pri každom kóde zohľadni OWASP: sanitizácia vstupov, ošetrenie chýb, žiadne slepé dôverovanie používateľskému vstupu.
- **Nikdy nevkladaj do kódu API kľúče, heslá ani tokeny.** Používaj premenné prostredia a v repozitári nechaj len príklad bez hodnôt.
- Nepridávaj závislosti, ktoré nie sú nutné. Menej balíkov, menej rizika.
- Pri zmenách existujúceho kódu meň len to, čo súvisí s úlohou. Nerefaktoruj popri tom veci, na ktoré si nedostal zadanie.

## Presnosť a poctivosť

- Ak si niečím nie si istý, napíš **„toto neviem potvrdiť"**. Nehádaj a nevymýšľaj si.
- Číselné tvrdenia podlož výpočtom alebo zdrojom.
- Netvrď, že niečo funguje, kým to nemáš čím dokázať. Vizuál a reálne používanie appky overiť nevieš — to napíš otvorene a nechaj na mňa.

## Nevratné zmeny

- Čokoľvek, čo sa nedá jednoducho vrátiť (mazanie súborov, prepis histórie, deploy, zmena nastavení repozitára), **najprv ukáž a počkaj na moje výslovné OK**.
- Čítanie a analýza kódu súhlas nepotrebujú.

## Postup práce

Pre tento projekt sú k dispozícii dve zručnosti v `.claude/skills/`:

1. **`rozhovor-pred-stavanim`** — použi ju **skôr**, než začneš stavať čokoľvek zložitejšie.
2. **`kontrolovana-slucka`** — použi ju **po** dokončení práce na overenie dôkazom.

Prvá je prevencia, druhá je kontrola. Pri väčšej úlohe patria obe.
