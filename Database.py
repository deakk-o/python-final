import sqlite3
from phobia import Phobia

class Database:
    def __init__(self, db_name="phobias.sqlite3"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):    #ბაზის შექმნა
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS phobias (
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            programme TEXT NOT NULL,
            year INTEGER NOT NULL,
            phobia TEXT NOT NULL,
            fear_level INTEGER NOT NULL)
        """)
        # self.conn.commit()

    def insert_phobia(self, fear: Phobia):      #მონაცემის დამატება ბაზაში
        self.cursor.execute("INSERT INTO phobias (name, age, programme, year, phobia, fear_level) VALUES "
                            "(?,?,?,?,?,?)",
                            fear.as_tuple())
        self.conn.commit()

    def update_phobia(self, fear: Phobia):     #მონაცემის განახლება სახელის მიხედვით
        self.cursor.execute("UPDATE phobias SET age=?, programme=?, year=?, phobia=?, fear_level=? WHERE "
                            "name=?",
                            (fear.age, fear.programme, fear.year, fear.phobia, fear.fear_level, fear.name))
        self.conn.commit()

    def delete_phobia(self, name):       #მონაცემის წაშლა
        self.cursor.execute("DELETE FROM phobias WHERE name=?", (name,))
        self.conn.commit()

    def fetch_phobia(self):     #ჩანაწერების სრულად ამოღება ბაზიდან
        self.cursor.execute("SELECT * FROM phobias")
        rows = self.cursor.fetchall()
        return [Phobia(*row) for row in rows]

    def num_people(self):      #ითვლის ადამიანთა რაოდენობას პროგრამების მიხედვით(დიაგრამისთვის)
        self.cursor.execute("SELECT programme, COUNT(*) FROM phobias GROUP BY programme")
        return self.cursor.fetchall()

    def most_common_fears(self):      #ითვლის ყველაზე გავრცელებულ ფობიებს(დიაგრამისთვის)
        self.cursor.execute("SELECT phobia, COUNT(*) FROM phobias GROUP BY phobia ORDER BY COUNT(*) DESC LIMIT 5")
        return self.cursor.fetchall()
