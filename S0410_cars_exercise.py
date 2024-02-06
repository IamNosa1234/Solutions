"""
Opgave "Cars":

Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Definer en funktion drive_car(), der udskriver en bils motorlyd (f.eks. "roooaar")

I hovedprogrammet:
    Definer variabler, som repræsenterer antallet af hjul og den maksimale hastighed for 2 forskellige biler
    Udskriv disse egenskaber for begge biler
    Kald derefter funktionen drive_car()

Hvis du ikke har nogen idé om, hvordan du skal begynde, kan du åbne S0420_cars_help.py og starte derfra.
Hvis du går i stå, kan du spørge google, de andre elever eller læreren (i denne rækkefølge).
Hvis du stadig er gået i stå, skal du åbne S0430_cars_solution.py og sammenligne den med din løsning.

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Team-besked til din lærer: <filename> færdig
Fortsæt derefter med den næste fil."""

""" før objektorientering
# for readability

def get_wheels(car):
    return car[0]

def get_top_speed(car):
    return car[1]

def drive_car():
    print("roooaar")
    return


car1 = [4, 365]
car2 = [6, 180]

print("wheels", get_wheels(car1))
print("top speed", get_top_speed(car2), "km/h")

drive_car()"""


# object orianted @540

class Vehicle:

    def __init__(self, wheels, topSpeed):
        self.wheels = wheels
        self.topSpeed = topSpeed

    def __repr__(self):
        return (f"\nwheels: {self.wheels}"
                f"\ntop speed: {self.topSpeed} km/h")

    def drive(self):
        print("roooaar")

class ElectricVehicle(Vehicle):
    def __init__(self, wheels, topSpeed, batteryCapacity):
        super().__init__(wheels, topSpeed)
        self.batteryCapacity = batteryCapacity

    def __repr__(self):
        return (f"\nElectricVehicle: wheels: {self.wheels}"
                f"\ntop speed: {self.topSpeed} km/h"
                f"\nbattery capacity: {self.batteryCapacity}")

    def drive(self):
        print("ssSSSSssss")


vehicles = [
    Vehicle(4, 365),
    Vehicle(6, 180),
    ElectricVehicle(4, 240, 1250),
    ]

for vehicle in vehicles:
    print(vehicle)
    vehicle.drive()