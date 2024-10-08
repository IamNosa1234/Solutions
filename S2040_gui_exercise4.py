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
from tkinter import filedialog

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
HEIGHT = 480

def main():
    root = ui.Tk()
    root.title("my first GUI")
    center_window(root, WIDTH, HEIGHT)

    container = ui.LabelFrame(root, text="Container")
    container.pack(padx=PADX, pady=PADY, fill=ui.BOTH, expand=True)

    scrollviewer_frame = ui.Frame(container)
    entry_frame = ui.Frame(container)
    buttons_frame = ui.Frame(container)
    json_label_frame = ui.LabelFrame(container, text="JSON")

    create = CreateLayout(entry_frame, buttons_frame, scrollviewer_frame, json_label_frame, root)

    create.create_treeview()
    create.create_entries()
    create.create_buttons()

    create.apply_style()

    for i in range(4):
        container.grid_rowconfigure(i, weight=1 if i != 0 else 15)
    container.grid_columnconfigure(0, weight=1)

    scrollviewer_frame.grid(row=0, column=0, sticky=ui.NSEW, padx=PADX, pady=PADY)
    scrollviewer_frame.grid_columnconfigure(0, weight=1)
    entry_frame.grid(row=1, column=0, padx=PADX, pady=PADY, sticky=ui.S)
    entry_frame.grid_columnconfigure(0, weight=1)
    buttons_frame.grid(row=2, column=0, padx=PADX, pady=PADY, sticky=ui.S)
    buttons_frame.grid_columnconfigure(0, weight=1)
    json_label_frame.grid(row=3, column=0, padx=PADX, pady=PADY, sticky=ui.S)
    json_label_frame.grid_columnconfigure(0, weight=1)

    root.mainloop()

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)

    root.minsize(width, height)

    root.geometry('%dx%d+%d+%d' % (width, height, x, y))  # width x height + x_offset + y_offset
    # This type of string formatting is very similar to cpp's string interpolation, though i'm not very good at it. been using f-strings for a while now, but this looks good.

