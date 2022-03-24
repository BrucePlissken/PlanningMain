import json

class PddlProblemWriter:
    def __init__(self, domain):
        file = open(domain)
        self.domain = file.read()
        file.close()
        self.doname = self.domain.partition("domain")[2].partition(")")[0].split()[0]
        self.initial = []
        self.objects = self.define_object_types()
    
    def define_object_types(self):
        ot = self.domain.partition(":types")[2].partition(")")[0].split()
        result = {}
        n = 0
        while(n < len(ot)):
            t = ot[n]
            if (t == "-"):
                n = n+1
            else:
                result[t] = []
                n += 1
        print(result)
        return result

    def make_header(self, name):
        header = "(define (problem "+name+") (:domain "+self.doname+")\n"
        return header

    def objectify(self, dictionary):
        keys = dictionary.keys()
        keys = list(keys)


        for k in keys:
            area = dictionary[k]
            for n in area:
                self.objects[k].append(n["name"])
                self.relate_area(n)

        print(self.objects)
        #print(self.initial)
        return dictionary[k]


    def relate_area(self, area):
        name = area["name"]
        for i in area["things"]:
            pass
        for sl in area["sublocations"]:
            self.initial.append("(inArea " + sl["name"] + " "+ name+")")
            self.objects["site"].append(sl["name"])
            self.relate_site(sl)         
 
    def relate_site(self, site):
        name = site["name"]
        for p in site["ppl"]:
            self.initial.append("(atLoc " + p["name"] +" "+ name +")")
            self.objects["npc"].append(p["name"])
            self.relate_character(p)          

    def relate_character(self, character):
        name = character["name"]
        for s in character["skills"]:
            self.initial.append("("+s +" "+ name+ ")")

        for k in character["knowledge"]:
            self.initial.append("(knowInfo " +name +" "+ k+ ")")

        for i in character["inventory"]:
            self.initial.append("(havething " + name + " " + i["name"]+ ")")
            self.relate_thing(i)

        for t in character["trophy"]:
            self.objects["trophy"].append(t["name"])
            self.initial.append("(haveBodyPart " + name +" " + t + ")")

        if (character["alive"] == False):
            self.initial.append("(isDead " + name + ")")

    def relate_thing(self, thing):
        name = thing["name"]
        if (self.objects[thing["subtype"]].count(name) < 1):
            self.objects[thing["subtype"]].append(name)
            for p in thing["properties"]:
                self.initial.append("(" + p + " " + name + ")")

    def create_problem_file(self, name, goals = ""):
        path = "tmp/"+name + ".pddl"
        
        file = open(path, "w")
        file.write(self.make_header(name))
        file.close()

        file = open(path, "a")
        file.write("(:objects\n")
        keys = list(self.objects.keys())
        for k in keys:
            if (self.objects[k] != []):
                line = "    "
                for i in self.objects[k]:
                    line = line + i + " "
                line = line + "- " +k +"\n"
                file.write(line)
        file.write(")\n(:init\n")
        for p in self.initial:
            file.write("    " +p+"\n")
        file.write(")\n(:goal\n    (and\n    "+goals+"\n    )\n)\n")
        #file.write("(:metric minimize (total-cost))\n")
        file.write(")")
        file.close


ppw = PddlProblemWriter("tmp/AdventureDom.pddl")

data = json.load(open('world.json','r'))

k = ppw.objectify(data)
ppw.create_problem_file("experiments")