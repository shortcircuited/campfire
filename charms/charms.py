import random
import pandas
import sqlite3
import sys
import character

class species:
    def __init__(self, race):
        if race in ['human','elf','dwarf','halfling','gnome','half-orc','tiefling','dragonborn','tabaxi']:
            self.race = race

class charms:
    def __init__(self, gender):
        self.gender = self.pronouns(gender)
        self.character = character.character('all', self.gender)
        print(f'{self.character.physical} {self.character.personality}')
    class pronouns():
        def __init__(self, gender):
            # checking pronouns
            if gender == '0':
                randgender = random.randrange(1,1000)
                if randgender <= 2:
                    gender = 'androgynous'
                elif randgender <= 501:
                    gender = 'female'
                else:
                    gender = 'male'
            if gender == 'male':
                self.subpronoun = 'he'
                self.objpronoun = 'him'
                self.pospronoun = 'his'
                self.identity = 'man'
                self.noun = 'man'
                self.verb = 'is'
            elif gender == 'female':
                self.subpronoun = 'she'
                self.objpronoun = 'her'
                self.pospronoun = 'hers'
                self.identity = 'woman'
                self.noun = 'woman'
                self.verb = 'is'
            else:
                self.subpronoun = 'they'
                self.objpronoun = 'them'
                self.pospronoun = 'theirs'
                self.identity = 'androgynous'
                self.noun = 'person'
                self.verb = 'are'



if __name__ == "__main__":
    name = str(sys.argv[1])
    seed = int(sys.argv[2])
    gender  = str(sys.argv[3])
    race = str(sys.argv[4])
    job  = str(sys.argv[5])
    age  = int(sys.argv[6])
    if seed == 0:
        seed = str(random.randrange(sys.maxsize))
    random.seed(seed)
    result = charms(gender)
