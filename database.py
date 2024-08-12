import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect("profiles.db")
        self.cursor = self.connection.cursor()

        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY,
                link TEXT,
                score INTEGER
            )''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS qualitymapping (
                    link TEXT PRIMARY KEY,
                    category TEXT,
                    score INTEGER
            )''')
        self.connection.commit()
    
    def setProfile(self,profileUrl,score):
        try:
            self.cursor.execute('''INSERT INTO profiles (link,score) VALUES (?,?)''',(profileUrl,int(score)))
            self.connection.commit()
            return True
        except Exception as E:
            print(E)
            return False
    def getProfile(self,profileUrl):
        try:
            data = self.cursor.execute('''SELECT * FROM profiles WHERE link = ? ''',(str(profileUrl),)).fetchall()
            if len(data) == 0:
                return (False,None)
            return (True,data[0][2])
            
        except Exception as E:
            print(E)
            return False
        
    def setQualityProfiles(self,category,profileList):
        try:
            for profile in profileList:
                (link,score) = profile
                self.cursor.execute('''INSERT OR IGNORE INTO qualitymapping (link,category,score) VALUES (?,?,?)''',(link,category,score))
                self.connection.commit()
        except Exception as E:
            print(E)
            return False
        
    def getQualityProfileByCategory(self,category):
        try:
            data = self.cursor.execute('''SELECT link,score FROM qualitymapping WHERE category=?''',(category,)).fetchall()
            return list(data)

        except Exception as E:
            print(E)
            return False
    def getE(self):
        print(self.cursor.execute("SELECT * FROM qualitymapping").fetchall())
# profiles = [("222.com",100),("oosada.com",90)]
# category = "CEO"
# # # # Example usage
db = Database()
# result = db.setProfile("http://examp1le.com/profile", 100)
# print(result)
# profile = db.getProfile("http://examp1le.com/profile")
# print(profile)
# db.setQualityProfiles(category,profiles)
# print(db.getQualityProfileByCategory(category))
db.getE()