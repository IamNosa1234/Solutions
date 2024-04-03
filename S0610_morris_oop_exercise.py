"""
Opgave "Morris The Miner" (denne gang objekt orienteret)

Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Omskriv din oprindelige Morris-kode til en objektorienteret version.

Definer en klasse Miner med attributter som sleepiness, thirst osv.
og metoder som sleep, drink osv.
Opret Morris og initialiser hans attributter ved at kalde konstruktoren for Miner:
morris = Miner()

Hvis du går i stå, så spørg google, de andre elever eller læreren (i denne rækkefølge).

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Teams-meddelelse til din lærer: <filename> færdig
Fortsæt derefter med den næste fil."""

import os
import re
import time

PLAYER_TURNS = 1000

class Actions:
    def __init__(self):
        self.count = 0

        self.sleepiness = self.thirst = self.hunger = self.whisky = self.gold = 0

    def sleep(self):
        if self.sleepiness > 0:
            self.sleepiness -= 10 if self.sleepiness >= 10 else self.sleepiness; self.thirst += 1; self.hunger += 1; self.whisky += 0; self.gold += 0; self.count += 1
        else:
            print("\033[31mNot feeling sleepy right now.\033[0m")
            time.sleep(2)

    def mine(self):
        self.sleepiness += 5; self.thirst += 5; self.hunger += 5; self.whisky += 0; self.gold += 5; self.count += 1

    def eat(self):
        if self.hunger > 0 and self.gold >= 2:
            self.sleepiness += 5; self.thirst -= 5 if self.thirst >= 5 else self.thirst; self.hunger -= 20 if self.hunger >= 20 else self.hunger; self.whisky += 0; self.gold -= 2; self.count += 1
        elif not self.gold >= 2:
            print("\033[31mNot enough gold.\033[0m")
            time.sleep(2)
        else:
            print("\033[31mNot feeling hungry.\033[0m")
            time.sleep(2)

    def buy_whisky(self):
        if self.gold > 0 and self.whisky < 10:
            self.sleepiness += 5; self.thirst += 1; self.hunger += 1; self.whisky += 1; self.gold -= 1; self.count += 1
        elif not self.gold > 0:
            print("\033[31mNot enough gold.\033[0m")
            time.sleep(2)
        else:
            print("\033[31mPockets are full, seems they only fit 10 whisky.\033[0m")
            time.sleep(2)

    def drink(self):
        if self.whisky > 0 and self.thirst > 0:
            self.sleepiness += 5; self.thirst -= 15 if self.thirst >= 15 else self.thirst; self.hunger -= 1 if self.hunger >= 1 else self.hunger; self.whisky -= 1; self.gold += 0; self.count += 1
        elif not self.whisky > 0:
            print("\033[31mNo whisky.\033[0m")
            time.sleep(2)
        elif not self.thirst > 0:
            print("\033[31mNot thirsty.\033[0m")
            time.sleep(2)


