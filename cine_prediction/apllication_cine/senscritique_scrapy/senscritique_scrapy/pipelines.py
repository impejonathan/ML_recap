# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter


# class SenscritiqueScrapyPipeline:
#     def process_item(self, item, spider):
#         return item


from itemadapter import ItemAdapter
import pyodbc
from dotenv import load_dotenv
import os


# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

class SQLPipeline:
    def open_spider(self, spider):
        """
        Méthode appelée lorsque la toile (spider) est ouverte.

        Cette méthode initialise la connexion à la base de données SQL Server
        en utilisant les informations de connexion stockées dans les variables d'environnement.

        Args:
            spider (scrapy.Spider): L'instance du spider en cours d'exécution.
        """
        server = 'cinemanager.database.windows.net'
        database = 'cinemanager_bdd'
        username = os.environ.get('DB_USERNAME')
        password = os.environ.get('DB_PASSWORD')
        driver = '{ODBC Driver 18 for SQL Server}'

        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

        self.conn = pyodbc.connect(conn_str)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        """
        Méthode appelée lorsque la toile (spider) est fermée.

        Cette méthode ferme la connexion à la base de données SQL Server.

        Args:
            spider (scrapy.Spider): L'instance du spider en cours d'exécution.
        """
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        """
        Méthode appelée pour traiter chaque élément (item) extrait.

        Cette méthode insère les données extraites dans la table "films_prediction" de la base de données.

        Args:
            item (dict): Dictionnaire contenant les données extraites de la page Web.
            spider (scrapy.Spider): L'instance du spider en cours d'exécution.

        Returns:
            dict: L'objet item d'origine qui sera transmis aux autres pipelines (s'il en existe).
        """
        self.cursor.execute(
        'INSERT INTO [dbo].[films_prediction] (titre, acteur_1, acteur_2, acteur_3, realisateur, distributeur, duree, genre, pays, nominations, prix, date, annee_production,vacances,saison,reputation_distributeur,nombre_films_distributeur,actor_1_popularity,actor_2_popularity,actor_3_popularity,director_popularity,type,budget,langue,genre1) '
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (item["titre"], item["acteur_1"], item["acteur_2"], item["acteur_3"], item["realisateur"], item["distributeur"], item["duree"], item["genre"], item["pays"], item["nominations"], item["prix"], item["date"], item["annee_production"],item['vacances'] , item['saison'] ,item['reputation_distributeur'],item['nombre_films_distributeur'], item['actor_1_popularity'],item['actor_2_popularity'], item['actor_3_popularity'], item['director_popularity'],item['type'],item['budget'],item['langue'],item['genre1']))
        self.conn.commit()

        return item