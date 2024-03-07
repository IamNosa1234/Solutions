"""Opgave: Objektorienteret rollespil, afsnit 1 :

Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Del 1:
    Definer en klasse "Character" med attributterne "name", "max_health", "_current_health", "attackpower".
    _current_health skal være en protected attribut, det er ikke meningen at den skal kunne ændres udefra i klassen.

Del 2:
    Tilføj en konstruktor (__init__), der accepterer klassens attributter som parametre.

Del 3:
    Tilføj en metode til udskrivning af klasseobjekter (__repr__).

Del 4:
    Tilføj en metode "hit", som reducerer _current_health af en anden karakter med attackpower.
    Eksempel: _current_health=80 og attackpower=10: et hit reducerer _current_health til 70.
    Metoden hit må ikke ændre den private attribut _current_health i en (potentielt) fremmed klasse.
    Definer derfor en anden metode get_hit, som reducerer _current_health for det objekt, som den tilhører, med attackpower.

Del 5:
    Tilføj en klasse "Healer", som arver fra klassen Character.
    En healer har attackpower=0 men den har en ekstra attribut "healpower".

Del 6:
    Tilføj en metode "heal" til "Healer", som fungerer som "hit" men forbedrer sundheden med healpower.
    For at undgå at "heal" forandrer den protected attribut "_current_health" direkte,
    tilføj en metode get_healed til klassen Character, som fungerer lige som get_hit.

Hvis du er gået i stå, kan du spørge google, de andre elever eller læreren (i denne rækkefølge).
Hvis du ikke aner, hvordan du skal begynde, kan du åbne S0720_rpg1_help.py og starte derfra.

Når dit program er færdigt, skal du skubbe det til dit github-repository
og sammenlign det med lærerens løsning i S0730_rpg1_solution.py

Send derefter denne Teams-besked til din lærer: <filename> færdig
Fortsæt derefter med den næste fil."""


class Character:
    def __init__(self, name: str, max_health: int, attackpower: int):
        self.name = name
        self.max_health = max_health
        self._current_health = max_health
        self.attackpower = attackpower
        self.is_dead = False

    def __repr__(self):
        return f"{self.name} (Health: {self._current_health}/{self.max_health}, Attack Power: {self.attackpower})"

    def hit(self, target):
        if not isinstance(target, Character):
            raise TypeError("Target must be an instance of Character")
        elif self.is_dead:
            return f"{self.name} cannot hit {target.name} because {self.name} is dead"
        else:
            return target.get_hit(self.attackpower)

    def get_hit(self, damage) -> str:
        if self.is_dead:
            return f"{self.name} has already fallen"
        else:
            self._current_health -= damage

        self.is_dead = self._current_health < 1

        return f"{self.name} has felled" if self._current_health < 1 else f"{self.name} took {damage} damage"

    def get_healed(self, healpower) -> str:
        if self._current_health >= self.max_health:
            return f"{self.name}: is already at full hp"
        elif self.is_dead:
            return f"{self.name} cannot be healed because they're dead"
        else:
            amount_to_heal = healpower if self._current_health + healpower <= self.max_health else self.max_health - self._current_health
            self._current_health += amount_to_heal
            return f"{self.name} was healed by {amount_to_heal} hp"


class Healer(Character):
    def __init__(self, name: str, max_health: int, healpower: int):
        super().__init__(name, max_health, attackpower=0)
        self.healpower = healpower

    def heal(self, target):
        if self.is_dead:
            return f"{self.name} cannot heal {target.name} because they're dead"
        return target.get_healed(self.healpower)


print("\nShippuden browl:")
naruto = Character("Naruto", 150, 45)
sasuke = Character("Sasuke", 90, 30)
sakura = Healer("Sakura", 100, 15)

sakura.hit(naruto)
sasuke.hit(naruto)
print(naruto)
sakura.heal(naruto)
naruto.hit(sasuke)
print(sasuke)
