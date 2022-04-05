class Location:
    def __init__(self, name):
        self.name = name
        self.onground = []
        self.atloc = []

class Area(Location):
    def __init__(self, name):
        super().__init__(name)
        self.inarea = []

class Site(Location):
    def __init__(self, name, parentLocation_name):
        super().__init__(name)
        self.name = parentLocation_name + name

class Character:
    def __init__(self, name):
        self.name = name
        self.can = []
        self.knows = []
        self.havething = []
        self.havebodypart = []
        self.alive = True

class Item:
    def __init__(self, name, subtype = "item", properties = []):
        self.name = name
        self.subtype = subtype
        self.properties = properties

class Trophy(Item):
    def __init__(self, name):
        super().__init__(name)


prefabthings = [
    ["dagger", "weapon", ["cancut"]],
    ["stick", "weapon", []],
    ["bread", "consumable", []],
    ["crusifix", "item", []],
    ["poison", "consumable", ["poisonuos"]]
]
    
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
