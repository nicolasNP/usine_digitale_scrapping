import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time
import datetime

def elapsed_time(a, b):
    elapsed = round(b - a)
    res = datetime.timedelta(seconds = elapsed)
    print(res)

start = time.time()
link_list = []
records = []
usine_url = 'https://www.usine-digitale.fr'
try: 
    for page_number in range(0, 1000, 1):
        
        if page_number != 1:
            source = 'https://www.usine-digitale.fr/annuaire-start-up/{}/'.format(page_number)
            r = requests.get(source)
            soup = BeautifulSoup(r.text, 'html.parser')
            link_total = len(soup.find_all('a', attrs = {'class': 'contenu'}))
            
            if soup.find('section', attrs = {'class':'blocType1'}) is not None:
                for number_on_the_page in range(0, link_total, 1):
                    link_end = soup.find_all('a', attrs = {'class': 'contenu'})[number_on_the_page]['href']
                    link_list.append('{}{}'.format(usine_url,link_end))
                    number_on_the_page += 1  
            else:
                break
except:
    print("An error occured at page number {} please verify".format(page_number))
    
end = time.time()
elapsed_time(start, end)

start = time.time()
i = 0
records = []

for links in link_list:
    try:
        r = requests.get(links)
        soup = BeautifulSoup(r.text, 'html.parser')
        name = soup.find('h1', attrs = {'itemprop': 'name'}).contents[0]
        products = soup.find('div', attrs = {'itemprop': 'makesOffer'}).p.contents[0].strip()
        market = soup.find_all('div', attrs = {'class': 'txtArt'})[3].p.contents[0].strip()
        founders = soup.find('div', attrs = {'itemprop': 'founders'}).p.contents
        i = 0
        if len(founders) > 1:
            founders_list = []
            for i in range(0, len(founders), 2):
                founder = soup.find('div', attrs = {'itemprop': 'founders'}).p.contents[i].strip()
                founders_list.append(founder)
        location =  soup.find('div', attrs = {'itemprop': 'address'}).p.text[3:]

        try:
            creation = soup.find('meta', itemprop='foundingDate')['content']
        except:
            creation = ""
        try:
            address = soup.find('p', attrs = {'itemprop': 'address'}).text
        except:
            address = ""
        try:
            employees = soup.find('p', attrs = {'itemprop': 'numberOfEmployees'}).text
        except:
            employees = ""
        try:
            website = soup.find('a', attrs = {'itemprop': 'url'})['href']
        except:
            website = ""
        try:
            mail = soup.find('p', attrs = {'itemprop': 'email'}).text
        except:
            mail = ""
        try:
            phone = soup.find('p', attrs = {'itemprop': 'telephone'}).text
        except:
            phone = ""
    except Exception as e:
        print('Erreur: {}, sur le lien {}'.format(str(e), _, links))
    records.append((name, products, market, founders_list, location, creation, address, employees, website, mail, phone))

end = time.time()
elapsed_time(start, end)

dataframe_usine_digitale = pd.DataFrame(records, columns=['Nom', 'Produits', 'Marché', 'Créateurs', 'Implantation', 'Date de création', 'Adresse du siège', 'Nombre d\'employés', 'Site web', 'Email', 'Téléphone'])
dataframe_usine_digitale.to_csv('TD_usine_digitale.csv', index = False, encoding = 'utf-8')
dataframe_usine_digitale

