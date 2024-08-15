
# PROGRAM GUI LOGIC STARTS HERE #

import tkinter as ui
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

# GUI class
class PlusBusGUI:
    def __init__(self, root, DBActions):
        self.root = root
        self.DBActions = DBActions
        self.root.title("PlusBus")
        self.root.geometry("800x600")
        # self.root.resizable(False, False)

        # create a notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=ui.BOTH, expand=True)

        # create tabs
        self.create_customer_tab()
        self.create_bus_tab()
        self.create_travel_tab()

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
        self.customer_load_button = ui.Button(self.customer_button_frame, text="Search Customers", command=self.search_customers)
        self.customer_load_button.pack(side=ui.LEFT)

        self.load_customers()

    def load_customers(self):
        # Get all customers from the database
        customers = self.DBActions.get_customers()

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
        pass

    def edit_customer(self):
        pass

    def delete_customer(self):
        pass

    def search_customers(self):
        pass

    def create_bus_tab(self):
        # create a frame for the tab
        self.bus_tab = ui.Frame(self.notebook)
        self.notebook.add(self.bus_tab, text="Buses")

        # create a treeview
        self.bus_tree = ttk.Treeview(self.bus_tab, columns=("name", "seats", "is_accessible"))
        self.bus_tree.heading("#0", text="ID")
        self.bus_tree.heading("name", text="Name")
        self.bus_tree.heading("seats", text="Seats")
        self.bus_tree.heading("is_accessible", text="Is Accessible")
        self.bus_tree.pack(fill=ui.BOTH, expand=True)

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
        self.bus_load_button = ui.Button(self.bus_button_frame, text="Search Buses", command=self.search_buses)
        self.bus_load_button.pack(side=ui.LEFT)

    def load_busses(self):
        # Get all customers from the database
        busses = self.DBActions.get_busses()

        # Clear the treeview
        self.bus_tree.delete(*self.bus_tree.get_children())

        # iterate over the customers
        for bus in busses:
            # Sort the data into a tuple, in the same order as the columns.
            data = (bus.id, bus.bus_name, bus.price, bus.capacity)

            # Insert the data into the treeview
            self.bus_tree.insert("", "end", text=bus.id, values=data)

    def add_bus(self):
        pass

    def edit_bus(self):
        pass

    def delete_bus(self):
        pass

    def search_buses(self):
        pass

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
        self.travel_load_button = ui.Button(self.travel_button_frame, text="Search Travel Arrangements", command=self.search_travel_arrangements)
        self.travel_load_button.pack(side=ui.LEFT)

    def add_travel_arrangement(self):
        pass

    def edit_travel_arrangement(self):
        pass

    def delete_travel_arrangement(self):
        pass

    def search_travel_arrangements(self):
        pass

