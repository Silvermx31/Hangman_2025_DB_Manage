from tkinter import END, filedialog
from models.database import Database


class Controller:
    def __init__(self, model, view):
        """
        Kontrolleri konstruktor
        """
        self.model = model
        self.view = view

        # Seome nupud meetoditega
        self.view.get_btn_add.config(command=self.add_word)
        self.view.get_btn_edit.config(command=self.update_word)
        self.view.get_btn_delete.config(command=self.delete_word)
        self.load_words()
        self.load_categories()
        # Andmete laadimine tabelisse
        #print("Controller töötab!")  # TESTIMINE
        self.load_words()

    def load_words(self):
        """
        Laeb sõnad ja kategooriad andmebaasist tabelisse
        """
        self.view.get_my_table.delete(*self.view.get_my_table.get_children())
        words = self.model.fetch_words()
        for idx, (word_id, word, category) in enumerate(words, start=1):
            self.view.get_my_table.insert("", "end", values=(idx, word_id, word, category))
        print("Sõnad uuendatud tabelis!")  # TEST

    def load_categories(self):
        """
        Laeb andmebaasis olevad kategooriad rippmenüüsse.
        """
        categories = self.model.db.fetch_categories()
        categories.insert(0, "Vali kategooria")  #  Lisame vaikevaliku esimeseks
        self.view.get_combo_categories["values"] = categories  # Seame rippmenüü väärtused
        self.view.get_combo_categories.current(0)  #  Määrame vaikevalikuks "Vali kategooria"

    def add_word(self):
        """
        Lisab uue sõna ja kategooria andmebaasi ning uuendab tabelit
        """
        word = self.view.get_txt_word.get().strip()  # Sõna väljast
        selected_category = self.view.get_combo_categories.get().strip()  # Kategooria rippmenüüst!
        new_category = self.view.get_txt_category.get().strip()
        category = new_category if new_category else selected_category

        if word and category and category != "Vali kategooria":  # Väldime tühje väärtusi
            self.model.add_word(word, category)
            print("Sõna lisatud andmebaasi!")  # TEST
            self.load_words()  # Uuendab tabelit
            self.load_categories()
            self.view.get_txt_word.delete(0, END)  # Tühjendab sõna sisestusvälja
            self.view.get_txt_category.delete(0, END)
        else:
            print("Sõna või kategooria puudub või valiti 'Vali kategooria'!")  # Kui kasutaja ei täitnud välju

    def update_word(self):
        """
        Uuendab valitud sõna ja kategooriat andmebaasis
        """
        selected = self.view.get_my_table.selection()  # Võtab valitud rea

        if selected:
            word_id = self.view.get_my_table.item(selected)['values'][1]  # Saab ID veerust
            new_word = self.view.get_txt_word.get().strip()  # Saab sõna sisestusväljast
            new_category = self.view.get_combo_categories.get().strip()  # Saab kategooria rippmenüüst

            if new_word and new_category and new_category != "Vali kategooria":
                self.model.update_word(word_id, new_word, new_category)
                print("Sõna uuendatud andmebaasis!")  # TEST
                self.load_words()  # Uuendab tabelit
            else:
                print("Uus sõna või kategooria puudub!")
        else:
            print("Ühtegi rida pole valitud!")

    def delete_word(self):
        """
        Kustutab valitud sõna andmebaasist ja uuendab tabelit
        """
        selected = self.view.get_my_table.selection()
        if selected:
            word_id = self.view.get_my_table.item(selected)['values'][1]
            self.model.delete_word(word_id)
            self.load_words()

    def open_database(self):

        file_path = filedialog.askopenfilename(filetypes=[("SQLite Database", "*.db")])
        if file_path:
            self.model.db.open_database(file_path)
            self.load_words()
            print(f'Ei toimi {file_path}')