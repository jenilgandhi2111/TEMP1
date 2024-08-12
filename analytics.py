from database import Database
import csv
class Analytics:
    def __init__(self):
        self.db = Database()

    def getQualityProfiles(self,category):
        data = self.db.getQualityProfileByCategory(category)
        if data:
            data = [("Profile Link","score")] + data
            with open(f'{category}.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                
                # Write each sub-list to a new row
                writer.writerows(data)
        else:
            print("No data found for this category")

analytics = Analytics()
analytics.getQualityProfiles("")