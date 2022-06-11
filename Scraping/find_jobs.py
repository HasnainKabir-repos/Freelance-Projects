from bs4 import BeautifulSoup
import requests
import time
import os
print('Put some skill you are not familiar with')
unfamiliar_skills = input('>')
print(f'Filtering out {unfamiliar_skills}')


def find_jobs():
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text
    soup = BeautifulSoup(html_text, 'lxml')
    # Lets find the jobs posted a few days ago only
    jobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')

    for index, job in enumerate(jobs):
        published_date = job.find('span', class_='sim-posted').span.text
        if 'few' in published_date:
            company_names = job.find('h3', class_='joblist-comp-name').text.replace(" ", "")
            skill = job.find('span', class_='srp-skills').text.replace(' ', '')
            more_info = job.header.h2.a['href']
            if unfamiliar_skills not in skill:
            #print(published_date)
                if not os.path.exists('posts'):
                    os.mkdir('posts')
                with open(f'posts/{index}.txt', 'w') as f:

                    f.write(f'Company Name: {company_names.strip()}\n')
                    f.write(f'Required Skills: {skill.strip()}\n')
                    f.write(f'More Info: {more_info}\n')
                print(f'File Saved: {index}')



if __name__ == '__main__':
    while True:
        find_jobs()
        time.sleep(60)