#!/usr/bin/env python3
"""Construit en/index.json (la liste que lit en.developpia.fr/blog/) à partir des
articles anglais en/articles/<slug>.md.

    python3 outils/construire-index-en.py
    python3 outils/construire-index-en.py --fr-index chemin/index.json   (hors dépôt)
    python3 outils/construire-index-en.py --touche <slug> [<slug>...]

Même structure et même ordre de champs que l'index.json français (publier.py) :
slug, titre, description, date, lecture, sujets, resume, puis maj, genre si présents,
ordre (recopié de l'article français, pour garder le même ordre de lecture),
modifie (conservé d'un passage à l'autre), et enfin fr (le slug français).

- `modifie` prend la date du jour quand l'en-tête d'un article déjà listé a changé
  (titre, description, résumé, sujets, lecture, maj) : le plan du site dit alors à
  Google de relire la page. Avec --touche, seule cette date est posée (corps corrigé
  sans toucher à l'en-tête).
- `date` vient de l'en-tête (c'est la date de l'article français, inchangée).
- Le script s'arrête sans rien écrire à la moindre erreur (en-tête incomplet,
  slug invalide, `fr:` absent ou inconnu, sujet hors de la liste anglaise).

Emplacements : dans le dépôt developpia-blog, les articles anglais sont dans en/articles/
et l'index français est index.json à la racine. Si le dossier en/ n'existe pas à côté de
outils/ (copie de travail), le script lit articles/ et écrit index.json à côté de outils/.
Écriture : json.dump(..., ensure_ascii=False, indent=1) + saut de ligne final, comme publier.py.
"""
import io
import json
import os
import re
import sys
from datetime import date

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EN = os.path.join(RACINE, "en") if os.path.isdir(os.path.join(RACINE, "en")) else RACINE
ARTICLES = os.path.join(EN, "articles")
INDEX = os.path.join(EN, "index.json")
FR_INDEX_DEFAUT = os.path.join(RACINE, "index.json") if EN != RACINE else None

OBLIGATOIRES = ("titre", "titre_court", "description", "accroche", "date", "lecture", "sujets", "resume", "fr")
SUJETS = {"deciding", "practice website", "Dental Council rules", "Google Maps", "social media",
          "measuring", "visibility", "AI search", "by type of practice", "glossary"}
SUIVIS = ("titre", "description", "date", "lecture", "sujets", "resume", "maj", "genre")
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def en_tete(chemin):
    texte = io.open(chemin, encoding="utf-8").read().replace("\r\n", "\n").replace("\r", "\n")
    m = re.match(r"^---\n(.*?)\n---\n", texte, re.S)
    if not m:
        return None
    champs = {}
    for ligne in m.group(1).split("\n"):
        p = re.match(r"^([a-zA-Zéèà_]+)\s*:\s*(.*)$", ligne)
        if p:
            champs[p.group(1).strip().lower()] = p.group(2).strip()
    return champs


def charger(chemin):
    if not chemin or not os.path.exists(chemin):
        return []
    d = json.load(io.open(chemin, encoding="utf-8"))
    return d if isinstance(d, list) else d.get("articles", [])


def main(args):
    fr_index = FR_INDEX_DEFAUT
    if "--fr-index" in args:
        i = args.index("--fr-index")
        fr_index = args[i + 1]
        args = args[:i] + args[i + 2:]
    touche = []
    if args and args[0] == "--touche":
        touche = args[1:]
        if not touche:
            raise SystemExit("--touche attend au moins un slug.")

    francais = {a["slug"]: a for a in charger(fr_index)}
    if not francais:
        print("⚠️ index français introuvable : « ordre » non recopié et slugs fr non vérifiés.")
    anciens = {a["slug"]: a for a in charger(INDEX)}
    auj = date.today().isoformat()

    if not os.path.isdir(ARTICLES):
        raise SystemExit("dossier introuvable : " + ARTICLES)
    erreurs, articles, vus_fr = [], [], {}
    for nom in sorted(os.listdir(ARTICLES)):
        if not nom.endswith(".md"):
            continue
        slug = nom[:-3]
        meta = en_tete(os.path.join(ARTICLES, nom))
        if meta is None:
            erreurs.append(f"{nom} : en-tête --- introuvable")
            continue
        if not SLUG.match(slug) or not 3 <= len(slug) <= 100:
            erreurs.append(f"{nom} : slug invalide")
        manquants = [c for c in OBLIGATOIRES if not meta.get(c)]
        if manquants:
            erreurs.append(f"{nom} : champ(s) manquant(s) : {', '.join(manquants)}")
            continue
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", meta["date"]):
            erreurs.append(f"{nom} : date au mauvais format (AAAA-MM-JJ)")
        sujets = [s.strip() for s in meta["sujets"].split(",") if s.strip()]
        hors = [s for s in sujets if s not in SUJETS]
        if hors:
            erreurs.append(f"{nom} : sujet(s) hors liste anglaise : {', '.join(hors)}")
        fr = meta["fr"]
        if francais and fr not in francais:
            erreurs.append(f"{nom} : fr: {fr} absent de l'index français")
        if fr in vus_fr:
            erreurs.append(f"{nom} : fr: {fr} déjà traduit par {vus_fr[fr]}")
        vus_fr[fr] = slug
        if francais and fr in francais and francais[fr].get("date") != meta["date"]:
            print(f"⚠️ {slug} : date {meta['date']} différente de l'article français ({francais[fr].get('date')})")

        entree = {"slug": slug, "titre": meta["titre"], "description": meta["description"], "date": meta["date"],
                  "lecture": meta["lecture"], "sujets": sujets, "resume": meta["resume"]}
        if meta.get("maj"):
            entree["maj"] = meta["maj"]
        if meta.get("genre"):
            entree["genre"] = meta["genre"]
        if meta.get("brouillon"):
            entree["brouillon"] = meta["brouillon"]
        ordre = francais.get(fr, {}).get("ordre")
        if isinstance(ordre, int):
            entree["ordre"] = ordre
        ancien = anciens.get(slug)
        modifie = ancien.get("modifie") if ancien else None
        if ancien and any(ancien.get(c) != entree.get(c) for c in SUIVIS):
            modifie = auj
            print(f"✓ {slug} : en-tête changé, modifie = {auj}")
        if slug in touche:
            modifie = auj
            print(f"✓ {slug} : modifie = {auj}")
        if modifie:
            entree["modifie"] = modifie
        entree["fr"] = fr
        if not ancien:
            print(f"✓ {slug} : nouvel article")
        articles.append(entree)

    inconnus = [s for s in touche if s not in {a["slug"] for a in articles}]
    if inconnus:
        erreurs.append("--touche : slug(s) sans fichier : " + ", ".join(inconnus))
    for s in anciens:
        if s not in {a["slug"] for a in articles}:
            print(f"⚠️ {s} : était dans en/index.json mais n'a plus de fichier, retiré de la liste")
    if erreurs:
        print(f"✗ {len(erreurs)} problème(s), en/index.json n'est pas écrit :")
        for e in erreurs:
            print("  -", e)
        sys.exit(1)

    articles.sort(key=lambda a: (a["date"], a["slug"]), reverse=True)
    with io.open(INDEX, "w", encoding="utf-8") as f:
        json.dump({"articles": articles}, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"✓ {os.path.relpath(INDEX, RACINE)} : {len(articles)} article(s).")


if __name__ == "__main__":
    main(sys.argv[1:])
