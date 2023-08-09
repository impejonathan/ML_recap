# # import requests
# # from bs4 import BeautifulSoup

# # # Définir l'URL de la page que vous souhaitez scraper (page 2 dans cet exemple)
# # url = 'https://www.allocine.fr/films/?page=2'

# # # Envoyer une requête GET à l'URL
# # response = requests.get(url)

# # # Vérifier si la requête a réussi (statut 200)
# # if response.status_code == 200:
# #     # Obtenir le contenu HTML de la page
# #     html_content = response.text

# #     # Utiliser BeautifulSoup pour analyser le contenu HTML
# #     soup = BeautifulSoup(html_content, 'html.parser')

# #     # Trouver tous les titres de films sur la page
# #     titres_films = soup.find_all('a', class_='meta-title-link')

# #     # Parcourir les titres de films et scraper les informations supplémentaires
# #     for titre_film in titres_films:
# #         titre = titre_film.text.strip()  # Titre du film
# #         lien_film = titre_film['href']   # Lien vers la page du film
# #         # Vous pouvez continuer à scraper les informations supplémentaires à partir de "lien_film"

# #         print(titre, lien_film)

# # else:
# #     print('La requête a échoué avec le statut :', response.status_code)
# import requests
# from bs4 import BeautifulSoup

# # Fonction pour obtenir le lien complet à partir du lien relatif
# def get_full_link(rel_link):
#     base_url = 'https://www.allocine.fr'
#     return base_url + rel_link.replace('fichefilm_gen_cfilm=', 'fichefilm-').replace('.html', '/box-office/')

# # Définir l'URL de la page que vous souhaitez scraper (page 2 dans cet exemple)
# url = 'https://www.allocine.fr/films/?page=2'

# # Envoyer une requête GET à l'URL
# response = requests.get(url)

# # Vérifier si la requête a réussi (statut 200)
# if response.status_code == 200:
#     # Obtenir le contenu HTML de la page
#     html_content = response.text

#     # Utiliser BeautifulSoup pour analyser le contenu HTML
#     soup = BeautifulSoup(html_content, 'html.parser')

#     # Trouver tous les titres de films sur la page
#     titres_films = soup.find_all('a', class_='meta-title-link')

#     # Parcourir les titres de films et scraper les informations supplémentaires
#     for titre_film in titres_films:
#         titre = titre_film.text.strip()  # Titre du film
#         lien_film = titre_film['href']   # Lien vers la page du film

#         # Obtenir le lien complet à partir du lien relatif
#         full_link = get_full_link(lien_film)

#         # Envoyer une requête GET à la nouvelle URL
#         film_response = requests.get(full_link)

#         if film_response.status_code == 200:
#             # Obtenir le contenu HTML de la page du film
#             film_html_content = film_response.text

#             # Utiliser BeautifulSoup pour analyser le contenu HTML de la page du film
#             film_soup = BeautifulSoup(film_html_content, 'html.parser')

#             # Trouver le nombre d'entrées du film
#             entrees_element = film_soup.select_one('td[data-heading="Entrées"]')
#             if entrees_element:
#                 entrees = entrees_element.text.strip()
#                 print(titre, full_link, entrees)
#             else:
#                 print(titre, full_link, "Informations sur les entrées non trouvées")
#         else:
#             print('La requête pour le film a échoué avec le statut :', film_response.status_code)
# else:
#     print('La requête a échoué avec le statut :', response.status_code)

import requests
from bs4 import BeautifulSoup
import csv

# Fonction pour obtenir le lien complet à partir du lien relatif
def get_full_link(rel_link):
    base_url = 'https://www.allocine.fr'
    return base_url + rel_link.replace('fichefilm_gen_cfilm=', 'fichefilm-').replace('.html', '/box-office/')

# Ouvrir le fichier CSV en mode écriture
with open('films_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)

    # Ajouter les en-têtes du CSV
    csv_writer.writerow(['Titre', 'Entrées'])

    # Boucle pour parcourir les pages de films
    for page_number in range(1, 7694):  # Start from page 1 and end at page 7693
        # Construire l'URL de la page à scraper
        url = f'https://www.allocine.fr/films/?page={page_number}'

        # Envoyer une requête GET à l'URL
        response = requests.get(url)

        # Vérifier si la requête a réussi (statut 200)
        if response.status_code == 200:
            # Obtenir le contenu HTML de la page
            html_content = response.text

            # Utiliser BeautifulSoup pour analyser le contenu HTML
            soup = BeautifulSoup(html_content, 'html.parser')

            # Trouver tous les titres de films sur la page
            titres_films = soup.find_all('a', class_='meta-title-link')

            # Parcourir les titres de films et scraper les informations supplémentaires
            for titre_film in titres_films:
                titre = titre_film.text.strip()  # Titre du film
                lien_film = titre_film['href']   # Lien vers la page du film

                # Obtenir le lien complet à partir du lien relatif
                full_link = get_full_link(lien_film)

                # Envoyer une requête GET à la nouvelle URL
                film_response = requests.get(full_link)

                if film_response.status_code == 200:
                    # Obtenir le contenu HTML de la page du film
                    film_html_content = film_response.text

                    # Utiliser BeautifulSoup pour analyser le contenu HTML de la page du film
                    film_soup = BeautifulSoup(film_html_content, 'html.parser')

                    # Trouver le nombre d'entrées du film
                    entrees_element = film_soup.select_one('td[data-heading="Entrées"]')
                    if entrees_element:
                        entrees = entrees_element.text.strip()
                        csv_writer.writerow([titre, entrees])  # Écrire dans le fichier CSV
                    else:
                        csv_writer.writerow([titre, "Informations sur les entrées non trouvées"])
                else:
                    print('La requête pour le film a échoué avec le statut :', film_response.status_code)
        else:
            print('La requête a échoué avec le statut :', response.status_code)


