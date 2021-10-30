import json
import random
from random import choices
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
    
def create_item(name):
    number = 0
    if (items.__contains__(name)):
        number = items[name] +1
        items[name] = number
    if (number != 0):
        name = name+"_"+str(number)
    result = Item(name)
    if (name == 'knife'):
        result.properties.append("canCut")
    return result

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

def populate(min = 1, max = 4, item = False):
    number = random.randrange(min,max +1)
    ppl = []
    while (number > 0):
        char = create_character()
        if (item) :
            it = rndm_item()
            if (it != -1):
                char.inventory.append(it)
        ppl.append(char)
        number -=1
    return ppl

def rndm_item():
    numbers = [-1, 0, 1, 2, 3, 4]
    weights = [0.5,0.3,0.2,0.01,0.2,0.2]

    n = choices(numbers, weights)
    if (n[0] == -1):
        return -1
    return create_item(list(items.keys())[n[0]])

def populate_area(area, item = False):
    for x in area.sublocations:
        x.ppl = populate(item = item)

def create_village(name = '', main = -1):
    if main == -1:
        main = random.randrange(4,6)
    return create_town(0, random.randrange(3,6), random.randrange(0,3),random.randrange(3,7), random.randrange(0,2), main, name)

def print_area(town, plusppl = False, plusinv = False):
    print(town.name)
    for x in town.sublocations:
        print(x.name)
        if (plusppl):
            for y in x.ppl:
                print(y.name)
                if (plusinv):
                    for i in y.inventory:
                        print(i.name)
                print()
    print()

town1 = create_village(main=5)
populate_area(town1, True)
town2 = create_village(main=4)
populate_area(town2, True)
town3 = create_village(main=5)
populate_area(town3, True)
forrest = create_area(4)

print_area(town1)
print_area(town2)
print_area(town3, True, True)
print_area(forrest)

#print (char.name + ', age: ' + str(char.age) + ', rank: ' + char.get_rank() + ', lives in: ' + char.home.name)

