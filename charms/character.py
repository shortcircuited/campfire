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
            self.gender = 'man'
            self.noun = 'man'
            self.verb = 'is'
        elif gender == 'female':
            self.subpronoun = 'she'
            self.objpronoun = 'her'
            self.pospronoun = 'hers'
            self.gender = 'woman'
            self.noun = 'woman'
            self.verb = 'is'
        else:
            self.subpronoun = 'they'
            self.objpronoun = 'them'
            self.pospronoun = 'theirs'
            self.gender = 'androgynous'
            self.noun = 'person'
            self.verb = 'are'
            


class character:
    def __init__(self, gentype, gender):
        if gentype == 'physical':
            self.physical = self.gen_physical(gender)
        elif gentype == 'personality':
            self.personality = self.gen_personality(gender)
        else:
            self.physical = self.gen_physical(gender)
            self.personality = self.gen_personality(gender)
    def gen_physical(self, gender):
        traits = []
        table = pandas.read_sql_query(f"SELECT * from Character", conn)
        for i in range(0,random.randrange(2,5)):
            Neg_Pos = random.choices(["Positive","Negative"],weights=[3,1],k=1)
            for i in Neg_Pos:
                Neg_Pos = i
            choice = random.choice(table[Neg_Pos+" Desc"].dropna())
            while choice in traits:
                choice = random.choice(table[Neg_Pos+" Desc"].dropna())
            traits.append(choice)
        traits = ("{}, and {}".format(", ".join(traits[:-1]),  traits[-1])).lower()
        return(f'{gender.subpronoun.capitalize()} {gender.verb} {traits}.')
    def gen_personality(self, gender):
        traits = []
        table = pandas.read_sql_query(f"SELECT * from Character", conn)
        numtraits = random.randrange(2,5)
        for i in range(0,numtraits):
            Neg_Pos = random.choices(["Positive","Negative"],weights=[3,1],k=1)
            for i in Neg_Pos:
                Neg_Pos = i
            choice = random.choice(table[Neg_Pos+" Pers"].dropna())
            while choice in traits:
                choice = random.choice(table[Neg_Pos+" Pers"].dropna())
            traits.append(choice)
        traits = ("{}, and {}".format(", ".join(traits[:-1]),  traits[-1])).lower()
        vowels = 'aeiou'
        if traits[0].lower() in vowels:
            article = "an"
        else:
            article =  "a"
        return(f'Personality wise, {gender.subpronoun} {gender.verb} {article} {traits} {gender.noun}.')


if __name__ == "__main__":
    seed = int(sys.argv[1])
    sex = str(sys.argv[2])
    gentype = str(sys.argv[3])
    if seed == 0:
        seed = str(random.randrange(sys.maxsize))
    random.seed(seed)
    if sex == '0':
        randsex = random.randrange(1,1000)
        if randsex == 1:
            sex = 'androgynous'
        elif randsex <= 500:
            sex = 'male'
        else:
            sex = 'female'
    gender = pronouns(sex)
    result = character(gentype, gender)
    print(f'Seed: {seed}')
    print(f'{result.physical} {result.personality}')


