import os
import time
import random
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.firefox.service import Service as FirefoxService
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from categories import SearchCategory
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import asyncio


def login_linkedin(driver, email, password):
    driver.get("https://www.linkedin.com/login")
    time.sleep(random.uniform(2, 4))
    
    driver.find_element(By.ID, "username").send_keys(email)
    time.sleep(random.uniform(2, 4))
    driver.find_element(By.ID, "password").send_keys(password)
    time.sleep(random.uniform(2, 4))
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    
    time.sleep(30)  # Adjust this as per the time you need to enter 2FA code

# Load cookies from a JSON file to maintain session
def load_cookies(driver, cookies_path):
    with open(cookies_path, 'r') as cookies_file:
        cookies = json.load(cookies_file)
        for cookie in cookies:
            driver.add_cookie(cookie)

# Save cookies to a JSON file to maintain session
def save_cookies(driver, cookies_path):
    cookies = driver.get_cookies()
    with open(cookies_path, 'w') as cookies_file:
        json.dump(cookies, cookies_file)

def login(driver):
    try:
        driver.get("https://www.linkedin.com/login")

        # Waits for the field to be visible for 10 seconds
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )

        email_field = driver.find_element(By.ID, "username")
        email_field.send_keys(os.getenv("EMAIL"))
        time.sleep(random.uniform(2, 4))

        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(os.getenv("PASSWORD"))
        time.sleep(random.uniform(2, 4))

        # Submit the login form
        password_field.send_keys(Keys.RETURN)
        time.sleep(random.uniform(2, 4))

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "global-nav-search"))
        ) # This indicates we are on the feeds page.

        # We now dump the cookies in the cookie.json file
        save_cookies(driver,"./cookie.json")
        return True

    except Exception as E:
        print(E)
        return False

# Initialize the Selenium driver
def init_driver():
    chrome_options = Options()
    # firefox_options.headless = True
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)
    time.sleep(random.randint(3,5))
    driver.get("https://www.linkedin.com/")
    time.sleep(random.randint(3,5))
    load_cookies(driver,"cookie.json")
    driver.refresh()
    # Here add logic to login if we do not get redirected to feed page
    if driver.current_url != "https://www.linkedin.com/feed/":
        if not login(driver):
            return False
    
    return driver

def read_json(filePath):
    with open(filePath, 'r') as file:
        data = json.load(file)
    return data
     

def run(driver):
    categories = read_json("criteria.json")

    for category in categories:
        time.sleep(random.randint(10,20))
        SearchCategory(driver,category["search"],None if "location" not in category else category["location"])

def main():
    load_dotenv()
    driver = init_driver()
    if driver:
        run(driver)
    else:
        print("SOME ERROR OCCURED!")


if __name__ == "__main__":
    main()