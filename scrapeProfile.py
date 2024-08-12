import os
import time
import random
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from database import Database
class ScrapeProfile:

    def __init__(self,driver,profileLink):
        # This should open the profile on the browser and run the scrape method
        self.driver = driver
        self.profileUri = profileLink
        self.driver.get(profileLink)
        self.db = Database()
        self.scrape()
        
    def checkAbout(self):
        try:
            self.driver.find_element(By.XPATH, "//div[@id='about']")
            return 10
        except Exception as E:
            return 0
    
    def checkProfileImage(self):
        try:
            if self.driver.find_element(By.XPATH,"//img[contains(@class, 'pv-top-card-profile-picture__image--show')]").get_attribute('src')!="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7":
                return 10
            return 0
        except Exception as E:
            print(E)
            return 0
        
    
    def checkBackgroundImage(self):
        return 2
    
    def checkExp(self):
        try:
            experience_section = self.driver.find_element(By.XPATH, "//div[@id='experience']")
            if experience_section:
                return 6
            else:
                return 0
        except Exception as E:
            print(E)
            return 0
        
    def checkActivity(self):
        try:
            if self.driver.find_element(By.XPATH, "//div[@id='content_collections']"):
                return 5
            else:
                return 0
        except Exception as E:
            print(E)
            return 0
    def checkEducation(self):
        try:
            if self.driver.find_element(By.XPATH, "//div[@id='education']"):
                return 8
            return 0
        except Exception as E:
            print(E)
            return 0
        
    def checkSkills(self):
        try:
            if self.driver.find_element(By.XPATH, "//div[@id='skills']"):
                return 5
            return 0
        except Exception as E:
            print(E)
            return 0
    
    def scrape(self):
        status = self.db.getProfile(self.profileUri)[1]
        if status != None:
            return int(status)

        time.sleep(random.randint(3,6))
        score = 0 # Each method it would call would have a score parameter based on its importance

        # Check profile photo
        score += self.checkProfileImage() # 10 or 0

        # Check background image
        score += self.checkBackgroundImage() # 2
        
        # Check About more recently updated the better
        score += self.checkAbout() # 10 points
        
        # Check Experience
        score += self.checkExp() # No of entries * 3 or 3 per exp
        
        # Check Activity
        score += self.checkActivity() # 5 for activity
        
        # Check Education
        score += self.checkEducation() # 8 for education
        
        # Check skills
        score += self.checkSkills() # 5 for skills


        # Store it to db so that if it pops up again we can simply return the score
        self.db.setProfile(self.profileUri,score)

        time.sleep(random.randint(3,6))
        
        return score
        
        # Check Languages
        # score += self.checkLanguages()
        
        # # Check email 
        # score += self.checkEmail()
        
        # # Check honors, certificate, licenses
        # score += self.checkHonors()
        
        # # Check Volunteering
        # score += self.checkVolunteering()
        
        # # Check recomendation 
        # score += self.checkRecomendation()
        
        # # Check mutuals
        # score += self.checkMutuals()

