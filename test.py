

import datetime
from datetime import timedelta



# Liste des noms des mois en français
mois_en_francais = [
    'janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout',
    'septembre', 'octobre', 'novembre', 'decembre'
]

def get_week_range(date):
    # Aller au mercredi de la semaine
    start = date - timedelta(days=date.weekday() - 2)
    # Aller au mardi de la semaine suivante
    end = start + timedelta(days=6)

    # Formater les dates
    start_str = f"{start.day}"
    end_str = f"{end.day} {mois_en_francais[end.month - 1]} {end.year}"

    # Vérifier si le début et la fin de la semaine sont dans des mois différents
    if start.month != end.month:
        start_str += f" {mois_en_francais[start.month - 1]}"

    return f"http://www.cinecomedies.com/box-office-semaine/box-office-francais-du-{start_str}-au-{end_str}/"

def remplacer_espaces_par_tirets(phrase):
    return phrase.replace(' ', '-')

def start_requests(start_date, end_date):
    list_periode = []
    current_date = start_date
    while current_date < end_date:
        # Construire l'URL pour chaque période de mercredi à mardi suivant
        url = remplacer_espaces_par_tirets(get_week_range(current_date))
        print(url)  # Juste pour afficher l'URL, vous pouvez faire autre chose avec l'URL ici
        list_periode.append(url)
        current_date += timedelta(weeks=1)


    
start_date = datetime.datetime(2014, 1, 1)  # Date de début de l'année 2020
end_date = datetime.datetime.now()  # Date actuelle 

      
start_requests(start_date, end_date)



