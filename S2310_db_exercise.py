"""
Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Anvend det, du har lært i dette kapitel om databaser, på en første opgave.

Trin 1:
Opret en ny SQLite database "S2311_my_second_sql_database.db" i din solutions mappe.
Denne database skal indeholde 2 tabeller.
Den første tabel skal hedde "customers" og repræsenteres i Python-koden af en klasse kaldet "Customer".
Tabellen bruger sin første attribut "id" som primærnøgle.
De andre attributter i tabellen hedder "name", "address" og "age".
Definer selv fornuftige datatyper for attributterne.

Trin 2:
Den anden tabel skal hedde "products" og repræsenteres i Python-koden af en klasse kaldet "Product".
Denne tabel bruger også sin første attribut "id" som primærnøgle.
De andre attributter i tabellen hedder "product_name", "price" og "brand".

Trin 3:
Skriv en funktion create_test_data(), der opretter testdata for begge tabeller.

Trin 4:
Skriv en metode __repr__() for begge dataklasser, så du kan vise poster til testformål med print().

Til læsning fra databasen kan du genbruge de to funktioner select_all() og get_record() fra S2240_db_class_methods.py.

Trin 5:
Skriv hovedprogrammet: Det skriver testdata til databasen, læser dataene fra databasen med select_all() og/eller get_record() og udskriver posterne til konsollen med print().

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Teams-besked til din lærer: <filename> færdig
Fortsæt derefter med den næste fil.
"""

import sqlite3
import os

class Customer:
    def __init__(self, id, name, address, age):
        self.id = id
        self.name = name
        self.address = address
        self.age = age

    def __repr__(self):
        return f"Customer({self.id}, {self.name}, {self.address}, {self.age})"

class Product:
    def __init__(self, id, product_name, price, brand):
        self.id = id
        self.product_name = product_name
        self.price = price
        self.brand = brand

    def __repr__(self):
        return f"Product({self.id}, {self.product_name}, {self.price}, {self.brand})"

def create_test_data():
    customers = [
        Customer(1, "John Doe", "Elm Street 1", 42),
        Customer(2, "Jane Doe", "Elm Street 2", 39),
        Customer(3, "Alice", "Elm Street 3", 23)
    ]

    products = [
        Product(1, "Toothpaste", 10.00, "Colgate"),
        Product(2, "Toothbrush", 5.00, "Jordan"),
        Product(3, "Floss", 20.00, "Oral-B")
    ]

    return customers, products

def table_exists(cursor, table_name):
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    return cursor.fetchone() is not None

def test():
    db_file = "S2311_my_second_sql_database.db"
    db_exists = os.path.exists(db_file)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    if not db_exists or not table_exists(cursor, "customers") or not table_exists(cursor, "products"):
        # Create tables if they don't exist
        cursor.execute("CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, name TEXT, address TEXT, age INTEGER)")
        cursor.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, product_name TEXT, price REAL, brand TEXT)")

        customers, products = create_test_data()

        # Insert data into the tables
        for customer in customers:
            cursor.execute("INSERT INTO customers VALUES (?, ?, ?, ?)", (customer.id, customer.name, customer.address, customer.age))

        for product in products:
            cursor.execute("INSERT INTO products VALUES (?, ?, ?, ?)", (product.id, product.product_name, product.price, product.brand))

        conn.commit()

    # Fetch and display customers
    cursor.execute("SELECT * FROM customers")
    print("Customers:")
    for row in cursor.fetchall():
        print(Customer(*row))

    # Fetch and display products
    cursor.execute("SELECT * FROM products")
    print("\nProducts:")
    for row in cursor.fetchall():
        print(Product(*row))

    conn.close()


if __name__ == "__main__":
    test()
