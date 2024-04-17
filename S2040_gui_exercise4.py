""" Opgave "GUI step 4":

Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Bruge det, du har lært i GUI-eksempelfilerne, og byg den GUI, der er afbildet i images/gui_2040.png

Genbrug din kode fra "GUI step 3".

Fyld treeview'en med testdata.
Leg med farveværdierne. Find en farvekombination, som du kan lide.

Funktionalitet:
    Klik på knappen "clear entry boxes" sletter teksten i alle indtastningsfelter (entries).
    Hvis du klikker på en datarække i træoversigten, kopieres dataene i denne række til indtastningsfelterne.

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Teams-meddelelse til din lærer: <filename> færdig
Fortsæt derefter med den næste fil."""


import tkinter as ui
import json
from tkinter import ttk
from tkinter import messagebox

"""padding constants"""
PADX = 8
PADY = 4

"""scrollviewer constants"""
ROW_HEIGHT = 24
TV_BACKGROUND = "#eeeeee"
TV_FOREGROUND = "black"
TV_SELECTED = "grey"
TV_ODDROW = "lightgrey"
TV_EVENTROW = "#e0e0e0"

"""window constants"""
WIDTH = 550
HEIGHT = 445

def main():
    root = ui.Tk()
    root.title("my first GUI")
    root.resizable(False, False)
    center_window(root, WIDTH, HEIGHT)

    container = ui.LabelFrame(root, text="Container")
    container.pack()

    scrollviewer_frame = ui.Frame(container)
    entry_frame = ui.Frame(container)
    buttons_frame = ui.Frame(container)

    create = CreateLayout(entry_frame, buttons_frame, scrollviewer_frame, root)

    create.create_treeview()
    create.create_entries()
    create.create_buttons()

    create.apply_style()

    scrollviewer_frame.grid(row=0, column=0, padx=PADX, pady=PADY)
    entry_frame.grid(row=1, column=0, padx=PADX, pady=PADY)
    buttons_frame.grid(row=2, column=0, padx=PADX, pady=PADY)

    root.mainloop()

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)

    root.geometry('%dx%d+%d+%d' % (width, height, x, y))  # width x height + x_offset + y_offset
    # This type of string formatting is very similar to cpp's string interpolation, though i'm not very good at it. been using f-strings for a while now, but this looks good.

