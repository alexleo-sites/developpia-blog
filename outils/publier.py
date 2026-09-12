#!/usr/bin/env python3
"""Publie un article du blog DeveloppIA.

    python3 outils/publier.py articles/<slug>.md [--sujet "ligne du calendrier"] [--sans-push]
    python3 outils/publier.py --liens "sujet 1, sujet 2"

Ce que fait le script, dans l'ordre :
1. Vérifie l'article contre CONSIGNES.md (en-tête, longueur, interdits, liens, FAQ, encart),
   ses liens vers au moins deux articles déjà publiés, et les anciens articles modifiés pour
   renvoyer vers lui : au moins deux, un lien ajouté et rien d'autre.
   La moindre erreur arrête tout : rien n'est publié.
2. Ajoute l'article à index.json (la liste que le site lit).
3. Coche la ligne du calendrier éditorial (sujets.md) si --sujet est donné.
4. git add / commit / push (trois commandes séparées), anciens articles modifiés compris.
   Le site developpia.fr lit le dépôt à chaque visite (cache de dix minutes) : l'article est
   en ligne sans mise en ligne du site.
5. Prévient Bing, Yandex et les autres moteurs IndexNow des adresses changées.
6. Vérifie que l'adresse répond, et affiche le lien.

--liens "sujets" liste les articles déjà publiés : ceux qui partagent le plus de sujets d'abord
et, à égalité, ceux qui reçoivent le moins de liens des autres articles. Ce sont les articles
à relier au nouveau (CONSIGNES.md, « Relier le nouvel article aux anciens »).

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
LIGNES_MAX_ANCIEN = 6  # un ancien article ne reçoit qu'un lien vers le nouveau : quelques lignes au plus


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


def lien_vers(texte, slug):
    """Vrai si le texte contient un lien Markdown vers l'article `slug` du blog."""
    motif = r"\]\((?:https://developpia\.fr)?/blog/" + re.escape(slug) + r"/?(?:#[^)]*)?\)"
    return re.search(motif, texte) is not None


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
    lexique = meta.get("genre") == "lexique"
    if lexique:
        if not 2000 <= mots <= 6000:
            erreurs.append(f"{mots} mots (un lexique en attend 2 500 à 3 800)")
        termes = len(re.findall(r"^###\s", corps, re.M))
        if termes < 30:
            erreurs.append(f"{termes} termes ###, attendu au moins 30")
    elif not 1100 <= mots <= 1750:
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
    if not lexique:
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


def lire_article(slug):
    p = os.path.join(RACINE, "articles", slug + ".md")
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def proposer_liens(sujets_texte):
    """Articles à relier au nouveau : le plus de sujets en commun d'abord, puis les moins reliés."""
    voulus = {s.strip().lower() for s in sujets_texte.split(",") if s.strip()}
    articles = [a for a in charger_index() if a.get("genre") != "lexique"]
    textes = {a["slug"]: lire_article(a["slug"]) for a in articles}
    lignes = []
    for a in articles:
        communs = [s for s in a.get("sujets", []) if s.lower() in voulus]
        recus = sum(1 for s, t in textes.items() if s != a["slug"] and lien_vers(t, a["slug"]))
        lignes.append((-len(communs), recus, a["slug"], communs, a["titre"]))
    lignes.sort()
    print("Articles déjà publiés, du plus proche au moins proche (à égalité, le moins relié d'abord) :")
    for _, recus, slug, communs, titre in lignes:
        print(f"- {slug} | sujets en commun : {', '.join(communs) or 'aucun'} | reçoit {recus} lien(s) | {titre}")
    print(f"Adresse d'un article : {SITE}blog/<slug>/")


def anciens_modifies(chemin_nouveau):
    """Articles déjà enregistrés dans git et modifiés dans le dossier, hors nouvel article."""
    r = subprocess.run(["git", "status", "--porcelain", "--", "articles"], cwd=RACINE, capture_output=True, text=True)
    noms = []
    for ligne in r.stdout.splitlines():
        etat, nom = ligne[:2], ligne[3:].strip()
        if "M" in etat and os.path.abspath(os.path.join(RACINE, nom)) != os.path.abspath(chemin_nouveau):
            noms.append(nom)
    return noms


