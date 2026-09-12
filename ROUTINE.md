# La routine « un article de blog » (texte exact de la tâche automatique)

Tâche planifiée sur le Mac de Léo (application Claude ouverte) : `blog-developpia-article`,
du lundi au vendredi à 7 h 30. Le même texte peut être collé dans une routine cloud
(claude.ai/code/routines) le jour où le dépôt GitHub `alexleo-sites/developpia-blog` y est
rattaché : rien d'autre ne change.

---

Tu publies UN SEUL article sur le blog de DeveloppIA (agence de référencement pour les
cabinets dentaires, site https://developpia.fr), puis tu t'arrêtes. Réponds en français,
en phrases simples, sans vocabulaire technique.

DOSSIER : `/Users/poinc/Desktop/Agence IA/developpia-blog` (dépôt git relié à GitHub
`alexleo-sites/developpia-blog`). Le site lit ce dépôt à chaque visite : déposer un
article et le pousser suffit à le publier. Tu ne touches à rien d'autre.

ÉTAPES, dans cet ordre, sans en sauter :

1. Mets le dépôt à jour : `git -C "/Users/poinc/Desktop/Agence IA/developpia-blog" pull --ff-only`.
   Si la commande échoue, arrête-toi et dis-le.
2. Lis `CONSIGNES.md` en entier, puis `sujets.md` et `index.json`.
3. Choisis le sujet : la première ligne `- [ ]` de `sujets.md` qui contient « PRIORITÉ »,
   sinon la première ligne `- [ ]` du fichier. Ignore les lignes contenant « ÉCARTÉ ».
   S'il ne reste aucun sujet, envoie sur Slack, canal #direction (C0BKPKZHC2D) :
   « Le calendrier du blog DeveloppIA est vide : ajoutez des sujets dans sujets.md » et arrête-toi.
4. Pour ne pas te répéter, lis les trois derniers articles publiés (les trois premiers
   slugs de `index.json`, fichiers dans `articles/`). Lis aussi, avec WebFetch, la page de
   developpia.fr la plus proche du sujet (une page de service ou un guide) : ton article
   la complète, il ne la recopie pas.
5. Écris l'article dans `articles/<slug>.md` en respectant `CONSIGNES.md` à la lettre :
   en-tête complet, 1 200 à 1 600 mots, 5 à 8 titres `##`, exactement un encart, au moins
   une liste, trois questions fréquentes, au moins trois liens vers developpia.fr, un ou
   deux liens vers une source officielle, aucun chiffre hors de la liste des faits
   autorisés, aucun tiret cadratin, aucune promesse de position, aucun prix, aucun
   témoignage, aucun mot anglais non expliqué. La date est celle d'aujourd'hui.
6. Lance `python3 outils/publier.py articles/<slug>.md --sujet "<la ligne du sujet, sans le - [ ]>"`
   depuis le dossier du dépôt. S'il refuse, corrige l'article et relance, trois
   tentatives au maximum. S'il refuse encore : supprime le fichier, ne publie rien, et
   dis pourquoi dans ta réponse et sur Slack.
7. Vérifie avec WebFetch que https://developpia.fr/blog/<slug>/ affiche bien le titre.
   Si la page ne répond pas, attends deux minutes et réessaie une fois.
8. Envoie sur Slack #direction (C0BKPKZHC2D) un message de trois lignes au plus :
   « 📝 Nouvel article sur le blog DeveloppIA : <titre> », puis « À lire : <adresse> (le blog) »,
   puis le nombre total d'articles publiés. Une adresse ne termine jamais une ligne.

INTERDITS : modifier un autre fichier que l'article, `index.json` et `sujets.md` ; toucher
au dossier developpia-site ; lancer une mise en ligne Vercel ; publier deux articles dans
le même passage ; inventer un chiffre ; écrire un prix ou une promesse de résultat.
