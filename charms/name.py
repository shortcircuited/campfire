import random
import pandas
import sqlite3
import sys
import os

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
conn = sqlite3.connect(f"{os.path.dirname(__file__)}\\CHARMS.db")

class pronouns:
    def __init__(self, gender):
        # checking pronouns
        if gender == 'male':
            self.subpronoun = 'he'
            self.objpronoun = 'him'
            self.pospronoun = 'his'
            self.sex = 'male'
            self.identity = 'man'
            self.noun = 'man'
            self.verb = 'is'
        elif gender == 'female':
            self.subpronoun = 'she'
            self.objpronoun = 'her'
            self.pospronoun = 'hers'
            self.sex = 'female'
            self.identity = 'woman'
            self.noun = 'woman'
            self.verb = 'is'
        else:
            self.subpronoun = 'they'
            self.objpronoun = 'them'
            self.pospronoun = 'theirs'
            self.sex = 'androgynous'
            self.identity = 'androgynous'
            self.noun = 'person'
            self.verb = 'are'
            

class species:
    def __init__(self, race):
        if race in ['human','elf','dwarf','halfling','gnome','half-orc','tiefling','dragonborn','tabaxi']:
            self.race = race
        else: 
            randrace = random.randrange(1,1000)
            if randrace <= 750:         # 75.0% chance of human
                self.race = 'human'  
            elif randrace <= 810:       # 6.0% chance of elf
                self.race = 'elf'    
            elif randrace <= 860:       # 5.0% chance of dwarf
                self.race = 'dwarf'  
            elif randrace <= 890:       # 3.0% chance of halfling
                self.race = 'halfling'   
            elif randrace <= 910:       # 2.0% chance of gnome
                self.race = 'gnome'  
            elif randrace <= 925:       # 1.5% chance of half-orc
                self.race = 'half-orc'   
            elif randrace <= 940:       # 1.5% chance of tiefling
                self.race = 'tiefling'   
            elif randrace <= 955:       # 1.5% chance of dragonborn
                self.race = 'dragonborn' 
            elif randrace <= 965:       # 1.0% chance of tabaxi
                self.race = 'tabaxi'
            elif randrace <= 975:       # 1.0% chance of kobold
                self.race = 'kobold'
            elif randrace <= 985:       # 1.0% chance of goblin
                self.race = 'goblin'
            elif randrace <= 990:       # 0.5% chance of aarakocra
                self.race = 'aarakocra'
            elif randrace <= 995:       # 0.5% chance of orc
                self.race = 'orc'
            elif randrace <= 998:       # 0.3% chance of bugbear
                self.race = 'bugbear'
            else: 
                self.race = 'human'

class define_name:
    def __init__(self, race, gender):
        if race != 'Half-Elf' and race != 'Half-Orc':
            name_table = pandas.read_sql_query(f"SELECT * from {race}", conn)
        elif race == 'Half-Orc':
            name_table = pandas.read_sql_query("SELECT * from Half_Orc", conn)
        else:
            table = random.choice(['Human','Elf'])
            name_table = pandas.read_sql_query(f"SELECT * from {table}", conn)
        self.given = random.choice(name_table[gender.sex.capitalize()].dropna())
        self.surname = random.choice(name_table['Surnames'].dropna())
        



if __name__ == "__main__":
    seed   = int(sys.argv[1])
    race   = str(sys.argv[2])
    sex = str(sys.argv[3])
    if seed == 0:
        seed = str(random.randrange(sys.maxsize))
    random.seed(seed)
    if race == '0':
        race = species(race)
    if sex == '0':
        randsex = random.randrange(1,1000)
        if randsex == 1:
            sex = 'androgynous'
        elif randsex <= 500:
            sex = 'male'
        else:
            sex = 'female'
    gender = pronouns(sex)
    result = define_name(race.race, gender)
    print(f'{result.given} {result.surname}\n{gender.sex} {race.race}')

    