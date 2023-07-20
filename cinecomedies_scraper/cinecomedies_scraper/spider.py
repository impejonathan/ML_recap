import scrapy
import csv
import datetime
from datetime import timedelta
import os

class CineComediesSpider(scrapy.Spider):
    name = "cinecomedies_spider"
    
    # Liste des noms des mois en français
    mois_en_francais = [
        'janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout',
        'septembre', 'octobre', 'novembre', 'decembre'
    ]   

    def get_week_range(self, date):
        # Aller au mercredi de la semaine
        start = date - timedelta(days=date.weekday() - 2)
        # Aller au mardi de la semaine suivante
        end = start + timedelta(days=6)

        # Formater les dates
        start_str = f"{start.day}"
        end_str = f"{end.day} {self.mois_en_francais[end.month - 1]} {end.year}"

        # Vérifier si le début et la fin de la semaine sont dans des mois différents
        if start.month != end.month:
            start_str += f" {self.mois_en_francais[start.month - 1]}"

        return f"http://www.cinecomedies.com/box-office-semaine/box-office-francais-du-{start_str}-au-{end_str}/"

    def remplacer_espaces_par_tirets(self, phrase):
        return phrase.replace(' ', '-')

    def start_requests(self):
        list_periode = []
        current_date = self.start_date
        while current_date < self.end_date:
            # Construire l'URL pour chaque période de mercredi à mardi suivant
            url = self.remplacer_espaces_par_tirets(self.get_week_range(current_date))
            list_periode.append(url)
            current_date += timedelta(weeks=1)

        for url in list_periode:
            yield scrapy.Request(url=url, callback=self.parse)

    start_date = datetime.datetime(2014, 1, 1)  # Date de début de l'année 2020
    end_date = datetime.datetime.now()  # Date actuelle 
    
    def parse(self, response):
        # Utilisez le sélecteur CSS pour obtenir toutes les lignes de la table
        rows = response.css("table.dataTable tbody tr")

        if rows:
            data = []
            for row in rows:
                # Sélectionnez le titre dans les deux types de balises spécifiées
                title_part1 = row.css("td:nth-child(1) strong::text").getall()
                title_part2 = row.css("td:nth-child(1) strong a::text").getall()

                # Choisissez le titre en fonction de celui qui est présent
                if title_part1:
                    title = " ".join(title_part1).strip().replace('\n', '').lower()
                elif title_part2:
                    title = " ".join(title_part2).strip().replace('\n', '').lower()
                else:
                    title = None
                entries_net = row.css("td:nth-child(2)::text").get()
                entries = entries_net.replace(".", "")
                weeks = row.css("td:nth-child(3)::text").get()
                # copies = row.css("td:nth-child(6)::text").get()

                # Vérifiez si la valeur de "Semaines" est égale à 1 avant d'ajouter les données
                if weeks == '1':
                    data.append([title, entries, weeks])
            
            # Enregistrez les données dans le fichier CSV
            filename = "cinecomedies_box_office.csv"
            if not os.path.exists(filename):
                with open(filename, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Titre", "Entrées", "Semaines"])

            with open(filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data)
            
            # # Créez le chemin complet vers le dossier "data"
            # dossier_data = "data"
            # if not os.path.exists(dossier_data):
            #     os.mkdir(dossier_data)

            # # Concaténez le chemin du dossier "data" avec le nom du fichier CSV
            # chemin_complet = os.path.join(dossier_data, filename)

            # # Vérifiez si le fichier CSV existe déjà, et si non, créez-le avec les en-têtes de colonnes
            # if not os.path.exists(chemin_complet):
            #     with open(chemin_complet, mode='w', newline='') as file:
            #         writer = csv.writer(file)
            #         writer.writerow(["Titre", "Entrées", "Semaines"])

            # # Écrivez les données dans le fichier CSV
            # with open(chemin_complet, mode='a', newline='') as file:
            #     writer = csv.writer(file)
            #     writer.writerows(data)





    
    

