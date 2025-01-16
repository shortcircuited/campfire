import random
import pandas
import sqlite3
import sys
import os

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
conn = sqlite3.connect(f"{os.path.dirname(__file__)}\\CHARMS.db")

class statblock:
    def __init__(self,job):
        try: 
            if job.job_class == 'Nobility':
                if job.job == 'Knight':
                    self.statblock = '[Knight](https://www.dndbeyond.com/monsters/16938-knight?srsltid=AfmBOopLga8k0gHg4WUmuOqPU4p4QgF8I2uOOXElw3rcLs7TvNRVSJFt)'
                else:
                    self.statblock = '[Noble](https://www.dndbeyond.com/monsters/16966-noble?srsltid=AfmBOoqOTzgYUuE5_Bb-4eUrW3cAHj-Arpput_dMGtvYyzyAk00JaJT1)'
            elif job.job_class == 'Merchants' or job.job_class == 'Artisans' or job.job_class == 'Laborers' or  job.job_class == 'Hospitality':
                self.statblock = '[Commoner](https://www.dndbeyond.com/monsters/16829-commoner?srsltid=AfmBOoq5g21rC0SG0l_OkUBqP2DsvhCDjm9KoB66Lvw0mwzv4CqePxCQ)'
            elif job.job_class == 'Military':
                if job.job == 'Scout' or job.job == 'Archer':
                    self.statblock = '[Scout](https://www.dndbeyond.com/monsters/17007-scout)'
                elif job.job == 'Mercenary' or job.job == 'Sergeant':
                    self.statblock = '[Veteran](https://www.dndbeyond.com/monsters/17045-veteran)'
                elif job.job == 'Captain':
                    self.statblock = '[Knight](https://www.dndbeyond.com/monsters/16938-knight)'
                else:
                    self.statblock = '[Guard](https://www.dndbeyond.com/monsters/16915-guard)'    
            elif job.job_class == 'Religion':
                if job.job == 'Priest' or job.job == 'Bishop' or job.job == 'Relic Keeper' or job.job == 'Chant Leader':
                    self.statblock = '[Priest](https://www.dndbeyond.com/monsters/16985-priest)'
                elif job.job == 'Acolyte' or job.job == 'Shrine Keeper' or job.job == 'Sacristan' or job.job == 'Confessor' or job.job == 'Hermit' or job.job == 'Monk':
                    self.statblock = '[Acolyte](https://www.dndbeyond.com/monsters/16763-acolyte)'
                elif job.job == 'Oracle' or job.job == 'Diviner':
                    self.statblock = '[Oracle](https://www.dndbeyond.com/monsters/909498-oracle)'
                elif job.job == 'Temple Guard' or job.job == 'Pilgrim Guide':
                    self.statblock = '[Knight](https://www.dndbeyond.com/monsters/16938-knight)'
            elif job.job_class == 'Adventurers':
                if job.job == 'Spy':
                    self.statblock = '[Spy](https://www.dndbeyond.com/monsters/17021-spy)'
                elif job.job == 'Scout' or job.job == 'Pathfinder' or job.job == 'Ranger' or job.job == 'Explorer' or job.job == 'Cartographer':
                    self.statblock = '[Scout](https://www.dndbeyond.com/monsters/17007-scout)'
                elif job.job == 'Bounty Hunter' or job.job == 'Monster Slayer' or job.job == 'Treasure Hunter' or job.job == 'Mercenary' or job.job == 'Sellsword' or job.job == 'Relic Seeker':
                    self.statblock = '[Veteran](https://www.dndbeyond.com/monsters/17045-veteran)'
                elif job.job == 'Arcane Researcher' or job.job == 'Alchemist-for-Hire':
                    self.statblock = '[Mage](https://www.dndbeyond.com/monsters/16947-mage)'
                else:
                    self.statblock = '[Commoner](https://www.dndbeyond.com/monsters/16829-commoner)'
            elif job.job_class == 'Criminal':
                if job.job == 'Highwayman':
                    self.statblock = '[Thug](https://www.dndbeyond.com/monsters/17035-thug)'
                elif job.job == 'Assassin' or job.job == 'Poisoner':
                    self.statblock = '[Assassin](https://www.dndbeyond.com/monsters/16790-assassin)'
                elif job.job == 'Bandit Leader' or job.job == 'Crime Lord':
                    self.statblock = '[Bandit Leader](https://www.dndbeyond.com/monsters/16799-bandit-captain)'
                elif job.job == 'Spy':
                    self.statblock = '[Spy](https://www.dndbeyond.com/monsters/17021-spy)'
                else: self.statblock = '[Bandit](https://www.dndbeyond.com/monsters/16798-bandit)'
        except:
            self.statblock = 'Use [Commoner](https://www.dndbeyond.com/monsters/16829-commoner) unless another fits better'

