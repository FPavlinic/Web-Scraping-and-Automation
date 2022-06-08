# used libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

URL = "http://orteil.dashnet.org/experiments/cookie/"  # url to an online game

# open the game url in browser controlled by Selenium
driver = webdriver.Chrome(service=Service("C:/Development/chromedriver.exe"))
driver.get(URL)

# specify important time intervals
time_to_buy = time.time() + 5  # buy an item every 5 seconds
stop_time = time.time() + 5 * 60  # stop playing after 5 minutes

while True:
    cookie = driver.find_element(by=By.ID, value="cookie")  # find cookie to click on, on the web page
    cookie.click()  # click on the cookie to earn more cookies

    if time.time() >= time_to_buy:  # when 5 seconds passed go to store
        store_items = driver.find_elements(by=By.CSS_SELECTOR, value="#store b")  # find all store items
        not_available = driver.find_elements(by=By.CSS_SELECTOR, value=".grayed b")  # find unavailable store items
        available = [item for item in store_items if item not in not_available]  # create list of available store items

        for item in available[::-1]:  # select the most expensive store item --> produces more cookies
            item.click()  # click on it --> make purchase
            break  # leave for loop

        time_to_buy = time.time() + 5  # add 5 seconds before next purchase is made

    if time.time() >= stop_time:  # check if 5 minutes have passed
        cps = driver.find_element(by=By.ID, value="cps").text  # get amount of cookies after 5 minutes
        print(cps)  # print amount of cookies after 5 minutes
        break  # leave while loop and stop playing the game
