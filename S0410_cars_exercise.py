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


class Vehicle:

    def drive(self):
        print("roooaar")

    def get_wheels(self, car):
        return car[0]

    def get_top_speed(self, car):
        return car[1]


car1 = Vehicle()
car1.wheels = 4
car1.topSpeed = 365

car2 = Vehicle()
car2.wheels = 6
car2.topSpeed = 180

vehicles = [car1, car2]

for vehicle in vehicles:
    print("wheels", vehicle.wheels, "top speed", vehicle.topSpeed)
    vehicle.drive()