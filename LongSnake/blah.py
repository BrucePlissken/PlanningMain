import json
import Character
from Character import Character
import Place
from Place import Place
dutchy = Place("dutchy")
town = Place("town")
house = Place("house")


town.set_parent(dutchy)
house.set_parent(town)



user = Character("Ringo", 45, 0)
user.set_location(house)

user.set_rank(0)

print(user.get_rank())
list = user.get_location()

for i in list:
    print(i.name, end= " ")
