import json
import random
import LongSnake.Character
from LongSnake.Character import Character
import LongSnake.Place
from LongSnake.Place import Place, Building

data = json.load(open('LongSnake/Names.json','r'))
nameList = data['names']
townNameList = data['towns']

def create_character(home, name = '', age = 0, rank = 0):
    if (name == ''):
        number = random.randrange(0,len(nameList))
        name = nameList[number]
    if (age == 0):
        age = random.randrange(14, 70)
    return Character(name, age, rank, home)

def create_town(type, name = ''):
    if (name == ''):
        number = random.randrange(0,len(townNameList))
        name = townNameList[number]
    return Place(name, type)

def create_building(number, type, parent):
    return Building(number, type, parent)

def create_forrest(number):
    return Place("forest " + str(number), 4)



town1 = create_town(0)
house = create_building(1,1,town1)
town1.set_child(town1)

char = create_character(house)
print (char.name + ', age: ' + str(char.age) + ', rank: ' + char.get_rank() + ', lives in: ' + char.home.name)