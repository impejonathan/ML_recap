import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import subprocess
import re
import pandas as pd
import numpy as np
import pyodbc
from dotenv import load_dotenv
import os
from datetime import datetime
from datetime import datetime, timedelta

def remove_duplicates(cursor):
    cursor.execute("""
        DELETE FROM [dbo].[films_prediction]
        WHERE [titre] IN (
            SELECT [titre]
            FROM [dbo].[films_prediction]
            GROUP BY [titre]
            HAVING COUNT(*) > 1
        )
    """)


def clean_date(date_str):
    if isinstance(date_str, float):  # Ignorer les valeurs de type float
        return None
    date_str = date_str.strip()  # Enlever les espaces au début et à la fin
    date_str = date_str.replace(',', '')
    date_str = date_str.replace('\n', '')  # Enlever les virgules et sauts de ligne
    
    # Trouver l'année en dehors de la première occurrence de la date
    year_pos = date_str.find('\t')
    if year_pos != -1:
        year_str = date_str[year_pos + 1:]  # Extraire l'année
        date_str = date_str[:year_pos]  # Garder seulement la première occurrence de la date
    else:
        year_str = ''
    
    # Vérifier si la date est bien formatée avec trois parties : jour, mois et année
    parts = date_str.split()
    if len(parts) != 3:
        return None  # Retourner None si la date n'est pas bien formatée
    
    day, month, year = parts  # Séparer le jour, le mois et l'année
    month_dict = {
        'janvier': '01',
        'février': '02',
        'mars': '03',
        'avril': '04',
        'mai': '05',
        'juin': '06',
        'juillet': '07',
        'août': '08',
        'septembre': '09',
        'octobre': '10',
        'novembre': '11',
        'décembre': '12'
    }
    # Formater la date avec des zéros pour le jour et le mois si nécessaire
    day = day.zfill(2)
    month = month_dict.get(month.lower(), '00')  # Utiliser '00' si le mois n'est pas valide
    return f"{day}-{month}-{year}{year_str}"

def convert_to_minutes(time: str) -> int or None:
    if time:
        # Remove any leading/trailing whitespace or newline characters
        time = time.strip()

        if 'h' in time and 'min' in time:
            hours, minutes = time.split('h ')
            minutes = minutes.replace('min', '').strip()
            duration = int(hours) * 60 + int(minutes)
        elif 'h' in time:
            hours = time.replace('h', '').strip()
            duration = int(hours) * 60
        elif 'min' in time:
            minutes = time.replace('min', '').strip()
            duration = int(minutes)
        else:
            duration = None
    else:
        duration = None

    return duration

class SenscritiqueSpider(CrawlSpider):
    name = "allocine_sortie"
    allowed_domains = ["www.allocine.fr"]
    url = [
        "https://www.allocine.fr/film/agenda/",
    ]
    start_urls = ["https://www.allocine.fr/film/agenda/"]
    film_details = LinkExtractor(restrict_css='h2 > a')
    rule_film_details = Rule(film_details,
                             callback='parse_item',
                             follow=False,
                             )

    rules = (rule_film_details,)

    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers={
                'User-Agent': self.user_agent
            })

    def parse_item(self, response):
        item = {}
        item["titre"] = response.xpath('//*[@id="content-layout"]/div[2]/div[1]/text()').get()

        # Utiliser css pour extraire la liste des acteurs
        acteurs = response.css('div.meta-body-item.meta-body-actor span:not(.light)::text').getall()

        # Diviser la liste des acteurs en trois nouvelles colonnes
        item['acteur_1'] = acteurs[0].strip() if len(acteurs) >= 1 else None
        item['acteur_2'] = acteurs[1].strip() if len(acteurs) >= 2 else None
        item['acteur_3'] = acteurs[2].strip() if len(acteurs) >= 3 else None

        item['realisateur'] = response.css('span.light + span.blue-link::text').get()
        
        item['distributeur'] = response.css('div.item span.that.blue-link::text').get()
        

        duration = response.xpath(
            '//div[@class="meta-body-item meta-body-info"]/span[@class="spacer"]/following-sibling::text()[1]').get()
        item["duree"] = convert_to_minutes(duration)

        # Utiliser la boucle pour extraire les genres
        genres = response.css('div.meta-body-item.meta-body-info span::text').getall()
        item['genre'] = genres[3].split(',')[0].strip() if len(genres) >= 4 else None
    
        
        # Utiliser la boucle pour extraire les nationalités
        nationalites = response.css('span.that>.nationality::text').getall()
        if nationalites:
            item['pays'] = nationalites[0].split(',')[0].strip()
        else:
            item['pays'] = None

        # Utiliser la fonction pour extraire les récompenses et gérer les cas vides, 5 nominations ou 1 prix et 8 nominations
        recompenses = response.xpath('//span[@class="what light" and contains(text(), "Récompenses")]/following-sibling::span/text()').get()
        if recompenses:
            recompenses = recompenses.strip()
            if "nominations" in recompenses:
                nominations, *prix_list = re.findall(r'\d+', recompenses)
                item['nominations'] = int(nominations)
                item['prix'] = int(prix_list[0]) if prix_list else 0
            elif "prix" in recompenses:
                item['nominations'] = 0
                item['prix'] = int(re.findall(r'\d+', recompenses)[0])
            else:
                item['nominations'] = 0
                item['prix'] = 0
        else:
            item['nominations'] = 0
            item['prix'] = 0
                
                    
        item['date'] = response.css('span.date.blue-link::text').get()
        item['annee_production'] = response.xpath(
            '//span[@class="what light" and contains(text(), "Année de production")]/following-sibling::span[@class="that"]/text()').get()

        
            # Utiliser la fonction clean_date pour nettoyer la date
        item['date'] = clean_date(item['date'])
        
        # Charger les variables d'environnement à partir du fichier .env
        load_dotenv()

        # Récupérer les informations de connexion à la base de données à partir des variables d'environnement
        server = os.environ['DB_SERVER']
        database = os.environ['DB_DATABASE']
        username = os.environ['DB_USERNAME']
        password = os.environ['DB_PASSWORD']
        driver = os.environ['DRIVER']

        # Construire la chaîne de connexion à la base de données
        cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

        # Créer un curseur pour exécuter des requêtes SQL
        cursor = cnxn.cursor()
        
        remove_duplicates(cursor)


        # Exemple d'insertion d'une ligne dans la table films_prediction
        cursor.execute("""
            INSERT INTO [dbo].[films_prediction] (titre, acteur_1, acteur_2, acteur_3, realisateur, distributeur, duree, genre, pays, nominations, prix, date, annee_production)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, item["titre"], item["acteur_1"], item["acteur_2"], item["acteur_3"], item["realisateur"], item["distributeur"], item["duree"], item["genre"], item["pays"], item["nominations"], item["prix"], item["date"], item["annee_production"])

        
        
        
        # Valider les changements dans la base de données
        cnxn.commit()
        
# Fonction pour exécuter le web scraping
def run_spider():
    subprocess.run(["scrapy", "crawl", "allocine_sortie"])


run_spider()
