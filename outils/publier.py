#!/usr/bin/env python3
"""Publie un article du blog DeveloppIA.

    python3 outils/publier.py articles/<slug>.md [--sujet "ligne du calendrier"] [--sans-push]

Ce que fait le script, dans l'ordre :
1. Vérifie l'article contre CONSIGNES.md (en-tête, longueur, interdits, liens, FAQ, encart).
   La moindre erreur arrête tout : rien n'est publié.
2. Ajoute l'article à index.json (la liste que le site lit).
3. Coche la ligne du calendrier éditorial (sujets.md) si --sujet est donné.
4. git add / commit / push (trois commandes séparées). Le site developpia.fr lit le dépôt
   à chaque visite (cache de dix minutes) : l'article est en ligne sans mise en ligne du site.
5. Prévient Bing, Yandex et les autres moteurs IndexNow de la nouvelle adresse.
6. Vérifie que l'adresse répond, et affiche le lien.

Le script ne lit aucun secret : la clé IndexNow est publique par construction (elle est
servie par le site) et le push utilise l'identité git déjà configurée sur la machine.
"""
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import date

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://developpia.fr/"
CLE_INDEXNOW = "6f6ba1667f13c0ba36df6c17605d8c2f"  # même valeur que le fichier <clé>.txt à la racine du site
MOTS_INTERDITS = [r"meilleur dentiste", r"pas cher", r"\bpromotion\b", r"\bspécialiste\b", "—", "–"]


def separer_en_tete(texte):
    t = texte.replace("\r\n", "\n").replace("\r", "\n")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", t, re.S)
    if not m:
        return {}, t
    meta = {}
    for ligne in m.group(1).split("\n"):
        p = re.match(r"^([a-zA-Zéèà_]+)\s*:\s*(.*)$", ligne)
        if p:
            meta[p.group(1).strip().lower()] = p.group(2).strip()
    return meta, m.group(2)


def decouper_faq(corps):
    lignes = corps.split("\n")
    idx = next((i for i, l in enumerate(lignes) if re.match(r"^##\s+questions?\s+fr[ée]quentes?\s*$", l, re.I)), -1)
    if idx < 0:
        return corps, []
    faq, q, rep = [], None, []
    for l in lignes[idx + 1:]:
        m = re.match(r"^###\s+(.+)$", l)
        if m:
            if q:
                faq.append((q, " ".join(rep)))
            q, rep = m.group(1).strip(), []
        elif q and l.strip():
            rep.append(l.strip())
    if q:
        faq.append((q, " ".join(rep)))
    return "\n".join(lignes[:idx]), [f for f in faq if f[1]]


def texte_brut(t):
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t)
    return re.sub(r"[*`]", "", t)


def compter_mots(principal):
    sans_titres = re.sub(r"^#+\s.*$", "", principal, flags=re.M)
    return len(texte_brut(sans_titres).split())


def verifier(chemin):
    texte = open(chemin, encoding="utf-8").read()
    slug = os.path.basename(chemin)[:-3]
    meta, corps = separer_en_tete(texte)
    principal, faq = decouper_faq(corps)
    erreurs = []
    for champ in ("titre", "description", "accroche", "date", "lecture", "sujets", "resume"):
        if not meta.get(champ):
            erreurs.append(f"en-tête : champ « {champ} » manquant")
    if meta.get("description") and not 120 <= len(meta["description"]) <= 160:
        erreurs.append(f"description de {len(meta['description'])} caractères (attendu 120 à 160)")
    if meta.get("date") and not re.match(r"^\d{4}-\d{2}-\d{2}$", meta["date"]):
        erreurs.append("date au mauvais format (AAAA-MM-JJ)")
    if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", slug) or not 3 <= len(slug) <= 100:
        erreurs.append("nom de fichier (slug) invalide : minuscules, chiffres et tirets seulement")
    mots = compter_mots(principal)
    if not 1100 <= mots <= 1750:
        erreurs.append(f"{mots} mots dans le corps (attendu 1 200 à 1 600)")
    if re.search(r"^#\s", corps, re.M):
        erreurs.append("titre de niveau 1 (#) interdit, le titre vient de l'en-tête")
    if re.search(r"<[a-z][^>]*>", corps, re.I):
        erreurs.append("HTML interdit dans le corps")
    for motif in MOTS_INTERDITS:
        if re.search(motif, corps, re.I):
            erreurs.append(f"motif interdit trouvé : {motif}")
    internes = len(re.findall(r"\]\((https://developpia\.fr/[^)]*|/[^)]*)\)", corps))
    externes = len(re.findall(r"\]\(https?://(?!developpia\.fr)[^)]+\)", corps))
    if internes < 3:
        erreurs.append(f"{internes} lien(s) interne(s), attendu au moins 3")
    if externes < 1:
        erreurs.append("aucun lien externe vers une source")
    if len(faq) != 3:
        erreurs.append(f"{len(faq)} question(s) fréquente(s), attendu 3")
    encarts = len(re.findall(r"^>\s*\*\*", corps, re.M))
    if encarts != 1:
        erreurs.append(f"{encarts} encart(s), attendu exactement 1")
    h2 = len(re.findall(r"^##\s", principal, re.M))
    if not 5 <= h2 <= 8:
        erreurs.append(f"{h2} titres ##, attendu 5 à 8")
    return slug, meta, mots, erreurs


