import json
import random
from random import choices

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
    numbers = [0, 1, 2, 3, 4]
    weights = [0.2,0.2,0.2,0.2,0.01]

    n = choices(numbers, weights)

    item = prefabItems[n[0]]
    result = Item(item[0], item[1], item[2])
    return result

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

def dictify_area(area):
    result = area.__dict__

    items = []
    for i in area.items:
        items.append(i.__dict__)
    result["items"] = items

    ppl = []
    for p in area.ppl:
        ppl.append(dictify_character(p))
    result["ppl"] = ppl
    
    sublocations = []
    for s in area.sublocations:
        sublocations.append(dictify_site(s))
    result["sublocations"] = sublocations

    return result

def dictify_site(site):
    result = site.__dict__
    
    items = []
    for i in site.items:
        items.append(i.__dict__)
    result["items"] = items

    ppl = []
    for p in site.ppl:
        ppl.append(dictify_character(p))
    result["ppl"] = ppl
    
    return result

#print (char.name + ', age: ' + str(char.age) + ', rank: ' + char.get_rank() + ', lives in: ' + char.home.name)
def dictify_character(character):
    inventory = []
    for i in character.inventory:
        inventory.append(i.__dict__)
   
    result = character.__dict__
    result["inventory"] = inventory
   
    return result


town1 = create_village(main=5)
populate_area(town1, True)
town2 = create_village(main=4)
populate_area(town2, True)
town3 = create_village(main=5)
populate_area(town3, True)
forrest = create_area(4)
"""
print_area(town1)
print_area(town2)
print_area(town3, True, True)
print_area(forrest)
"""
town1 = dictify_area(town1)
town2 = dictify_area(town2)
town3 = dictify_area(town3)

world = {"area" : [town1,town2,town3]}

#print(town1)


with open('world.json', 'w') as fp:
    json.dump(world, fp)