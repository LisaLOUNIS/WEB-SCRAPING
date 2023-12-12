import requests
from bs4 import BeautifulSoup

urls = [
    "https://www.welcometothejungle.com/fr/companies/quantcube-technology/jobs/stagiaire-intern-advanced-macro-data-scientist_paris?q=f3cdd48ce0a998f317ecc1d16b8088d1&o=2266581", 
    "https://www.welcometothejungle.com/fr/companies/wivoo/jobs/consultant-senior-data-analyst_paris?q=f3cdd48ce0a998f317ecc1d16b8088d1&o=2069426",
    "https://www.welcometothejungle.com/fr/companies/groupe-micropole/jobs/stage-consultant-customer-data-management-f-h_levallois-perret_MICRO_RAz4krm?q=f3cdd48ce0a998f317ecc1d16b8088d1&o=1405897",
    "https://www.welcometothejungle.com/fr/companies/meilleurtaux-com/jobs/data-engineer-senior-h-f_paris?q=f3cdd48ce0a998f317ecc1d16b8088d1&o=2291701",
    "https://www.welcometothejungle.com/fr/companies/meilleurtaux-com/jobs/head-of-data-engineering-h-f_paris?q=f3cdd48ce0a998f317ecc1d16b8088d1&o=2291695",
    "https://www.welcometothejungle.com/fr/companies/meilleurtaux-com/jobs/product-manager-plateforme-data-h-f_paris_MEILL_DZqxyql?q=0852cdbe92c9248226e4a3fa7c95bc85&o=2289438",
    "https://www.welcometothejungle.com/fr/companies/quantcube-technology/jobs/intern-data-scientist-nlp_paris?q=0852cdbe92c9248226e4a3fa7c95bc85&o=1565637",
    "https://www.welcometothejungle.com/fr/companies/skiils/jobs/data-scientist-pricing-senior-h-f?q=bf40d746ee3afd6b88506af9e2585a6c&o=2283993",
    "https://www.welcometothejungle.com/fr/companies/carbo/jobs/carbon-data-scientist-stage_paris?q=bf40d746ee3afd6b88506af9e2585a6c&o=1936014",
    "https://www.welcometothejungle.com/fr/companies/datascientest/jobs/data-scientist_levallois-perret?q=bf40d746ee3afd6b88506af9e2585a6c&o=367193"
]

for url in urls:
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    title = soup.find('h1').get_text()
    company = soup.find('span', color="white").get_text()
    address = soup.findAll('span', class_='wui-text')[1].get_text()
    profil_recherche_section = soup.findAll('div', class_='sc-18ygef-1 ezamTS')[4] 
    lists = profil_recherche_section.find_all('ul')
    competences = []
    for ul in lists:
        items = ul.find_all('li')
        for item in items:
            competences.append(item.get_text(strip=True))
    print(f"Job offer: {title}")
    print(f"Company: {company}")
    print(f"Location: {address}")
    print(f"Demanded skills:")
    for c in competences:
        print(f" - {c}")
    print("----------------------------------------------------------")