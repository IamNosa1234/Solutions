"""Opgave "GUI step 3":

Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Bruge det, du har lært i GUI-eksempelfilerne, og byg den GUI, der er afbildet i images/gui_2030.png

Genbrug din kode fra "GUI step 2".

GUI-strukturen bør være som følger:
    main window
        labelframe
            frame
                treeview and scrollbar
            frame
                labels and entries
            frame
                buttons

Funktionalitet:
    Klik på knappen "clear entry boxes" sletter teksten i alle indtastningsfelter (entries).


Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Teams-meddelelse til din lærer: <filename> færdig
Fortsæt derefter med den næste fil."""


import tkinter as ui
from tkinter import ttk

"""padding constants"""
PADX = 8
PADY = 4

"""scrollviewer constants"""
ROW_HEIGHT = 24
TV_BACKGROUND = "#eeeeee"
TV_FOREGROUND = "black"
TV_SELECTED = "#773333"
# copied values from S2026_gui_treeview_format.py, i will change them later in exercise 4.

def main():
    root = ui.Tk()
    root.title("my first GUI")
    root.geometry("550x410")
    root.resizable(False, False)

    container = ui.LabelFrame(root, text="Container")
    container.pack()

    scrollviewer_frame = ui.Frame(container)
    entry_frame = ui.Frame(container)
    buttons_frame = ui.Frame(container)

    create = CreateLayout(entry_frame, buttons_frame, scrollviewer_frame)

    create.create_treeview()
    create.create_entries()
    create.create_buttons()

    create.apply_style()

    scrollviewer_frame.grid(row=0, column=0, padx=PADX, pady=PADY)
    entry_frame.grid(row=1, column=0, padx=PADX, pady=PADY)
    buttons_frame.grid(row=2, column=0, padx=PADX, pady=PADY)

    root.mainloop()

class CreateLayout:
    def __init__(self, entry_frame, buttons_frame, scrollviewer_frame):
        self.entry_frame = entry_frame
        self.buttons_frame = buttons_frame
        self.scrollviewer_frame = scrollviewer_frame

        self.id_entry, self.weight_entry, self.destination_entry, self.weather_entry = None, None, None, None

    def create_entries(self):
        def pack(label, entry, column=0):
            label.grid(row=0, column=column, padx=PADX, pady=PADY)
            entry.grid(row=1, column=column, padx=PADX, pady=PADY)

        id_label = ui.Label(self.entry_frame, text="Id")
        self.id_entry = ui.Entry(self.entry_frame, width=4)
        pack(id_label, self.id_entry)

        weight_label = ui.Label(self.entry_frame, text="Weight")
        self.weight_entry = ui.Entry(self.entry_frame, width=8)
        pack(weight_label, self.weight_entry, 1)

        destination_label = ui.Label(self.entry_frame, text="Destination")
        self.destination_entry = ui.Entry(self.entry_frame, width=18)
        pack(destination_label, self.destination_entry, 2)

        weather_label = ui.Label(self.entry_frame, text="Weather")
        self.weather_entry = ui.Entry(self.entry_frame, width=14)
        pack(weather_label, self.weather_entry, 3)

    def create_buttons(self):
        def pack(button, column=0):
            button.grid(row=0, column=column, padx=PADX, pady=PADY)

        create_button = ui.Button(self.buttons_frame, text="Create")
        pack(create_button)

        update_button = ui.Button(self.buttons_frame, text="Update")
        pack(update_button, 1)

        delete_button = ui.Button(self.buttons_frame, text="Delete")
        pack(delete_button, 2)

        clear_button = ui.Button(self.buttons_frame, text="Clear Entry Boxes", command=self.clear_entries)
        pack(clear_button, 3)

    def create_treeview(self):
        self.scrollviewer_frame.grid(row=0, column=0, padx=PADX, pady=PADY)
        tree_scrollbar = ui.Scrollbar(self.scrollviewer_frame)
        tree_scrollbar.grid(row=0, column=1, sticky='ns')

        tree_1 = ttk.Treeview(self.scrollviewer_frame, yscrollcommand=tree_scrollbar.set, selectmode="browse")
        tree_1.grid(row=0, column=0)
        tree_scrollbar.config(command=tree_1.yview)

        tree_1['columns'] = ("#1", "#2", "#3")

        tree_1.column("#0", width=90, anchor=ui.W)
        tree_1.column("#1", width=130, anchor=ui.W)
        tree_1.column("#2", width=180, anchor=ui.W)
        tree_1.column("#3", width=90, anchor=ui.W)

        tree_1.heading("#0", text="Id", anchor=ui.CENTER)
        tree_1.heading("#1", text="Weight", anchor=ui.CENTER)
        tree_1.heading("#2", text="Destination", anchor=ui.CENTER)
        tree_1.heading("#3", text="Weather", anchor=ui.CENTER)

    @staticmethod
    def apply_style():
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background=TV_BACKGROUND, foreground=TV_FOREGROUND, rowheight=ROW_HEIGHT, fieldbackground=TV_BACKGROUND)
        style.map('Treeview', background=[('selected', TV_SELECTED)])

    def clear_entries(self):
        self.id_entry.delete(0, ui.END)
        self.weight_entry.delete(0, ui.END)
        self.destination_entry.delete(0, ui.END)
        self.weather_entry.delete(0, ui.END)


if __name__ == "__main__":
    main()

