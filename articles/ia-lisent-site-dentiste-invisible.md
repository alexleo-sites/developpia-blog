---
titre: Comment les IA lisent un site de dentiste, et pourquoi le vôtre est peut-être invisible
description: ChatGPT ne trouve pas mon cabinet : pourquoi un site de dentiste reste invisible pour les IA, les quatre murs à vérifier soi-même et la correction de chacun.
accroche: Une IA ne visite pas votre site comme un patient. Elle envoie un robot, lit le texte brut, recoupe avec d'autres sources, puis vous cite ou non. Cet article suit ce chemin pas à pas et montre les quatre murs qui rendent un site de dentiste invisible pour les IA, avec le test de deux minutes pour chacun.
date: 2026-09-18
lecture: 7 min
sujets: les IA, site du cabinet
resume: Le chemin d'un robot d'IA jusqu'à votre site, et les quatre murs qui le rendent invisible : scripts, blocage, texte flou, absence de sources, avec le test et la correction de chacun.
---

Vous avez suivi la méthode de notre article [Votre cabinet dentaire apparaît-il dans ChatGPT ?](https://developpia.fr/blog/cabinet-dentaire-chatgpt-verifier-en-dix-minutes/) et le résultat est tombé : ChatGPT ne trouve pas votre cabinet, ou le cite avec Doctolib et jamais avec votre site. Le chiffre est là. Reste la question du pourquoi.

La réponse tient dans le chemin qu'une IA parcourt pour arriver jusqu'à votre site. Ce chemin est court, mais il passe par quatre portes. Si l'une est fermée, l'IA fait demi-tour et cite un confrère. Voici ce chemin en mots simples, puis chaque mur, avec un test de deux minutes et la correction qui va avec.

## Le chemin d'une IA jusqu'à votre site

Quand un patient tape « dentiste pour un implant à Nantes » dans ChatGPT, l'outil ne répond pas de mémoire. Il lance une recherche, comme vous le feriez sur Google, et obtient une liste de pages. Puis il envoie un robot lire celles qui l'intéressent.

Ce robot a un nom. Pour ChatGPT, c'est OAI-SearchBot, et non GPTBot : GPTBot collecte des textes pour entraîner les modèles, OAI-SearchBot cherche des pages à citer dans les réponses. La [page d'OpenAI sur ses robots](https://platform.openai.com/docs/bots) décrit les deux. Chez Anthropic, l'entreprise derrière Claude, le robot s'appelle ClaudeBot. Chez Perplexity, PerplexityBot.

Le robot demande la page à votre serveur, l'ordinateur qui héberge votre site. Le serveur lui renvoie un fichier texte : la page telle qu'elle part, avant tout affichage. Le robot lit ce fichier tel quel. Il ne lance pas les scripts, ces petits programmes qui construisent la page dans le navigateur du patient. Il ne « voit » pas la page, il lit le texte qui arrive.

Ensuite, l'IA recoupe. Elle compare ce qu'elle a lu chez vous avec votre fiche Google, Doctolib et l'annuaire de l'Ordre. Si tout concorde et répond à la question du patient, elle vous cite, avec la source. Sinon, elle passe au cabinet suivant. Notre guide [Comment ChatGPT choisit le dentiste qu'il recommande](https://developpia.fr/guides/comment-les-ia-choisissent-un-dentiste/) détaille ce choix final. Ici, on regarde ce qui se passe avant : les quatre murs qui arrêtent le robot en route.

## Premier mur : votre texte est construit par des scripts

Beaucoup de sites récents sont livrés presque vides. Le fichier envoyé par le serveur contient une coquille, et ce sont les scripts, écrits en JavaScript, qui vont chercher les textes et les horaires, puis les assemblent dans le navigateur. Pour un patient, tout s'affiche en une seconde. Pour le robot, la page reste vide : pas de soin, pas de ville, pas de nom. Les robots d'OpenAI, d'Anthropic et de Perplexity ne lisent pas le JavaScript. Un site qui affiche son contenu par script est invisible pour eux.

Le test tient en deux minutes. Dans les réglages de votre navigateur, cherchez « JavaScript » et désactivez-le, puis rechargez votre site. Ce que vous voyez alors est ce que voit le robot. Une page blanche, ou un titre seul sans les soins, confirme le problème. Autre façon de faire : clic droit sur la page, « Afficher le code source », puis cherchez une phrase de votre page d'accueil avec la recherche du navigateur. Si elle manque, elle arrive par script.

La correction ne demande pas de refaire le site. Il faut que le texte parte du serveur déjà écrit dans la page : on parle de « rendu côté serveur », et les outils modernes savent le faire. Posez la question à la personne qui gère votre site : « Le texte de mes pages est-il présent dans le code source, sans les scripts ? ». C'est l'une des bases d'un [site de cabinet dentaire](https://developpia.fr/site-internet-cabinet-dentaire/) lisible par une machine.

## Deuxième mur : un portier bloque le robot à l'entrée

Avant même de lire la page, le robot doit passer deux contrôles.

Le premier est Cloudflare, un service de protection utilisé par beaucoup d'hébergeurs pour filtrer le trafic indésirable. Depuis juillet 2025, Cloudflare bloque les robots des IA par défaut, souvent sans que vous le sachiez. Le robot demande la page et trouve porte close.

Le second est le fichier robots.txt, un petit fichier texte à la racine de votre site, qui dit à chaque robot ce qu'il a le droit de lire. Une ligne « Disallow: / », qui veut dire « interdit : tout », placée sous un nom de robot lui ferme le site entier. Certaines agences y ajoutent GPTBot pour éviter que les textes servent à l'entraînement, et mettent OAI-SearchBot dans le même sac. Résultat : ChatGPT ne peut plus vous citer.

Pour vérifier :

- Tapez l'adresse de votre site suivie de /robots.txt dans la barre du navigateur. Cherchez les noms OAI-SearchBot, ClaudeBot, PerplexityBot, ou l'étoile « * » qui désigne tous les robots. La ligne juste en dessous décide : « Disallow: / » bloque, « Allow: / », qui veut dire « autorisé », laisse passer.
- Si votre site passe par Cloudflare, ouvrez son tableau de bord, rubrique des robots d'IA, nommée « AI Crawl Control », le contrôle des robots d'IA. Vous y voyez les robots bloqués et autorisés, un par un.
- Sans ces accès, posez la question à votre hébergeur : « Les robots OAI-SearchBot, ClaudeBot et PerplexityBot sont-ils autorisés à lire mon site ? ».

La correction est un choix, pas une technique : autoriser les robots de recherche des IA. Vous pouvez garder GPTBot fermé si vous refusez que vos textes servent à l'entraînement. Les deux réglages sont indépendants.

## Troisième mur : le robot lit, mais ne comprend pas qui vous êtes

Le robot est entré, il a du texte. Encore faut-il que ce texte réponde à la question du patient. « Un cabinet moderne, une équipe à votre écoute » : aucun de ces mots ne dit un soin, une ville, un nom. L'IA ne devine pas. Elle cherche dans le texte le mot « implant », le mot « Nantes », le nom exact du cabinet.

Puis elle recoupe avec votre fiche Google et Doctolib. Prenez un cabinet fictif : « Cabinet du Parc » sur le site, « Docteur Martin » sur Google, « SELARL du Parc » sur Doctolib, un soin présent ici et absent là. L'IA n'est plus sûre de parler du même cabinet. Elle préfère un confrère dont les informations sont nettes.

Le test : lisez les premières lignes de votre page d'accueil comme un inconnu. Y trouvez-vous le nom du cabinet, la ville et un soin ? Ouvrez ensuite votre [fiche Google](https://developpia.fr/fiche-google-dentiste/) et votre page Doctolib à côté. Comparez le nom, l'adresse, le téléphone et les soins, ligne à ligne.

La correction : un nom identique partout, au caractère près. Une page par soin, avec la ville dans le titre et dans les premières lignes, le déroulé et les honoraires. Les données structurées, une fiche invisible qui décrit le cabinet aux machines, aident l'IA à comprendre la page. Elles ne font pas monter le classement, elles évitent une erreur de lecture.

> **À retenir**
> Une IA cite ce qu'elle a pu lire, comprendre et recouper. Un texte qui arrive par script, un portier qui bloque le robot, une page qui ne dit ni le soin ni la ville, une source unique : chacun de ces quatre murs suffit à rendre un cabinet invisible.

## Quatrième mur : personne d'autre ne parle de vous

Dernier contrôle : l'IA cherche des traces de votre cabinet ailleurs que chez vous. Un site seul, aussi bien fait soit-il, n'a que sa parole. L'annuaire de l'Ordre, votre fiche Google, Doctolib, les annuaires de santé sérieux : chaque page extérieure qui redit le même nom, la même adresse et les mêmes soins renforce la confiance.

Le test : tapez le nom exact de votre cabinet entre guillemets dans Google, suivi de votre ville. Comptez les pages qui ne sont ni votre site, ni votre fiche Google. Si vous n'en trouvez aucune, ou si elles donnent une adresse ancienne, l'IA voit la même chose que vous.

La correction : vérifier que chaque annuaire existe et dit la même chose que votre site, sans en créer de nouveaux à la chaîne. Un annuaire à jour vaut plus que dix fiches contradictoires.

## Ce qui ne change rien, et ce qui a changé

Deux idées circulent beaucoup. La première : un fichier llms.txt, une page de présentation en texte simple destinée aux IA, suffirait à se faire lire. Ce fichier n'a aucun effet prouvé sur le classement. Il ne gêne pas, il ne remplace rien. La deuxième : les données structurées feraient monter un site. Elles aident les machines à comprendre la page, rien de plus.

En revanche, une chose a bien changé. Depuis le 22 juillet 2026, Google affiche en France les Aperçus IA et le Mode IA : une réponse rédigée, placée avant la liste des sites. Google précise sur sa [page sur les fonctionnalités IA](https://developers.google.com/search/docs/appearance/ai-features) qu'aucun réglage à part n'est requis. Les mêmes murs s'appliquent : une page que Google ne peut pas lire n'apparaît ni dans les résultats classiques, ni dans l'Aperçu.

Les quatre murs se vérifient en une soirée. Les faire tomber relève du [référencement dans les IA](https://developpia.fr/referencement-ia-dentiste/), qui commence par le même travail que le référencement classique : un site lisible, des informations identiques partout, des pages qui répondent. Une fois les murs tombés, la question suivante est celle de la page à écrire pour chaque soin.

## Questions fréquentes

### Bloquer GPTBot fait-il disparaître mon cabinet de ChatGPT ?

Non. GPTBot collecte des textes pour entraîner les modèles, OAI-SearchBot cherche des pages à citer dans les réponses. Vous pouvez fermer le premier et laisser passer le second. Vérifiez que votre fichier robots.txt et Cloudflare font bien la différence entre les deux.

### Mon site s'affiche bien sur mon téléphone, il est donc lisible par les IA ?

Pas forcément. Votre téléphone lance les scripts qui construisent la page, le robot ne le fait pas. Le seul test fiable est d'afficher le code source, ou la page sans scripts, et d'y chercher vos textes.

### Faut-il un fichier llms.txt sur le site du cabinet ?

Il ne fait pas de mal, et il n'a aucun effet prouvé sur le classement. Le temps passé à l'écrire est mieux employé à ouvrir le site aux robots et à aligner vos informations partout. Si votre agence le propose en plus du reste, laissez-la faire.
