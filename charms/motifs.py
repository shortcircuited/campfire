import random
import pandas
import sqlite3
import sys
import os

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
conn = sqlite3.connect(f"{os.path.dirname(__file__)}\\CHARMS.db")

class Motifs:
    def __init__(self):
        table = pandas.read_sql_query(f"SELECT * from Motifs", conn)
        if random.choice(True,False) == True: # 50% chance of Motif
            self.motif = random.choice(table["Motifs"].dropna())
        else:
            self.motif = "No Motifs"

if __name__ == "__main__":
    seed = int(sys.argv[1])
    if seed == 0:
        seed = str(random.randrange(sys.maxsize))
    random.seed(seed)