def controler_ancien(nom, slug_nouveau):
    """Un ancien article ne change que par un lien vers le nouveau."""
    chemin = os.path.join(RACINE, nom)
    texte = open(chemin, encoding="utf-8").read()
    erreurs = []
    if not lien_vers(texte, slug_nouveau):
        erreurs.append(f"{nom} est modifié mais ne renvoie pas vers le nouvel article")
    avant = subprocess.run(["git", "show", f"HEAD:{nom}"], cwd=RACINE, capture_output=True, text=True).stdout
    if separer_en_tete(avant)[0] != separer_en_tete(texte)[0]:
        erreurs.append(f"{nom} : l'en-tête a changé, seul le texte peut recevoir le lien")
    stat = subprocess.run(["git", "diff", "--numstat", "HEAD", "--", nom], cwd=RACINE, capture_output=True, text=True).stdout.split()
    if len(stat) >= 2 and stat[0].isdigit() and stat[1].isdigit() and int(stat[0]) + int(stat[1]) > LIGNES_MAX_ANCIEN:
        erreurs.append(f"{nom} : {int(stat[0]) + int(stat[1])} lignes changées, au plus {LIGNES_MAX_ANCIEN}")
    erreurs += [f"{nom} : {e}" for e in verifier(chemin)[3]]
    return erreurs


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
    if args[0] == "--liens":
        proposer_liens(args[1] if len(args) > 1 else "")
        return
    chemin = os.path.join(RACINE, args[0]) if not os.path.isabs(args[0]) else args[0]
    sujet = args[args.index("--sujet") + 1] if "--sujet" in args else None
    sans_push = "--sans-push" in args

    slug, meta, mots, erreurs = verifier(chemin)
    articles = charger_index()
    if any(a["slug"] == slug for a in articles):
        erreurs.append("ce slug est déjà dans index.json (article déjà publié)")
    publies = [a["slug"] for a in articles if a.get("genre") != "lexique"]
    anciens = anciens_modifies(chemin)
    if meta.get("genre") != "lexique" and len(publies) >= 2:
        texte = open(chemin, encoding="utf-8").read()
        sortants = [s for s in publies if lien_vers(texte, s)]
        if len(sortants) < 2:
            erreurs.append(f"{len(sortants)} lien(s) vers des articles déjà publiés, attendu au moins 2 (voir --liens)")
        entrants = [n for n in anciens if lien_vers(open(os.path.join(RACINE, n), encoding="utf-8").read(), slug)]
        if len(entrants) < 2:
            erreurs.append(f"{len(entrants)} ancien(s) article(s) renvoient vers le nouveau, attendu au moins 2 "
                           "(CONSIGNES.md, « Relier le nouvel article aux anciens »)")
    for nom in anciens:
        erreurs += controler_ancien(nom, slug)
    if erreurs:
        print(f"✗ {slug} : {len(erreurs)} problème(s), rien n'est publié.")
        for e in erreurs:
            print("  -", e)
        sys.exit(1)
    print(f"✓ {slug} : {mots} mots, en-tête complet, règles respectées.")
    if anciens:
        print(f"✓ liens vers le nouvel article ajoutés dans : {', '.join(anciens)}")

    entree = {"slug": slug, "titre": meta["titre"], "description": meta["description"], "date": meta["date"],
              "lecture": meta["lecture"], "sujets": [s.strip() for s in meta["sujets"].split(",") if s.strip()],
              "resume": meta["resume"]}
    if meta.get("maj"):
        entree["maj"] = meta["maj"]
    if meta.get("genre"):
        entree["genre"] = meta["genre"]
    articles.append(entree)
    enregistrer_index(articles)
    print("✓ index.json mis à jour.")
    if sujet:
        print("✓ calendrier : sujet coché." if cocher_sujet(sujet, slug) else "⚠️ calendrier : ligne introuvable, rien coché.")

    if sans_push:
        print("(--sans-push : pas de git, pas d'IndexNow)")
        return
    git("add", os.path.relpath(chemin, RACINE), "index.json", "sujets.md", *anciens)
    message = f"Article : {meta['titre']}"
    if anciens:
        message += f" (relié depuis {len(anciens)} article{'s' if len(anciens) > 1 else ''})"
    git("commit", "-m", message)
    git("push")
    print("✓ envoyé sur GitHub.")
    url = f"{SITE}blog/{slug}/"
    adresses = [url, f"{SITE}blog/", f"{SITE}sitemap-blog.xml"] + [f"{SITE}blog/{os.path.basename(n)[:-3]}/" for n in anciens]
    print("IndexNow :", indexnow(adresses))
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (publier.py)"}), timeout=20) as r:
            print(f"✓ {url} répond {r.status}.")
    except Exception as e:
        print(f"⚠️ {url} : {e} (le cache peut mettre jusqu'à dix minutes ; réessayer)")


if __name__ == "__main__":
    main()
