#!/usr/bin/env python3
"""Remet index.json d'accord avec l'en-tête des articles déjà publiés.

    python3 outils/resynchroniser-index.py <slug> [<slug>...]
    python3 outils/resynchroniser-index.py --tous
    python3 outils/resynchroniser-index.py --touche <slug> [<slug>...]

`publier.py` écrit index.json au moment de la publication. Quand on corrige
ensuite le titre, la description, le résumé, les sujets ou le temps de lecture
d'un article, l'en-tête du fichier .md change mais index.json garde l'ancienne
valeur : le blog affiche alors un titre dans la liste et un autre sur la page.
Ce script recopie l'en-tête dans index.json, et pose la date du jour dans le
champ « modifie » pour que Google relise la page (api/blog.js prend la plus
récente de modifie, maj et date pour le plan du site).

Avec `--touche`, on ne recopie rien : on pose seulement la date du jour dans
« modifie ». C'est ce qu'il faut après avoir corrigé le corps d'un article sans
toucher à son en-tête.

Ce qui n'est jamais touché : `date` (la date de publication, qui ne change
pas), `ordre`, et tout champ que l'en-tête ne porte pas.
"""
import io
import json
import os
import re
import sys
from datetime import date

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(RACINE, "index.json")
ARTICLES = os.path.join(RACINE, "articles")
# Les champs de l'en-tête qui vivent aussi dans index.json. `date` en est
# volontairement absent : la date de publication ne se corrige pas ici.
CHAMPS = ("titre", "description", "resume", "lecture")


def en_tete(chemin):
    """Le bloc entre les deux --- en tête du fichier, en dictionnaire."""
    texte = io.open(chemin, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n", texte, re.S)
    if not m:
        raise SystemExit("en-tête introuvable dans " + chemin)
    champs = {}
    for ligne in m.group(1).split("\n"):
        if ":" in ligne and not ligne.startswith(" "):
            cle, valeur = ligne.split(":", 1)
            champs[cle.strip()] = valeur.strip()
    return champs


def main(args):
    index = json.load(io.open(INDEX, encoding="utf-8"))
    articles = index["articles"]
    touche = args[0] == "--touche"
    if touche:
        args = args[1:]
        if not args:
            raise SystemExit("--touche attend au moins un slug.")
    voulus = [a["slug"] for a in articles] if args == ["--tous"] else args
    inconnus = [s for s in voulus if not any(a["slug"] == s for a in articles)]
    if inconnus:
        raise SystemExit("slug absent d'index.json : " + ", ".join(inconnus))

    change = 0
    for a in articles:
        if a["slug"] not in voulus:
            continue
        if touche:
            if a.get("modifie") != date.today().isoformat():
                a["modifie"] = date.today().isoformat()
                change += 1
                print(a["slug"], ": modifie =", a["modifie"])
            continue
        chemin = os.path.join(ARTICLES, a["slug"] + ".md")
        if not os.path.exists(chemin):
            raise SystemExit("fichier introuvable : " + chemin)
        tete = en_tete(chemin)
        ecarts = []
        for champ in CHAMPS:
            if champ in tete and a.get(champ) != tete[champ]:
                ecarts.append(champ)
                a[champ] = tete[champ]
        if "sujets" in tete:
            sujets = [s.strip() for s in tete["sujets"].split(",") if s.strip()]
            if a.get("sujets") != sujets:
                ecarts.append("sujets")
                a["sujets"] = sujets
        if ecarts:
            a["modifie"] = date.today().isoformat()
            change += 1
            print(a["slug"], ":", ", ".join(ecarts))

    if not change:
        print("index.json était déjà d'accord avec les en-têtes.")
        return
    with io.open(INDEX, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(change, "article(s) mis à jour dans index.json.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    main(sys.argv[1:])
