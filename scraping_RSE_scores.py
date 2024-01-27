from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import pandas as pd 

# Doit imprimer le titre de la page Google
table_data = []

urls=['https://www.lepoint.fr/palmares-entreprises-responsables/assurances.php','https://www.lepoint.fr/palmares-entreprises-responsables/automobile.php','https://www.lepoint.fr/palmares-entreprises-responsables/btp-et-construction.php','https://www.lepoint.fr/palmares-entreprises-responsables/btp-et-construction.php','https://www.lepoint.fr/palmares-entreprises-responsables/banques-et-services-financiers.php','https://www.lepoint.fr/palmares-entreprises-responsables/commerce-distribution.php','https://www.lepoint.fr/palmares-entreprises-responsables/construction-aeronautique-ferroviaire-navale-et-autres-vehicules.php','https://www.lepoint.fr/palmares-entreprises-responsables/habillement-et-accessoires.php','https://www.lepoint.fr/palmares-entreprises-responsables/hotellerie-restauration-loisirs.php','https://www.lepoint.fr/palmares-entreprises-responsables/it-informatique-et-telecommunications.php','https://www.lepoint.fr/palmares-entreprises-responsables/immobilier.php','https://www.lepoint.fr/palmares-entreprises-responsables/industrie-chimique.php']

for url in urls :
    firefox_binary_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'  # Mettez à jour avec votre chemin

    service = Service(executable_path=r'C:\Users\lisac\Downloads\geckodriver-v0.34.0-win32\geckodriver.exe')
    firefox_options = Options()
    # firefox_options.add_argument("--headless")  # Enlevez le commentaire si vous voulez exécuter en mode sans tête
    firefox_options.binary_location = firefox_binary_path

    # Créez une instance du navigateur Firefox
    driver = webdriver.Firefox(service=service, options=firefox_options)

    # Naviguez vers Google comme test
    driver.get("https://www.google.com")
    print(driver.title)  
    # Ouvrir la page web
    driver.get(url)

    # Attendre que la page soit complètement chargée
    wait = WebDriverWait(driver, 10)

    # Attendre que la page soit complètement chargée
    wait = WebDriverWait(driver, 10)

    # Localiser le tableau
    table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".result_desktop.secteur")))

    # Récupérer toutes les lignes du tableau
    rows = table.find_elements(By.TAG_NAME, "tr")

    segments = url.split('/')

    # Récupérer le dernier segment (automobile.php) et enlever l'extension .php
    last_segment = segments[-1].replace('.php', '')

    # Créer une liste pour stocker les données

    all_data = []

    # Parcourir chaque ligne pour extraire les données
    for row in rows[1:]:  # Ignorer l'en-tête du tableau
        cells = row.find_elements(By.TAG_NAME, "td")
        if cells:  # Assurer que la ligne contient des cellules
            data = {
                "Secteur": last_segment,
                "Rang Secteur": cells[0].text,
                "Nom de l'Entreprise": cells[1].text,
                "Score Final": cells[2].text,
                "Rang Total": cells[3].text,
                "Score Environnement": cells[4].text,
                "Score Social": cells[5].text,
                "Score Gouvernance": cells[6].text
            }
            table_data.append(data)
    
    all_data.extend(table_data)
    # N'oubliez pas de fermer le navigateur une fois le scraping terminé
    driver.quit()

    # Afficher les données extraites
    for entry in table_data:
        print(entry)

# Créer un DataFrame à partir de toutes les données recueillies
df = pd.DataFrame(all_data)

# Exporter le DataFrame dans un fichier CSV
df.to_csv("donnees_RSE_entreprises.csv", index=False)








