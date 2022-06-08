# used libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# set up Selenium driven browser
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service("C:/Development/chromedriver.exe"), options=options)


class FormFiller:
    """Models form filling bot"""

    def __init__(self, form_link, links, prices, addresses):
        driver.get(form_link)  # open the rentals url in browser controlled by Selenium

        # go through all data on rentals in created lists
        for n in range(len(addresses)):
            time.sleep(2)
            address = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            price = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            link = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            submit_button = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')

            # fill form with the data
            address.send_keys(addresses[n])
            price.send_keys(f"${prices[n]}")
            link.send_keys(links[n])
            submit_button.click()
            time.sleep(1)

            # jump to next form
            next_answer = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
            next_answer.click()
            time.sleep(1)

        driver.quit()  # close browser
