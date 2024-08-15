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

import tkinter as tk

from S4010_PlusBus_GUI import PlusBusGUI

from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy.inspection import inspect

Base = declarative_base()

# bus class with their prices/km and capacity
class Bus(Base):
    __tablename__ = 'buses'

    id = Column(Integer, primary_key=True)
    bus_name = Column(String)
    price = Column(Float)  # price per km
    capacity = Column(Integer)

    def __repr__(self):
        return f"Bus({self.id}, {self.bus_name}, {self.price}, {self.capacity})"

# costumer with their first and last names, address, age, amount of people and travel_arrangements and
# the bus they are traveling with will be listed under their travel_arrangements
# added enterprise information
class Customer(Base):
    __tablename__ = 'customers'

    # organizer / customer information
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    age = Column(Integer)
    # organizer / customer contact
    phone = Column(String)  # danish tranvel agency, so I'm gonna exclude country codes
    email = Column(String)
    # enterprise information
    is_enterprise = Column(Boolean)  # does the customer represent an enterprise?
    enterprise_name = Column(String)
    # enterprise contact
    enterprise_phone = Column(String)  # danish tranvel agency, so I'm gonna exclude country codes
    enterprise_email = Column(String)
    guest_quantity = Column(Integer)  # wasdwwasdwasdwasdwasd

    travel_arrangements = relationship('TravelArrangements', back_populates='customer')  # list/tuple of travel_arrangements by travel_arrangements' id

    def __repr__(self):
        return (f"Customer({self.id}, {self.first_name}, {self.last_name}, {self.address}, {self.age}, "
                f"{self.guest_quantity}, {self.travel_arrangements})")

# travel_arrangements with the costumer id, the bus id, the amount of people and the total price
# added transit segment with the date, time, from and to
class TravelArrangements(Base):
    __tablename__ = 'travel_arrangements'

    # general
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    bus_id = Column(Integer, ForeignKey('buses.id'))
    guest_quantity = Column(Integer)
    total_price = Column(Float)
    # transit segment
    transit_date = Column(String)
    transit_time = Column(String)
    transit_from = Column(String)
    transit_to = Column(String)

    customer = relationship('Customer', back_populates='travel_arrangements')
    bus = relationship('Bus')

    def __repr__(self):
        return (f"TravelArrangements({self.id}, {self.customer_id}, {self.bus_id}, "
                f"{self.guest_quantity}, {self.total_price})")


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

    def get_travel_arrangements(self):
        return self.session.query(TravelArrangements).all()

    def get_buses(self):
        return self.session.query(Bus).all()

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

    def search_customers(self, **kwargs):
        return self.session.query(Customer).filter_by(**kwargs).all()

    def search_travel_arrangements(self, **kwargs):
        return self.session.query(TravelArrangements).filter_by(**kwargs).all()

    def search_buses(self, **kwargs):
        return self.session.query(Bus).filter_by(**kwargs).all()

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
        Bus(id=46351, bus_name="Bus 1", price=0.5, capacity=50),
        Bus(id=57892, bus_name="Bus 2", price=0.6, capacity=60),
        Bus(id=32414, bus_name="Bus 3", price=0.4, capacity=40)
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

    db.update_customer(9237864, first_name="mo", last_name="fo", address="Elm Street 111", age=42, phone="12345678")

    print("Customers:")
    for customer in db.get_customers():
        print(customer)

    print("\nTravel Arrangements:")
    for arrangement in db.get_travel_arrangements():
        print(arrangement)

    print("\nBuses:")
    for bus in db.get_buses():
        print(bus)

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
