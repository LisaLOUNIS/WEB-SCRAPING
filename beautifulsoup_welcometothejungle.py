import requests
from bs4 import BeautifulSoup

# scraping title and demanded skills from a generic page

url = 'https://www.welcometothejungle.com/fr/companies/datascientest/jobs/data-engineer-h-f-cdi_puteaux_DATAS_ZMLPerq'

response = requests.get(url)
data = response.text

soup = BeautifulSoup(data, 'html.parser')


job_title = soup.find('h1').get_text()
print(job_title)

profil_recherche_section = soup.find_all('section')[3] 

lists = profil_recherche_section.find_all('ul')

competences = []
for ul in lists:
    items = ul.find_all('li')
    for item in items:
        competences.append(item.get_text(strip=True))

for c in competences:
    print(c)