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


# I was gonna try to import my old charater class, but decided to have a seperate version.
class Character:
    def __init__(self, name: str, max_health: int, attackpower: int):
        self.name = name
        self.max_health = max_health
        self._current_health = max_health
        self.attackpower = attackpower
        self.is_dead = False

    def __repr__(self):
        return f"{self.name} (Health: {self._current_health}/{self.max_health}, Attack Power: {self.attackpower})"

    def hit(self, target) -> str:
        if not isinstance(target, Character):
            raise TypeError("Target must be an instance of Character")

        # check if attacker is dead
        elif self.is_dead:
            return f"{self.name} cannot hit {target.name} because {self.name} is dead"

        # else hit target
        else:
            return target.get_hit(self.attackpower)

    def get_hit(self, damage) -> str:
        # return early if Character the is dead
        if self.is_dead:
            return f"{self.name} has already fallen"
        # else deal damage
        else:
            self._current_health -= damage

        self.is_dead = self._current_health < 1

        # return either Character is dead, or damage taken.
        return f"{self.name} has felled" if self._current_health < 1 else f"{self.name} took {damage} damage"

    def get_healed(self, healpower) -> str:

        # target is full hp ( hit points ) so return early
        if self._current_health >= self.max_health:
            return f"{self.name} is already at full hp"

        # target is dead so return early
        elif self.is_dead:
            return f"{self.name} cannot be healed because they're dead"

        # finally heal target
        else:
            amount_to_heal = healpower if self._current_health + healpower <= self.max_health else self.max_health - self._current_health
            self._current_health += amount_to_heal
            return f"{self.name} was healed by {amount_to_heal} hp"
            # conditions can both be chacked in hit() and get_hit(), i think it looks better and more readable this way..


class Healer(Character):
    def __init__(self, name: str, max_health: int, healpower: int):
        super().__init__(name, max_health, attackpower=0)
        self.healpower = healpower

    def heal(self, target) -> str:
        if not isinstance(target, Character):
            raise TypeError(f"target must be of type Character, not {type(target)}")

        # if dead return
        if self.is_dead:
            return f"{self.name} cannot heal {target.name} because they're dead"
        else:  # else heal target
            delta = 5
            # added rng to heal power ( heal power +- delta )
            return target.get_healed(random.randint(self.healpower-delta, self.healpower+delta))

    def __repr__(self) -> str:
        return f"{self.name} (Health: {self._current_health}/{self.max_health}, Heal Power: {self.healpower})"


class Uchiha(Character):
    def __init__(self, name: str, max_health: int, attackpower: int, tomoe: int = 0, mangekyo: bool = False):
        super().__init__(name, max_health, attackpower)
        # using max inside min was a Microsoft Copilot suggestion, simply asked "how to ensure a int value does not precede 0 or exceed 3.
        # in C#/C++ I use theree slashes "///" to create a summery to explain a method, couldn't find any equivalents in python ( the explanation shows when calling a method, along with the parametres. )
        self.tomoe = min(max(0, tomoe), 3) if not mangekyo else 3  # it's unheard of for someone to have a mangekyo and not have all three tomoe
        self.sharingan = bool(self.tomoe)  # A sharingan starts with one tomoe when unlocked
        self.mangekyo = mangekyo

    def genjutsu(self, target) -> str:
        # error handle target
        if not isinstance(target, Character):  # apparently this will return true even if its an instance of another class that inharits Character
            raise TypeError(f"target must be of type Character, not {type(target)}")

        # return if no tomoe/sharingan
        if self.tomoe <= 0:
            return f"{self.name} does not have a sharingan"

        # 25% chance of success per tomoe
        hit_chance = 0.25 * self.tomoe if not self.mangekyo else 1  # mangekyo brings the chance of success to 100 percent

        # enemy sharingan can resist genjutsu
        if isinstance(target, Uchiha):
            hit_chance -= 0.25 * target.tomoe if not target.mangekyo else 1  # mangekyo also brings resistance to 100 percent

        # using random for chance calculus was a ChatGPT suggestion

        # attempt genjutsu
        if random.random() < hit_chance and self.tomoe and not target.is_dead:
            dmg = round(self.attackpower * self.tomoe / random.uniform(1.6, 2.2))  # calculate genjutsu damage with a bit of random chance
            return "Genjutsu was successful and " + target.get_hit(damage=dmg)

        # failed to effect the mind
        elif self.tomoe and not target.is_dead:
            return f"{self.name} failed to trap {target.name} in a genjutsu"

        # can't use genjutsu without a sharingan
        elif not self.tomoe:
            return f"{self.name} has not yet unlocked their sharingan"

        # can't effect a dead mind
        else:
            return "genjutsu don't work against dead people"

    # get_hit() overload from the Character class, added exclusive dodge ability.
    def get_hit(self, damage: int) -> str:
        # the sharingan can be used to anticipate and evade
        chance_of_evasion = 0.20 * self.tomoe if not self.mangekyo else 0.85
        evaded = random.random() < chance_of_evasion  # store result as boolean, found out this is the same as using ( evaded = bool(random.random() < chance_of_evasion) ). nice a similar to C

        if self.is_dead:
            return f"{self.name} has already fallen"
        elif not evaded:  # modified, switched else for elif.
            self._current_health -= damage

        self.is_dead = self._current_health < 1

        # added check for 'evaded'
        if not evaded:
            return f"{self.name} has felled" if self._current_health < 1 else f"{self.name} took {damage} damage"
        else:
            return f"{self.name} dodged {damage} damage"

    def unlock_manegekyo(self) -> str:
        # whitnessing trauma unlike any other causes the awakening
        result = str
        if self.mangekyo:
            result = f"{self.name} has already unlocked their mangekyo"
        else:
            self.tomoe = 3
            self.mangekyo = True
            result = f"{self.name} has now unlocked their mangekyo"

        self.sharingan = bool(self.tomoe)

        return result

    def level_up_sharingan(self) -> str:
        result = str
        if self.tomoe < 3:
            self.tomoe += 1
            if self.tomoe == 1:
                result = f"{self.name} has now unlocked their"
            else:
                result = f"{self.name} now has a {self.tomoe} tomoe sharingan"
        else:
            result = f"{self.name} already has a 3 tomoe sharingan"

        self.sharingan = bool(self.tomoe)

        return result

class Jinchuriki(Character):  # "with the power of human sacrifice the one shall have God-Reaching power"
    def __init__(self):
        super().__init__()
        self.biju_is_dead = False

    def baryon_mode(self):  # in exchange for the biju's life a jinchuriki can gain unmatched strength and speed for 2-5 minutes, when the biju is dead all the benefits are relinquished.
        NotImplemented

    def biju_mode(self):  # covered in chackra this mode increases strength, health and speed.
        NotImplemented

    def beast_bomb(self):  # strong AOE attack
        NotImplemented


print("\nShippuden browl:")

# team7
naruto = Character("Naruto", 150, 45)
sasuke = Uchiha("Sasuke", 90, 30, mangekyo=True)  # mangekyo automatically sets tomoe to 3
sakura = Healer("Sakura", 100, 25)

# versus

# the ghost of the uchiha
madara = Uchiha("Madara", 340, 60, 3, True)


# battleground

sakura.hit(naruto)
sasuke.hit(naruto)
print(naruto)
sakura.heal(naruto)
naruto.hit(sasuke)
print(sasuke)
