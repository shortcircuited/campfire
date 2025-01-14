import random
import sys
from CHARMS import CHARMS
import os
import numpy as np
import sqlite3
import pandas

#finish export lists -- Fishing

# Definitions of possible attributes
Gen_folder = "d:\\Coding\\SPERM 2_0"
Adj_1 = [
    'Sapphire','Crimson','Gilded','Ethereal','Emerald','Lustrous',
    'Obsidian','Radiant','Iridescent','Celestial','Opulent','Enigmatic',
    'Regal','Harmonious','Vibrant','Silvery','Resplendent','Tranquil',
    'Mysterious','Ornate','Glittering','Timeless','Ephemeral','Velvety',
    'Cobalt','Aetherial','Glacial','Effulgent','Cerulean','Astral',
    'Perpetual','Verdant','Ethereal','Pearly','Illustrious','Quicksilver',
    'Grandiose','Harmonic','Majestic','Nocturnal','Scintillating','Pinnacle',
    'Vesperal','Enchanting','Luminous','Nebulous','Golden','Velour',
    'Resonant','Sovereign'
    ]
Adj_2 = [
    'Vile','Pestilent','Abhorrent','Nauseating','Ominous','Corrupt',
    'Pestilential','Blighted','Malevolent','Putrid','Malignant','Sinister',
    'Decaying','Sinister','Noxious','Wretched','Tainted','Odious',
    'Desolate','Maleficent','Squalid','Execrable','Diabolical','Grisly',
    'Malefic','Loathsome','Execrable','Morbid','Infernal','Grim',
    'Cursed','Harrowing','Depraved','Macabre','Dismal','Unholy',
    'Mephitic','Ghastly','Nefarious','Grotesque','Sinuous','Abysmal',
    'Cacophonic','Pestiferous','Malefic','Abominable','Malevolent','Blasphemous',
    'Repugnant','Accursed'
    ]
Noun_1 = [
    'Sparrow','Unicorn','Lamb','Pegasus','Kitten','Dolphin',
    'Fawn','Faun','Swan','Hummingbird','Griffin','Bunny',
    'Otter','Cherub','Songbird','Corgi','Sylph','Alpaca',
    'Butterfly','Dove','Kitsune','Puppy','Doe','Chimera',
    'Firefly','Owl','Hedgehog','Gryphon','Puffin','Pixie',
    'Seraph','Quokka','Faerie','Phoenix','Lark','Koala',
    'Sprite','Jackalope','Lanternfly','Mermaid','Chipmunk','Siren',
    'Starling','Otter','Angel','Albatross','Selkie','Pika',
    'Gazer','Treant'
    ]
Noun_2 = [
'Ghoul','Banshee','Wraith','Necromancer','Lich','Specter',
'Demon','Hellhound','Chimera','Minotaur','Harpy','Goblin',
'Orc','Kobold','Troll','Ogre','Hydra','Basilisk',
'Manticore','Succubus','Incubus','Vampire','Werewolf','Gargoyle',
'Revenant','Doppelganger','Changeling','Ghost','Shade','Imp',
'Warlock','Witch','Gorgon','Satyr','Wendigo','Rakshasa',
'Siren','Nightstalker','Gremlin','Hobgoblin','Djinn','Kraken',
'Marid','Oni','Lamia','Asura','Shade','Centaur',
'Wight','Cultist',
]

def generate_population(mean=3, sigma=3):
    while True:
        population = np.random.lognormal(mean, sigma)
        if population <= 70:
            population = random.randrange(75,150)
        population = np.round(population).astype(int)
        if 70 <= population <= 200000:
            return population
def calculate_weights(population, max_pop=200000):
    # Ensure population is within the range
    population = min(max(population, 0), max_pop)
    
    # Calculate weights based on population
    # Here we linearly interpolate the weights between two sets of values
    # Adjust these formulas as needed
    weight1 = max(1 - (population / max_pop), 0.1)  # Ensures weight1 never goes to 0
    weight2 = (population / max_pop) / 2  # Increases up to 0.5
    weight3 = (population / max_pop) * 0.9 + 0.1  # Ensures weight3 starts at 0.1 and goes up to 1
    
    return [weight1, weight2, weight3]
