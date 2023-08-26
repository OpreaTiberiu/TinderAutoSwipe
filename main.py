import os
import pickle
from time import sleep
from selenium import webdriver
from dotenv import load_dotenv
from selenium.common import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.by import By

load_dotenv()


def handle_popups(driver):
    try:
        match_popup = driver.find_element(By.CSS_SELECTOR, ".itsAMatch a")
        match_popup.click()
    except NoSuchElementException as e:
        print(e)
        sleep(2)
    try:
        driver.find_element(By.XPATH, "//*[@id='u1031468980']/main/div/div[3]/button[2]").click()
    except NoSuchElementException as e:
        print(e)
        sleep(2)

    try:
        driver.find_element(by=By.XPATH, value="//*[@id='u1031468980']/main/div[1]/div[2]/button[2]").click()
    except NoSuchElementException as e:
        print(e)
        sleep(2)


def check_tinder_plus_popup(driver):
    try:
        tinder_plus_popup = driver.find_element(
            by=By.XPATH,
            value="//*[@id='u1031468980']/main/div/div[1]/div[3]/div[2]/div/div/div[1]/span"
        )
        if tinder_plus_popup and "Tinder Plus" in tinder_plus_popup.text:
            return False
    except NoSuchElementException as e:
        print(e)
        sleep(2)
    return True


def save_cookies(driver):
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))


def load_cookies(driver):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)


def facebook_login(driver):
    driver.find_element(
        by=By.CSS_SELECTOR,
        value="div div div span div button"
    ).click()
    sleep(3)
    base_window = driver.window_handles[0]
    for window in driver.window_handles:
        driver.switch_to.window(window)
        if "facebook" in driver.title.lower():
            break
    driver.find_element(
        by=By.XPATH,
        value="/html/body/div[2]/div[2]/div/div/div/div/div[4]/button[2]"
    ).click()
    sleep(3)
    driver.find_element(value="email").send_keys(os.environ["email"])
    driver.find_element(value="pass").send_keys(os.environ["pass"])
    driver.find_element(
        by=By.CSS_SELECTOR,
        value="label.uiButton.uiButtonConfirm.uiButtonLarge"
    ).click()
    driver.switch_to.window(base_window)


options = webdriver.ChromeOptions()

driver = webdriver.Chrome()

driver.get("https://tinder.com/")
load_cookies(driver)
sleep(3)

driver.find_element(
    by=By.XPATH,
    value="/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]"
).click()
sleep(3)

# Facebook login
facebook_login(driver)

sleep(10)
driver.find_element(by=By.XPATH, value="//*[@id='u1031468980']/main/div[1]/div/div/div[3]/button[1]").click()
sleep(1)
driver.find_element(by=By.XPATH, value="//*[@id='u1031468980']/main/div[1]/div/div/div[3]/button[1]").click()
sleep(10)
save_cookies(driver)

can_keep_going = True
# Like profiles
while can_keep_going:
    # Like the profile
    try:
        driver.find_elements(by=By.CSS_SELECTOR, value="div button span span svg path")[2].click()
        sleep(3)
    except ElementClickInterceptedException as e:
        print("Could not like")
        print(e)
        handle_popups(driver)
    can_keep_going = check_tinder_plus_popup(driver)


print("Reached the profile limit for the day!")