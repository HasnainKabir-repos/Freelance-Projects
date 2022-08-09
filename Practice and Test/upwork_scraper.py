from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


driver = webdriver.Chrome(Service(ChromeDriverManager(version='103.0.5060.134').install()))
driver.get('https://www.upwork.com/ab/account-security/login')

sleep(3)

def login():
    username = driver.find_element(By.XPATH, value= '//input[@id="login_username"]')
    username.send_keys('hasnainkabir120@gmail.com')
    sleep(1)

    continue_btn = driver.find_element(By.XPATH,value= '//button[@id="login_password_continue"]')
    continue_btn.click()
    sleep(3)

    password = driver.find_element(By.XPATH, value = '//input[@id="login_password"]')
    password.send_keys('Nibirkabir991_')

    sleep(1)
    login_btn = driver.find_element(By.XPATH, value='//input[@id="login_control_continue"]')
    login_btn.click()

login()