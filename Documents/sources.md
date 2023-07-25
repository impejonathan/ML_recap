*Identification des sources de données et mise en place des outils de scraping*


Nous avons identifié de nombreux sites internets qui fournissent différentes données sur les films :

- http://www.cine-directors.net/
    manques de données sur les films
- https://www.cineserie.com/box-office/
    manques de données sur les films
- https://www.ecranlarge.com/films/box-office/fr
    manques de données sur les films
- https://www.senscritique.com/
    manques de données sur les films
...
- https://fr.wikipedia.org/wiki/Liste_des_plus_gros_succ%C3%A8s_du_box-office_en_France
    les informations sur les films assez completes mais pas pratique a scraper
- https://cbo-boxoffice.com/v4/page000.php3
    tres bonnes informations sur les films et complets mais nécessite un abonnement payant
- https://www.allocine.fr/
    les informations sur les films assez completes et pratique a scraper

Le site que nous avons retenus est `allociné` car il rassemble des données assez completes sur les films deja sortie et à sortir.
Le fait d'avoir 1 seul site à scraper permet d'avoir une certaine homogénéité sur les données.


Nous allons réaliser différents scraping :

- pour créer une bdd qui servira à l'entrainement du model
    1 scraping pour les features (nom du film, acteurs, producteur, date de sortie, ...)
    1 scraping pour la target (nombre de spectateur pour la 1ere semaine en France)
- pour récupérer les films qui vont sortir
- pour récupérer le nombre de spectateur pour la 1ere semaine des films sortie la semaine précédente
