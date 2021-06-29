import json
from os import name
import random
import LongSnake.Character
from LongSnake.Character import *
import LongSnake.Place
from LongSnake.Place import *
data = json.load(open('LongSnake/Names.json','r'))
nameList = data['names']

def create_character(home, name = '', age = 0, rank = 0):
    if (name == ''):
        number = random.randrange(0,len(nameList))
        name = nameList[number]
    if (age == 0):
        age = random.randrange(14, 70)
    return Character(name, age, rank, home)

town = Place("town")
house = Building(1,0, town)

house.set_parent(town)


char = create_character(house)
print (char.name + ', age: ' + str(char.age) + ', rank: ' + char.get_rank() + ', lives in: ' + char.home.name)