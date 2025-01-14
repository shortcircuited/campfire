import random
import sys
import numpy as np


def generate_size(size): #Here we choose the settlement size, if it wasn't predetermined by the user
    if size == '0':
        randsize = random.randrange(1, 1000)
        if randsize <= 250:         # 25% probability
            size = 'hamlet' 
        elif randsize <= 800:       # 55% probability
            size = 'village'    
        elif randsize <= 950:       # 15% probability
            size = 'town'   
        elif randsize <= 995:       # 4.5% probability
            size = 'city'   
        else:                       # 0.5% probability
            size = "big city"

def generate_race(race): #Here we choose the race, if it wasn't predetermined by the user
    if race == '0':
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
        elif randrace <= 999:       # 0.1% chance of werewolf
            race = 'werewolf'
        else:                       # 0.1% chance of werebear
            race = 'werebear'


class legacy:
    def __init__(self, size, seed):
        pass


if __name__ == "__main__":
    # name of the settlement
    name = str(sys.argv[1])
    # Size class of settlement
    size = str(sys.argv[2])
    # Seed for the random generators
    seed = int(sys.argv[3])
    # primary race of the settlement
    race = str(sys.argv[4])
    if seed == 0:
        seed = str(random.randrange(sys.maxsize))
    random.seed(seed)
    generate_size(size)
    generate_race(race)
