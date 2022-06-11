from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import numpy as np

def find_jobs():
    cols = ['Category', 'Company Name', 'Website', 'Phone Number', 'Street Address', 'City', 'State', 'Zip Code']
    df = pd.DataFrame(columns=cols)
    for page in range(1,8):
        url = "https://www.yellowpages.com/search?search_terms=accountants&geo_location_terms=Dallas%2C%20TX&page="+str(page)
        print(url)
        html_text = requests.get(url)
        soup = BeautifulSoup(html_text.text, 'lxml')
        jobs = soup.find_all('div', class_='result')
        for job in jobs:
            categories = job.find('div', class_ = 'categories')
            if "Accounting" or "Accountant" in categories.find_all('a').text:
                links = []
                try:
                    company_name = job.find('a', class_ = 'business-name').span.text
                except AttributeError as a:
                    continue
                soup2 = soup.find_all('a', class_ = 'track-visit-website')
                for link in soup2:
                    links.append(link.get('href'))

                website = links[0]

                try:
                    phone = job.find('div', class_='phones phone primary').text
                    street = job.find('div', class_ = 'street-address').text
                    locality = job.find('div', class_ = 'locality').text
                    city = locality.split()[0].replace(',', '')
                    state = locality.split()[1]
                    zip = locality.split()[2]
                except Exception as a:
                    regex = re.compile(r'(<p class="adr">)|(</p>)')
                    street1 = job.find('p', class_ = 'adr')
                    street = regex.sub('', str(street1))
                    locality = street
                    city = locality
                    state = locality
                    zip = locality
                    phone = np.nan
                category = 'Accounting'

                data = [[category, company_name, website,phone, street, city, state, zip]]
                df = df.append(pd.DataFrame(data, columns=cols),ignore_index=True)
                df.to_csv('accounting_draft.csv')
                with open('Accountants.txt', 'a') as f:
                    f.write(f'Company Name: {company_name}\nWebsite: {website}\nPhone Number: {phone}\nStreet: {street}\nCity {city}\nstate: {state}\nZip: {zip}\n\n')




find_jobs()
