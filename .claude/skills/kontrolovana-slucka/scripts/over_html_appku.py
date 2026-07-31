#!/usr/bin/env python3
"""
Overovaci skript pre jednosuborove HTML aplikacie.

Kontroluje to, co sa da overit strojovo a co sa v tomto type projektu
opakovane lame:
  1. syntax JSON a SVG/XML suborov
  2. duplicitne id v HTML
  3. kazde getElementById('x') ma svoj prvok s id="x"
  4. kazda funkcia volana z onclick / onchange / oninput existuje
  5. odkazovane subory existuju na disku
  6. subory na disku su niekde odkazovane (mrtve assety)
  7. zdvojene segmenty v cestach (avatar-assets/avatar-assets/...)

Bez externych zavislosti - len standardna kniznica.

Pouzitie:
    python3 .claude/skills/kontrolovana-slucka/scripts/over_html_appku.py
    python3 .../over_html_appku.py --html index.html --korenad .

Navratovy kod:
    0 = ziadna CHYBA (varovania mozu byt)
    1 = najdena aspon jedna CHYBA
    2 = skript sa nedal spustit (chybajuci subor a pod.)
"""

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

# Atributy, v ktorych hladame volania funkcii
UDALOSTI = ("onclick", "onchange", "oninput", "onsubmit", "onload", "onkeyup", "onkeydown")

# Pripony, ktore povazujeme za assety na kontrolu mrtvych suborov
ASSET_PRIPONY = (".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif", ".mp3", ".wav", ".ogg")

# Vstavane funkcie a objekty, ktore v HTML definovane byt nemusia
VSTAVANE = {
    "alert", "confirm", "prompt", "console", "window", "document", "event",
    "setTimeout", "setInterval", "parseInt", "parseFloat", "Number", "String",
    "location", "history", "navigator", "JSON", "Math", "Date", "Array", "Object",
}


class Nalezy:
    def __init__(self):
        self.chyby = []
        self.varovania = []
        self.ok = []

    def chyba(self, kategoria, sprava):
        self.chyby.append((kategoria, sprava))

    def varovanie(self, kategoria, sprava):
        self.varovania.append((kategoria, sprava))

    def preslo(self, sprava):
        self.ok.append(sprava)


def nacitaj(cesta):
    with open(cesta, "r", encoding="utf-8") as f:
        return f.read()


def vyber_skripty(html):
    """Vrati spojeny obsah vsetkych inline <script> blokov."""
    return "\n".join(re.findall(r"<script\b[^>]*>(.*?)</script>", html, re.S | re.I))


def sesterske_skripty(koren):
    """Obsah vsetkych .js a .css suborov v projekte (service-worker a spol.)."""
    kusy = []
    for adresar, _, subory in os.walk(koren):
        if any(x in adresar for x in (".git", "node_modules", ".claude", ".agents")):
            continue
        for meno in subory:
            if meno.endswith((".js", ".css")):
                try:
                    kusy.append(nacitaj(os.path.join(adresar, meno)))
                except (OSError, UnicodeDecodeError):
                    pass
    return "\n".join(kusy)


ZNAME_PRIPONY = re.compile(
    r"\.(png|jpe?g|svg|webp|gif|mp3|wav|ogg|js|css|json|webmanifest|html|ico|woff2?|ttf)$", re.I
)


def je_dynamicka(cesta):
    """Cesta skladana za behu - regex ju precitat nevie, nehodnotime ju."""
    return any(x in cesta for x in ("${", "+", "\\", "*", "<", ">"))


def vyzera_ako_cesta(cesta):
    """Odfiltruje zasahy typu 'req.url' z new URL(...) alebo nazvy premennych."""
    return bool(ZNAME_PRIPONY.search(cesta)) or "/" in cesta


def kontrola_json(koren, n):
    for meno in os.listdir(koren):
        if meno in ("skills-lock.json", "package-lock.json"):
            continue
        if meno.endswith((".json", ".webmanifest")):
            cesta = os.path.join(koren, meno)
            try:
                json.loads(nacitaj(cesta))
                n.preslo(f"JSON platny: {meno}")
            except json.JSONDecodeError as e:
                n.chyba("JSON", f"{meno}: {e}")


def kontrola_svg(koren, n):
    pocet = 0
    for adresar, _, subory in os.walk(koren):
        if ".git" in adresar or "node_modules" in adresar:
            continue
        for meno in subory:
            if meno.endswith(".svg"):
                cesta = os.path.join(adresar, meno)
                try:
                    ET.parse(cesta)
                    pocet += 1
                except ET.ParseError as e:
                    n.chyba("SVG", f"{os.path.relpath(cesta, koren)}: {e}")
    if pocet:
        n.preslo(f"SVG suborov s platnym XML: {pocet}")


def kontrola_id(html, n):
    idcka = re.findall(r'\bid\s*=\s*["\']([^"\']+)["\']', html)
    videne, duplicity = set(), set()
    for i in idcka:
        if i in videne:
            duplicity.add(i)
        videne.add(i)
    for d in sorted(duplicity):
        n.chyba("DUPLICITNE ID", f'id="{d}" je v HTML viackrat')
    if not duplicity:
        n.preslo(f"Ziadne duplicitne id ({len(videne)} unikatnych)")
    return videne


def kontrola_getelementbyid(js, idcka, n):
    volane = set(re.findall(r"getElementById\(\s*['\"]([^'\"]+)['\"]\s*\)", js))
    chybajuce = sorted(volane - idcka)
    for c in chybajuce:
        n.chyba("CHYBAJUCE ID", f"getElementById('{c}') - prvok s tymto id v HTML nie je")
    if not chybajuce:
        n.preslo(f"Vsetkych {len(volane)} getElementById ma svoj prvok")


def kontrola_funkcii(html, js, n):
    volane = set()
    for udalost in UDALOSTI:
        for telo in re.findall(rf'{udalost}\s*=\s*["\']([^"\']+)["\']', html, re.I):
            for meno in re.findall(r"\b([A-Za-z_$][\w$]*)\s*\(", telo):
                if meno not in VSTAVANE:
                    volane.add(meno)

    definovane = set()
    definovane |= set(re.findall(r"\bfunction\s+([A-Za-z_$][\w$]*)", js))
    definovane |= set(re.findall(r"\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?(?:function\b|\()", js))
    definovane |= set(re.findall(r"\bwindow\.([A-Za-z_$][\w$]*)\s*=", js))
    definovane |= set(re.findall(r"\b([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?(?:function\b|\([^)]*\)\s*=>)", js))

    chybajuce = sorted(volane - definovane)
    for c in chybajuce:
        n.chyba("CHYBAJUCA FUNKCIA", f"z inline udalosti sa vola {c}(), definicia sa nenasla")
    if not chybajuce:
        n.preslo(f"Vsetkych {len(volane)} funkcii z inline udalosti je definovanych")


def zbierka_odkazov(html, js, koren):
    """Vrati mnozinu relativnych ciest odkazovanych z HTML, CSS a JS."""
    odkazy = set()
    for vzor in (
        r'(?:src|href)\s*=\s*["\']([^"\'#?]+)["\']',
        r'url\(\s*["\']?([^"\')?#]+)["\']?\s*\)',
        r'["\']([^"\']*(?:avatar-assets|assets|img|images)/[^"\']+)["\']',
        r'["\']([\w./-]+\.(?:png|jpe?g|svg|webp|gif|mp3|wav|ogg|js|css|json|webmanifest|html))["\']',
    ):
        for zdroj in (html, js):
            for m in re.findall(vzor, zdroj, re.I):
                cesta = m.strip().lstrip("./")
                if not cesta or je_dynamicka(cesta) or not vyzera_ako_cesta(cesta):
                    continue
                if cesta.startswith(("http://", "https://", "data:", "//", "mailto:")):
                    continue
                odkazy.add(cesta)
    return odkazy


def kontrola_ciest(odkazy, koren, n):
    chybajuce = []
    for o in sorted(odkazy):
        if not os.path.exists(os.path.join(koren, o)):
            chybajuce.append(o)
    for c in chybajuce:
        n.chyba("CHYBAJUCI SUBOR", f"odkaz na '{c}', subor na disku nie je")
    if not chybajuce:
        n.preslo(f"Vsetkych {len(odkazy)} odkazovanych ciest existuje")

    # zdvojene segmenty typu avatar-assets/avatar-assets/
    for o in sorted(odkazy):
        casti = o.split("/")
        for i in range(len(casti) - 1):
            if casti[i] and casti[i] == casti[i + 1]:
                n.chyba("ZDVOJENA CESTA", f"'{o}' obsahuje segment '{casti[i]}' dvakrat za sebou")


