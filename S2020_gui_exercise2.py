""" Opgave "GUI step 2":

Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Bruge det, du har lært i GUI-eksempelfilerne, og byg den GUI, der er afbildet i images/gui_2020.png

Genbrug din kode fra "GUI step 1".

GUI-strukturen bør være som følger:
    main window
        labelframe
            frame
                labels and entries
            frame
                buttons
                    THX :)

Funktionalitet:
    Klik på knappen "clear entry boxes" sletter teksten i alle indtastningsfelter (entries).

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Teams-meddelelse til din lærer: <filename> færdig
Fortsæt derefter med den næste fil."""

import tkinter as ui

PADX = 8
PADY = 4

def main():
    root = ui.Tk()
    root.title("my first GUI")
    root.geometry("400x150")

    container = ui.LabelFrame(root, text="Container")
    container.pack()

    entry_frame = ui.Frame(container)
    buttons_frame = ui.Frame(container)

    create = CreateLayout(entry_frame, buttons_frame)

    create.create_entries()
    create.create_buttons()

    entry_frame.grid(row=0, column=0, padx=PADX, pady=PADY)
    buttons_frame.grid(row=1, column=0, padx=PADX, pady=PADY)

    root.mainloop()

class CreateLayout:
    def __init__(self, entry_frame, buttons_frame):
        self.entry_frame = entry_frame
        self.buttons_frame = buttons_frame

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

        create_button = ui.Button(self.buttons_frame, text="CreateLayout")
        pack(create_button)

        update_button = ui.Button(self.buttons_frame, text="Update")
        pack(update_button, 1)

        delete_button = ui.Button(self.buttons_frame, text="Delete")
        pack(delete_button, 2)

        clear_button = ui.Button(self.buttons_frame, text="Clear Entry Boxes", command=self.clear_entries)
        pack(clear_button, 3)

    def clear_entries(self):
        # could be dynamic?
        self.id_entry.delete(0, ui.END)
        self.weight_entry.delete(0, ui.END)
        self.destination_entry.delete(0, ui.END)
        self.weather_entry.delete(0, ui.END)


if __name__ == "__main__":
    main()
