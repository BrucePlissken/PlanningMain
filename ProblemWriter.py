import json
import PDDLController
import pprint


class PddlProblemWriter:
    def __init__(self, domain):
        self.pdc = PDDLController.PDDLController(domain)
        file = open(domain)
        self.domain = file.read()
        file.close()
        self.domainName = self.domain.partition("domain")[2].partition(")")[0].split()[0]
        self.state = []
        #self.objects = self.define_object_types()
        

    def make_header(self, name):
        header = "(define (problem "+name+") (:domain "+self.domainName+")\n"
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

    #somtimes I wish I was writing in a functional language
    def unwrap_dict(self, dictionary):
        keys = dictionary.keys()
        keys = list(keys)

        probjects = ""
        initial = ""
        for k in keys:
            probjects = probjects + self.probject_string(k, dictionary[k])
            initial = initial + self.predicate_string(dictionary[k])
        return (probjects, initial)

    def predicate_string(self, thing):
        result = ""
        for t in thing:
            preds = t["predicates"]
            for k in preds:
                for x in preds[k]:
                    temp = "    " + parenthesise(k + " " + x + " "+ t["name"])
                    result = result + temp + "\n"
        return result

    def probject_string(self, probT, l):
        result = "    "
        for i in l:
            result = result + i["name"] + " "
        result = result + probT + "\n"
        return result

    def create_problem_file(self, name, probjects, initial, goals = ""):        
        path = "tmp/"+name + ".pddl"
        file = open(path, "w")
        file.write(self.make_header(name))
        file.close()
        file = open(path, "a")
        file.write("(:objects\n")
        file.write(probjects)
        file.write(")\n(:init\n")
        file.write(initial)
        file.write(")\n(:goal\n    (and\n    "+goals+"\n    )\n)\n")
        #file.write("(:metric minimize (total-cost))\n")
        file.write(")")
        file.close

def parenthesise(str):
    return "(" + str + ")"

    """
    def create_problem_file(self, name, probjects = False, initial = False, goals = ""):
        if not probjects:
            probjects = self.probjects
        if not initial:
            initial = self.initial
        
        path = "tmp/"+name + ".pddl"
        
        file = open(path, "w")
        file.write(self.make_header(name))
        file.close()

        file = open(path, "a")
        file.write("(:objects\n")
        keys = list(probjects.keys())
        for k in keys:
            if (probjects[k] != []):
                line = "    "
                for i in probjects[k]:
                    line = line + i + " "
                line = line + "- " +k +"\n"
                file.write(line)
        file.write(")\n(:init\n")
        for p in initial:
            file.write("    " +p+"\n")
        file.write(")\n(:goal\n    (and\n    "+goals+"\n    )\n)\n")
        #file.write("(:metric minimize (total-cost))\n")
        file.write(")")
        file.close

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
    """    


"""
pd = "tmp/AdventureDomCopy.pddl"

pd1 = "tmp/RedRidingHoodDom.pddl"

ppw = PddlProblemWriter(pd)

datac = {
    "- area" : [
        {   
            "name" : "stratholm",
            "predicates" : {
                "inarea" : ["farmhouse", "church", "manor"],
                "atloc" : ["dudeascii"]
                }
        },
        {
            "name" : "woods",
            "predicates" : {
                "inarea" : ["goblinlair", "clearing"]
                }
        },
        {
            "name" : "castle",
            "predicates" : {
                "inarea" : ["keep", "battlements", "cellar"]
                }
        }
    ],
    "- site" : [
        {
            "name" : "farmhouse",
            "predicates" : {
                "atloc" : ["farmer", "daughter"]
                }
        },
        {
            "name" : "church",
            "predicates" : {
                "atloc" : ["cleric"],
                "onground" : ["crusifix", "donationbox"]
                }
        },
        {
            "name" : "manor",
            "predicates" : {
                "atloc" : ["bailif"]
                }
        },
        {
            "name" : "goblinlair",
            "predicates" : {
                "atloc" : ["goblin"]
            }
        },
        {
            "name" : "clearing",
            "predicates" : {}
        },
        {
            "name" : "keep",
            "predicates" : {
                "atloc": ["lord", "lady"]
                }
        },
        {
            "name" : "battlements",
            "predicates" : {}
        }
    ],
    "- player" : [
        {
            "name" : "dudeascii",
            "predicates" : {
                "havething" : ["stick"],
                "cantrack" : [],
                }
        }
    ],
    "- npc" : [
        {
            "name" : "daughter",
            "predicates" : {}
        },
        {
            "name" : "farmer",
            "predicates" : {
                "knowinfo" : ["goblintracks"]
            }
        },
        {
            "name" : "cleric",
            "predicates" : {
                "havething" : ["holywater"]
            }
        },
        {
            "name" : "goblin",
            "predicates" : {
                "havething" : ["potion"],
                "havebodypart" : ["goblinhead"]
            }
        },
        {
            "name" : "lord",
            "predicates" : {
                "havething" : ["dagger"]
            }
        },
        {
            "name" : "bailif",
            "predicates" : {}
        },
        {
            "name" : "lady",
            "predicates" : {}
        }

    ],
    "- item" : [
        {
            "name" : "crusifix",
            "predicates" : {}
        },
        {
            "name" : "stick",
            "predicates" : {}
        },
        {
            "name" : "donationbox",
            "predicates" : {}
        },
        {
            "name" : "holywater",
            "predicates" : {}
        },
        {
            "name" : "potion",
            "predicates" : {}
        },
        {
            "name" : "dagger",
            "predicates" : {
                "cancut" : []
            }
        }
    ],
    "- trophy" : [
        {
            "name" : "goblinhead",
            "predicates" : {}
        }
    ],
    "- info" : [
        {
            "name" : "goblintracks",
            "predicates" : {}
        }
    ]

}  
        

thin = ppw.unwrap_dict(datac)
ppw.create_problem_file("OVERHERE", thin[0], thin[1])

"""

#data = json.load(open('world.json','r'))

#k = ppw.objectify(data)
#ppw.create_problem_file("experiments")
