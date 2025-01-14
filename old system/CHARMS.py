import random
import sys
import sqlite3
import pandas
import os

conn = sqlite3.connect(f"{os.path.dirname(__file__)}\\CHARMS.db")
if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    print(os.getcwd())

class CHARMS:
    def __init__(self, Occupation="", Race='',Sex='',save=False):
        if Race == '':
            self.race = self.Race()
        else:
            self.race = Race
        if Sex == '':
            self.sex = self.Sex()
        else:
            self.sex = Sex
        self.name = self.Name(self.race,self.sex)
        if Occupation == '':
            self.occupation = random.choice(pandas.read_sql_query(f"SELECT * from Occupations", conn)['Occupations'])
        else:
            self.occupation = Occupation
        self.character = self.Character()
        self.history = self.History()
        self.ambitions = self.Ambitions()
        self.relationships = self.Relationships()
        self.motifs = self.Motifs()
        if save == True:
            self.save_details()


    def Race(self): 
        return(random.choices(['Human','Dwarf','Elf','Halfling','Gnome','Dragonborn','Tiefling','Half-Elf','Half-Orc','Aasimar','Tabaxi','Goliath'], weights= (100,15,15,10,10,5,5,10,5,5,5,5),k=1))
    def Sex(self):
        return(random.choices(['Male','Female','Androgynous'],weights=(50,50,1),k=1))
    def Name(self, Race, Sex):
        if 'list' in str(type(Race)):
            for i in Race:
                Race = i
        if 'list' in str(type(Sex)):
            for i in Sex:
                Sex = i
        self.race = str(Race)
        self.sex = str(Sex)
        if self.race != 'Half-Elf' and self.race != 'Half-Orc':
            name_table = pandas.read_sql_query(f"SELECT * from {self.race}", conn)
        elif self.race == 'Half-Orc':
            name_table = pandas.read_sql_query("SELECT * from Half_Orc", conn)
        else:
            table = random.choice(['Human','Elf'])
            name_table = pandas.read_sql_query(f"SELECT * from {table}", conn)
        self.given = random.choice(name_table[self.sex].dropna())
        self.surname = random.choice(name_table['Surnames'].dropna())
        return{
            'Given':self.given,
            'Surname':self.surname
        }
    
    class Character:
        def __init__(self):
            self.description = self.Description()
            self.personality = self.Personality()

        def Description(self):
            traits = []
            table = pandas.read_sql_query(f"SELECT * from Character", conn)
            for i in range(2,4):
                Neg_Pos = random.choices(["Positive","Negative"],weights=[3,1],k=1)
                for i in Neg_Pos:
                    Neg_Pos = i
                choice = random.choice(table[Neg_Pos+" Desc"].dropna())
                while choice in traits:
                    choice = random.choice(table[Neg_Pos+" Desc"].dropna())
                traits.append(choice)
            return{
                "Physical Traits": ", ".join(traits)
            }
        def Personality(self):
            traits = []
            table = pandas.read_sql_query(f"SELECT * from Character", conn)
            for i in range(2,4):
                Neg_Pos = random.choices(["Positive","Negative"],weights=[3,1],k=1)
                for i in Neg_Pos:
                    Neg_Pos = i
                choice = random.choice(table[Neg_Pos+" Pers"].dropna())
                while choice in traits:
                    choice = random.choice(table[Neg_Pos+" Pers"].dropna())
                traits.append(choice)
            return{
                "Personality Traits": ", ".join(traits)
            }

    class History:
        def __init__(self):
            self.background = self.Background()
        def Background(self):
            table = pandas.read_sql_query(f"SELECT * from History", conn)
            Neg_Pos = random.choices(["Positive","Negative"],weights=[3,1],k=1)
            for i in Neg_Pos:
                Neg_Pos = i
            choice = random.choice(table[Neg_Pos].dropna())
            return(choice)
    class Ambitions:
        def __init__(self):
            self.ambition = self.Ambition()
        def Ambition(self):
            table = pandas.read_sql_query(f"SELECT * from Ambitions", conn)
            Neg_Pos = random.choices(["Good","Neutral","Evil"],weights=[1.5,8,0.5],k=1)
            for i in Neg_Pos:
                Neg_Pos = i
            choice = random.choice(table[Neg_Pos].dropna())
            return(choice)

    class Relationships:
        def __init__(self):
            self.relationships = self.Relationships()
        def Relationships(self):
            choices = []
            table = pandas.read_sql_query(f"SELECT * from Relationships", conn)
            for i in range(1,3):
                Neg_Pos = random.choices(["Positive","Negative"],weights=[3,1],k=1)
                for i in Neg_Pos:
                    Neg_Pos = i
                choice = random.choice(table[Neg_Pos].dropna())
                while choice in choices:
                    choice = random.choice(table[Neg_Pos].dropna())
                choices.append(choice)
            return{
                "Relationships": "\n    ".join(choices)
            }
    class Motifs:
        def __init__(self):
            self.visual_theme = self.Visual_theme()

        def Visual_theme(self):
            table = pandas.read_sql_query(f"SELECT * from Motifs", conn)
            chance = random.choices([True,False], weights=[0,3],k=1)
            for i in chance:
                chance=i
            if chance == True:
                return(f"Visual Theme: {random.choice(table['Visual Theme'].dropna())}")
            else:
                return("None")

    def display_details(self):
        print(f"Name: {self.name['Given']} {self.name['Surname']}")
        print(f"{self.sex} {self.race} {self.occupation}")
        print('\nCharacter===================================')
        for key, value in self.character.description.items():
            print(f"  {key.capitalize()}: {value}")
        for key, value in self.character.personality.items():
            print(f"  {key.capitalize()}: {value}")
        print('\nHistory=====================================')
        print(f'  Background:\n    {self.history.background}')
        print("\nAmbitions===================================")
        print(f'  Goal: {self.ambitions.ambition}')
        print("\nRelationships===============================")
        for key, value in self.relationships.relationships.items():
            print(f"    {value}")
        print("\nMotifs======================================")
        print(f"  {self.motifs.visual_theme}")
        print("\ntatblock===================================")
        print("  Use commoner statblock unless it makes more sense to use another.")
    
    def save_details(self):
        if os.path.exists(f"{self.name['Given']} {self.name['Surname']}.txt"):
            print('\n\nThis file already exists.')
            request = ''
            while request.lower() != 'y' and request.lower() != 'yes' and request.lower() != 'n' and request.lower() != 'no':
                request = input('Would you like us to overwrite the existing file? Y/N: ')
            if request.lower() == 'y' or request.lower() == 'yes':
                os.remove(f'{self.name}.txt')
            print('File deleted.')
        with open(f"{self.name['Given']} {self.name['Surname']}.txt",'a') as file:
            file.write(f"Name: {self.name['Given']} {self.name['Surname']}\n")
            file.write(f"{self.sex} {self.race} {self.occupation}\n")
            file.write('\nCharacter===================================\n')
            for key, value in self.character.description.items():
                file.write(f"  {key.capitalize()}: {value}\n")
            for key, value in self.character.personality.items():
                file.write(f"  {key.capitalize()}: {value}\n")
            file.write('\nHistory=====================================\n')
            file.write(f'  Background:\n    {self.history.background}\n')
            file.write("\nAmbitions===================================\n")
            file.write(f'  Goal: {self.ambitions.ambition}\n')
            file.write("\nRelationships===============================\n")
            for key, value in self.relationships.relationships.items():
                file.write(f"    {value}\n")
            file.write("\nMotifs======================================\n")
            file.write(f"  {self.motifs.visual_theme}\n")
            file.write("\nStatblock===================================\n")
            file.write("  Use commoner statblock unless it makes more sense to use another.\n")
        
if __name__ == "__main__":
    Occupation = input("Occupation: ")
    Race = input("Race: ")
    Sex = input("Sex: ")
    character = CHARMS(Occupation=Occupation,Race=Race,Sex=Sex)
    character.display_details()