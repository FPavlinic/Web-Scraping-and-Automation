# used libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException
import time


# create class to log in to Twitter and post complaint about provided internet speed
class InternetSpeedTwitterBot:
    """Models internet speed measuring and complaint tweeting bot"""

    def __init__(self):

        # set up Selenium driven browser
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service("C:/Development/chromedriver.exe"), options=options)

        self.up = 0  # default upload
        self.down = 0  # default download

    def get_internet_speed(self):
        """Measures internet speed"""

        # go to url to measure internet speed
        self.driver.get("https://www.speedtest.net/")

        # select notification
        consent = self.driver.find_element(by=By.CSS_SELECTOR, value="#_evidon-banner-acceptbutton")
        consent.click()
        time.sleep(3)

        # select close button on notification
        dismiss = self.driver.find_element(by=By.CSS_SELECTOR, value=".close-btn")
        dismiss.click()

        # click start to start internet speed test
        start = self.driver.find_element(by=By.CSS_SELECTOR, value=".start-button a")
        start.click()

        # close notification and see results (wait if notification not present)
        while True:
            try:
                close = self.driver.find_element(by=By.XPATH, value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[8]/div/div/div[2]/a')
                close.click()
            except ElementNotInteractableException:
                time.sleep(5)
            else:
                download_result = self.driver.find_element(by=By.XPATH, value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span')
                self.down = download_result.text
                upload_results = self.driver.find_element(by=By.XPATH, value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[3]/div/div[2]/span')
                self.up = upload_results.text
                break

    def tweet_at_provider(self, my_email, my_password, measured_up, measured_down, promised_up, promised_down):
        """Tweets a complaint about low internet speed mentioning the internet provider"""

        # go to Twitter
        self.driver.get("https://twitter.com/")
        time.sleep(1)

        # close notification
        refuse_cookies = self.driver.find_element(by=By.XPATH, value='//*[@id="layers"]/div/div/div/div/div/div[2]/div[2]')
        refuse_cookies.click()

        # click sign in
        sign_in = self.driver.find_element(by=By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[5]/a')
        sign_in.click()
        time.sleep(1)

        # enter username and continue to enter password
        email = self.driver.find_element(by=By.XPATH, value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[5]/label/div/div[2]/div/input')
        email.click()
        time.sleep(1)
        email.send_keys(my_email)
        proceed = self.driver.find_element(by=By.XPATH, value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[6]')
        proceed.click()
        time.sleep(2)

        # enter password
        password = self.driver.find_element(by=By.XPATH, value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
        password.send_keys(my_password)
        password.send_keys(Keys.ENTER)
        time.sleep(2)

        # select tweet field
        tweet = self.driver.find_element(by=By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div/div/div/div')
        tweet.click()

        # create tweet and type it
        my_tweet = f"Hey A1, why is my internet speed {measured_down}down/{measured_up}up " \
                   f"when I pay for {promised_down}down/{promised_up}up?"
        time.sleep(1)
        tweet.send_keys(my_tweet)
        time.sleep(2)

        # post a tweet
        send_tweet = self.driver.find_element(by=By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]')
        send_tweet.click()
