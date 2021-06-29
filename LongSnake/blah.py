import json
import random
import Character
from Character import Character
import Place
from Place import Building, Place

dutchy = Place("dutchy")
town = Place("town")
house = Building(1,0)

town.set_parent(dutchy)
house.set_parent(town)

data = json.load(open('Names.json','r'))
nameList = data['names']


def create_character(name = '', age = 0, rank = 0):
    if (name == ''):
        number = random.randrange(0,len(nameList))
        name = nameList[number]
    if (age == 0):
        age = random.randrange(14, 70)
    return Character(name, age, rank)


user = create_character()
user.set_location(house)

print(user.name)
print(user.age)
print(user.get_rank())
list = user.get_location()

for i in list:
    print(i.name, end= " ")
