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

"""stats"""
sleepiness = 0
thirst = 0
hunger = 0
whisky = 0
gold = 0

def check_stats():
    global sleepiness, thirst, hunger, whisky, gold
    if sleepiness < 0:
        sleepiness = 0
    if thirst < 0:
        thirst = 0
    if hunger < 0:
        hunger = 0
    if whisky < 0:
        whisky = 0
    if whisky > 10:
        whisky = 10
    if gold < 0:
        gold = 0

    if sleepiness > 100 or thirst > 100 or hunger > 100:
        game_over()
    return


"""activities"""

def sleep():
    global sleepiness, thirst, hunger, whisky, gold
    sleepiness -= 10; thirst += 1; hunger += 1; whisky += 0; gold += 0
    check_stats()
    return

def mine():
    global sleepiness, thirst, hunger, whisky, gold
    sleepiness += 5; thirst += 5; hunger += 5; whisky += 0; gold += 5
    check_stats()
    return

def eat():
    global sleepiness, thirst, hunger, whisky, gold
    sleepiness += 5; thirst -= 5; hunger -= 20; whisky += 0; gold -= 2
    check_stats()
    return

def buy_whisky():
    global sleepiness, thirst, hunger, whisky, gold
    sleepiness += 5; thirst += 1; hunger += 1; whisky += 1; gold -= 1
    check_stats()
    return

def drink():
    global sleepiness, thirst, hunger, whisky, gold
    sleepiness += 5; thirst -= 15; hunger -= 1; whisky -= 1; gold += 0
    check_stats()
    return


"""program"""

def game_over():
    print("GAME OVER!\nmorris died.")
    exit(0)
    return

def game_won():
    print("GAME WON!\nmorris collected all the gold.")
    exit(0)
    return

