import random
import pandas
import sqlite3
import sys
import os

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
conn = sqlite3.connect(f"{os.path.dirname(__file__)}\\CHARMS.db")

class relationships:
    def __init__(self):
        table = pandas.read_sql_query(f"SELECT * from Relationships", conn)
        num_relationships = random.randrange(3,4)
        relationships = []
        for i in range(0,num_relationships):
            identifier = random.choice(table["Identifier"].dropna())
            status = random.choice(table["Status"].dropna())
            relationships.append(f'- {status.replace("{identifier}", identifier)}')
        self.final = '\n'.join(relationships)
        print(self.final)

        
if __name__ == "__main__":
    seed = int(sys.argv[1])
    if seed == 0:
        seed = str(random.randrange(sys.maxsize))
    random.seed(seed)
    result = relationships()