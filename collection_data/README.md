# Allociné et Obtention des infos depuis TMDb

Ce dossier combine le scraping de données de films à partir du site web Allociné et l'obtention d'autre informations à partir de l'API TMDb (The Movie Database). L'objectif est de collecter le max des informations sur les films.

## Utilisation

    Assurez-vous d'installer les dépendances requises pour chaque script en exécutant :

    sh

    pip install scrapy requests pandas

    Exécutez le script movies_spider.py pour collecter les données de films à partir d'Allociné :

    sh

    scrapy runspider movies_spider.py -o films.json

    Exécutez le script get_movie_budgets.py pour obtenir les budgets de films à partir de TMDb en utilisant les données collectées précédemment :

    sh

    python get_movie_budgets.py -i films.json -o films_with_budgets.json