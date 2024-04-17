"""
Opgave "GUI step 1":

Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Bruge det, du har lært i GUI-eksempelfilerne, og byg den GUI, der er afbildet i images/gui_2010.png

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Teams-meddelelse til din lærer: <filename> færdig
Fortsæt derefter med den næste fil."""

import tkinter as ui

PADX = 24
PADY = 8

def main():
    root = ui.Tk()
    root.title("my first GUI")
    root.geometry("100x150")

    lf = ui.LabelFrame(root, text="Container")
    lf.pack()

    id_label = ui.Label(lf, text="Id")
    id_label.grid(row=0, column=0, padx=PADX, pady=PADY)

    id_entry = ui.Entry(lf, width=4)
    id_entry.grid(row=1, column=0, padx=PADX, pady=PADY)

    create_button = ui.Button(lf, text="CreateLayout")
    create_button.grid(row=2, column=0, padx=PADX, pady=PADY)

    root.mainloop()


if __name__ == "__main__":
    main()