class CreateLayout:
    def __init__(self, entry_frame, buttons_frame, scrollviewer_frame, json_label_frame, root):
        self.entry_frame = entry_frame
        self.buttons_frame = buttons_frame
        self.scrollviewer_frame = scrollviewer_frame
        self.json_label_frame = json_label_frame
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

        save_json_button = ui.Button(self.json_label_frame, text="Quick Save", command=self.save_to_json)
        pack(save_json_button, 0, 1)

        load_json_button = ui.Button(self.json_label_frame, text="Load from JSON", command=self.load_from_json)
        pack(load_json_button, 1, 1)

        append_json_button = ui.Button(self.json_label_frame, text="Append from JSON", command=lambda: self.load_from_json(True))
        pack(append_json_button, 2, 1)

        save_as_json_button = ui.Button(self.json_label_frame, text="Save as...", command=lambda: self.save_to_json(True))
        pack(save_as_json_button, 3, 1)

    def create_treeview(self):
        tree_scrollbar = ui.Scrollbar(self.scrollviewer_frame)
        tree_scrollbar.grid(row=0, column=1, sticky='ns')

        self.tree = ttk.Treeview(self.scrollviewer_frame, yscrollcommand=tree_scrollbar.set, selectmode="browse")
        self.tree.grid(row=0, column=0, sticky=ui.NSEW, padx=PADX, pady=PADY)

        tree_scrollbar.config(command=self.tree.yview)

        self.tree.bind("<ButtonRelease-1>", lambda e: self.edit_record(e))

        self.tree['columns'] = ("#1", "#2", "#3", "#4")

        # remove text column
        self.tree.column("#0", width=0, stretch=ui.NO)

        self.tree.column("#1", width=90, anchor=ui.CENTER)
        self.tree.column("#2", width=130, anchor=ui.W)
        self.tree.column("#3", width=180, anchor=ui.W)
        self.tree.column("#4", width=70, anchor=ui.W)

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
        if not self.check_record():
            return

        self.tree.insert(parent='', index='end', text='', tags="evenrow" if self.tree_counter % 2 == 0 else "oddrow",  # not using tuple because it was ugly and i only need one value anyway
                         values=(self.id_entry.get().zfill(4) if not self.id_entry.get() == '0' else self.asign_id(),  # make sure the id is unique
                                 self.weight_entry.get(),
                                 self.destination_entry.get(),
                                 self.weather_entry.get()
                                 ))

        self.tree_counter += 1
        self.tree.yview_moveto(1.0)

    def edit_record(self, event):
        index_selected = self.tree.focus()
        if index_selected:
            try:
                values = self.tree.item(index_selected, 'values')
                self.id_entry.delete(0, ui.END)
                self.id_entry.insert(0, values[0])
                self.weight_entry.delete(0, ui.END)
                self.weight_entry.insert(0, values[1])
                self.destination_entry.delete(0, ui.END)
                self.destination_entry.insert(0, values[2])
                self.weather_entry.delete(0, ui.END)
                self.weather_entry.insert(0, values[3])
            except IndexError as e:
                print("Error while trying to edit record: ", e)

    def update_record(self):
        if not self.check_record(update=True):
            return

        if self.tree.focus():
            self.tree.item(self.tree.focus(),
                           values=(self.id_entry.get().zfill(4),
                                   self.weight_entry.get(),
                                   self.destination_entry.get(),
                                   self.weather_entry.get()
                                   ))

    def check_record(self, update: bool = False) -> bool:
        # Check if all fields are filled
        if not self.id_entry.get() or not self.weight_entry.get() or not self.destination_entry.get() or not self.weather_entry.get():
            messagebox.showerror("Error", "Please fill all fields")
            return False

        # Check if id is an integer value
        if not self.id_entry.get().isdigit():
            messagebox.showerror("Error", "Id must be a number")
            return False

        # Check if weight is an integer or float value
        if not self.weight_entry.get().lower().replace(".", "").replace("kg", "").replace("lb", "").replace(' ', '').isdigit():
            messagebox.showerror("Error", "Weight must be a number")
            return False

        # Check if id is unique
        if not update:
            if not self.id_entry.get() == '0' and self.id_entry.get().zfill(4) in [self.tree.item(item, "values")[0] for item in self.tree.get_children()]:
                messagebox.showerror("Error", "Id already exists\nPut 0 to auto assign id")
                return False

        return True

    def delete_record(self):
        if focus := (tree := self.tree).focus():  # COOOl dude  walRUSSSSS, he looks funny, i like him.
            if messagebox.askyesno("Delete Record", "Are you sure you want to delete this record?"):
                tree.delete(focus)  # idk how much effect extraction has on performance in python. all i know is that its a good practice in c# and java.
                self.tree_counter -= 1
                for index, item in enumerate(tree.get_children()):
                    tree.item(item, tags="evenrow" if index % 2 == 0 else "oddrow")

    def save_to_json(self, save_as: bool = False):
        if not self.tree.get_children():
            return messagebox.showerror("Error", "No data to save")

        if not save_as:
            if not messagebox.askyesno("Quick Save", "This will overwrite last quick save or data.json\nAre you sure you want to save?"):
                return

        data = {}
        for index, item in enumerate(self.tree.get_children()):
            values = self.tree.item(item, 'values')
            data[index] = {
                "id": values[0],
                "weight": values[1],
                "destination": values[2],
                "weather": values[3]
            }

        file_path = "data.json" if not save_as else filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not file_path:
            return

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def load_from_json(self, append: bool = False):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file_path:  # if the user cancels the file dialog
            return

        if not append and len(self.tree.get_children()) > 0:
            if not messagebox.askyesno("Load Data", "Are you sure you want to load data?\nThis will overwrite any unsaved data."):
                return

        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError as e:
            return messagebox.showerror("Error", "No data to load\n%s" % str(e))

        if not self.verify_json(data):
            return

        if not append:
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.tree_counter = 0

        for index, item in enumerate(data.values()):
            self.tree.insert(parent='', index='end', text='', tags=("evenrow" if self.tree_counter % 2 == 0 else "oddrow"),
                             values=(item["id"].zfill(4) if not append else self.asign_id(),  # make sure the id is unique, originally i was doing "item["id"].zfill(4) if not append str(self.tree_counter).zfill(4)" but that caused duplicate id's
                                     item["weight"], item["destination"], item["weather"]))
            self.tree_counter += 1

    def asign_id(self):
        # probably not the most efficient way to do this but it works,
        ids = [self.tree.item(item, "values")[0] for item in self.tree.get_children()]
        for i in range(1, 9999):
            if str(i).zfill(4) not in ids:
                return str(i).zfill(4)

    @staticmethod
    def verify_json(items):
        if not isinstance(items, dict):
            return False

        # check json format
        if not all(key in item for item in items.values() for key in ("id", "weight", "destination", "weather")):  # some of the python methods are crazy, crazy convenient. list comprehension is killing me. ok that took the longest time to get right.
            messagebox.showerror("Error", "Invalid JSON format")
            return False

        for item in items.values():
            # Check if all fields are filled
            if not item["id"] or not item["weight"] or not item["destination"] or not item["weather"]:
                messagebox.showerror("Error", "Please fill all fields")
                return False

            # Check if id is an integer value
            if not item["id"].isdigit():
                messagebox.showerror("Error", "Id must be a number")
                return False

            # Check if weight is an integer or float value
            if not item["weight"].lower().replace(".", "").replace("kg", "").replace("lb", "").replace(' ', '').isdigit():
                messagebox.showerror("Error", "Weight must be a number")
                return False

            # Check if id is unique
            if len(items) != len(set(item["id"] for item in items.values())):  # genius solution but it was a gpt suggestion😔cant take credit😔  simply put. set() removes duplicates from a list. so if the length of the set is less than the length of the list, there are duplicates.
                messagebox.showerror("Error", "All Id's must be unique")
                return False

        return True


if __name__ == "__main__":
    main()
