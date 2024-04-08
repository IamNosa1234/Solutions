"""
Opgave "Morris the Miner":

Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Udgangssituation:
Morris har egenskaberne sleepiness, thirst, hunger, whisky, gold.
Alle attributter har startværdien 0.

Regler:
Hvis sleepiness, thirst eller hunger kommer over 100, dør Morris.
Morris kan ikke opbevare mere end 10 flasker whisky.
Ingen attribut kan gå under 0.

Ved hver omgang kan Morris udføre præcis én af disse aktiviteter:
sleep:      sleepiness-=10, thirst+=1,  hunger+=1,  whisky+=0, gold+=0
mine:       sleepiness+=5,  thirst+=5,  hunger+=5,  whisky+=0, gold+=5
eat:        sleepiness+=5,  thirst-=5,  hunger-=20, whisky+=0, gold-=2
buy_whisky: sleepiness+=5,  thirst+=1,  hunger+=1,  whisky+=1, gold-=1
drink:      sleepiness+=5,  thirst-=15, hunger-=1,  whisky-=1, gold+=0

Din opgave:
Skriv et program, der giver Morris så meget guld som muligt på 1000 omgange.

Hvis du ikke har nogen idé om hvordan du skal begynde, så åbn S0185_morris_help.py og start derfra.
Hvis du går i stå, så spørg google, de andre elever eller læreren (i denne rækkefølge).

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Teams-meddelelse til din lærer: <filename> færdig
Fortsæt derefter med den næste fil.
"""

NUMBER_OF_ACTIONS = 1000


def check_stats(stats: dict):

    stats["numberOfActions"] += 1

    if stats["sleepiness"] >= 100 or stats["thirst"] >= 100 or stats["hunger"] >= 100:
        game_over(stats)
    return


"""activities"""


def sleep(stats: dict):
    if stats["sleepiness"] > 0:
        stats["sleepiness"] -= 10 if stats["sleepiness"] >= 10 else stats["sleepiness"]
        stats["thirst"] += 1
        stats["hunger"] += 1
        stats["whisky"] += 0
        stats["gold"] += 0
        check_stats(stats)
    else:
        message = "Not feeling sleepy right now."
        return message
    return None

def mine(stats: dict):
    stats["sleepiness"] += 5
    stats["thirst"] += 5
    stats["hunger"] += 5
    stats["whisky"] += 0
    stats["gold"] += 5
    check_stats(stats)
    return None


def eat(stats: dict):
    if stats["gold"] >= 2:
        stats["sleepiness"] += 5
        stats["thirst"] -= 5 if stats["thirst"] >= 5 else stats["thirst"]
        stats["hunger"] -= 20 if stats["hunger"] >= 20 else stats["hunger"]
        stats["whisky"] += 0
        stats["gold"] -= 2 if stats["gold"] >= 2 else stats["gold"]
        check_stats(stats)
    else:
        message = "Not enough gold."
        return message
    return None


def buy_whisky(stats: dict):
    if stats["gold"] < 1:
        message = "Not enough gold."
        return message
    if stats["whisky"] < 10:
        stats["sleepiness"] += 5
        stats["thirst"] += 1
        stats["hunger"] += 1
        stats["whisky"] += 1
        stats["gold"] -= 1 if stats["gold"] >= 1 else stats["gold"]
        check_stats(stats)
    else:
        message = "Pockets are full, seems they only fit 10 whisky."
        return message
    return None


def drink(stats: dict):
    if stats["whisky"] > 0:
        stats["sleepiness"] += 5
        stats["thirst"] -= 15 if stats["thirst"] >= 15 else stats["thirst"]
        stats["hunger"] -= 1 if stats["hunger"] >= 1 else stats["hunger"]
        stats["whisky"] -= 1 if stats["whisky"] >= 1 else stats["whisky"]
        stats["gold"] += 0
        check_stats(stats)
    else:
        message = "No whisky."
        return message
    return None


"""program"""

def clear():
    from os import system
    system('cls')


def game_over(stats: dict):
    print("GAME OVER!\nmorris died.")
    print(f"\nstats: sleepiness: {stats["sleepiness"]} - thirst: {stats["thirst"]} - hunger: {stats["hunger"]} - whisky: {stats["whisky"]} - gold: {stats["gold"]}\n")
    input("Press enter to exit")
    exit(0)


def game_won(stats: dict):
    print(f"GAME WON!\nmorris collected {stats["gold"]} gold.")
    print(f"\nstats: sleepiness: {stats["sleepiness"]} - thirst: {stats["thirst"]} - hunger: {stats["hunger"]} - whisky: {stats["whisky"]} - gold: {stats["gold"]}\n")
    input("Press enter to exit")
    exit(0)


def auto_play():
    stats = {"sleepiness": 0,
             "thirst": 0,
             "hunger": 0,
             "whisky": 0,
             "gold": 0,
             "numberOfActions": 0
             }

    while stats["numberOfActions"] <= NUMBER_OF_ACTIONS:
        mine(stats)
        if stats["sleepiness"] > 80:
            sleep(stats)
        if stats["hunger"] > 80:
            eat(stats)
        if stats["thirst"] > 80:
            buy_whisky(stats)
            drink(stats)

    game_won(stats)
    return


def manual_play():
    stats = {"sleepiness": 0,
             "thirst": 0,
             "hunger": 0,
             "whisky": 0,
             "gold": 0,
             "numberOfActions": 0
             }

    message = None

    while True:
        clear()

        if message is not None:
            print(f"\033[0;33m{message}\033[0m\n")

        _input = input("Goal: gain as much gold as possible in 1000 turns - sleepiness, thirst or hunger > 100 = game over\n\nactions:"
                       "\n1: sleep; -10 sleepiness - +1 thurst - +1 hunger."
                       "\n2: mine; +5 sleepiness - +5 thurst - +5 hunger - +5 gold"
                       "\n3: eat; +5 sleepiness - -5 thurst - +20 hunger - -2 gold"
                       "\n4: buy whisky; +5 sleepiness - +1 thurst - +1 hunger - +1 whisky - -1 gold"
                       "\n5: drink; +5 sleepiness - -15 thurst - -1 whisky"
                       f"\n\nActions left: {NUMBER_OF_ACTIONS - stats["numberOfActions"]}\nstats: sleepiness: {stats["sleepiness"]} - thirst: {stats["thirst"]} - hunger: {stats["hunger"]} - whisky: {stats["whisky"]} - gold: {stats["gold"]}\n")

        if _input == "1":
            message = sleep(stats)
        if _input == "2":
            message = mine(stats)
        if _input == "3":
            message = eat(stats)
        if _input == "4":
            message = buy_whisky(stats)
        if _input == "5":
            message = drink(stats)
        if stats["numberOfActions"] >= NUMBER_OF_ACTIONS:
            game_won(stats)


def main():
    user_choice = input("Use auto play? [Y] yes [N] no")
    if user_choice.lower() == "y":
        auto_play()
    elif user_choice.lower() == "n":
        manual_play()
    else:
        main()


main()
