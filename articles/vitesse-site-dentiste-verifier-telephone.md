---
titre: Vitesse du site d'un dentiste : la vérifier sur téléphone en cinq minutes
titre_court: Vitesse du site d'un dentiste : le test en cinq minutes
description: Mesurer la vitesse de votre site de dentiste : le test gratuit de Google, les trois chiffres et leurs seuils officiels, puis six gestes sur téléphone.
accroche: La vitesse du site d'un dentiste se vérifie sans connaissance technique, en cinq minutes, avec l'outil gratuit de Google et votre propre téléphone. Voici les trois chiffres à lire, les seuils que Google publie, ce qu'une étude sur des millions de pages a mesuré, et qui doit corriger quoi.
date: 2026-10-26
lecture: 7 min
sujets: site du cabinet, mesurer
resume: Comment vérifier la vitesse et l'affichage sur téléphone du site d'un cabinet dentaire : le test PageSpeed Insights, les trois signaux de Google et leurs seuils, l'étude Ahrefs sur 43,66 millions de pages, six gestes sur téléphone et le tableau des causes.
etude: https://ahrefs.com/blog/core-web-vitals-study
---

Un samedi matin, dans un cabinet fictif de Nantes. Une patiente a mal depuis la veille. Elle tape « dentiste urgence Nantes » sur son téléphone, dans le bus, avec une connexion moyenne. Elle ouvre le premier site de la liste. L'écran reste blanc, puis une grande photo s'affiche, puis le texte saute vers le bas au moment où elle veut toucher le numéro. Elle revient en arrière et ouvre le cabinet suivant.

Le praticien n'en saura jamais rien. Sur son ordinateur du cabinet, relié à une bonne connexion, son site s'ouvre très bien. C'est tout le piège : la vitesse du site d'un dentiste se juge là où le patient le regarde, sur un téléphone, et rarement dans de bonnes conditions. Cet article vous donne une vérification en deux temps, d'abord avec l'outil gratuit de Google, ensuite avec votre propre téléphone.

## Pourquoi la vitesse compte pour un site de dentiste

Elle compte deux fois. Pour le patient d'abord : il cherche souvent un cabinet dans l'urgence, depuis son téléphone, et il veut appeler. Chaque seconde d'écran blanc lui donne une raison d'aller voir ailleurs. Pour Google ensuite : le moteur mesure l'expérience que vivent les visiteurs sur chaque site, et il recommande clairement d'obtenir de bons résultats sur ces mesures, comme l'écrit sa [page officielle sur les signaux web essentiels](https://developers.google.com/search/docs/appearance/core-web-vitals?hl=fr).