class CreateLayout:
    def __init__(self, entry_frame, buttons_frame, scrollviewer_frame, root):
        self.entry_frame = entry_frame
        self.buttons_frame = buttons_frame
        self.scrollviewer_frame = scrollviewer_frame
        self.root = root

        self.id_entry, self.weight_entry, self.destination_entry, self.weather_entry = None, None, None, None

        self.tree = None
        self.tree_counter = 0

    def create_entries(self):
        def pack(label, entry, column=0):
            label.grid(row=0, column=column, padx=PADX, pady=PADY)
            entry.grid(row=1, column=column, padx=PADX, pady=PADY)

        def id_syntax(value):
            return (len(value) <= 4 and value.isdigit()) or value == ''
            #  cool i was able to solve thing just usin the documentation, thought it'd be harder :)

        validate_id = (self.root.register(id_syntax), '%P')  # can't figure out whether %P is a value or permission, maybe a conditional value?

        id_label = ui.Label(self.entry_frame, text="Id")
        self.id_entry = ui.Entry(self.entry_frame, width=4, validate="key", validatecommand=validate_id)
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
        def pack(button, column=0, row=0):
            button.grid(row=row, column=column, padx=PADX, pady=PADY)

        create_button = ui.Button(self.buttons_frame, text="Create", command=self.append_data)
        pack(create_button)

        update_button = ui.Button(self.buttons_frame, text="Update", command=self.update_record)
        pack(update_button, 1)

        delete_button = ui.Button(self.buttons_frame, text="Delete", command=self.delete_record)
        pack(delete_button, 2)

        clear_button = ui.Button(self.buttons_frame, text="Clear Entry Boxes", command=self.clear_entries)
        pack(clear_button, 3)

        save_json_button = ui.Button(self.buttons_frame, text="Save to JSON", command=self.save_to_json)
        pack(save_json_button, 1, 1)

        load_json_button = ui.Button(self.buttons_frame, text="Load from JSON", command=self.load_from_json)
        pack(load_json_button, 2, 1)

    def create_treeview(self):
        self.scrollviewer_frame.grid(row=0, column=0, padx=PADX, pady=PADY)
        tree_scrollbar = ui.Scrollbar(self.scrollviewer_frame)
        tree_scrollbar.grid(row=0, column=1, sticky='ns')

        self.tree = ttk.Treeview(self.scrollviewer_frame, yscrollcommand=tree_scrollbar.set, selectmode="browse")
        self.tree.grid(row=0, column=0)
        tree_scrollbar.config(command=self.tree.yview)

        self.tree.bind("<ButtonRelease-1>", lambda e: self.edit_record(e))  # lambda error sometime occur, value[0] is not defined, troubleshooting required.

        self.tree['columns'] = ("#1", "#2", "#3", "#4")

        # remove text column
        self.tree.column("#0", width=0, stretch=ui.NO)

        self.tree.column("#1", width=90, anchor=ui.CENTER)
        self.tree.column("#2", width=130, anchor=ui.W)
        self.tree.column("#3", width=180, anchor=ui.W)
        self.tree.column("#4", width=90, anchor=ui.W)

        self.tree.heading("#1", text="Id", anchor=ui.CENTER)
        self.tree.heading("#2", text="Weight", anchor=ui.CENTER)
        self.tree.heading("#3", text="Destination", anchor=ui.CENTER)
        self.tree.heading("#4", text="Weather", anchor=ui.CENTER)

        self.tree.tag_configure("oddrow", background=TV_ODDROW)
        self.tree.tag_configure("evenrow", background=TV_EVENTROW)

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

    def append_data(self):
        # Check if all fields are filled
        if not self.id_entry.get() or not self.weight_entry.get() or not self.destination_entry.get() or not self.weather_entry.get():
            return messagebox.showerror("Error", "Please fill all fields")

        # Check if id is an integer value
        if not self.id_entry.get().isdigit():
            return messagebox.showerror("Error", "Id must be a number")

        # Check if weight is an integer or float value
        if not self.weight_entry.get().replace(".", "").isdigit():
            return messagebox.showerror("Error", "Weight must be a number")

        self.tree.insert(parent='', index='end', text='', tags="evenrow" if self.tree_counter % 2 == 0 else "oddrow",  # not using tuple because it was ugly and i only need one value anyway
                         values=(self.id_entry.get().zfill(4),
                                 self.weight_entry.get(),
                                 self.destination_entry.get(),
                                 self.weather_entry.get()
                                 ))

        self.tree_counter += 1

    def edit_record(self, event):
        index_selected = self.tree.focus()
        values = self.tree.item(index_selected, 'values')
        self.id_entry.delete(0, ui.END)
        self.id_entry.insert(0, values[0])
        self.weight_entry.delete(0, ui.END)
        self.weight_entry.insert(0, values[1])
        self.destination_entry.delete(0, ui.END)
        self.destination_entry.insert(0, values[2])
        self.weather_entry.delete(0, ui.END)
        self.weather_entry.insert(0, values[3])

    def update_record(self):
        if self.tree.focus():
            self.tree.item(self.tree.focus(), values=(self.id_entry.get().zfill(4),
                                                      self.weight_entry.get(),
                                                      self.destination_entry.get(),
                                                      self.weather_entry.get()
                                                      ))

    def delete_record(self):
        if focus := (tree := self.tree).focus():  # COOOl dude  walRUSSSSS, he looks funny, i like him.
            tree.delete(focus)                      # idk how much effect extraction has on performance in python. all i know is that its a good practice in c# and java.
            self.tree_counter -= 1
            for index, item in enumerate(tree.get_children()):
                tree.item(item, tags="evenrow" if index % 2 == 0 else "oddrow")

    def save_to_json(self):
        if not self.tree.get_children():
            return messagebox.showerror("Error", "No data to save")

        data = {}
        for index, item in enumerate(self.tree.get_children()):
            values = self.tree.item(item, 'values')
            data[index] = {
                "id": values[0],
                "weight": values[1],
                "destination": values[2],
                "weather": values[3]
            }

        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)

    def load_from_json(self):
        if not messagebox.askyesno("Load Data", "Are you sure you want to load data?\nThis will overwrite any unsaved data."):
            return

        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            return messagebox.showerror("Error", "No data to load")

        for item in self.tree.get_children():
            self.tree.delete(item)

        for index, item in enumerate(data.values()):
            self.tree.insert(parent='', index='end', text='', tags="evenrow" if index % 2 == 0 else "oddrow",
                             values=(item["id"], item["weight"], item["destination"], item["weather"]))


if __name__ == "__main__":
    main()

