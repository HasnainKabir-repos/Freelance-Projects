from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class CourseFeedbackSubmitter:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome("C:\Program Files\Google\Chrome\Application\chromedriver.exe")
        self.wait = WebDriverWait(self.driver, 5)

    def login(self):
        self.driver.get('https://sis.iutoic-dhaka.edu/')
        sleep(1)

        username_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='User ID']")))
        password_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Password']")))

        username_input.send_keys(self.username)
        password_input.send_keys(self.password)

        login_btn = self.driver.find_element("xpath", "//button[@id='m_login_signin_submit']")
        login_btn.click()

    def navigate_to_course_feedback(self):
        toggler = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='kt_aside_mobile_toggler']")))
        toggler.click()

        button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Course Feedback']")))
        button.click()

    def submit_feedback(self):
        evaluate_links = self.wait.until(EC.presence_of_all_elements_located((By.LINK_TEXT, 'Evaluate')))
        evaluate_links[0].click()

        radio_buttons = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@value='5']")))
        for radio_button in radio_buttons:
            radio_button.click()

        text_areas = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//textarea[@class='form-control']")))
        for text_area in text_areas:
            text_area.send_keys("Overall satisfactory")

        submit_btn = self.driver.find_element("xpath", "//button[text()='Submit']")
        submit_btn.click()

    def submit_course_feedback(self):
        self.login()
        self.navigate_to_course_feedback()
        self.submit_feedback()


# Example usage:
username = ""
password = ""
feedback_submitter = CourseFeedbackSubmitter(username, password)
feedback_submitter.submit_course_feedback()