Gardez la juste mesure. Un site rapide ne remplace pas un bon contenu : une page de soin claire, des honoraires lisibles et un numéro visible pèsent davantage. Nous avons classé la lenteur parmi [les sept erreurs qu'on voit sur les sites de cabinets dentaires](https://developpia.fr/blog/sept-erreurs-sites-cabinets-dentaires/), mais elle se règle souvent en dernier, une fois le contenu en place.

## Les trois chiffres que Google regarde

Google résume l'expérience d'une page en trois mesures, qu'il appelle les signaux web essentiels (Core Web Vitals en anglais). Le [lexique du référencement dentaire](https://developpia.fr/blog/lexique-referencement-dentaire/#vitesse-de-chargement-core-web-vitals) les présente en une ligne. Les voici expliqués avec une scène du cabinet.

- **L'affichage du contenu principal** (LCP, pour « Largest Contentful Paint »). C'est le temps que met la plus grande chose de l'écran, souvent la photo d'accueil ou le grand titre, à apparaître. Le patient le vit comme « la page est là ».
- **La réaction au toucher** (INP, pour « Interaction to Next Paint »). C'est le délai entre le moment où le patient touche un bouton, par exemple « Prendre rendez-vous », et le moment où l'écran réagit.
- **La stabilité de la page** (CLS, pour « Cumulative Layout Shift »). C'est ce qui bouge pendant le chargement. Le patient veut toucher le numéro, une image arrive, le texte descend, et il touche autre chose.

Google publie les seuils de chacune de ces mesures dans l'[aide de la Search Console](https://support.google.com/webmasters/answer/9205520?hl=fr) :

| Mesure | Bon | Amélioration nécessaire | Médiocre |
|---|---|---|---|
| Affichage du contenu principal (LCP) | jusqu'à 2,5 secondes | jusqu'à 4 secondes | plus de 4 secondes |
| Réaction au toucher (INP) | jusqu'à 200 millisecondes | jusqu'à 500 millisecondes | plus de 500 millisecondes |
| Stabilité de la page (CLS) | jusqu'à 0,1 | jusqu'à 0,25 | plus de 0,25 |

La même aide précise deux points utiles. Ces mesures viennent de vrais visiteurs qui utilisent le navigateur Chrome, sur les 28 derniers jours. Et quand une page réunit trop peu de visites, Google ne la note pas seule : il se rabat sur l'ensemble du site, ou n'affiche rien.

## Ce qu'une étude a mesuré sur des millions de pages

Beaucoup de sites ne passent pas ces trois seuils, et ce n'est pas propre aux dentistes. En janvier 2022, l'éditeur d'outils Ahrefs a publié une [étude sur les signaux web essentiels](https://ahrefs.com/blog/core-web-vitals-study), signée par Patrick Stox. Elle croise les mesures publiques de Google et l'analyse de 43,66 millions de pages par l'outil de l'éditeur. Parmi elles, 5,21 millions avaient au moins une mesure publiée par Google.

Deux chiffres en ressortent. Près de 33 % des sites passaient les trois seuils. Au niveau des pages, la part tombait à 21,2 %. L'auteur relève que la mesure la plus difficile à tenir est l'affichage du contenu principal, surtout sur une connexion lente.

Lisez ces chiffres avec leurs limites. L'étude date de 2022, elle porte sur le web en général, pas sur les cabinets dentaires, et elle mesurait la réactivité avec un indicateur que Google a remplacé depuis. Elle dit au moins une chose solide : un site qui passe les trois seuils fait partie d'une minorité, et c'est presque toujours la grande image du haut de page qui coince.

> **La phrase à retenir**
> La vitesse de votre site se juge sur un téléphone, avec une connexion moyenne, pas sur l'ordinateur du cabinet. Si la page met du temps à s'afficher ou bouge sous le doigt, c'est le patient pressé qui part, avant même d'avoir lu votre nom.

## Étape 1 : le test de Google en deux minutes

L'outil s'appelle PageSpeed Insights. Il est gratuit et ne demande aucun compte.

1. Ouvrez [PageSpeed Insights](https://pagespeed.web.dev/?hl=fr) sur un ordinateur.
2. Collez l'adresse de votre page d'accueil, puis lancez l'analyse.
3. Restez sur l'onglet « Mobile », celui du téléphone. C'est lui qui compte.
4. Lisez d'abord le bloc du haut, celui des données de vrais visiteurs. Il dit si la page réussit ou échoue à l'évaluation des signaux web essentiels, et donne les trois mesures avec leur couleur.
5. Si ce bloc indique qu'il n'y a pas assez de données, c'est fréquent pour un site de cabinet, qui reçoit peu de visites. Passez alors au bloc du dessous, le diagnostic. Il simule un téléphone sur une connexion moyenne et donne une note sur 100.
6. Refaites le test avec votre page de soin la plus importante, par exemple la page implants ou la page urgences.

Ne vous attachez pas à la note sur 100. Elle sert à comparer une page avant et après une correction, pas à juger le site. Ce qui compte, ce sont les trois mesures et leur couleur.

## Étape 2 : six gestes sur votre propre téléphone

Le test de Google ne voit pas tout. Il ne sait pas si votre numéro est facile à toucher ou si votre tableau d'honoraires se lit sans zoomer. Pour ça, prenez votre téléphone et coupez le wifi pour passer en 4G.

- **Ouvrez le site depuis Google**, en tapant le nom du cabinet, comme un patient. Comptez en silence jusqu'à ce que le texte soit lisible.
- **Touchez le numéro de téléphone.** L'appel doit se proposer tout de suite, sans copier ni recopier de chiffres.
- **Ouvrez le menu** et allez sur une page de soin. Le menu doit s'ouvrir du premier coup et se refermer facilement.
- **Lisez une page sans zoomer.** Si vous écartez les doigts pour lire, le texte est trop petit.
- **Regardez si quelque chose saute** pendant le chargement : une bannière qui pousse le texte, une fenêtre qui arrive après coup.
- **Touchez le bouton de rendez-vous.** Le lien vers votre agenda en ligne doit s'ouvrir sans détour.

Faites le même tour sur un téléphone plus ancien, celui d'un proche ou de l'assistante. Vos patients n'ont pas tous un appareil récent. Si l'un de ces gestes coince, notez la page et le moment exact : c'est l'information qui fera gagner du temps à la personne qui corrigera.

## Ce que vous voyez, et qui corrige

Les causes se ressemblent d'un site de cabinet à l'autre. Ce tableau vous aide à savoir à qui en parler.

| Ce que vous voyez | Cause la plus fréquente | Qui corrige |
|---|---|---|
| L'écran reste blanc, puis une grande photo arrive | Photo d'accueil trop lourde, envoyée telle quelle depuis un appareil | Celui qui met à jour le site, souvent en une séance |
| Le texte descend pendant le chargement | Image ou bandeau sans place réservée | Le prestataire du site |
| Les boutons réagissent avec retard | Trop de modules ajoutés : fenêtre de discussion, carte, animations | Le prestataire, en retirant ce qui ne sert pas |
| La page est lente même sans photo | Habillage chargé ou hébergement faible | À trancher : corriger ou refaire |
| Le texte est trop petit, il faut zoomer | Site pensé pour un écran d'ordinateur | Souvent une refonte |

Les deux premières lignes se corrigent sans toucher au reste du site. Les deux dernières posent une vraie question de construction : les cinq questions pour [refaire le site d'un cabinet dentaire ou le corriger](https://developpia.fr/blog/refaire-site-cabinet-dentaire-comment-decider/) aident à trancher.

Un point à surveiller pendant les corrections : un site rendu plus rapide par des effets affichés par script peut devenir invisible pour les robots des IA, qui ne lisent pas ce type de contenu. Nous l'expliquons dans l'article sur [la façon dont les IA lisent un site de dentiste](https://developpia.fr/blog/ia-lisent-site-dentiste-invisible/). Le texte des pages doit rester dans le code de la page.

## Quand refaire le test

Une fois suffit rarement. Trois moments s'y prêtent :

1. Après chaque ajout de photo ou de vidéo sur le site.
2. Après l'ajout d'un module : prise de rendez-vous intégrée, fenêtre de discussion, carte.
3. Une fois par trimestre, en même temps que vous regardez le reste de votre présence en ligne.

Rappelez-vous que les mesures de vrais visiteurs portent sur 28 jours. Une correction faite aujourd'hui n'apparaîtra donc pleinement dans le bloc du haut qu'un mois plus tard. Le diagnostic du dessous, lui, change tout de suite.

La vitesse n'est qu'une partie de ce que doit réussir un [site internet de cabinet dentaire](https://developpia.fr/site-internet-cabinet-dentaire/) : la page explique comment nous construisons des sites pensés d'abord pour le téléphone. Et pour voir comment la vitesse s'inscrit dans le travail global de visibilité, la page [référencement dentiste](https://developpia.fr/referencement-dentiste/) reprend l'ensemble. Si vous voulez un premier regard sur votre site, le [test gratuit du référencement](https://developpia.fr/tester-mon-referencement/) donne un score en quelques minutes.

## Questions fréquentes

### Comment savoir si le site de mon cabinet dentaire est trop lent ?

Passez la page d'accueil dans PageSpeed Insights, l'outil gratuit de Google, onglet mobile. Regardez les trois mesures et leur couleur : vert veut dire bon, orange à améliorer, rouge médiocre. Complétez par un essai sur votre téléphone en 4G, wifi coupé, en comptant jusqu'à ce que le texte se lise.

### La vitesse du site joue-t-elle sur la place du cabinet dans Google ?

Google mesure l'expérience des visiteurs et recommande d'obtenir de bons résultats sur ses trois signaux web essentiels. Mais un site rapide ne passe pas devant un site plus utile : le contenu des pages, la fiche Google et la cohérence des informations comptent davantage. La vitesse aide surtout à ne pas perdre le patient qui a déjà cliqué.

### Pourquoi PageSpeed Insights n'affiche-t-il pas de données pour mon site ?

Les données du haut viennent de vrais visiteurs qui utilisent Chrome, et il en faut un minimum pour que Google les publie. Un site de cabinet reçoit souvent trop peu de visites pour ça. Utilisez alors le diagnostic du bloc du dessous, qui simule un téléphone, et refaites-le après chaque correction.

La prochaine fois que vous ajoutez une belle photo à votre site, ouvrez-le juste après sur votre téléphone, wifi coupé : c'est le geste le plus simple pour garder un site rapide.
