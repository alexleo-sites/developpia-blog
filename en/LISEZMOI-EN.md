# Le blog en anglais (en.developpia.fr/blog/)

Le site anglais lit le même dépôt `developpia-blog` que le site français, mais dans le dossier `en/` :

- `en/index.json` : la liste des articles anglais (celle que lit en.developpia.fr/blog/) ;
- `en/articles/<slug-anglais>.md` : un article, même format que les articles français.

Comme en français, il n'y a aucune mise en ligne à faire : l'article est visible sur `https://en.developpia.fr/blog/<slug-anglais>/` dans les dix minutes qui suivent le push. Le site français lit aussi `en/index.json` : son bouton EN mène alors directement à l'article anglais.

## Règle

Chaque nouvel article français reçoit sa version anglaise LE JOUR MÊME. La version anglaise est relue contre le français, paragraphe par paragraphe, en particulier pour le vocabulaire technique (SEO, Google Business Profile, AI Overviews, Dental Council, fees, etc.) : consignes complètes dans `CONSIGNES-BLOG-EN.md`.

## Marche à suivre

1. **Traduire.** Choisir le slug anglais (court, en minuscules, avec la requête visée en anglais) et l'ajouter à `slugs.json` (français → anglais). Écrire `en/articles/<slug-anglais>.md` :
   - mêmes clés d'en-tête que le français (`titre`, `titre_court`, `description`, `accroche`, `date`, `lecture`, `sujets`, `resume`, `genre` si présent), valeurs en anglais ;
   - `date` identique à celle de l'article français ;
   - `sujets` pris uniquement dans la liste anglaise : deciding, practice website, Dental Council rules, Google Maps, social media, measuring, visibility, AI search, by type of practice, glossary ;
   - une dernière ligne d'en-tête `fr: <slug-français>` ;
   - la FAQ sous le titre `## Frequently asked questions`, une question par `###` ;
   - les liens vers nos pages en version anglaise (`https://en.developpia.fr/...`, correspondances dans `CONSIGNES-BLOG-EN.md`).
2. **Relier.** Comme en français, ajouter dans deux anciens articles anglais un lien vers le nouveau (le même que dans les articles français reliés).
3. **Reconstruire l'index.** Depuis la racine du dépôt :

   ```
   python3 outils/construire-index-en.py
   ```

   Le script relit tous les fichiers `en/articles/*.md`, vérifie l'en-tête (champs, sujets, slug `fr` connu dans `index.json`), recopie le champ `ordre` de l'article français et écrit `en/index.json`. À la moindre erreur, il n'écrit rien et affiche la liste des problèmes.
   Si on corrige seulement le corps d'un article (sans toucher à l'en-tête) : `python3 outils/construire-index-en.py --touche <slug-anglais>` pour que Google relise la page.
4. **Commit et push**, fichier par fichier (jamais `git add -A`) :

   ```
   git add en/articles/<slug-anglais>.md en/index.json
   git commit -m "Blog EN : <titre>"
   git push
   ```

5. **Vérifier** : `https://en.developpia.fr/blog/<slug-anglais>/` répond, et le bouton EN de l'article français y mène.

## Bon à savoir

- Un article anglais daté dans le futur ou avec `brouillon: oui` reste caché, comme en français.
- Une adresse anglaise tapée avec le slug français (`en.developpia.fr/blog/<slug-français>/`) redirige vers l'article anglais.
- Les pages anglaises sont pour l'instant en `noindex` (comme tout le site anglais) : le jour du lancement, changer `ROBOTS` en haut de `api/blog.js` dans le projet anglais.
