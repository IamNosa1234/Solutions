"""
Opgave "Animals"

Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Alt, hvad du har brug for at vide for at løse denne opgave, finder du i cars_oop-filerne.

Del 1:
    Definer en klasse ved navn Animal.
    Hvert objekt i denne klasse skal have attributterne name (str), sound (str), height (float),
    weight (float), legs (int), female (bool).
    I parentes står data typerne, dette attributterne typisk har.

Del 2:
    Tilføj til klassen meningsfulde metoder __init__ og __repr__.
    Kald disse metoder for at oprette objekter af klassen Animal og for at udskrive dem i hovedprogrammet.

Del 3:
    Skriv en klassemetode ved navn make_noise, som udskriver dyrets lyd i konsollen.
    Kald denne metode i hovedprogrammet.

Del 4:
    Definer en anden klasse Dog, som arver fra Animal.
    Hvert objekt af denne klasse skal have attributterne tail_length (int eller float)
    og hunts_sheep (typisk bool).

Del 5:
    Tilføj til klassen meningsfulde metoder __init__ og __repr__.
    Ved skrivning af konstruktoren for Dog skal du forsøge at genbruge kode fra klassen Animal.
    Kald disse metoder for at oprette objekter af klassen Hund og for at udskrive dem i hovedprogrammet.

Del 6:
    Kald metoden make_noise på Dog-objekter i hovedprogrammet.

Del 7:
    Skriv en klassemetode ved navn wag_tail for Dog.
    Denne metode udskriver i konsollen noget i stil med
    "Hunden Snoopy vifter med sin 32 cm lange hale"
    Kald denne metode i hovedprogrammet.

Del 8:#
    Skriv en funktion mate(mother, father). Begge parametre er af typen Dog.
    Denne funktion skal returnere et nyt objekt af typen Dog.
    I denne funktion skal du lave meningsfulde regler for den nye hunds attributter.
    Hvis du har lyst, brug random numbers så mate() producerer tilfældige hunde.
    Sørg for, at denne funktion kun accepterer hunde med det korrekte køn som argumenter.

Del 9:
    I hovedprogrammet kalder du denne metode og udskriver den nye hund.

Del 10:
    Gør det muligt at skrive puppy = daisy + brutus i stedet for puppy = mate(daisy, brutus)
    for at opnå den samme effekt.  Du bliver nok nødt til at google det først.

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Teams-meddelelse til din lærer: <filename> færdig
Fortsæt derefter med den næste fil."""

import random


class Animal:
    def __init__(self, name: str, sound: str, height: float, weight: float, legs: int, female: bool):
        self.name   = name
        self.sound  = sound
        self.height = height
        self.weight = weight
        self.legs   = legs
        self.female = female

    def __repr__(self):
        return f'{self.name=}\t- {self.sound=}\t- {self.height=}\t- {self.weight=}\t- {self.legs=}\t- {self.female=}'

    def make_noise(self):
        print(self.sound)

class Dog(Animal):
    def __init__(self, name: str, sound: str, height: float, weight: float, legs: int, female: bool, tail_length: float, hunts_sheep: bool):
        super().__init__(name, sound, height, weight, legs, female)
        self.tail_length = tail_length
        self.hunts_sheep = hunts_sheep

    def __repr__(self):
        return f'{self.name=}\t- {self.sound=}\t- {self.height=}\t- {self.weight=}\t- {self.tail_length=}\t- {self.legs=}\t- {self.female=}'

    def wag_tail(self):
        print(f'Hunden {self.name} vifter med sin {self.tail_length} cm lange hale')

    def __add__(self, other):
        if not isinstance(other, Dog):
            raise Exception('Can only mate dogs.')
        if self.female == other.female:
            raise ValueError('Cannot mate dogs of the same gender.')

        return Dog(
            f'{self.name}_{other.name}_pup',
            random.choice([self.sound, other.sound]),
            round(random.uniform(self.height, other.height), 2),
            round(random.uniform(self.weight, other.weight), 2),
            random.randint(self.legs, other.legs),
            random.choice([True, False]),
            round(random.uniform(self.tail_length, other.tail_length), 2),
            random.choice([True, False])
        )


def mate(mother: Dog, father: Dog) -> list[Dog]:
    if not mother.female:
        raise Exception("mother is not female")
    if father.female:
        raise Exception("father is not male")

    pups = []

    for c in range(random.randint(2, 10)):
        pups.append(Dog(f"pup{c}", "eew", random.randint(3, 6), random.randint(1, 3), 4,
                        random.choice([True, False]), random.randint(1, 3), random.choice([True, False])))

    return pups


tiger = Animal(name='Tiger', sound='rawr', height=12, weight=100, legs=1, female=False)

tiger.make_noise()

femaledog = Dog(name='Maddie', sound='wof', height=24, weight=12, legs=4, female=True, tail_length=8, hunts_sheep=False)

maledog = Dog(name='buster', sound='woof', height=33, weight=14, legs=4, female=False, tail_length=9, hunts_sheep=True)

femaledog.make_noise()

print(femaledog)

femaledog.wag_tail()

breed = mate(femaledog, maledog)

for i in breed:
    print(f"Breed: {i}")

puppy = maledog + femaledog

print(f'\nPuppy: {puppy}\n')

for i in range(random.randint(2, 10)):
    print(f"Puppies: {maledog + femaledog}")
