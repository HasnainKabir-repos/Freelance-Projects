from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text
#print(html_text)
soup = BeautifulSoup(html_text, 'lxml')
job = soup.find('li', class_ = 'clearfix job-bx wht-shd-bx')
# We can see that names of companies are h3 tagged inside jobs
company_name = job.find('h3', class_ = 'joblist-comp-name').text.replace(" ", "")
#replace white spaces with nothing

skills = job.find('span', class_ = 'srp-skills').text.replace(' ', '')
#print(f'''
#Company Name = {company_name}
#Required Skills = {skills}
#''')

print('Put some skill you are not familiar with')
unfamiliar_skills = input('>')
print(f'Filtering out{unfamiliar_skills}')

# Lets find the jobs posted a few days ago only
jobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')

for job in jobs:
    published_date = job.find('span', class_='sim-posted').span.text
    if 'few' in published_date:
        company_names = job.find('h3', class_='joblist-comp-name').text.replace(" ", "")
        skill = job.find('span', class_='srp-skills').text.replace(' ', '')
        more_info = job.header.h2.a['href']
        if unfamiliar_skills not in skill:
        #print(published_date)
            print(f'Company Name: {company_names.strip()}')
            print(f'Required Skills: {skill.strip()}')
            print(f'More Info: {more_info}')