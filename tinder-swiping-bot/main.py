# used libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time

# url to Tinder
URL = "https://tinder.com/"

# set up Selenium driven browser
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service("C:/Development/chromedriver.exe"), options=options)

# go to Tinder url
driver.get(URL)
time.sleep(1)

# find log in button and click it
log_in = driver.find_element(by=By.CSS_SELECTOR, value=".button")
log_in.click()
time.sleep(1)

# find log in with Facebook button and click it
login_with_fb = driver.find_element(by=By.XPATH, value='//*[@id="c-879141390"]/div/div/div[1]/div/div/div[3]/span/div[2]/button')
login_with_fb.click()
time.sleep(1)

# switch from the main to the log in window
main_window = driver.window_handles[0]
login_window = driver.window_handles[1]
driver.switch_to.window(login_window)
driver.maximize_window()
time.sleep(2)

# close accept cookies notification
accept_cookies = driver.find_element(by=By.CSS_SELECTOR, value="._9xo5 button")
accept_cookies.click()

# enter log in data and press enter to log in
email = driver.find_element(by=By.CSS_SELECTOR, value="#email")
email.send_keys("knows.nobody.2022@gmail.com")
password = driver.find_element(by=By.CSS_SELECTOR, value="#pass")
password.send_keys("#NobodyKnows22")
password.send_keys(Keys.ENTER)
time.sleep(2)

# switch back to the main window
driver.switch_to.window(main_window)
time.sleep(5)

# close privacy preferences notification
privacy_preferences = driver.find_element(by=By.XPATH, value='//*[@id="c849239686"]/div/div[2]/div/div/div[1]/div[1]/button')
privacy_preferences.click()

# close allow location notification
allow_location = driver.find_element(by=By.XPATH, value='//*[@id="c-879141390"]/div/div/div/div/div[3]/button[1]')
allow_location.click()
time.sleep(1)

# close accept notifications notification
reject_notifications = driver.find_element(by=By.XPATH, value='//*[@id="c-879141390"]/div/div/div/div/div[3]/button[2]')
reject_notifications.click()
time.sleep(2)

# swipe through 100 profiles
for _ in range(100):
    time.sleep(2)

    try:
        # swipe right
        swipe = driver.find_element(by=By.CSS_SELECTOR, value="body")
        swipe.send_keys(Keys.ARROW_RIGHT)

    except ElementClickInterceptedException:
        # if swapping is intercepted by pop-up
        try:
            # close you found a match pop-up
            match_popup = driver.find_element(by=By.CSS_SELECTOR, value=".itsAMatch a")
            match_popup.click()

        except NoSuchElementException:
            # wait if swapping intercepted but can't find close button
            time.sleep(2)

# close Selenium driven browser when task is complete
driver.quit()
