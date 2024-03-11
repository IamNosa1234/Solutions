"""opgave: Objektorienteret rollespil, afsnit 2 :

Som altid skal du læse hele øvelsesbeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Byg videre på din løsning af afsnit 1.

Del 1:
    Opfind to nye klasser, som arver fra klassen Character. For eksempel Hunter og Magician.
    Dine nye klasser skal have deres egne ekstra metoder og/eller attributter.
    Måske overskriver de også metoder eller attributter fra klassen Character.

Del 2:
    Lad i hovedprogrammet objekter af dine nye klasser (dvs. rollespilfigurer) kæmpe mod hinanden,
    indtil den ene figur er død. Udskriv, hvad der sker under kampen.

I hver omgang bruger en figur en af sine evner (metoder). Derefter er det den anden figurs tur.
Det er op til dig, hvordan dit program i hver tur beslutter, hvilken evne der skal bruges.
Beslutningen kan f.eks. være baseret på tilfældighed eller på en smart strategi

Del 3:
    Hver gang en figur bruger en af sine evner, skal du tilføje noget tilfældighed til den anvendte evne.

Del 4:
    Lad dine figurer kæmpe mod hinanden 100 gange.
    Hold styr på resultaterne.
    Prøv at afbalancere dine figurers evner på en sådan måde, at hver figur vinder ca. halvdelen af kampene.

Hvis du går i stå, kan du spørge google, de andre elever eller læreren (i denne rækkefølge).

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Teams-besked til din lærer: <filename> done
Fortsæt derefter med den næste fil."""
import random


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
            return f"{self.name} is already at full hp"
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

    def __repr__(self):
        return f"{self.name} (Health: {self._current_health}/{self.max_health}, Heal Power: {self.healpower})"


class Uchiha(Character):
    def __init__(self, name: str, max_health: int, attackpower: int, tomoe: int = 0, mangekyo: bool = False):
        super().__init__(name, max_health, attackpower)
        self.tomoe = min(max(0, tomoe), 3) if not mangekyo else 3  # it's unheard of for someone to have a mangekyo and not have all three tomoe
        self.sharingan = bool(self.tomoe)  # A sharingan starts with one tomoe when unlocked
        self.mangekyo = mangekyo

    def genjutsu(self, target):
        # 25% chance of success per tomoe
        hit_chance = 0.25 * self.tomoe if not self.mangekyo else 1  # mangekyo brings the chance of success to 100 percent

        # enemy sharingan can resist genjutsu
        if isinstance(target, Uchiha):
            hit_chance -= 0.25 * target.tomoe if not target.mangekyo else 1  # mangekyo also brings resistance to 100 percent

        # using random for chance calculus was a ChatGPT suggestion
        if random.random() < hit_chance and self.tomoe and not target.is_dead:  # attempt genjutsu
            dmg = round(self.attackpower * self.tomoe / 1.6)  # calculate genjutsu effectiveness
            return "Genjutsu was successful and " + target.get_hit(damage=dmg)
        elif self.tomoe and not target.is_dead:  # failed to effect the mind
            return f"{self.name} failed to trap {target.name} in a genjutsu"
        elif not self.tomoe:  # can't use genjutsu without a sharingan
            return f"{self.name} has not yet unlocked their sharingan"
        else:  # can't effect a dead mind
            return "genjutsu don't work against dead people"

    def get_hit(self, damage) -> str:
        # the sharingan can be used to anticipate and evade
        chance_of_evasion = 0.20 * self.tomoe if not self.mangekyo else 0.85
        evaded = random.random() < chance_of_evasion  # store result as boolean

        if self.is_dead:
            return f"{self.name} has already fallen"
        elif not evaded:  # modified
            self._current_health -= damage

        self.is_dead = self._current_health < 1

        if not evaded:
            return f"{self.name} has felled" if self._current_health < 1 else f"{self.name} took {damage} damage"
        else:
            return f"{self.name} dodged {damage} damage"


print("\nShippuden browl:")

# team7
naruto = Character("Naruto", 150, 45)
sasuke = Uchiha("Sasuke", 90, 30, mangekyo=True)  # mangekyo automatically sets tomoe to 3
sakura = Healer("Sakura", 100, 15)

# vs ghost of the uchiha
madara = Uchiha("Madara", 340, 60, 3, True)

sakura.hit(naruto)
sasuke.hit(naruto)
print(naruto)
sakura.heal(naruto)
naruto.hit(sasuke)
print(sasuke)
