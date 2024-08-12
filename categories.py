import os
import time
import random
import json
import pandas as pd
from scrapeProfile import ScrapeProfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database import Database

class SearchCategory:
    def __init__(self,driver:webdriver,searchPosition,location=None): # More params could be added
        self.category = searchPosition
        self.searchStr = searchPosition+"+"+location if location != None else ""
        self.driver = driver
        self.N = 2
        self.database = Database()
        print(self.run())

    def loadUp(self): # This loads up the people page and enters the search criteria
        search_box = self.driver.find_element(By.XPATH, "//input[@placeholder='Search']")
        search_box.clear()
        search_box.send_keys(self.searchStr)
        search_box.send_keys(Keys.RETURN)
        time.sleep(random.uniform(2, 4))

        people_filter = self.driver.find_element(By.XPATH, "//button[text()='People']")
        people_filter.click()
        time.sleep(random.uniform(2, 4))

    def scrape(self):
        profileUrls = []
        for page in range(1, self.N + 1):
            # Wait for the profiles to load (optional, depending on your setup)
            time.sleep(random.randint(3,7))
            
            # Find profiles on the current page
            WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='reusable-search__entity-result-list list-style-none']/li//a"))
            )
            profiles = self.driver.find_elements(By.XPATH, "//ul[@class='reusable-search__entity-result-list list-style-none']//a[contains(@href, '/in/')]")

            pc = 0
            for profile in profiles:
                link = profile.get_attribute('href')
                if link and "Profile" in link:  # Check if the link is not None
                    profileUrls.append(link)
                    
            try:
                currentUrl = str(self.driver.current_url)

                if "page" not in currentUrl:
                    newUri = currentUrl+"&page="+str(page+1)
                else:
                    newUri = currentUrl.split("&page=")[0] + "&page=" + str(page + 1)
                self.driver.implicitly_wait(random.randint(2,4))
                self.driver.get(newUri)
                self.driver.implicitly_wait(random.randint(2,5))
                pc+=1
                if pc%200 == 0:
                    self.driver.implicitly_wait(300)
            except Exception as e:
                print("No more pages or error:", e)
                break 
            
        return profileUrls[0::2]

    def scrapeProfile(self,uri):
        # This would call scrapeprofile class
        time.sleep(random.randint(2,5))
        return ScrapeProfile(self.driver,uri).scrape()


    def scrapeProfiles(self,profileUris): # Total could be 49 points but criteria could be 40 atleast
        selectedProfiles = []
        for uri in profileUris:
            # We can store this in db and check if it exists we might skip it
            score = self.scrapeProfile(uri)
            if score > 40:
                selectedProfiles.append([uri,score])
        return selectedProfiles


    def run(self):

        # We navigate to search bar and type the search str
        self.loadUp()
        
        # Will store all the profile urls
        profileUrls = self.scrape()

        # We call the scrape profile method to scrape the data from all the profiles
        selectedProfiles =  self.scrapeProfiles(profileUrls)

        self.database.setQualityProfiles(self.category,selectedProfiles)

        return selectedProfiles
        
        

