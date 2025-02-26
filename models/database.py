import sqlite3
import os

class Database:
    def __init__(self, db_name='hangman_2025.db'):
        """
        Loob ühenduse andmebaasiga.
        Kui andmebaasi ei ole, siis loob selle ja lisab vajalikud tabelid.
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect_to_db()

    def connect_to_db(self):
        """ Ühendub andmebaasiga ja loob tabeli, kui seda pole. """
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self.create_table()
            print(f"Ühendatud andmebaasiga: {self.db_name}")
        except sqlite3.Error as e:
            print(f"Andmebaasi viga: {e}")

    def create_table(self):
        """ Loob sõnade tabeli, kui see ei eksisteeri. """
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS words (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    word TEXT NOT NULL,
                                    category TEXT NOT NULL)''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Tabeli loomise viga: {e}")

    def add_word(self, word, category):
        """ Lisab andmebaasi uue sõna ja kategooria. """
        try:
            self.cursor.execute("INSERT INTO words (word, category) VALUES (?, ?)", (word, category))
            self.conn.commit()
            print(f" Lisatud andmebaasi: {word} - {category}")  # TEST
        except sqlite3.Error as e:
            print(f"Andmebaasi lisamise viga: {e}")

    def update_word(self, word_id, new_word, new_category):
        """ Uuendab olemasolevat sõna ja selle kategooriat. """
        try:
            self.cursor.execute("UPDATE words SET word = ?, category = ? WHERE id = ?",
                                (new_word, new_category, word_id))
            self.conn.commit()
            print(f" Andmebaasis uuendatud: ID={word_id}, Sõna={new_word}, Kategooria={new_category}")  # TEST
        except sqlite3.Error as e:
            print(f" Andmete uuendamise viga: {e}")

    def delete_word(self, word_id):
        """ Kustutab sõna andmebaasist. """
        try:
            self.cursor.execute("DELETE FROM words WHERE id = ?", (word_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Andmete kustutamise viga: {e}")

    def fetch_words(self):
        """ Tagastab kõik sõnad ja kategooriad andmebaasist. """
        try:
            self.cursor.execute("SELECT * FROM words")
            words = self.cursor.fetchall()
            print("Andmebaasist loetud sõnad:", words)  # ← Test
            return words
        except sqlite3.Error as e:
            print(f"Andmete lugemise viga: {e}")
            return []

    def fetch_categories(self):
        """ Tagastab kõik unikaalsed kategooriad andmebaasist """
        try:
            self.cursor.execute("SELECT DISTINCT category FROM words")  # võtab unikaalsed kategooriad
            categories = [row[0] for row in self.cursor.fetchall()]
            #print(f" Andmebaasist loetud kategooriad: {categories}")  # TEST
            return categories
        except sqlite3.Error as e:
            #print(f" Kategooriate lugemise viga: {e}")
            return []

    def open_database(self, new_db_name):
        """ Avab kasutaja poolt valitud andmebaasi ja kontrollib selle terviklikkust. """
        if not os.path.exists(new_db_name):
            print(f"️ Andmebaasi '{new_db_name}' ei leitud! Loome uue. ")
            self.db_name = new_db_name
            self.connect_to_db()
            return
        try:
            self.conn.close()
            self.db_name = new_db_name
            self.connect_to_db()
        except sqlite3.Error as e:
            print(f"Viga andmebaasi avamisel: {e}")

    def fetch_words(self):
        """ Tagastab kõik sõnad ja kategooriad andmebaasist. """
        try:
            self.cursor.execute("SELECT * FROM words")
            words = self.cursor.fetchall()
            #print(f" Andmebaasist loetud sõnad: {words}")  # TEST
            return words
        except sqlite3.Error as e:
            print(f"Andmebaasi viga: {e}")
            return []

    def close_connection(self):
        """ Sulgeb andmebaasi ühenduse. """
        try:
            if self.conn:
                self.conn.close()
                print("Andmebaasi ühendus suletud.")
        except sqlite3.Error as e:
            print(f"Andmebaasi sulgemise viga: {e}")

