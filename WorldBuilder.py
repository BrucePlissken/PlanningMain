import json
import random
import pprint
from random import choices
from ProblemWriter import PddlProblemWriter
from LongSnake.PddlObjects import *

data = json.load(open('LongSnake/Names.json','r'))
nameList = data['names']
townNameList = data['towns']
seed1 = "treefitty"
seed2 = "the blood in my urine tastes too much of iron"
random.seed(seed2)

def create_character(name, whereabouts):
    if (name == ''):
        number = random.randrange(0,len(nameList))
        name = nameList.pop(number)
    char = {
            "name" : name,
            "predicates" : {
                "inventory" : [],
                "whereabouts" : whereabouts
            }
        }
    return char

def create_town_location(place, name = ''):
    if (name == ''):
        number = random.randrange(0,len(townNameList))
        name = townNameList.pop(number).split()[0]
        name = name+"_"+areas[place]
    loc = {
            "name" : name,                
            "predicates" : {
                "atloc" : []
            }
        }
    return loc

def create_site(number, building, parent, atloc = []):
    name = sites[building] + "_"
    if (number != 0):
        name = name +str(number) +"_"
    name = name + parent
    loc = {
            "name" : name,                
            "predicates" : {
                "atloc" : atloc
            }
        }
    return loc
    
def create_forrest(number):
    loc = {"location" : {
            "name" : "forrest_" + str(number),                
            "predicates" : {
                "atloc" : []
            }
        }
    }
    return loc

def create_town(placeType, houses, shops, farms, inns, mainBuilding, name = ''):
    result = []
    town = create_town_location(placeType, name)
    result.append(town)

    bighouse = create_site(0,mainBuilding,town["name"])
    town["predicates"]["atloc"].append(bighouse["name"])
    result.append(bighouse)
    while (houses > 0):
        house = create_site(houses,0,town["name"])
        town["predicates"]["atloc"].append(house["name"])
        result.append(house)
        houses -=1
    
    while (farms > 0):
        farm = create_site(farms,1,town["name"])
        town["predicates"]["atloc"].append(farm["name"])
        result.append(farm)
        farms -=1

    while (shops > 0):
        shop = create_site(shops,2,town["name"])
        town["predicates"]["atloc"].append(shop["name"])
        result.append(shop)
        shops -=1

    while (inns > 0):
        inn =create_site(inns,3,town["name"])
        town["predicates"]["atloc"].append(inn["name"])
        result.append(inn)
        inns -=1

    return result

def populate(whereabouts, min = 0, max = 4):
    number = random.randrange(min,max +1)
    ppl = []
    while (number > 0):
        char = create_character('', whereabouts)
        ppl.append(char)
        number -=1
    return ppl

def rndm_thing(holder, no):
    numbers = [0, 1, 2, 3, 4]
    weights = [0.2,0.4,0.3,0.2,0.01]
    n = random.choices(numbers, weights)
    thing = prefabthings[n[0]]
    result = {
        "name" : thing[0] +"_" + str(no),
        "predicates" : {
        }
        }
    holder[thing[1]].append(result)

def mk_things(no):
    result = {
        "- consumable" : [],
        "- weapon" : [],
        "- item" : []}
    for n in range(no):
        rndm_thing(result, n)
    return result

def populate_area(area):
    result = []
    for x in area[0]["predicates"]["atloc"]:
        pp = populate([x])
        result = result + pp
    return result

def get_character(world, character = ''):
    if (character == ''):
        n = random.randint(0, len(world["- character"]) -1)
        return world["- character"][n]

def grant_item(character, item):
    character["predicates"]["inventory"].append(item["name"])

def create_village(name = '', main = -1):
    if main == -1:
        main = random.randrange(4,6)
    return create_town(0, random.randrange(3,6), random.randrange(0,3),random.randrange(3,7), random.randrange(0,2), main, name)

"""
testing stuff

town1 = create_village(main=5)
ppl1 = populate_area(town1)
town2 = create_village(main=4)
ppl2 = populate_area(town2)
town3 = create_village(main=5)
ppl3 = populate_area(town3)
forrest = create_town_location(4)
items = mk_things(50)

world = {
    "- location" : town1 + town2 + town3 + [forrest],
    "- character" : ppl1 + ppl2 + ppl3
}
for c in items["- consumable"]:
    grant_item(get_character(world), c)
for w in items["- weapon"]:
    grant_item(get_character(world), w)
for i in items["- item"]:
    grant_item(get_character(world), i)

world.update(items)
#pprint.pprint(world)
dom = "tmp/CharacterPlanningDom.pddl"
ppw = PddlProblemWriter(dom)
thin = ppw.unwrap_dict(world)
ppw.create_problem_file("OVERHERE", thin[0], thin[1])
pprint.pprint(town1)
pprint.pprint(town2)
pprint.pprint(town3)
pprint.pprint(forrest)
town1 = dictify_area(town1)
town2 = dictify_area(town2)
town3 = dictify_area(town3)

world = {"area" : [town1,town2,town3]}

#print(town1)


with open('tmp/world.json', 'w') as fp:
    json.dump(world, fp, indent=4)
"""