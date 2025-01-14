import random
import pandas
import sqlite3
import sys
import os

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
conn = sqlite3.connect(f"{os.path.dirname(__file__)}\\CHARMS.db")


class History:
    def __init__(self, gentype, age):
        table = pandas.read_sql_query(f"SELECT * from History", conn)
        if gentype == 'all' or gentype == 'Early Life' or gentype == '0':
            self.early_life = f'They {random.choice(table["Early Life"].dropna())}'
        if gentype == 'all' or gentype == 'Key Events' or gentype == '0':
            if age == 'child':
                num_key_events = 1
            elif age == 'young':
                num_key_events = random.randrange(1,3)
            elif age == 'young adult':
                num_key_events = random.randrange(2,4)
            elif age == 'adult':
                num_key_events = random.randrange(4,6)
            else:
                num_key_events = 6
            self.key_events = []
            for i in range(1, num_key_events):
                self.key_events.append(random.choice(table["Key Events"].dropna()))
        # Add Recent Event

        
if __name__ == "__main__":
    seed = int(sys.argv[1])
    gentype = str(sys.argv[2])
    age = str(sys.argv[3])
    if seed == 0:
        seed = str(random.randrange(sys.maxsize))
    if age == 0:
        randage = random.rarandom.randrange(1,100)
        if randage <= 5:
            age = 'child'
        elif randage <= 19:
            age = 'young'
        elif randage <= 56:
            age = 'young adult'
        elif randage <= 86:
            age = 'adult'
        elif randage <= 99:
            age = 'elder'
        elif randage == 100:
            age = 'ancient'
    if gentype == 0:
        gentype == 'all'
    random.seed(seed)
    print(f'Seed: {seed}')
    result = History(gentype, age)
    conn.close()

