from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Treeview, Button, Scrollbar

class View(Tk):
    def __init__(self, model, controller):
        """
        Põhiakna konstruktor
        """
        super().__init__()
        self.model = model
        self.__myTable = None
        self.controller = controller

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Põhiaken
        self.__width = 500
        self.__height = 350
        self.title('Poomismängu andmebaasi haldus')
        self.center(self.__width, self.__height)

        # Loome komponendid
        self.__frame_top, self.__frame_bottom, self.__frame_right = self.create_frames()
        self.__lbl_category, self.__txt_category, self.__lbl_word, self.__txt_word = self.create_main_form()
        self.__lbl_old_categories, self.__combo_categories = self.create_combobox()
        self.__btn_add, self.__btn_edit, self.__btn_delete = self.create_buttons()
        self.create_table()

    def center(self, w, h):
        """
        Paigutab akna ekraani keskele.
        """
        x = int((self.winfo_screenwidth() / 2) - (w / 2))
        y = int((self.winfo_screenheight() / 2) - (h / 2))
        self.geometry(f'{w}x{h}+{x}+{y}')

    def create_frames(self):
        """
        Loob põhikujunduse frame'id.
        """
        top = Frame(self, height=100, background='lightblue')
        bottom = Frame(self, background='lightyellow')
        right = Frame(top, background='lightgray')

        top.pack(fill=BOTH)
        bottom.pack(fill=BOTH, expand=True)
        right.grid(row=0, column=2, rowspan=3, padx=5, pady=5, sticky=NS)

        return top, bottom, right

    def create_main_form(self):
        """
        Loob põhilised sisestuskastid.
        """
        lbl_1 = Label(self.__frame_top, text='Uus kategooria:', background='lightblue', font=('Verdana', 10, 'bold'))
        txt_1 = Entry(self.__frame_top)
        lbl_1.grid(row=0, column=0, pady=5, padx=5, sticky=W)
        txt_1.grid(row=0, column=1, pady=5, padx=5, sticky=EW)

        lbl_2 = Label(self.__frame_top, text='Sõna:', background='lightblue', font=('Verdana', 10, 'bold'))
        txt_2 = Entry(self.__frame_top)
        lbl_2.grid(row=2, column=0, pady=5, padx=5, sticky=W)
        txt_2.grid(row=2, column=1, pady=5, padx=5, sticky=EW)

        return lbl_1, txt_1, lbl_2, txt_2

    def create_buttons(self):
        """
        Loob vajalikud nupud.
        """
        btn_1 = Button(self.__frame_right, text='Lisa')
        btn_2 = Button(self.__frame_right, text='Muuda')
        btn_3 = Button(self.__frame_right, text='Kustuta')
        #btn_4 = Button(self.__frame_right, text='Ava andmebaas')

        btn_1.grid(row=0, column=1, padx=1, sticky=EW)
        btn_2.grid(row=1, column=1, padx=1, sticky=EW)
        btn_3.grid(row=0, column=2, padx=1, sticky=EW)

        return btn_1, btn_2, btn_3

    def create_combobox(self):
        """
        Loob rippmenüü kategooriate valimiseks.
        """
        label = Label(self.__frame_top, text='Vana kategooria:', background='lightblue', font=('Verdana', 10, 'bold'))
        label.grid(row=1, column=0, pady=5, padx=5, sticky=W)

        combo = Combobox(self.__frame_top)
        combo['values'] = ('Vali kategooria', 'Hooned', 'Loomad', 'Sõidukid')
        combo.current(0)
        combo.grid(row=1, column=1, padx=5, sticky=EW)

        return label, combo

    def create_table(self):
        """
        Loob andmetabeli.
        """
        self.__myTable = Treeview(self.__frame_bottom, columns=("jrk", "id", "word", "category"), show="headings")

        vsb = Scrollbar(self.__frame_bottom, orient=VERTICAL, command=self.__myTable.yview)
        vsb.pack(side=RIGHT, fill=Y)
        self.__myTable.configure(yscrollcommand=vsb.set)

        self.__myTable.heading("jrk", text="Jrk", anchor=CENTER)
        self.__myTable.heading("id", text="ID", anchor=CENTER)
        self.__myTable.heading("word", text="Sõna", anchor=CENTER)
        self.__myTable.heading("category", text="Kategooria", anchor=CENTER)

        self.__myTable.column("jrk", anchor=W, width=30)
        self.__myTable.column("id", anchor=W, width=50)
        self.__myTable.column("word", anchor=W, width=150)
        self.__myTable.column("category", anchor=W, width=150)

        self.__myTable.pack(fill=BOTH, expand=True)
        self.__btn_open_db = Button(self.__frame_right, text="Ava andmebaas")
        self.__btn_open_db.grid(row=3, column=1, padx=1, sticky=EW)
        self.get_my_table.bind('<Double-1>', self.on_row_double_click)

    def set_controller(self, controller):
        """ Seob kontrolleri pärast selle loomist """
        self.controller = controller
        self.__btn_open_db.config(command=self.controller.open_database)  # Seob nupu funktsiooniga

    def on_row_double_click(self, event):
        """
        Kui kasutaja teeb tabelis topeltklõpsu, avaneb popup aken valitud info näitamiseks.
        """
        selected_item = self.get_my_table.selection()
        if selected_item:
            row_values = self.get_my_table.item(selected_item, 'values')
            word_id, word, category = row_values[1], row_values[2], row_values[3]

    # Näitame pop-up aknas infot
        self.get_txt_word.delete(0, END)
        self.get_txt_word.insert(0, word)
        self.get_combo_categories.set(category)

    # Getterid, mida kontroller vajab
    @property
    def get_txt_word(self):
        return self.__txt_word

    @property
    def get_txt_category(self):
        return self.__txt_category

    @property
    def get_my_table(self):
        return self.__myTable

    @property
    def get_combo_categories(self):
        return self.__combo_categories

    @property
    def get_btn_add(self):
        return self.__btn_add

    @property
    def get_btn_edit(self):
        return self.__btn_edit

    @property
    def get_btn_delete(self):
        return self.__btn_delete

