#!/usr/bin/env python
# coding: utf-8

# In[68]:


import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time
import datetime


# In[69]:


def elapsed_time(a, b):
    elapsed = round(b - a)
    res = datetime.timedelta(seconds = elapsed)
    print(res)


# In[70]:


start = time.time()
link_list = []
records = []
usine_url = 'https://www.usine-digitale.fr/annuaire-start-up/'
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
except Exception as e:
    print("An error occured at page number {} please verify. {}".format(page_number,print(e)))
    
end = time.time()
elapsed_time(start, end)


# In[66]:


# r = requests.get("https://www.usine-digitale.fr/annuaire-start-up/tapvalue,252906")
# soup = BeautifulSoup(r.text, 'html.parser')
# name = soup.find('h1', attrs = {'itemprop': 'name'}).contents[0]
# products = soup.find('div', attrs = {'itemprop': 'makesOffer'}).p.contents[0].strip()
# market = soup.find(text = re.compile('Marché')).next.next.contents[0].text[3:]
# founders = soup.find('div', attrs = {'itemprop': 'founders'}).p.contents[0][5:]
# founders


# In[72]:


start = time.time()
i = 0
records = []

for links in link_list:
    try:
        r = requests.get(links)
        soup = BeautifulSoup(r.text, 'html.parser')
        name = soup.find('h1', attrs = {'itemprop': 'name'}).contents[0]
        products = soup.find('div', attrs = {'itemprop': 'makesOffer'}).p.contents[0].strip()
        market = soup.find(text = re.compile('Marché')).next.next.contents
        if len(market) > 1:
            market_list = []
            for i in range(0, len(market), 2):
                market = soup.find(text = re.compile('Marché')).next.next.contents[i].text[3:]
                market_list.append(market)
            market = market_list
        else:
            market = soup.find(text = re.compile('Marché')).next.next.contents[0].text[3:]
            
        founders = soup.find('div', attrs = {'itemprop': 'founders'}).p.contents
        i = 0
        if len(founders) > 1:
            founders_list = []
            for i in range(0, len(founders), 2):
                founder = soup.find('div', attrs = {'itemprop': 'founders'}).p.contents[i].strip()
                founders_list.append(founder)
            founders = founders_list
        else:
            founders = soup.find('div', attrs = {'itemprop': 'founders'}).p.contents[0][5:]
        try:        
            location =  soup.find('div', attrs = {'itemprop': 'address'}).p.text[3:]
        except:
            location = ""
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
        print('Erreur: {}, sur le lien {}'.format(str(e), links))
    
    records.append((name, products, market, founders, location, creation, address, employees, website, mail, phone))

end = time.time()
elapsed_time(start, end)


# In[73]:


dataframe_usine_digitale = pd.DataFrame(records, columns=['Nom', 'Produits', 'Marché', 'Créateurs', 'Implantation', 'Date de création', 'Adresse du siège', 'Nombre d\'employés', 'Site web', 'Email', 'Téléphone'])
dataframe_usine_digitale.to_csv('TD_usine_digitale.csv', index = False, encoding = 'utf-8')
dataframe_usine_digitale


# In[ ]:




