
# PROGRAM GUI LOGIC STARTS HERE #

import tkinter as ui
from tkinter import ttk, messagebox

from sqlalchemy import column, Integer, Boolean

import S4010_PlusBus_Tables

import re


# GUI class
class PlusBusGUI:
    def __init__(self, root, DBActions):
        self.root = root
        self.DBActions = DBActions
        self.root.title("PlusBus")
        self.center_window(800, 600)

        # create a notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=ui.BOTH, expand=True)

        # create tabs
        self.create_customer_tab()
        self.create_bus_tab()
        self.create_travel_tab()

        # cycle through tabs with ctrl+tab and ctrl+shift+tab
        self.root.bind("<Control-Tab>", lambda event: self.notebook.select((self.notebook.index(self.notebook.select()) + 1) % self.notebook.index("end")))
        self.root.bind("<Control-Shift-Tab>", lambda event: self.notebook.select((self.notebook.index(self.notebook.select()) - 1) % self.notebook.index("end")))

        # bind ctrl+f to search current table
        self.root.bind(
            "<Control-f>", lambda event: self.search_table(
                # selected table
                "Customer" if self.notebook.index(self.notebook.select()) == 0 else
                "Bus" if self.notebook.index(self.notebook.select()) == 1 else
                "TravelArrangements",
                # selected table name
                "Customers" if self.notebook.index(self.notebook.select()) == 0 else
                "Buses" if self.notebook.index(self.notebook.select()) == 1 else
                "Travel Arrangements"))

        self.current_search = None

    def center_window(self, width, height):  # reused from my gui_exorcise
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        self.root.minsize(width, height)

        self.root.geometry('%dx%d+%d+%d' % (width, height, x, y))

    @staticmethod
    def set_column_width(tree):
        # the tkinter auto resize feature will fit all columns to the content.
        # unless the columns exist frame, setting them all to 1px will make them all the same size.
        # I would like to add that AI was beyond useless in this case.
        for column in tree["columns"]:
            tree.column(column, width=1)
        tree.column("#0", width=1)  # set default column width

    def create_customer_tab(self):
        # create a frame for the tab
        self.customer_tab = ui.Frame(self.notebook)
        self.notebook.add(self.customer_tab, text="Customers")

        # create a treeview
        self.customer_tree = ttk.Treeview(self.customer_tab, columns=("first_name", "last_name", "address", "age", "phone", "email", "is_enterprise", "enterprise_name", "enterprise_phone", "enterprise_email", "guest_quantity"))
        self.customer_tree.heading("#0", text="ID")
        self.customer_tree.heading("first_name", text="First Name")
        self.customer_tree.heading("last_name", text="Last Name")
        self.customer_tree.heading("address", text="Address")
        self.customer_tree.heading("age", text="Age")
        self.customer_tree.heading("phone", text="Phone")
        self.customer_tree.heading("email", text="Email")
        self.customer_tree.heading("is_enterprise", text="Is Enterprise")
        self.customer_tree.heading("enterprise_name", text="Enterprise Name")
        self.customer_tree.heading("enterprise_phone", text="Enterprise Phone")
        self.customer_tree.heading("enterprise_email", text="Enterprise Email")
        self.customer_tree.heading("guest_quantity", text="Guest Quantity")
        self.customer_tree.pack(fill=ui.BOTH, expand=True)

        # set column width to fix sizes
        self.set_column_width(self.customer_tree)

        # create a button frame
        self.customer_button_frame = ui.Frame(self.customer_tab)
        self.customer_button_frame.pack(fill=ui.X)

        # create buttons
        self.customer_add_button = ui.Button(self.customer_button_frame, text="Add Customer", command=self.add_customer)
        self.customer_add_button.pack(side=ui.LEFT)
        self.customer_edit_button = ui.Button(self.customer_button_frame, text="Edit Customer", command=self.edit_customer)
        self.customer_edit_button.pack(side=ui.LEFT)
        self.customer_delete_button = ui.Button(self.customer_button_frame, text="Delete Customer", command=self.delete_customer)
        self.customer_delete_button.pack(side=ui.LEFT)
        self.customer_search_button = ui.Button(self.customer_button_frame, text="Search Customers", command=lambda: self.search_table("Customer", "Customers"))
        self.customer_search_button.pack(side=ui.LEFT)

        self.customer_search_cancel_button = ui.Button(self.customer_button_frame, text="Cancel Search", command=lambda: (self.load_all_customers(),
                                                                                                                          self.customer_search_cancel_button.config(state=ui.DISABLED)))
        self.customer_search_cancel_button.pack(side=ui.LEFT), self.customer_search_cancel_button.config(state=ui.DISABLED)

        self.customer_tree.bind("<Button-3>", lambda event: (self.customer_tree.selection_set(selected_record := self.customer_tree.identify_row(event.y)),
                                                             self.context_menu(self.customer_tree, selected_record).post(event.x_root, event.y_root) if selected_record else None))

        self.load_all_customers()

    def load_all_customers(self):
        # Get all customers from the database
        customers = self.DBActions.get_customers()
        self.load_customers(customers)

    def load_customers(self, customers):
        # Clear the treeview
        self.customer_tree.delete(*self.customer_tree.get_children())

        # iterate over the customers
        for customer in customers:
            # Sort the data into a tuple, in the same order as the columns.
            data = (customer.first_name, customer.last_name, customer.address, customer.age,
                    customer.phone, customer.email, customer.is_enterprise, customer.enterprise_name,
                    customer.enterprise_phone, customer.enterprise_email, customer.guest_quantity)

            # Insert the data into the treeview
            self.customer_tree.insert("", "end", text=customer.id, values=data)

    def add_customer(self):
        self.add_or_edit_table("Customer", edit=False)

    def edit_customer(self):
        self.add_or_edit_table("Customer", edit=True)

    def delete_customer(self):
        self.delete_table("Customer")

    def create_bus_tab(self):
        # create a frame for the tab
        self.bus_tab = ui.Frame(self.notebook)
        self.notebook.add(self.bus_tab, text="Buses")

        # create a treeview
        self.bus_tree = ttk.Treeview(self.bus_tab, columns=("name", "capacity", "is_accessible"))
        self.bus_tree.heading("#0", text="ID")
        self.bus_tree.heading("name", text="Name")
        self.bus_tree.heading("capacity", text="Capacity")
        self.bus_tree.heading("is_accessible", text="Is Accessible")
        self.bus_tree.pack(fill=ui.BOTH, expand=True)

        # set column width to fix sizes
        self.set_column_width(self.bus_tree)

        # create a button frame
        self.bus_button_frame = ui.Frame(self.bus_tab)
        self.bus_button_frame.pack(fill=ui.X)

        # create buttons
        self.bus_add_button = ui.Button(self.bus_button_frame, text="Add Bus", command=self.add_bus)
        self.bus_add_button.pack(side=ui.LEFT)
        self.bus_edit_button = ui.Button(self.bus_button_frame, text="Edit Bus", command=self.edit_bus)
        self.bus_edit_button.pack(side=ui.LEFT)
        self.bus_delete_button = ui.Button(self.bus_button_frame, text="Delete Bus", command=self.delete_bus)
        self.bus_delete_button.pack(side=ui.LEFT)
        self.bus_search_button = ui.Button(self.bus_button_frame, text="Search Buses", command=lambda: self.search_table("Bus", "Buses"))
        self.bus_search_button.pack(side=ui.LEFT)

        self.bus_search_cancel_button = ui.Button(self.bus_button_frame, text="Cancel Search", command=lambda: (self.load_all_buses(),
                                                                                                                self.bus_search_cancel_button.config(state=ui.DISABLED)))
        self.bus_search_cancel_button.pack(side=ui.LEFT), self.bus_search_cancel_button.config(state=ui.DISABLED)

        self.bus_tree.bind("<Button-3>", lambda event: (self.bus_tree.selection_set(selected_record := self.bus_tree.identify_row(event.y)),
                                                        self.context_menu(self.bus_tree, selected_record).post(event.x_root, event.y_root) if selected_record else None))

        self.load_all_buses()

    def load_all_buses(self):
        # Get all buses from the database
        buses = self.DBActions.get_buses()
        self.load_buses(buses)

    def load_buses(self, buses):
        # Clear the treeview
        self.bus_tree.delete(*self.bus_tree.get_children())

        # iterate over the buses
        for bus in buses:
            # Sort the data into a tuple, in the same order as the columns.
            data = (bus.bus_name, bus.capacity, bus.is_accessible)

            # Insert the data into the treeview
            self.bus_tree.insert("", "end", text=bus.id, values=data)

    def add_bus(self):
        self.add_or_edit_table("Bus", edit=False)

    def edit_bus(self):
        self.add_or_edit_table("Bus", edit=True)

    def delete_bus(self):
        self.delete_table("Bus")

    def create_travel_tab(self):
        # create a frame for the tab
        self.travel_tab = ui.Frame(self.notebook)
        self.notebook.add(self.travel_tab, text="Travel Arrangements")

        # create a treeview
        self.travel_tree = ttk.Treeview(self.travel_tab, columns=("customer_id", "bus_id", "departure", "arrival", "price"))
        self.travel_tree.heading("#0", text="ID")
        self.travel_tree.heading("customer_id", text="Customer ID")
        self.travel_tree.heading("bus_id", text="Bus ID")
        self.travel_tree.heading("departure", text="Departure")
        self.travel_tree.heading("arrival", text="Arrival")
        self.travel_tree.heading("price", text="Price")
        self.travel_tree.pack(fill=ui.BOTH, expand=True)

        # set column width to fix sizes
        self.set_column_width(self.travel_tree)

        # create a button frame
        self.travel_button_frame = ui.Frame(self.travel_tab)
        self.travel_button_frame.pack(fill=ui.X)

        # create buttons
        self.travel_add_button = ui.Button(self.travel_button_frame, text="Add Travel Arrangement", command=self.add_travel_arrangement)
        self.travel_add_button.pack(side=ui.LEFT)
        self.travel_edit_button = ui.Button(self.travel_button_frame, text="Edit Travel Arrangement", command=self.edit_travel_arrangement)
        self.travel_edit_button.pack(side=ui.LEFT)
        self.travel_delete_button = ui.Button(self.travel_button_frame, text="Delete Travel Arrangement", command=self.delete_travel_arrangement)
        self.travel_delete_button.pack(side=ui.LEFT)
        self.travel_search_button = ui.Button(self.travel_button_frame, text="Search Travel Arrangements", command=lambda: self.search_table("TravelArrangements", "Travel Arrangements"))
        self.travel_search_button.pack(side=ui.LEFT)

        self.travel_search_cancel_button = ui.Button(self.travel_button_frame, text="Cancel Search", command=lambda: (self.load_all_travel_arrangements(),
                                                                                                                      self.travel_search_cancel_button.config(state=ui.DISABLED)))
        self.travel_search_cancel_button.pack(side=ui.LEFT), self.travel_search_cancel_button.config(state=ui.DISABLED)

        self.travel_tree.bind("<Button-3>", lambda event: (self.travel_tree.selection_set(selected_record := self.travel_tree.identify_row(event.y)),
                                                              self.context_menu(self.travel_tree, selected_record).post(event.x_root, event.y_root) if selected_record else None))

        self.load_all_travel_arrangements()

    def load_all_travel_arrangements(self):
        # Get all travel_arrangements from the database
        travel_arrangements = self.DBActions.get_travel_arrangements()
        self.load_travel_arrangements(travel_arrangements)

    def load_travel_arrangements(self, travel_arrangements):
        # Clear the treeview
        self.travel_tree.delete(*self.travel_tree.get_children())

        # iterate over the travel_arrangements
        for travel_arrangement in travel_arrangements:
            # Sort the data into a tuple, in the same order as the columns.
            data = (travel_arrangement.customer_id, travel_arrangement.bus_id, f"{travel_arrangement.transit_date} at {travel_arrangement.transit_time}", "arrival logic missing", f"{travel_arrangement.total_price} DKK")

            # Insert the data into the treeview
            self.travel_tree.insert("", "end", text=travel_arrangement.id, values=data)

    def add_travel_arrangement(self):
        self.add_or_edit_table("TravelArrangements", edit=False)

    def edit_travel_arrangement(self):
        self.add_or_edit_table("TravelArrangements", edit=True)

    def delete_travel_arrangement(self):
        self.delete_table("TravelArrangements")

    def search_table(self, table_class, placeholder):
        # popup a search dialog
        search_dialog = ui.Toplevel(self.root)
        search_dialog.title(f"Search {placeholder}")
        search_dialog.resizable(False, False)
        search_dialog.geometry("400x100")

        def center_in_main_window():  # meant to be global, testing it locally.
            search_dialog.update_idletasks()
            x = self.root.winfo_x() + (self.root.winfo_width() / 2) - (search_dialog.winfo_width() / 2)
            y = self.root.winfo_y() + (self.root.winfo_height() / 2) - (search_dialog.winfo_height() / 2)
            search_dialog.geometry("+%d+%d" % (x, y))

        center_in_main_window()

        # create a frame for the search dialog
        search_frame = ui.Frame(search_dialog)
        search_frame.pack(fill=ui.BOTH, expand=True)

        # create a search label
        search_label = ui.Label(search_frame, text=f"Search for {placeholder}:")
        search_label.pack()

        # create a search entry
        search_entry = ui.Entry(search_frame)
        search_entry.pack(fill=ui.X)

        table = S4010_PlusBus_Tables.Customer if table_class == "Customer" else S4010_PlusBus_Tables.Bus if table_class == "Bus" else S4010_PlusBus_Tables.TravelArrangements

        # create a search button
        search_button = ui.Button(search_frame,
                                  text="Search",
                                  command=lambda: (
                                      set_current_search(),
                                      self.load_customers(self.DBActions.search(table, search_entry.get())), search_dialog.destroy()) if table_class == "Customer"
                                  else (set_current_search(), self.load_buses(self.DBActions.search(table, search_entry.get())), search_dialog.destroy()) if table_class == "Bus"
                                  else (set_current_search(), self.load_travel_arrangements(self.DBActions.search(table, search_entry.get())), search_dialog.destroy()))

        def set_current_search():
            print("Setting current search")
            self.current_search = search_entry.get()
            if table_class == "Customer":
                if self.current_search in ("", None):
                    self.customer_search_cancel_button.config(state=ui.DISABLED)
                else:
                    self.customer_search_cancel_button.config(state=ui.NORMAL)
            elif table_class == "Bus":
                if self.current_search in ("", None):
                    self.bus_search_cancel_button.config(state=ui.DISABLED)
                else:
                    self.bus_search_cancel_button.config(state=ui.NORMAL)
            else:
                if self.current_search in ("", None):
                    self.travel_search_cancel_button.config(state=ui.DISABLED)
                else:
                    self.travel_search_cancel_button.config(state=ui.NORMAL)

        # cancel on esc
        search_dialog.bind("<Escape>", lambda event: search_dialog.destroy())

        # trigger button on enter key
        search_entry.bind("<Return>", lambda event: search_button.invoke())
        search_button.pack()

        search_entry.focus_set()
        self.root.wait_window(search_dialog)

    def delete_table(self, table_class):
        # ask for confirmation
        if ui.messagebox.askokcancel("Delete", f"Are you sure you want to delete the selected {table_class}?"):
            # get the selected item
            selected_item = self.customer_tree.selection()[0] if table_class == "Customer" else self.bus_tree.selection()[0] if table_class == "Bus" else self.travel_tree.selection()[0]

            # get the id of the selected item
            selected_id = self.customer_tree.item(selected_item)["text"] if table_class == "Customer" else self.bus_tree.item(selected_item)["text"] if table_class == "Bus" else self.travel_tree.item(selected_item)["text"]

            # delete the item
            if table_class == "Customer":
                self.DBActions.delete_customer(selected_id)
                self.load_all_customers()
            elif table_class == "Bus":
                self.DBActions.delete_bus(selected_id)
                self.load_all_buses()
            else:
                self.DBActions.delete_travel_arrangement(selected_id)
                self.load_all_travel_arrangements()

    def context_menu(self, tree, selected_record):
        # right click menu
        context = ui.Menu(self.root, tearoff=0)
        # submenu for copy columns
        copy_submenu = ui.Menu(context, tearoff=0)

        columns = tree.item(selected_record, 'values')
        column_names = [tree.heading(col)["text"] for col in tree["columns"]]

        for column_name, column_value in zip(column_names, columns):
            if column_value is None or column_value == "None":
                continue
            copy_submenu.add_command(
                label=f"{column_name}: {column_value}",
                command=lambda value=column_value: self.copy_to_clipboard(value)
            )

        context.add_cascade(label="Copy", menu=copy_submenu)
        context.add_separator()
        # edit / delete
        context.add_command(label="Edit", command=lambda: self.add_or_edit_table("Customer" if tree == self.customer_tree else "Bus" if tree == self.bus_tree else "TravelArrangements", edit=True))
        context.add_command(label="Delete", command=lambda: (self.delete_customer() if tree == self.customer_tree else self.delete_bus() if tree == self.bus_tree else self.delete_travel_arrangement()))

        return context

    def copy_to_clipboard(self, value):
        self.root.clipboard_clear()
        self.root.clipboard_append(value)
        self.root.update()

    @staticmethod
    def validate_data(data):
        # Check data formats using regex patterns
        email_pattern = r"[^@]+@[^@]+\.[^@]+"
        phone_pattern = r"^[0-9]{8}$"

        # Check email format, using a regex pattern
        if data.get("email") and not re.match(email_pattern, data.get("email")):
            messagebox.showerror("Invalid email", "Please enter a valid email address.")
            return False
        # Check Enterprise email format, if present.
        if data.get("enterprise_email") and not re.match(email_pattern, data.get("enterprise_email")):
            messagebox.showerror("Invalid email", "Please enter a valid email address.")
            return False
        # Check phone number format, (danish numbers only, no country code, 8 digits)
        if data.get("phone") and not re.match(phone_pattern, data.get("phone")):
            messagebox.showerror("Invalid phone number", "Please enter a valid phone number.")
            return False
        # Check Enterprise phone number format, if present.
        if data.get("enterprise_phone") and not re.match(phone_pattern, data.get("enterprise_phone")):
            messagebox.showerror("Invalid phone number", "Please enter a valid phone number.")
            return False

        return True

    def save_record(self, record, form, edit, dialog):
        data = {}

        # Ensure a new record object is created if not editing
        if record is None:
            raise ValueError("Record object cannot be None")

        for key, widget in form.items():
            if isinstance(widget, ui.Entry):
                value = widget.get().strip()

                # Handle integer fields (convert from string to int)
                if isinstance(record.__class__.__table__.columns[key].type, Integer):
                    try:
                        data[key] = int(value) if value else None
                    except ValueError:
                        raise ValueError(f"Invalid integer value for {key}: {value}")
                else:
                    data[key] = value if value else None

            elif isinstance(widget, ui.StringVar):  # Handle dropdown (boolean fields)
                data[key] = True if widget.get() == "True" else False

        # Check data formats
        if not self.validate_data(data):
            return

        if edit:
            self.DBActions.update_record(record, **data)
        else:
            # For new records, pass the data to create a new instance
            new_record = record.__class__(**data)
            self.DBActions.add_record(new_record)

        # Reload the table
        if record.__class__.__name__ == "Customer":
            self.load_all_customers()
        elif record.__class__.__name__ == "Bus":
            self.load_all_buses()
        else:
            self.load_all_travel_arrangements()

        dialog.destroy()

    def add_or_edit_table(self, table_class, edit):
        # Select class based on table name
        select_class = S4010_PlusBus_Tables.Customer if table_class == "Customer" else S4010_PlusBus_Tables.Bus if table_class == "Bus" else S4010_PlusBus_Tables.TravelArrangements

        tree = self.customer_tree if table_class == "Customer" else self.bus_tree if table_class == "Bus" else self.travel_tree

        # Create dialog
        dialog = ui.Toplevel(self.root)
        dialog.title(f"{'Edit' if edit else 'Add'} {table_class}")
        dialog.resizable(True, False)
        dialog.geometry("400x400")

        dialog_frame = ui.Frame(dialog)
        dialog_frame.pack(fill=ui.BOTH, expand=True)

        form = {}
        columns = [column for column in select_class.__table__.columns]

        record = self.DBActions.get_record(select_class, tree.item(tree.selection())["text"]) if edit else select_class()  # Create a new instance if adding

        for column in columns:
            column_name = column.key
            field_type = column.type

            # Create label for each field
            form[f"{column_name}_label"] = ui.Label(dialog_frame, text=column_name)
            form[f"{column_name}_label"].pack(fill=ui.X)

            if isinstance(field_type, Boolean):  # Dropdown for boolean fields
                form[column_name] = ui.StringVar(value="True" if getattr(record, column_name, False) else "False")
                boolean_menu = ui.OptionMenu(dialog_frame, form[column_name], "True", "False")
                boolean_menu.pack(fill=ui.X)

            elif isinstance(field_type, Integer):  # Validated Entry for integer fields
                validate_cmd = dialog_frame.register(self.validate_int)  # Register validation function
                form[column_name] = ui.Entry(dialog_frame, validate="key", validatecommand=(validate_cmd, "%P"))
                form[column_name].pack(fill=ui.X)
                if edit and record:
                    try:
                        form[column_name].insert(0, str(getattr(record, column_name, "")))
                    except Exception as e:
                        print(f"Error inserting value into field: {e}")

            else:  # Default to Entry for other fields
                form[column_name] = ui.Entry(dialog_frame)
                form[column_name].pack(fill=ui.X)
                if edit and record:
                    try:
                        form[column_name].insert(0, getattr(record, column_name, ""))
                    except Exception as e:
                        print(f"Error inserting value into field: {e}")

        button_frame = ui.Frame(dialog)
        button_frame.pack(fill=ui.X)

        save_button = ui.Button(button_frame, text="Save", command=lambda: self.save_record(record, form, edit, dialog))
        save_button.pack(side=ui.LEFT)

        cancel_button = ui.Button(button_frame, text="Cancel", command=dialog.destroy)
        cancel_button.pack(side=ui.LEFT)

        # Force geometry update
        dialog.update_idletasks()

        # Get the height of the dialog after widgets have been packed
        desired_height = dialog.winfo_reqheight()
        dialog.geometry(f"400x{desired_height}")

    @staticmethod
    def validate_int(value_if_allowed):
        if value_if_allowed == "" or value_if_allowed.isdigit():
            return True
        else:
            return False
