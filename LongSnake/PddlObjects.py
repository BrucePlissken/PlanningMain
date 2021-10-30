class Location:
    def __init__(self, name):
        self.name = name
        self.items = []
        self.ppl = []

class Area(Location):
    def __init__(self, name):
        super().__init__(name)
        self.sublocations = []

class Site(Location):
    def __init__(self, name, parentLocation_name):
        super().__init__(name)
        self.name = parentLocation_name + name

class Character:
    def __init__(self, name):
        self.name = name
        self.skills = []
        self.knowledge = []
        self.inventory = []
        self.trophy = []
        self.alive = True

class Item:
    def __init__(self, name):
        self.name = name
        self.value = 0
        self.properties = []

class Weapon(Item):
    def __init__(self, name):
        super().__init__(name)

class Consumable(Item):
    def __init__(self, name):
        super().__init__(name)
        self.effect = []

class Trophy(Item):
    def __init__(self, name):
        super().__init__(name)


items = { 
    'stick' : 0,
    'knife': 0,
    'poison': 0,
    'bread': 0,
    'crusifix' : 0,
}
    
sites = [
    'house',
    'farm',
    'shop',
    'inn',
    'church',
    'manor',
    'keep',
    'lair',
    'cellar',
    'crypt'
]

areas = [
    'village',
    'town',
    'city',
    'castle',
    'forrest',
    'mountains'
]

#this needs a change, I think some sort of arbitrary integer
caste = [
    "serf",
    "freeman",
    "cleric",
    "bailiff",
    "duke",
    'merchant'
]
