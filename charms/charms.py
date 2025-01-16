import random
import pandas
import sqlite3
import sys
import os
import name
import character, history, ambitions, relationships, motifs, statblock

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
conn = sqlite3.connect(f"{os.path.dirname(__file__)}\\CHARMS.db")



class charms:
    def __init__(self,gender,age,job,race,predefined_name):
        self.gender = self.pronouns(gender)
        self.race = self.define_race(race)
        if predefined_name == '0':
            self.name = name.define_name(self.race, self.gender)
        else:
            self.name.given = predefined_name
            self.name.surname = ''
        self.age = self.define_age(age)
        self.job = self.define_job(job)
        self.character = character.character('all', self.gender)
        self.history = history.history('all', self.age)
        self.ambitions = ambitions.ambitions('all')
        self.relationships = relationships.relationships()
        self.motifs = motifs.motifs()
        self.statblock = statblock.statblock(self.job)
        print(f'{self.name.given} {self.name.surname}\n{self.age.capitalize()} {self.race} {self.job.job}\n')
        print(f'{self.character.physical} {self.character.personality}')
        print(f'Early Life:\n{self.history.early_life}\n\nKey Events:\n{self.history.key_events}\nRecent Event:\n{self.history.recent_event}\n')
        print(f'Ambitions:\nPersonal:\n- {self.ambitions.personal_goal}\n\nProfessional:\n- {self.ambitions.professional_goal}\n')
        print(f'Relationships:\n{self.relationships.final}\n')
        print(f'Motifs:\n{self.motifs.motif}\n')
        print(f'Suggested Statblock:\n{self.statblock.statblock}')

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
    def define_race(self, race):            
        if race in ['human','elf','dwarf','halfling','gnome','half-orc','tiefling','dragonborn','tabaxi']:
            self.race = race
        else: 
            randrace = random.randrange(1,1000)
            if randrace <= 750:         # 77.0% chance of human, overflow at the end
               return('human')  
            elif randrace <= 810:       # 6.0% chance of elf
               return('elf')
            elif randrace <= 860:       # 5.0% chance of dwarf
               return('dwarf')
            elif randrace <= 890:       # 3.0% chance of halfling
               return('halfling') 
            elif randrace <= 910:       # 2.0% chance of gnome
               return('gnome')  
            elif randrace <= 925:       # 1.5% chance of half-orc
               return('half-orc')   
            elif randrace <= 940:       # 1.5% chance of tiefling
               return('tiefling')   
            elif randrace <= 955:       # 1.5% chance of dragonborn
               return('dragonborn') 
            elif randrace <= 965:       # 1.0% chance of tabaxi
               return('tabaxi')
            elif randrace <= 975:       # 1.0% chance of kobold
               return('kobold')
            elif randrace <= 985:       # 1.0% chance of goblin
               return('goblin')
            elif randrace <= 990:       # 0.5% chance of aarakocra
               return('aarakocra')
            elif randrace <= 995:       # 0.5% chance of orc
               return('orc')
            elif randrace <= 998:       # 0.3% chance of bugbear
               return('bugbear')
            else: 
               return('human')
    class define_job:
        def __init__(self, job):
            if job in ('Nobility','Merchants','Artisans','Laborers','Military','Hospitality','Religion','Adventurers','Criminal'):
                self.job_class = job
                gen_job = True
            elif job == '0':
                randjob = random.randrange(1,100)
                if randjob == 1:
                    self.job_class = 'Nobility'
                elif randjob <= 8:
                    self.job_class = 'Merchants'
                elif randjob <= 21:
                    self.job_class = 'Artisans'
                elif randjob <= 71:
                    self.job_class = 'Laborers'
                elif randjob <= 75:
                    self.job_class = 'Military'
                elif randjob <= 80:
                    self.job_class = 'Hospitality'
                elif randjob <= 93:
                    self.job_class = 'Religion'
                elif randjob <= 95:
                    self.job_class = 'Adventurers'
                elif randjob <= 100:
                    self.job_class = 'Criminal'
                gen_job = True
            else:
                gen_job = False
                self.job = job
            if gen_job == True:
                table = pandas.read_sql_query(f"SELECT * from Jobs", conn)
                self.job = random.choice(table[self.job_class].dropna())
        


if __name__ == "__main__":
    predefined_name = str(sys.argv[1])
    print(predefined_name)
    seed = int(sys.argv[2])
    gender  = str(sys.argv[3])
    race = str(sys.argv[4])
    job  = str(sys.argv[5])
    age  = str(sys.argv[6])
    if seed == 0:
        seed = str(random.randrange(sys.maxsize))
    random.seed(seed)
    result = charms(gender,age,job,race,predefined_name)
