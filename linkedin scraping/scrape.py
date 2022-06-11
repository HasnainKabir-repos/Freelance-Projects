from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests

### load selenium driver
driver = webdriver.Chrome("chromedriver.exe")
driver.get('https://linkedin.com/')
sleep(1)

### get username and password input boxes path
username = driver.find_element_by_xpath('//*[@id="session_key"]')
password = driver.find_element_by_xpath('//*[@id="session_password"]')

### input the email id and password
username.send_keys("hasnainkabir120@gmail.com")
password.send_keys("Nibirkabir991_")

### click the login button
login_btn = driver.find_element_by_xpath\
            ("//button[@class='sign-in-form__submit-button']")
sleep(1)
login_btn.click()

html_text = requests.get('https://www.linkedin.com/jobs/search/?distance=25.0&geoId=104305776&keywords=data%20analyst').text
soup = BeautifulSoup(html_text, 'lxml')
# Lets find the jobs posted a few days ago only
jobs = soup.find_all('a', class_ = 'job-card-container__link job-card-container__company-name ember-view')
print(jobs)