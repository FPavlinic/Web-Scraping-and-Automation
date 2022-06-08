# used libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from time import sleep


class InstaFollower:
    """Models bot for following Instagram profiles"""

    def __init__(self):
        # set options to open Selenium driven browser in maximized window
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")

        # create driver for browser to be controlled
        self.driver = webdriver.Chrome(service=Service("C:/Development/chromedriver.exe"), options=options)

    def login(self, insta_username, insta_password):
        """Logins to Instagram"""

        self.driver.get("https://www.instagram.com/")  # go to Instagram home page
        sleep(1)

        # close first notification
        cookies = self.driver.find_element(by=By.XPATH, value='/html/body/div[4]/div/div/button[1]')
        cookies.click()
        sleep(1)

        # select username field and type username
        username = self.driver.find_element(by=By.XPATH, value='//*[@id="loginForm"]/div/div[1]/div/label/input')
        username.click()
        sleep(1)
        username.send_keys(insta_username)

        # select password field and type password
        password = self.driver.find_element(by=By.XPATH, value='//*[@id="loginForm"]/div/div[2]/div/label/input')
        password.click()
        sleep(1)
        password.send_keys(insta_password)
        sleep(2)

        # press enter to proceed with login
        password.send_keys(Keys.ENTER)
        sleep(3)

        # save info for future logins
        save_info = self.driver.find_element(by=By.XPATH, value='//*[@id="react-root"]/section/main/div/div/div/div/button')
        save_info.click()
        sleep(4)

        # close another notification (wait if not popping up)
        try:
            notifications = self.driver.find_element(by=By.XPATH, value='/html/body/div[5]/div/div/div/div[3]/button[2]')
            notifications.click()
        except NoSuchElementException:
            sleep(2)
            notifications = self.driver.find_element(by=By.XPATH, value='/html/body/div[5]/div/div/div/div[3]/button[2]')
            notifications.click()
        finally:
            sleep(3)

    def find_followers(self, insta_profile):
        """Opens predefined profile and a list of its followers"""

        # select for search field
        select_search = self.driver.find_element(by=By.XPATH, value='//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[1]')
        select_search.click()
        sleep(1)

        # type profile name
        search = self.driver.find_element(by=By.XPATH, value='//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
        search.send_keys(insta_profile)
        sleep(2)

        # select the profile
        select_profile = self.driver.find_element(by=By.XPATH, value='//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a')
        select_profile.click()
        sleep(3)

        # click on followers to open followers list
        followers = self.driver.find_element(by=By.XPATH, value='//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
        followers.click()
        sleep(2)

        # follow visible profiles and then pull down sidebar to see another 10 profiles
        sidebar = self.driver.find_element(by=By.XPATH, value='/html/body/div[6]/div/div/div/div[2]')
        for n in range(10):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", sidebar)
            sleep(2)
            self.follow()
            sleep(2)

    def follow(self):
        """Follows Instagram profiles"""

        # find follow button
        follow_buttons = self.driver.find_elements(by=By.CSS_SELECTOR, value="ul div li button")
        for follow_button in follow_buttons:
            sleep(2)

            # click on the follow button
            try:
                follow_button.click()
                sleep(1)

            # if window pops up close it
            except ElementClickInterceptedException:
                cancel = self.driver.find_element(by=By.XPATH, value='/html/body/div[7]/div/div/div/div[3]/button[2]')
                cancel.click()