def charger_index():
    p = os.path.join(RACINE, "index.json")
    if not os.path.exists(p):
        return []
    d = json.load(open(p, encoding="utf-8"))
    return d if isinstance(d, list) else d.get("articles", [])


def enregistrer_index(articles):
    articles.sort(key=lambda a: (a["date"], a["slug"]), reverse=True)
    with open(os.path.join(RACINE, "index.json"), "w", encoding="utf-8") as f:
        json.dump({"articles": articles}, f, ensure_ascii=False, indent=1)
        f.write("\n")


def cocher_sujet(ligne_sujet, slug):
    p = os.path.join(RACINE, "sujets.md")
    s = open(p, encoding="utf-8").read()
    cible = ligne_sujet.strip()
    if cible.startswith("- [ ]"):
        cible = cible[5:].strip()
    for l in s.split("\n"):
        if l.startswith("- [ ]") and l[5:].strip() == cible:
            s = s.replace(l, f"- [x] {cible} (publié le {date.today().isoformat()}, {slug})", 1)
            open(p, "w", encoding="utf-8").write(s)
            return True
    return False


def git(*args):
    r = subprocess.run(["git", *args], cwd=RACINE, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} a échoué :\n{r.stderr.strip()}")
    return r.stdout.strip()


def indexnow(urls):
    corps = json.dumps({"host": "developpia.fr", "key": CLE_INDEXNOW,
                        "keyLocation": f"{SITE}{CLE_INDEXNOW}.txt", "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/IndexNow", data=corps,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:  # réseau
        return str(e)


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    chemin = os.path.join(RACINE, args[0]) if not os.path.isabs(args[0]) else args[0]
    sujet = args[args.index("--sujet") + 1] if "--sujet" in args else None
    sans_push = "--sans-push" in args

    slug, meta, mots, erreurs = verifier(chemin)
    articles = charger_index()
    if any(a["slug"] == slug for a in articles):
        erreurs.append("ce slug est déjà dans index.json (article déjà publié)")
    if erreurs:
        print(f"✗ {slug} : {len(erreurs)} problème(s), rien n'est publié.")
        for e in erreurs:
            print("  -", e)
        sys.exit(1)
    print(f"✓ {slug} : {mots} mots, en-tête complet, règles respectées.")

    entree = {"slug": slug, "titre": meta["titre"], "description": meta["description"], "date": meta["date"],
              "lecture": meta["lecture"], "sujets": [s.strip() for s in meta["sujets"].split(",") if s.strip()],
              "resume": meta["resume"]}
    if meta.get("maj"):
        entree["maj"] = meta["maj"]
    articles.append(entree)
    enregistrer_index(articles)
    print("✓ index.json mis à jour.")
    if sujet:
        print("✓ calendrier : sujet coché." if cocher_sujet(sujet, slug) else "⚠️ calendrier : ligne introuvable, rien coché.")

    if sans_push:
        print("(--sans-push : pas de git, pas d'IndexNow)")
        return
    git("add", os.path.relpath(chemin, RACINE), "index.json", "sujets.md")
    git("commit", "-m", f"Article : {meta['titre']}")
    git("push")
    print("✓ envoyé sur GitHub.")
    url = f"{SITE}blog/{slug}/"
    print("IndexNow :", indexnow([url, f"{SITE}blog/", f"{SITE}sitemap-blog.xml"]))
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (publier.py)"}), timeout=20) as r:
            print(f"✓ {url} répond {r.status}.")
    except Exception as e:
        print(f"⚠️ {url} : {e} (le cache peut mettre jusqu'à dix minutes ; réessayer)")


if __name__ == "__main__":
    main()
