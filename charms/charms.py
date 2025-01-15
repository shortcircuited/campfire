import random
import pandas
import sqlite3
import sys
import character, history

class species:
    def __init__(self, race):
        if race in ['human','elf','dwarf','halfling','gnome','half-orc','tiefling','dragonborn','tabaxi']:
            self.race = race
        else: 
            randrace = random.randrange(1,1000)
            if randrace <= 750:         # 75.0% chance of human
                race = 'human'  
            elif randrace <= 810:       # 6.0% chance of elf
                race = 'elf'    
            elif randrace <= 860:       # 5.0% chance of dwarf
                race = 'dwarf'  
            elif randrace <= 890:       # 3.0% chance of halfling
                race = 'halfling'   
            elif randrace <= 910:       # 2.0% chance of gnome
                race = 'gnome'  
            elif randrace <= 925:       # 1.5% chance of half-orc
                race = 'half-orc'   
            elif randrace <= 940:       # 1.5% chance of tiefling
                race = 'tiefling'   
            elif randrace <= 955:       # 1.5% chance of dragonborn
                race = 'dragonborn' 
            elif randrace <= 965:       # 1.0% chance of tabaxi
                race = 'tabaxi'
            elif randrace <= 975:       # 1.0% chance of kobold
                race = 'kobold'
            elif randrace <= 985:       # 1.0% chance of goblin
                race = 'goblin'
            elif randrace <= 990:       # 0.5% chance of aarakocra
                race = 'aarakocra'
            elif randrace <= 995:       # 0.5% chance of orc
                race = 'orc'
            elif randrace <= 998:       # 0.3% chance of bugbear
                race = 'bugbear'
            else: 
                race = 'human'

class charms:
    def __init__(self,gender,age):
        self.gender = self.pronouns(gender)
        self.age = self.define_age(age)
        self.character = character.character('all', self.gender)
        print(f'{self.character.physical} {self.character.personality}')
        self.history = history.history('all', self.age)
        print(self.age)
        print(f'Early Life:\n{self.history.early_life}\n\nKey Events:\n{self.history.key_events}\nRecent Event:\n{self.history.recent_event}')
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
    def define_age(self, age):
            if age == '0':
                randage = random.randrange(1,100)
                if randage <= 5:
                    return('child')
                elif randage <= 19:
                    return('young')
                elif randage <= 56:
                    return('young adult')
                elif randage <= 86:
                    return('adult')
                elif randage <= 99:
                    return('elder')
                elif randage == 100:
                    return('ancient')


if __name__ == "__main__":
    name = str(sys.argv[1])
    seed = int(sys.argv[2])
    gender  = str(sys.argv[3])
    race = str(sys.argv[4])
    job  = str(sys.argv[5])
    age  = str(sys.argv[6])
    if seed == 0:
        seed = str(random.randrange(sys.maxsize))
    random.seed(seed)
    result = charms(gender,age)
