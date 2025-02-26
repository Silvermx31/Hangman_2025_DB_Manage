from models.database import Database

class Model:
    def __init__(self):
        self.db = Database()

    def add_word(self, word, category):
        self.db.add_word(word, category)

    def update_word(self, word_id, new_word, new_category):
        self.db.update_word(word_id, new_word, new_category)

    def delete_word(self, word_id):
        self.db.delete_word(word_id)

    def fetch_words(self):
        return self.db.fetch_words()
