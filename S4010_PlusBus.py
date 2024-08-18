#   road map for the PlusBus project, a notation and overview of the project.
#
#   create costumer table
#   create travel_arrangements table
#   - added bus table
#   create linking system between costumer tables to their travel_arrangements tables
#   create travel_arrangements overview for users (GUI)
#   SIDE NOTE - create travel_arrangements overview for staff / admins (GUI) (optional/extra)

#   ran into limitations with the sqlite3 library, so I switched to the sqlalchemy library
#   used ChatGPT for help with the conversion of sqlite3 to sqlalchemy, so theres still loads to learn about sqlalchemy.


# NOTICE: THE GUI IS CREATED IN A SEPERATE FILE, S4010_PlusBus_GUI.py


# PROGRAM BASE LOGIC STARTS HERE

from S4010_PlusBus_Tables import Customer, TravelArrangements, Bus, Base
import tkinter as tk

from S4010_PlusBus_GUI import PlusBusGUI

from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect


# db action class
class DBActions:
    def __init__(self, db_file):
        self.engine = create_engine(f'sqlite:///{db_file}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def insert_customer(self, customer):
        self.session.add(customer)
        self.session.commit()

    def insert_travel_arrangements(self, travel_arrangement):
        self.session.add(travel_arrangement)
        self.session.commit()

    def insert_bus(self, bus):
        self.session.add(bus)
        self.session.commit()

    def get_customers(self, amount=0):
        if amount > 0:
            return self.session.query(Customer).limit(amount).all()
        else:
            return self.session.query(Customer).all()

    def get_travel_arrangements(self, amount=0):
        if amount > 0:
            return self.session.query(TravelArrangements).limit(amount).all()
        else:
            return self.session.query(TravelArrangements).all()

    def get_buses(self, amount=0):
        if amount > 0:
            return self.session.query(Bus).limit(amount).all()
        else:
            return self.session.query(Bus).all()

    def get_table(self, table_class, amount=0):
        if amount > 0:
            return self.session.query(table_class).limit(amount).all()
        else:
            return self.session.query(table_class).all()

    def update_customer(self, customer_id, **kwargs):
        self.session.query(Customer).filter(Customer.id == customer_id).update(kwargs)
        self.session.commit()

    def update_travel_arrangements(self, travel_arrangement_id, **kwargs):
        self.session.query(TravelArrangements).filter(TravelArrangements.id == travel_arrangement_id).update(kwargs)
        self.session.commit()

    def update_bus(self, bus_id, **kwargs):
        self.session.query(Bus).filter(Bus.id == bus_id).update(kwargs)
        self.session.commit()

    def delete_customer(self, customer_id):
        self.session.query(Customer).filter(Customer.id == customer_id).delete()
        self.session.commit()

    def delete_travel_arrangements(self, travel_arrangement_id):
        self.session.query(TravelArrangements).filter(TravelArrangements.id == travel_arrangement_id).delete()
        self.session.commit()

    def delete_bus(self, bus_id):
        self.session.query(Bus).filter(Bus.id == bus_id).delete()
        self.session.commit()

    def get_customer(self, customer_id):
        return self.session.query(Customer).filter(Customer.id == customer_id).first()

    def get_travel_arrangement(self, travel_arrangement_id):
        return self.session.query(TravelArrangements).filter(TravelArrangements.id == travel_arrangement_id).first()

    def get_bus(self, bus_id):
        return self.session.query(Bus).filter(Bus.id == bus_id).first()

    def search(self, table_class, search_string, specific_column=None):
        words = search_string.split()
        filters = []

        if specific_column:
            for word in words:
                filters.append(getattr(table_class, specific_column).ilike(f"%{word}%"))
        else:
            for word in words:
                word_filters = [getattr(table_class, col).ilike(f"%{word}%") for col in table_class.__table__.columns.keys()]
                filters.append(or_(*word_filters))

        return self.session.query(table_class).filter(and_(True, *filters)).all()

    @staticmethod
    def convert_to_tuple(obj):
        mapper = inspect(obj.__class__)
        return tuple(getattr(obj, column.key) for column in mapper.attrs)

    def close(self):
        self.session.close()


# Create test data
def create_test_data():
    customers = [
        Customer(id=9237864, first_name="John", last_name="Doe", address="Elm Street 1", age=42, phone="12345678", email="John@Doe.com", guest_quantity=16),
        Customer(id=6548973, first_name="Jane", last_name="Doe", address="Elm Street 2", age=39, phone="87654321", email="Jane@Doe.com", guest_quantity=12)
    ]

    travel_arrangements = [
        TravelArrangements(id=2348977, customer_id=9237864, bus_id=46351, guest_quantity=16, total_price=10200, transit_date="2022-11-22", transit_time="21:00", transit_from="Copenhagen", transit_to="Aalborg"),
        TravelArrangements(id=2234897, customer_id=9237864, bus_id=57892, guest_quantity=12, total_price=8000, transit_date="2022-9-14", transit_time="9:00", transit_from="Svenstrup", transit_to="Aalborg"),
        TravelArrangements(id=3456763, customer_id=6548973, bus_id=32414, guest_quantity=14, total_price=5600, transit_date="2022-12-24", transit_time="19:00", transit_from="Vestbjerg", transit_to="Aalborg")
    ]

    buses = [
        Bus(id=46351, bus_name="Bus 1", price=0.5, capacity=50, is_accessible=True),
        Bus(id=57892, bus_name="Bus 22", price=0.6, capacity=60, is_accessible=False),
        Bus(id=32414, bus_name="Bus 3", price=0.4, capacity=40, is_accessible=True)
    ]

    return customers, travel_arrangements, buses

def test(db):
    customers, travel_arrangements, buses = create_test_data()

    if not db.get_customers() and not db.get_travel_arrangements() and not db.get_buses():
        for customer in customers:
            db.insert_customer(customer)

        for travel_arrangement in travel_arrangements:
            db.insert_travel_arrangements(travel_arrangement)

        for bus in buses:
            db.insert_bus(bus)

    db.update_bus(buses[1].id, is_accessible=buses[1].is_accessible)  # update bus 22

    print("Customers:")
    for customer in db.get_customers():
        print(customer)

    print("\nTravel Arrangements:")
    for arrangement in db.get_travel_arrangements():
        print(arrangement)

    print("\nBuses:")
    for bus in db.get_buses():
        print(bus)

    # SEARCH TEST ###############
    seach_customers = db.search(TravelArrangements, "9237864")  # search for customers with the last name "doe"

    if seach_customers:
        print("\nSearch Customers:")
        for customer in seach_customers:
            print(customer)
    else:
        print("No customers found")
    # SEARCH TEST ###############

    db.close()


ADMIN = True  # creating this ui first then a user ui

def main():
    db_file = "S4010_PlusBus_database.db"
    db = DBActions(db_file)

    test(db)

    root = tk.Tk()
    PlusBusGUI(root, db).root.mainloop()


if __name__ == "__main__":
    main()
