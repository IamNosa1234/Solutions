# This file contains the classes for the tables in the PlusBus database.
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# bus class with their prices/km and capacity
class Bus(Base):
    __tablename__ = 'buses'

    id = Column(Integer, primary_key=True)
    bus_name = Column(String)
    price = Column(Float)  # price per km
    capacity = Column(Integer)
    is_accessible = Column(Boolean)  # is the bus accessible for disabled people?

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
    phone = Column(String)
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
                f"{self.guest_quantity}, {[(arrangement.id, arrangement.transit_date, arrangement.transit_time) for arrangement in self.travel_arrangements]})")

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

    def __repr__(self):
        return (f"TravelArrangements(id={self.id}, customer_id={self.customer_id}, bus_id={self.bus_id}, "
                f"guest_quantity={self.guest_quantity}, total_price={self.total_price})")
    