class Player(Actions):
    def __init__(self):
        super().__init__()
        self.name = "Morris"

    def sleep_string(self):
        return (f"\033[31m{self.sleepiness}\033[0m"
                if self.sleepiness >= 80
                else f"\033[32m{self.sleepiness}\033[0m"
                if self.sleepiness <= 20
                else f"{self.sleepiness}")

    def thirst_string(self):
        return (f"\033[31m{self.thirst}\033[0m"
                if self.thirst >= 80
                else f"\033[32m{self.thirst}\033[0m"
                if self.thirst <= 20
                else f"{self.thirst}")

    def hunger_string(self):
        return (f"\033[31m{self.hunger}\033[0m"
                if self.hunger >= 80
                else f"\033[32m{self.hunger}\033[0m"
                if self.hunger <= 20
                else f"{self.hunger}")

    def whisky_string(self):
        return (f"\033[31m{self.whisky}\033[0m"
                if self.whisky == 0
                else f"{self.whisky}")

    def __repr__(self):
        return (f"sleepiness: {self.sleep_string()}, "
                f"thirst: {self.thirst_string()}, "
                f"hunger: {self.hunger_string()}, "
                f"whisky: {self.whisky_string()}, "
                f"gold: {self.gold}")

    def _game_over(self, player, reason: str = None, died: bool = False):
        os.system('cls')

        if died:
            print(f"{self.name} died because {reason} reached 100 or more\n")
        else:
            print("Game over! You've reached 1000 moves.\n"
                  f"Your score is {self.gold}!")

        _input = input("Would you like to try again? [Y] Yes [N] No\n")
        if _input.lower() == 'y':
            main(True, player.name)
        elif _input.lower() == 'n':
            main()
        else:
            self._game_over(player, reason, died)

    def check_stats(self, player, auto_mode: bool = False) -> bool:
        # if game is over return true and call _game_over()
        if self.count >= PLAYER_TURNS and not auto_mode:
            self._game_over(player)
            return True
        elif self.count > PLAYER_TURNS and auto_mode:
            os.system('cls')
            print(f"Morris reached {self.gold}!")
            input("Press enter key to continue...")
            main()
            return True

        if self.sleepiness > 99:
            self._game_over(player, "sleepiness", True)
        if self.thirst > 99:
            self._game_over(player, "thirst", True)
        if self.hunger > 99:
            self._game_over(player, "hunger", True)

        return False


def play_morris(player: Player):  # Auto Play
    while not player.count > PLAYER_TURNS:  # not player.check_stats(player)
        if player.sleepiness > 80: player.sleep()
        if player.hunger > 80: player.eat()
        if player.thirst > 80: player.buy_whisky(); player.drink()
        player.mine()
        player.check_stats(player, True)

def play(player: Player) -> None:
    while not player.check_stats(player):
        os.system('cls')
        _input = input(f"Hello {player.name}, your goal is simple. Gain as much gold as possible in a thousand moves!\n\n"
                       f"Moves left: {PLAYER_TURNS - player.count}\n\n"
                       f"{player}\n\n"
                       "[1] sleep:      sleepiness \033[32m-10\033[0m, thirst \033[31m+1\033[0m,  hunger \033[31m+1\033[0m\n"
                       "[2] mine:       sleepiness \033[31m+5\033[0m,  thirst \033[31m+5\033[0m,  hunger \033[31m+5\033[0m, gold \033[32m+5\033[0m\n"
                       "[3] eat:        sleepiness \033[31m+5\033[0m,  thirst \033[32m-5\033[0m,  hunger \033[32m-20\033[0m, gold \033[31m-2\033[0m\n"
                       "[4] buy_whisky: sleepiness \033[31m+5\033[0m,  thirst \033[31m+1\033[0m,  hunger \033[31m+1\033[0m,  whisky \033[32m+1\033[0m, gold \033[31m-1\033[0m\n"
                       "[5] drink:      sleepiness \033[31m+5\033[0m,  thirst \033[32m-15\033[0m, hunger \033[31m-1\033[0m,  whisky \033[31m-1\033[0m\n")

        if _input == "1": player.sleep()
        if _input == "2": player.mine()
        if _input == "3": player.eat()
        if _input == "4": player.buy_whisky()
        if _input == "5": player.drink()
        if _input == "menu": main()


def main(replay: bool = False, name: str = "Morris") -> None:
    os.system('cls')

    player = Player()

    if not replay:
        input_ = input("Would you like to play? [Y] Yes [N] no (auto play)\n")

        if input_.lower() == 'y':
            os.system('cls')
            _input = input("What's your name?\n")
            player.name = _input if re.match("^[a-zA-Z0-9_-]{3,15}$", _input) else name
            play(player)
        elif input_.lower() == 'n':
            play_morris(player)
        else:
            main(replay, name)
    else:
        player.name = name
        play(player)


main()
