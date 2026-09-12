# Le blog de DeveloppIA

Les articles de https://developpia.fr/blog/ vivent ici. Le site lit ce dépôt à chaque
visite (avec dix minutes de cache) : **déposer un article ici suffit à le publier**,
il n'y a aucune mise en ligne du site à faire.

## Publier un article, en trois gestes

1. Écrire l'article dans `articles/<slug>.md` en suivant `CONSIGNES.md` (format, règles,
   faits autorisés). Le slug devient l'adresse : `developpia.fr/blog/<slug>/`.
2. Lancer `python3 outils/publier.py articles/<slug>.md`. Le script vérifie l'article
   (il refuse tout ce qui contredit les consignes), l'ajoute à `index.json`, envoie sur
   GitHub et prévient les moteurs de recherche.
3. Ouvrir le lien affiché. C'est en ligne.

Pour cocher le sujet dans le calendrier : `--sujet "la ligne exacte de sujets.md"`.
Pour vérifier sans publier : `--sans-push`.

## Les fichiers

- `articles/` : un fichier Markdown par article.
- `index.json` : la liste des articles publiés (générée par le script, ne pas éditer à la main).
- `sujets.md` : le calendrier éditorial. La routine prend le premier sujet non coché.
  Léo ou Alex peuvent ajouter, réordonner ou écarter des sujets à tout moment.
- `CONSIGNES.md` : les règles d'écriture, la liste des faits que l'on peut citer, les interdits.
- `ROUTINE.md` : le texte de la routine automatique (deux articles par semaine).
- `outils/publier.py` : le script de publication.

## Comment le site lit ce dépôt

La page `developpia.fr/blog/…` est fabriquée à la demande par une petite fonction du site
(`api/blog.js` dans le dossier developpia-site) qui lit `index.json` et `articles/<slug>.md`
sur `raw.githubusercontent.com`. Un article daté dans le futur reste caché jusqu'à sa date.
Un article avec `brouillon: oui` dans l'en-tête reste caché.
