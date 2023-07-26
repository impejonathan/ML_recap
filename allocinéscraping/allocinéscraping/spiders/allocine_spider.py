
from bs4 import BeautifulSoup
import requests
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import csv
from ..items import AllocinscrapingItem, AllocinescrapingItem

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import subprocess
import re
import random

def convert_to_minutes(time: str) -> int or None:
    '''
    Convert the duration of a movie to minutes.

    Args:
        time (str): The duration of a movie in the format 'h min' or 'h'.

    Returns:
        [int, None]: The duration of the movie in minutes or None if the duration is invalid.
    '''
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



class FilmAgenda(CrawlSpider):
    name = "films_a_venir"
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

        item['note_presse'] = response.css(
            'div.rating-item:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)::text').get()
        item['note_spectateur'] = response.css(
            'div.rating-item:nth-child(2) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)::text').get()

        duration = response.xpath(
            '//div[@class="meta-body-item meta-body-info"]/span[@class="spacer"]/following-sibling::text()[1]').get()
        item["duree"] = convert_to_minutes(duration)

    # Utiliser la boucle pour extraire les genres
        genres = response.css('div.meta-body-item.meta-body-info span::text').getall()
        item['genre'] = [genre.strip() for genre in genres[3:]]        
        
    # Utiliser la fonction pour extraire les nationalités (pays)
        nationalites = response.css('span.that>.nationality::text').getall()
        if nationalites:
            item['pays'] = [nat.strip() for nat in nationalites]
        else:
            item['pays'] = None
            
        item['type'] = response.xpath(
            '//span[@class="what light" and contains(text(), "Type de film")]/following-sibling::span[@class="that"]/text()').get()

        # Utiliser la fonction pour extraire le budget et gérer le cas où il est None
        budget = response.xpath('//span[@class="what light" and contains(text(), "Budget")]/following-sibling::span[@class="that"]/text()').get()
        if budget is not None:
            item['budget'] = budget.strip()
        else:
            item['budget'] = None
            
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
                
        item['réalisateur '] = response.css('span.light + span.blue-link::text').get()
        item['distributeur '] = response.css('div.item span.that.blue-link::text').get()

        # Nettoyer la description en supprimant les sauts de ligne et les espaces inutiles
        description = response.xpath('//div[@class="content-txt "]//text()').get()
        if description is not None:
            item['description'] = description.replace('\n', '').strip()
        else:
            item['description'] = None

        item['date'] = response.css('span.date.blue-link::text').get()
        item['annee_production'] = response.xpath(
            '//span[@class="what light" and contains(text(), "Année de production")]/following-sibling::span[@class="that"]/text()').get()


        return item


def run_spider():
    subprocess.run(["scrapy", "crawl", "films_a_venir", "-O", "data/films_a_venir.csv"])


run_spider()