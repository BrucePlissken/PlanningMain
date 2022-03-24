import json
import random
#import LongSnake.Character
#from LongSnake.Character import Character
#import LongSnake.Place
#from LongSnake.Place import Place, Building
#import LongSnake.PddlObjects
from LongSnake.PddlObjects import *

data = json.load(open('LongSnake/Names.json','r'))
nameList = data['names']
townNameList = data['towns']
seed1 = "treefitty"
seed2 = "the blood in my urine tastes too much like iron"
random.seed(seed2)

def create_character(name = ''):
    if (name == ''):
        number = random.randrange(0,len(nameList))
        name = nameList.pop(number)
    return Character(name)

def create_area(place, name = ''):
    if (name == ''):
        number = random.randrange(0,len(townNameList))
        name = townNameList.pop(number).split()[0]
        name = name+"_"+areas[place]
    return Area(name)

def create_site(number, building, parent):
    if (number != 0):
        return Site("_"+sites[building]+"_"+str(number), parent.name)
    return Site("_"+sites[building], parent.name)
    

def create_forrest(number):
    return Area("forrest_" + str(number))

def create_town(placeType, houses, shops, farms, inns, mainBuilding, name = ''):
    town = create_area(placeType, name)

    while (houses > 0):
        town.sublocations.append(create_site(houses,0,town))
        houses -=1
    
    while (farms > 0):
        town.sublocations.append(create_site(farms,1,town))
        farms -=1

    while (shops > 0):
        town.sublocations.append(create_site(shops,2,town))
        shops -=1

    while (inns > 0):
        town.sublocations.append(create_site(inns,3,town))
        inns -=1

    town.sublocations.append(create_site(0,mainBuilding,town))
    town.sublocations.reverse()

    return town

def populate()
    
def create_village(name = '', main = -1):
    if main == -1:
        main = random.randrange(4,6)
    return create_town(0, random.randrange(3,6), random.randrange(0,3),random.randrange(3,7), random.randrange(0,2), main, name)

def print_area(town):
    print(town.name + ":")
    for x in town.sublocations:
        print(x.name)
    print()

town1 = create_village(main=5)
town2 = create_village(main=4)
town3 = create_village(main=5)
forrest = create_area(4)

print_area(town1)
print_area(town2)
print_area(town3)
print_area(forrest)

#print (char.name + ', age: ' + str(char.age) + ', rank: ' + char.get_rank() + ', lives in: ' + char.home.name)