def political_weights(population, base_weights=[15, 115, 15, 35, 5, 25]):
# Unpack base weights for readability
    democracy, feudal, oligarchy, theocracy, commune, autocracy = base_weights
    
    # Adjust weights based on population size
    if population > 1000:
        # Increase Oligarchy weights as population grows, with a simple linear growth model
        oligarchy += (population - 1000) // 10000  # Adjust the divisor for finer control
    else:
        # Make Oligarchy impossible for small populations
        oligarchy = 0

    # Decrease Democracy and Communism as population grows, using a simple decay model
    democracy = max(democracy - (population // 50000), 0)  # Ensure it never goes to 0 but decreases
    commune = max(commune - (population // 50000), 0)  # Ensure it never goes to 0 but decreases

    return [democracy, feudal, oligarchy, theocracy, commune, autocracy]
def calculate_title_weights(population, title_peaks={'Sir (knight)': 0, 'Baron': 1000,'Count': 5000,'Duke': 10000, 'King':20000}, std_dev=10000):
    x=0
    for title, limit in title_peaks.items():
        if int(population) >= limit:
            x+=1
        else: break
    weights = [0, 0, 0, 0, 0]  # Initialize the weights list with zeros

    if 1 <= x <= 5:
        weights[x - 1] = 1 
        if x != 1:
            weights[x-2]=1
    return(weights)

class SettlementGenerator:
    def __init__(self, name='',population=''):

        # Calling all of the settlement sections
        if name != '':
            self.name = name
        else:
            self.name = self.Name()
        if population == '':
            self.population = generate_population()
        else:
            self.population = int(population)
        if os.path.isdir(f"{Gen_folder}\\{self.name}") == False:
            os.mkdir(f"{Gen_folder}\\{self.name}")
            os.chdir(f"{os.path.dirname(__file__)}\\{self.name}")


        global weights
        weights = calculate_weights(self.population)
        global political_weights
        political_weights = political_weights(self.population)
        global title_weights
        title_weights = calculate_title_weights(self.population)

        self.social     = self.Social()
        self.political  = self.Political()
        self.economy    = self.Economy()
        self.religion   = self.Religion()
        self.military   = self.Military()
        
    def Name(self, type=random.choice(['Geo','Founder'])):
        conn = sqlite3.connect(f"{Gen_folder}\\SPERM.db")
        list = pandas.read_sql_query("SELECT * from Names",conn)
        if type == 'Geo':
            return(f"{random.choice(list['Geo_pre'].dropna())}{random.choice(list['Geo_suf'].dropna())}")
        else:
            Founder = CHARMS(save=True)
            return(f"{Founder.name['Given']}{random.choice(list['Founder_suf'].dropna())}")

    class Social:
        def __init__(self):
            self.town_square = self.generate_town_square_details()
            self.tavern = self.generate_tavern_details()

        def generate_town_square_details(self):
            activities = [
                'Market Day: Vendors selling various goods, from local produce to exotic items.',
                'Festival Celebration: Seasonal or cultural festivals with music, dance, and games.',
                'Tournament: Competitions such as jousting, archery, or melee battles.',
                'Public Speeches: Leaders or important figures addressing the public.',
                'Street Performers: Jugglers, musicians, acrobats, and magicians entertaining crowds.',
                'Religious Ceremony: Rituals or celebrations pertaining to the dominant religion.',
                'Craft Fair: Local artisans showcasing and selling their handmade goods.',
                'Town Meetings: Gathering of townsfolk to discuss important issues.',
                'Historical Reenactments: Dramatizations of significant historical events.',
                'Public Trials: Legal proceedings held in front of the townsfolk.',
                'Art Exhibits: Display of artwork by local or visiting artists.',
                'Food Festival: Celebration of culinary delights with various food stalls.',
                'Parades: Processions for holidays, victories, or other special occasions.',
                'Magic Shows: Wizards or sorcerers demonstrating their magical abilities.',
                'Astronomy Nights: Observing and discussing celestial events and constellations.',
                'Poetry Readings: Poets sharing their work with an audience.',
                'Storytelling Sessions: Storytellers captivating the audience with tales of adventure and myth.',
                'Music Concerts: Performances by solo musicians or bands.',
                'Dance Competitions: Contests showcasing different styles of dance.',
                'Charity Auctions: Auctions held to raise funds for a good cause.',
                "Children's Games: Area designated for children to play games and activities.",
                'Bird or Pet Shows: Exhibitions of trained animals or rare species.',
                'Herbalist and Alchemist Fairs: Display and sale of potions, herbs, and remedies.',
                'Arm Wrestling and Strength Contests: Tests of physical strength and endurance.',
                'Fortune Telling: Seers, oracles, or fortune tellers offering insights into the future.'
        ]
            features = [
                "Grand Fountain: A large, ornate fountain, possibly magical or historical.",
                "Statue of a Local Hero: A monument dedicated to a famed individual from the town's history.",
                "Sundial: An ancient or artistically crafted sundial, used for telling time.",
                "Giant Chessboard: A life-sized chessboard for public games.",
                "Memorial Obelisk: A tall, narrow monument commemorating an important event.",
                "Community Notice Board: A board where notices, quests, and announcements are posted.",
                "Central Fire Pit: Used for warmth, cooking, or ceremonial purposes.",
                "Herbal Garden: A small public garden with medicinal and culinary herbs.",
                "Ancient Tree: A large, possibly magical tree that is central to local lore.",
                "Stone Circle: A mysterious or sacred arrangement of stones.",
                "Public Library or Book Stand: A place for reading and borrowing books.",
                "Wishing Well: An old well believed to grant wishes when coins are tossed in.",
                "Clock Tower: A towering structure with a large, visible clock.",
                "Market Stalls: Permanent structures for vendors to sell their goods.",
                "Bandstand or Gazebo: A platform for musical performances and public speeches.",
                "Interactive Sculpture: Art pieces that people can touch or climb on.",
                "Historical Plaques: Informative plaques detailing the town's history.",
                "Bird Baths and Feeders: Areas attracting and supporting local wildlife.",
                "Mosaic Tiles: Colorful, artistic tiles depicting local legends or stories.",
                "Drinking Fountain: A fountain providing clean water for public use.",
                "Labyrinth or Maze: A small, walkable labyrinth for meditation or play.",
                "Outdoor Gallery: Space for exhibiting art and sculptures.",
                "Magical Light Display: Enchanted lights or floating lanterns that illuminate at night.",
                "Petting Zoo or Animal Enclosure: A small area with domestic or magical creatures.",
                "Astronomical Model: A representation of the planetary system or constellations."
            ]
            atmosphere = [
                'Bustling and Lively',
                'Serene and Peaceful',
                'Festive and Joyous',
                'Tense and Suspicious',
                'Historic and Reverent',
                'Elegant and Refined',
                'Rustic and Charming',
                'Busy and Commercial',
                'Romantic and Quaint',
                'Mystical and Magical',
                'Foreboding and Ominous',
                'Artistic and Creative',
                'Decrepit and Forgotten',
                'Cheerful and Welcoming',
                'Sacred and Solemn',
                'Opulent and Luxurious',
                'Diverse and Cosmopolitan',
                'Natural and Earthy',
                'Noisy and Chaotic',
                'Gloomy and Melancholic',
                'Scholarly and Intellectual',
                'Adventurous and Exciting',
                'Haunted and Eerie',
                'Seasonal Atmosphere'
            ]

            return {
                'activity': random.choice(activities),
                'feature': random.choice(features),
                'atmosphere': random.choice(atmosphere)
            }

        def generate_tavern_details(self):
            patron_type = ['Adventurers', 'Locals', 'Merchants','Nobles']
            entertainment = [
                'Live Band Performance',
                'Bardic Storytelling',
                'Stand-up Comedy',
                'Magic Tricks Show',
                'Puppet Show',
                'Poetry Slam',
                'Local Dance Troupe',
                'Fortune Telling',
                'Arm Wrestling Contests',
                'Dice Games',
                'Card Tournaments',
                'Drinking Games',
                'Mystery Dinner Theater',
                'Open Mic Night',
                'Juggling Act',
                'Fire Breathing Performance',
                'Knife Throwing Display',
                'Singing Competition',
                'Karaoke Night',
                'Chess Tournament',
                'Play or Skit Performance',
                'Acrobatic Display',
                'Illusionist Show',
                'Riddle Contests',
                'Folklore Nights'
            ]
            specialty_food = [
        # Mundane options
                'Grilled Sausages',
                'Savory Pies',
                'Fried Fish',
                'Roast Chicken',
                'Meat and Cheese Board',
                'Stuffed Vegetables',
                'Homemade Pastas',
                'Fresh Salads',
                'Hearty Soups',
                'Wood-Fired Pizzas',
                'Smoked Meats',
                'Local Delicacies',
                'Baked Potatoes',
                'Seasonal Fruit Tarts',
                'Sandwich Assortment',
                'Pan-Fried Dumplings',
                'Marinated Olives',
                'Artisanal Breads',
                'BBQ Ribs',
                'Chocolate Desserts',
                'Spiced Nuts',
                'Pickled Vegetables',
        # Magical options
                'Ever-Warm Stew',
                'Changing Flavor Pie',
                'Floating Sweet Cakes',
            ]
            specialty_drink = [
        # Mundane
                'Dark Ales',
                'Light Lagers',
                'Fruit Ciders',
                'Red Wines',
                'White Wines',
                'Aged Scotch',
                'Herbal Teas',
                'Iced Coffees',
                'Seasonal Juices',
                'Berry Lemonades',
                'Spicy Hot Chocolate',
                'House Special Cocktails',
                'Craft Sodas',
                'Flavored Waters',
                'Local Brews',
                'Bitter Tonics',
                'Mead',
                'Milkshakes',
                'Non-Alcoholic Beers',
                'Chilled Sangria',
                'Traditional Liquors',
                'Mulled Wine',
        # Magical
                'Elixir of Vivid Dreams',
                'Ale of Truth-Telling',
                'Wine of Timeless Joy',
            ]
            types = ['Inn','Pub','Tavern','Hostel','Meadery','Brewery']
            num_of_taverns = int(''.join(random.choices(['1','2','3'],weights=weights,k=1)))
            taverns = {}
            for i in range(num_of_taverns):
                patrons = random.choice(patron_type)
                Owner = CHARMS(Occupation="Innkeeper",save=True)
                if patrons == 'merchants' or patrons == 'nobles':
                    name = random.choice([f"The {random.choice(Adj_1)} {random.choice(Noun_1)}",f"{Owner.name['Given']}'s {random.choice(types)}"])
                else:
                    name = random.choice([f"The {random.choice(Adj_1)} {random.choice(Noun_1)}",f"{Owner.name['Given']}'s {random.choice(types)}",f"The {random.choice(Adj_2)} {random.choice(Noun_2)}"])
                taverns[name] = {
                    'Owner':           f"{Owner.name['Given']} {Owner.name['Surname']}, {Owner.sex} {Owner.race}", 
                    'patron type':     patrons,
                    'entertainment':   random.choice(entertainment),
                    'specialty food':  random.choice(specialty_food),
                    'specialty drink': random.choice(specialty_drink)
                }
            
            return {
                'Name': taverns
            }
        


    class Political:
        def __init__(self):
            self.structure = self.Structure()
        def Structure(self):
            political_structures = ['Democracy', 'Feudal', 'Oligarchy', 'Theocracy', 'Commune','Autocracy']
            for i in random.choices(political_structures,weights=political_weights,k=1):
                choice = i
            sex = random.choice(["Male","Female"])
            if choice == "Democracy":
                self.leader_title = random.choice(['Mayor','Chancellor'])
                self.leader = CHARMS(Occupation=self.leader_title,Sex=sex,save=True)
                governing_bodies = ["Town Council", "Citizens' Assembly","Wizards' Consortium","Education Committee","Defense Committee","Legal Affairs Committee","Merchant Guild Council","Shadow Council"]
                laws = ["Freedom of Speech","Universal Suffrage Law","Right to Assembly","Equal Representation Act","Public Office Integrity Law","Land and Property Rights","Trade and Commerce Fairness Act","Public Education Mandate","Welfare Law","Public Health and Safety Codes","Environmental Protection Laws","Criminal Justice Reform Act","Magic Regulation and Oversight","Emergency Powers Limitation"]
            elif choice == "Oligarchy":
                self.leader_title = "High Councillor"
                self.leader = CHARMS(Occupation=self.leader_title,Sex=sex,save=True)
                governing_bodies = ["Trade Guilds","Nobility","Elders","Guilds' Council","Banking Consortium","Judicial Court","Military Command Council","Magical Conclave","Landowners' Conclave"]
                laws = ["Trade Regulation", "Guild Membership Requirements","Land Acquisition Laws","Selective Law Enforcement","Restricted Political Participation","Military Service Exemptions","Restricted Access to Education","Debt Bondage Laws","Censorship of Press and Expression","Tax Exemption for the Elite","Inheritance and Succession Laws","Immunity Statutes","Restricted Suffrage","Property Rights for the Elite"]
            elif choice == "Theocracy":
                self.leader_title = "High Priest" if sex == 'Male' else "High Priestess"
                self.leader = CHARMS(Occupation=self.leader_title,Sex=sex,save=True)
                governing_bodies = ["religious council", 'High Council of Clerics','Divine Tribunal','Sacred Synod','Order of Oracles','Council of Temple Guardians','Assembly of Holy Scholars',"Divine Prophets' Circle",'Ecclesiastical Court','Congregation of Rituals and Ceremonies','Ministry of Sacred Teachings']
                laws = ["religious observance",'Mandatory Worship Attendance Law','Blasphemy Prohibition Act','Holy Days Observance Decree','Tithing and Religious Offerings Mandate','Sacred Texts Preservation Act','Prohibition of Heretical Teachings','Divine Law Supremacy Statute','Religious Education Requirement Law','Holy Sanctuaries Protection Ordinance','Clerical Immunity and Privilege Law','Sacred Pilgrimage Regulation','Religious Assembly and Procession Act','Divine Prophecy and Oracle Law','Holy Rites and Rituals Compliance Decree','Ban on Unsanctioned Religious Practices']
            elif choice == "Autocracy":
                self.leader_title = random.choice(['General','Admiral','Supreme Leader','Sovereign'])
                self.leader = CHARMS(Occupation=self.leader_title,Sex=sex,save=True)
                governing_bodies = [f"{self.leader_title}'s Council","Imperial Advisory Board","Central Intelligence Directorate","Military Command","National Security Assembly","High Court of Justice","State Propaganda Office","Ministry of State Resources","Merchants' Financial Consortium","Elite Traders' Circle"]
                laws = ['Absolute Allegiance to the Leader Act','Censorship of Media and Information Law','Prohibition of Unauthorized Assemblies','State Approval for Public Speeches','Mandatory Military Service Decree','Surveillance and Espionage Act','Restricted Foreign Travel Regulation','Ban on Political Opposition Parties','Loyalty Pledge Requirement for Government Positions','Nationalization of Key Industries Law','State Control of Education and Curriculum','Mandatory State Religion Adherence','Prohibition of Unsanctioned Protests','Elite Class Privilege Protection Law','Curfew and Public Order Maintenance Act']
            elif choice == "Feudal":
                leader_title = random.choices(["Sir","Baron","Count","Duke","King"],weights=title_weights,k=1) if sex == 'Male' else random.choices(["Dame","Baroness","Countess","Duchess","Queen"],weights=title_weights,k=1)
                for i in leader_title:
                    self.leader_title = i
                self.leader = CHARMS(Occupation=self.leader_title,Sex=sex,save=True)
                governing_bodies = ["Noble Court", "Advisory Council","Secret Council or Intelligence Network","Treasury Council","High Judicial Council","War Council","Trade and Commerce Council","Religious Council"]
                laws = ["Hereditary Rule", "Noble Hierarchy","Censorship Laws","Justice Administration Law","Royal Prerogative on War and Peace","Heresy Laws","Martial Law Powers","Trade and Guild Regulations","Land Inheritance Laws","Sumptuary Laws","Serfdom and Bondage Laws","Tithe Law","Feudal Obligations","Noble Privilege"]
            elif choice == "Commune":
                self.leader_title = 'Chairman' if sex == 'Male' else 'Chairwoman'
                self.leader = CHARMS(Occupation=self.leader_title,Sex=sex,save=True)
                governing_bodies = ["Workers' Council","Central Planning Committee","People's Assembly","Labor Syndicate","Agricultural Commune Council","Resource Allocation Bureau","Equality Oversight Commission","Public Services Committee","Cultural and Education Directorate","Revolutionary Defense Council"]
                laws = ["Equal Distribution of Resources Act","Collective Ownership of Production Means Law","Mandatory Labor Contribution Statute","Abolition of Private Property Rights","Income Redistribution Ordinance","State-Controlled Education and Healthcare Act","Ban on Private Enterprise and Trade","Prohibition of Exploitation Labor Law","Mandatory State Service Requirement","Classless Society Promotion Act","Universal Housing Allocation Law","Censorship of Anti-Collectivist Propaganda","Equal Representation in Workers' Councils Decree","Restriction on Religious Practices in Public Life","Nationalization of All Foreign Assets and Enterprises Act",]
            return{
                'Structure': choice,
                'Leader': f"{self.leader_title} {self.leader.name['Given']} {self.leader.name['Surname']}, {sex} {self.leader.race}",
                'Governing Bodies': ', '.join(random.choices(governing_bodies,k=random.randrange(1,3))),
                'Key Laws': ', '.join(random.choices(laws,k=random.randrange(2,4)))
            }
    
    class Economy:
        def __init__(self):
            self.profile = random.choice(['Agriculture', 'Trade Hub', 'Mining', 'Crafting', 'Fishing'])
            self.breakdown = self.import_export(self.profile)
        def import_export(self,profile):
            import_list = [
        # Mundane
                'Grain',
                'Meat/Livestock',
                'Lumber',
                'Fish',
                'Olive Oil',
                'Coffee/Tea',
                'Medicine',
                'Precious Gems',
                'Precious Metals',
                'Horses',
                'Ceramics',
                'Glassware',
                'Exotic Pets',
                'Leather',
                'Salt',
                'Produce',
                'Spices',
                'Cotton',
                'Wool',
        # Magical
                'Enchanted Items',
                'Magical Herbs',
                'Potions',
                'Magic Focuses'
                ]
            if profile == 'Agriculture':
                export_list = [
                    'Grain',
                    'Produce',
                    'Cotton',
                    'Wool',
                    'Meat/Livestock',
                    'Coffee/Tea',
                    'Olive Oil',
                    'Spices',
                    'Lumber',
                    'Horses',
                    'Magical Herbs',
                    ]
            elif profile == 'Trade Hub':
                export_list = [
            # Mundane
                    'Grain',
                    'Meat/Livestock',
                    'Lumber',
                    'Stone',
                    'Fish',
                    'Iron',
                    'Coal',
                    'Olive Oil',
                    'Coffee/Tea',
                    'Medicine',
                    'Precious Gems',
                    'Precious Metals',
                    'Horses',
                    'Ceramics',
                    'Glassware',
                    'Exotic Pets',
                    'Leather',
                    'Salt',
                    'Produce',
                    'Spices',
                    'Cotton',
                    'Wool',
                    'Boats/Ships and/or Wagons',
                    'Exotic Clothes'
            # Magical
                    'Enchanted Items',
                    'Magical Herbs',
                    'Potions',
                    'Magic Focuses'
                    ]
            elif profile == 'Mining':
                export_list = [
                    'Stone',
                    'Iron',
                    'Coal',
                    'Precious Gems',
                    'Precious Metals',
                    'Salt'
                ]
            elif profile == 'Crafting':
                export_list = [
                    'Ceramics',
                    'Glassware',
                    'Tools',
                    'Weapons/Armor',
                    'Jewelry',
                    'Medicine'
                    'Potions',
                ]
            elif profile == 'Fishing':
                export_list = [
                    'Salt',
                    'Fish',
                    'Pearls',
                    'Shellfish',
                    'Whale Oil',
                    'Boats/Ships'
                ]            
            return{
                'Profile' : self.profile,
                'Imports' : ', '.join(random.choices(import_list, k= random.randrange(1,3))),
                'Exports' : ', '.join(random.choices(export_list, k= random.randrange(1,3))),
            }
    
    class Religion:
        def __init__(self):
            self.deities = self.Gods()
            self.holidays = self.Holidays()
        def Gods(self):
            domains = [
                'Life: Healing, vitality, and wellness',
                'Light: Sun, daylight, and radiance',
                'Nature: Flora, fauna, and the natural order',
                'Agriculture: Farming, crops, and harvest',
                'Sea: Oceans, seas, and water travel',
                'Storm: Weather, tempests, and natural fury',
                'Craft/Forge: Artisans, creation, and construction',
                'Love: Affection, romance, and friendship',
                'Peace: Harmony, calm, and non-violence',
                'Fortune: Luck, fate, and chance',
                'Fertility: Childbirth, growth, and nurturing',
                'Home: Hearth, shelter, and protection of family',
                'Trade: Commerce, negotiation, and wealth',
                'Travel: Journeys, exploration, and adventure',
                'Knowledge: Wisdom, learning, and memory',
                'Wisdom: Insight, common sense, and understanding',
                'Protection: Defense, safeguarding, and warding',
                'Harvest: Gathering, autumn, and the cycle of seasons',
                'Moon: Tides, cycles, and mystery',
                'Sun: Daylight, clarity, and truth',
                'Justice: Law, fairness, and equity',
                'Forge: Metallurgy, fire, and creation',
                'Music: Song, harmony, and the arts',
                'Celebration: Festivals, joy, and happiness',
                'Animals: Wildlife, beasts, and creatures',
                'Healing: Recovery, medicine, and health',
                'Hope: Optimism, aspiration, and the future',
                'Stars: Navigation, prophecy, and destiny',
                'Ancestors: Lineage, tradition, and the past',
                'War: Battle, strength, and valor',
                'Adventure: Discovery, risk, and the unknown',
                'Magic: Arcane arts, spells, and mysticism',
                'Strength: Physical power, endurance, and resilience',
                'Strategy: Tactics, planning, and leadership',
                'Exploration: Uncharted lands, new horizons, and curiosity',
                'Victory: Triumph, conquest, and fame',
                'Mystery: Secrets, riddles, and enigmas',
                'Death: Decay, mortality, and the afterlife',
                'Trickery: Deceit, illusions, and cunning',
                ]
            
            primary_choices = []
            secondary_choices = []
            for i in range(random.randrange(1,2)):
                new = random.choice(domains)
                while new in primary_choices:
                    new = random.choice(domains)
                primary_choices.append(new)
            for i in range(random.randrange(2,4)):
                new = random.choice(domains)
                while new in secondary_choices or new in primary_choices:
                    new = random.choice(domains)
                secondary_choices.append(new)
            return{
                'Primary deities'  : ',\n                   '.join(primary_choices),
                'Secondary deities': ',\n                     '.join(secondary_choices)
            }
        def Holidays(self):
            types = [
                "Festival of First Light: Celebrated at the first sign of spring",
                "Harvest's End: Marking the end of the autumn harvest season",
                "Night of Stars: Observed on the clearest night of summer",
                "Winter's Embrace: Celebrated at the peak of winter, when nights are longest",
                "Blossom Festival: Coinciding with the early spring bloom",
                "The Great Thaw: Commemorated at the end of winter as ice and snow begin to melt",
                "Sun's Apex: Celebrated at the height of summer, when the sun is strongest",
                "Moon's Reflection: Observed on a night of a full moon in autumn",
                "Sea's Blessing: Celebrated at the start of the fishing season in early summer",
                "Winds of Change: Marking the transition from summer to autumn",
                "Fire's Night: Celebrated on a cold night in mid-winter, with bonfires and festivities",
                "Twilight's Eve: Observed during the fall, as days start to shorten",
                "Ancestors' Night: Celebrated at the start of winter, honoring the spirits of ancestors",
                "Feast of Fertility: Coinciding with the early days of spring planting",
                "Starfall Celebration: On a night when meteor showers are visible, usually in late summer",
                "Veil of Shadows: Celebrated during the darkest phase of the moon in autumn",
                "Earth's Renewal: Marked at the end of winter, symbolizing new beginnings",
                "Spirit Dance: Celebrated during the mid-autumn, when it is believed the veil between worlds is thin",
                "Harmony Day: Observed during the spring equinox, symbolizing balance",
                "Rite of Passage: Celebrated at the onset of summer, marking a time for youth coming of age",
            ]
            choices = []
            for i in range(random.randrange(2,4)):
                new = random.choice(types)
                while new in choices:
                    new = random.choice(types)
                choices.append(new)
            return{
                'Holidays': ',\n            '.join(choices)
            }

    class Military:
        def __init__(self):
            self.profile = self.Profile()
        def Profile(self):
            choices = []
            num_choices = int(''.join(random.choices(['1','2','3'],weights=weights,k=1)))
            types = ['Conscripts','Volunteer Guards','Mercenaries','Militia','Local Knights','No Formal Military']
            if num_choices != 1:
                types = ['Conscripts','Volunteer Guards','Mercenaries','Militia','Local Knights']
            for i in range(num_choices):
                if num_choices != 1:
                    new = random.choices(types,weights=[5,35,5,50,25],k=1)
                    while new in choices:
                        new = random.choices(types,weights=[5,35,5,50,25],k=1)
                    for i in new:
                        choices.append(i)
                else:
                    new = random.choices(types,weights=[5,35,5,50,25,75],k=1)
                    while new in choices:
                        new = random.choices(types,weights=[5,35,5,50,25,75],k=1)
                    for i in new:
                        choices.append(i)

            return{
                'Structure' : '\n             '.join(choices)
            }
    
    def display_details(self):
        print(f"Settlement: {self.name}")
        print(f"Seed: {seed}")
        print(f"Population: {self.population}")
        print('Social===============================================')
        print("  Town Square:")
        for key, value in self.social.town_square.items():
            print(f"    {key.capitalize()}: {value}")
        print("  Taverns:")
        # print(self.social.tavern)
        for key, value in self.social.tavern['Name'].items():
            print(f"    {key}: ")
            for key, value in value.items():
                print(f'      {key.capitalize()}: {value}')
        print('Political============================================')
        for key, value in self.political.structure.items():
            print(f"  {key.capitalize()}: {value}")
        print('Economic=============================================')
        for key, value in self.economy.breakdown.items():
            print(f"  {key.capitalize()}: {value}")
        print('Religion=============================================')
        for key, value in self.religion.deities.items():
            print(f"  {key.capitalize()}: {value}")
        for key, value in self.religion.holidays.items():
            print(f"  {key.capitalize()}: {value}")
        print('Military=============================================')
        for key, value in self.military.profile.items():
            print(f"  {key.capitalize()}: {value}")

    def save_details(self):
        if os.path.exists(f'{self.name}.txt'):
            print('\n\nThis file already exists.')
            request = ''
            while request.lower() != 'y' and request.lower() != 'yes' and request.lower() != 'n' and request.lower() != 'no':
                request = input('Would you like us to overwrite the existing file? Y/N: ')
            if request.lower() == 'y' or request.lower() == 'yes':
                os.remove(f'{self.name}.txt')
            print('File deleted.')
        with open(f'{self.name}.txt','a') as file:
            file.write(f"Settlement: {self.name}\n")
            file.write(f"Seed: {seed}\n")
            file.write(f"Population: {self.population}\n")
            file.write('\n\nSocial===============================================\n')
            file.write("  Town Square:\n")
            for key, value in self.social.town_square.items():
                file.write(f"    {key.capitalize()}: {value}\n")
            file.write("  Taverns:\n")
            for key, value in self.social.tavern['Name'].items():
                file.write(f"    {key}: \n")
                for key, value in value.items():
                    file.write(f'      {key.capitalize()}: {value}\n')
            file.write('\nPolitical============================================\n')
            for key, value in self.political.structure.items():
                file.write(f"  {key.capitalize()}: {value}\n")
            file.write('\nEconomic=============================================\n')
            for key, value in self.economy.breakdown.items():
                file.write(f"  {key.capitalize()}: {value}\n")
            file.write('\nReligion=============================================\n')
            for key, value in self.religion.deities.items():
                file.write(f"  {key.capitalize()}: {value}\n")
            for key, value in self.religion.holidays.items():
                file.write(f"  {key.capitalize()}: {value}\n")
            file.write('\nMilitary=============================================\n')
            for key, value in self.military.profile.items():
                file.write(f"  {key.capitalize()}: {value}\n")
        print('File saved!')


            




# Example usage
if __name__ == "__main__":
    settlement_name = input("Enter the name of the settlement: ")
    seed = input('Enter seed: ')
    if seed == '':
        seed = str(random.randrange(sys.maxsize))
        random.seed(seed)
    population = input("Population: ")
    while str(type(population)) != "<class 'int'>":
        if population == '':
            break
        else:
            population = input("Population: ")
        try: population = int(population)
        except: pass
        print(type(population))
    random.seed = seed
    settlement = SettlementGenerator(settlement_name,population=population)
    settlement.display_details()
    settlement.save_details()