def kontrola_mrtvych_assetov(odkazy, koren, n):
    na_disku = set()
    for adresar, _, subory in os.walk(koren):
        if any(x in adresar for x in (".git", "node_modules", ".claude", ".agents")):
            continue
        for meno in subory:
            if meno.lower().endswith(ASSET_PRIPONY):
                rel = os.path.relpath(os.path.join(adresar, meno), koren).replace(os.sep, "/")
                na_disku.add(rel)

    neodkazovane = sorted(na_disku - odkazy)
    # subor moze byt odkazovany aj len menom bez adresara
    mena_v_odkazoch = {o.split("/")[-1] for o in odkazy}
    neodkazovane = [x for x in neodkazovane if x.split("/")[-1] not in mena_v_odkazoch]

    # zoskupenie podla adresara a pripony, nech vystup nie je stena textu
    skupiny = {}
    for x in neodkazovane:
        adresar = x.rsplit("/", 1)[0] if "/" in x else "(koren)"
        pripona = os.path.splitext(x)[1].lower()
        skupiny.setdefault((adresar, pripona), []).append(x)

    for (adresar, pripona), polozky in sorted(skupiny.items()):
        ukazka = ", ".join(p.rsplit("/", 1)[-1] for p in polozky[:3])
        zvysok = f" a dalsich {len(polozky) - 3}" if len(polozky) > 3 else ""
        n.varovanie(
            "MRTVY ASSET",
            f"{adresar}/ - {len(polozky)}x {pripona} sa nikde neodkazuje: {ukazka}{zvysok}",
        )

    if not neodkazovane:
        n.preslo(f"Vsetkych {len(na_disku)} assetov na disku je odkazovanych")
    else:
        n.preslo(f"Odkazovanych assetov: {len(na_disku) - len(neodkazovane)} z {len(na_disku)}")


def main():
    p = argparse.ArgumentParser(description="Overenie jednosuboroveho HTML projektu")
    p.add_argument("--html", default="index.html", help="hlavny HTML subor")
    p.add_argument("--koren", default=".", help="korenovy adresar projektu")
    a = p.parse_args()

    cesta_html = os.path.join(a.koren, a.html)
    if not os.path.isfile(cesta_html):
        print(f"CHYBA: {cesta_html} neexistuje", file=sys.stderr)
        return 2

    html = nacitaj(cesta_html)
    js_inline = vyber_skripty(html)
    js = js_inline + "\n" + sesterske_skripty(a.koren)
    n = Nalezy()

    kontrola_json(a.koren, n)
    kontrola_svg(a.koren, n)
    idcka = kontrola_id(html, n)
    kontrola_getelementbyid(js_inline, idcka, n)
    kontrola_funkcii(html, js, n)
    odkazy = zbierka_odkazov(html, js, a.koren)
    kontrola_ciest(odkazy, a.koren, n)
    kontrola_mrtvych_assetov(odkazy, a.koren, n)

    print("=" * 62)
    print(f"OVERENIE: {a.html}")
    print("=" * 62)

    for s in n.ok:
        print(f"  OK       {s}")
    if n.varovania:
        print()
        for k, s in n.varovania:
            print(f"  VAROVANIE  [{k}] {s}")
    if n.chyby:
        print()
        for k, s in n.chyby:
            print(f"  CHYBA      [{k}] {s}")

    print("-" * 62)
    print(f"preslo: {len(n.ok)}   varovania: {len(n.varovania)}   chyby: {len(n.chyby)}")

    if n.chyby:
        print("\nVYSLEDOK: NEPRESLO - oprav chyby vyssie.")
        return 1
    print("\nVYSLEDOK: PRESLO (strojove kontroly).")
    print("Toto NIE JE dokaz, ze appka funguje. Skript nevidi vykreslenu stranku,")
    print("nekontroluje vecnu spravnost obsahu ani pouzitelnost. Obsah precitaj ocami.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
