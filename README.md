# Projet d'Optimisation de Programmation Cinématographique

    Ce projet a été réalisé dans le cadre de la formation Dev IA chez Simplon HDF. Il s'agit d'une collaboration en méthode agile entre Olivier Kotwica, Jonathan Impe et Ahmad Darwiche, qui a duré un mois. On vise à développer un modèle de machine learning afin d'aider les gérants de salles de cinéma à optimiser leur programmation. Actuellement, les gérants passent beaucoup de temps à sélectionner les films à projeter en se basant sur les dernières nouveautés et en assistant à des festivals majeurs comme Cannes et Deauville. Notre objectif est de simplifier ce processus en créant un outil d'aide à la décision.

# Objectifs Principaux

    Créer une application utilisant des techniques d'apprentissage automatique pour prédire l'affluence des films lors de leur première semaine de diffusion.
    Maximiser les revenus en recommandant les films les plus susceptibles de générer un grand nombre d'entrées.
    Optimiser la programmation en suggérant le nombre de salles, le nombre de séances et les horaires pour chaque film.

# Caractéristiques de la Salle de Cinéma

    Le cinéma en question dispose de quatre salles avec les capacités suivantes :

    Salle 1 : 140 personnes
    Salle 2 : 100 personnes
    Salle 3 : 80 personnes
    Salle 4 : 80 personnes

# Méthode Agile

    Nous sommes une équipe junior de 3 personnes travaillant dans le domaine des données. Pour garantir une organisation efficace, nous adopterons une approche agile pour le développement de l'application. Nous utiliserons l'outil Jira pour planifier les différentes étapes du projet, attribuer des tâches et suivre l'avancement en temps réel.

# Outils et Technologies

    Pour la collecte de données, nous utilisons l'outil Scrapy pour extraire les informations pertinentes d'un site web, nous requetons également des api's.
    Les données collectées seront stockées dans une base de données SQL Azure pour une analyse ultérieure.
    Pour les analyses et les visualisations de données, nous utiliserons des bibliothèques Python telles que pandas, matplotlib, seaborn et plotly express.
    Pour l'interface utilisateur conviviale, nous créerons un MVP (Minimum Viable Product) en utilisant Streamlit.
    Le projet final sera développé sur le framework web Django, reconnu pour sa puissance et sa flexibilité.

# Prévisions et Recommandations

    Notre application utilisera des techniques d'apprentissage automatique pour générer des recommandations personnalisées pour chaque gérant de salle. Ces recommandations se baseront sur des algorithmes de filtrage basé sur le contenu, prenant en compte les genres et les styles des films.
    Nous nous appuierons sur des données de fréquentation passées et des tendances du box-office pour prédire quels films seront les plus susceptibles de réussir en première semaine.
    Contraintes et Rentabilité

    Il est important de noter que l'ouverture d'une salle de cinéma qui ne remplit pas au minimum 20 % de sa capacité ne serait pas rentable. Par conséquent, en utilisant la ressource "répartition des spectateurs par semaine" en 2017, nous déterminerons les jours et les salles à ouvrir pour garantir la rentabilité.
    Échéancier

    Nous disposons de 4 semaines pour réaliser cette application. Notre approche agile nous permettra de répartir efficacement les tâches, de suivre les progrès et d'ajuster notre stratégie en cours de route.

    En résumé, ce projet consiste à développer une application utilisant des techniques d'apprentissage automatique pour aider les gérants de salles de cinéma à optimiser leur programmation en prédisant l'affluence des films lors de la première semaine de diffusion. Notre équipe s'appuiera sur des méthodes agiles, des outils de collecte de données et d'analyse, ainsi que sur des technologies de développement web pour réaliser cet objectif dans le délai imparti.