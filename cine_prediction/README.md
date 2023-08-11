# Projet de prédiction de fréquentation de cinéma

Ce dossier utilise Django pour prédire le nombre d'entrées dans un cinéma, on fait le lien entre une API et une base de données déployées sur Azure.

## URL

Les URL disponibles sont les suivantes :

- `admin/` : accès à l'interface d'administration de Django.
- `login` : page de connexion.
- `signup` : page d'inscription.
- `logout/` : déconnexion de l'utilisateur.
- `prediction` : page de prédiction pour le cinéma et les estimations françaises.
- `bot` : page donnant un mini agenda de 7 jours pour optimiser les 4 salles réservées.
- `prediction_VS_reel` : envoie dans la base de données les chiffres du cinéma.
- `scraping/` : page de scraping.
- `delete_data/` : suppression des données.
- `video/` : page vidéo.

## Fonctionnalités

- La page `prediction` donne les prédictions pour le cinéma et les estimations françaises. Elle fait le lien entre une API et une base de données Azure.
- La page `bot` donne un mini agenda de 7 jours pour optimiser les 4 salles réservées.
- La page `prediction_VS_reel` envoie dans la base de données les chiffres du cinéma.

