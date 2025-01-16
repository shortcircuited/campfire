import random
import pandas
import sqlite3
import sys
import os

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
conn = sqlite3.connect(f"{os.path.dirname(__file__)}\\CHARMS.db")


class ambitions:
    def __init__(self,gentype):
        table = pandas.read_sql_query(f"SELECT * from Ambitions", conn)
        if gentype == 'all' or gentype == '0':
            gen_personal = True
            gen_professional = True
        elif gentype == 'personal':
            gen_personal = True
            gen_professional = False
        else:
            gen_personal = False
            gen_professional = True
        if gen_personal == True:
            self.personal_goal = random.choice(table["Personal"].dropna())
        if gen_professional == True:
            self.professional_goal = random.choice(table["Professional"].dropna())



if __name__ == "__main__":
    seed = int(sys.argv[1])
    gentype = str(sys.argv[2])
    if seed == 0:
        seed = str(random.randrange(sys.maxsize))
    random.seed(seed)