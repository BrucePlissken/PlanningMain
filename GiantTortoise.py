"""
Let's try to make a genetic algorithm
Auth: Jakob Ehlers
"""
import PDDLController
import IntermediateParser
from IntermediateParser import *
import random
import copy

class GiantTortoise:
    def __init__(self, domainF, problemF, seed = "the blood in my urine tastes too much like iron"):
        self.pc = PDDLController.PDDLController(domainF, problemF)
        #self.goalPredicates = self.getGoalPredicates()
        pist = []
        for action in self.pc.actions:
            pist = pist + applyFunction(action["effect"],self.pc.pddltypes, listyfy, "",pist,andOp)
        result = []
        for effect in pist:
            if (effect.split()[0] == "(not"):
                k = 1
            else: k = 0
            for pred in self.pc.predicates:
                if (pred.count(effect.split()[k]) > 0):
                    if (k == 1):
                        temp = "(not " + pred + ")"
                        break
                    else:
                        temp = pred
                        break
            if (result.__contains__(temp) == False):
                result.append(temp)        
        self.goalPredicates = result



        self.thesaurus = {**self.expandDict(self.pc.pddltypes, self.pc.probjects, "- "), **self.pc.probjects}

        self.genome = [len(self.goalPredicates)] + self.mapGenome(self.thesaurus)
        if (seed != ""):
            random.seed(seed)
        
        #making a random gene from the genome for goalpredicates
        """
        for p in range(1000):
            dna = self.mk_random_dna()
        """
#            print(self.makeGene(dna, self.goalPredicates))


    #returns a list of lists of ints with the numbers shuffeled
    def mk_random_dna(self):
        gene = []
        for x in self.genome:
            temp = range(0,x)
            temp = list(temp)
            random.shuffle(temp)
            gene.append(temp)
        return gene

    #creates a list of achievable goal-state expressions from action effects and domain predicates
    def getGoalPredicates(self):
        result = []
        temp = ""
        for action in self.pc.actions:
            for effect in action["effect"]["and"]:
                ton = False
                if (type(effect) is dict):
                    #let's try skipping the "nots" and instead add them later on, by checking against the current state
                    #this introduces another issue however, where a not clause can cause an unachievable goal. Seems the safer route is to check for both
                    #or let's ignore not alltogether
                    #todo include foralls and when
                    #continue
                    if (list(effect.keys()).__contains__("not")):
                        ton = True
                        effect = effect["not"]
                    elif (list(effect.keys()).__contains__("forall")):
                        effect = effect["forall"][1]
                        print(effect)
                        
                    else: continue
                for pred in self.pc.predicates:
                    if (pred.count(effect.split()[0]) > 0):
                        if (ton):
                            temp = "(not " + pred + ")"
                            break
                        else:
                            temp = pred
                            break
                if (result.__contains__(temp) == False):
                    result.append(temp)
        return result

    #expand definitions so upper categories include sub's content
    def expandDict(self, super_dict, sub_dict, prefix = ""):
        result = {}
        for x in super_dict:
            temp = []
            for k in super_dict[x]:
                key = prefix + k
                if (list(super_dict.keys()).__contains__(key)):
                    for p in super_dict[key]:
                        pey = prefix + p
                        if(list(sub_dict.keys()).__contains__(pey)):
                            temp = temp + sub_dict[pey]        
                if(list(sub_dict.keys()).__contains__(key)):
                    temp = temp + sub_dict[key]
            result[x] = temp

        return result

    def makeGoalGene(self, dna):
        return self.makeGene(dna, self.goalPredicates)

    #returns a gene from an int[] by popping the first int and picking the complying expression from the pool, and using the rest of the list as choices for substitution
    def makeGene(self, dna, pool):
        cellShell = dna[0][0]

        cellShell = pool[cellShell]
        result = self.substituteVar(cellShell, dna)
        #to "not" or not to "not"
        """
        if (self.pc.state.count(result) > 0):
            result = "(not " + result + ")"
        print(result)
        """
        return result

    #takes in an expression and, if no variable is given the first, ?smth variable that gets substituted with a fitting string from the thesaurus
    #maybe this should be made more general and put in the parser
    def substituteVar(self, predicate, rootdna):
        result = predicate
        dna = copy.deepcopy(rootdna)
        while (result.count("?") > 0):    
            temp = result.partition("?")
            variable = "?" + temp[2].partition(" ")[0]
            signifier = temp[2].partition("- ")[2].partition(")")[0]

            if(signifier.count(" ") > 0):
                signifier = signifier.partition(" ")[0]
            signifier = "- " + signifier
            p = 1
            for x in self.thesaurus:
                if (x == signifier):
                    no = dna[p].pop(0)
                p += 1
            value = self.thesaurus[signifier][no]

            result = result.replace(variable,value)

            if (result.partition(signifier)[0].count("?") < 1):
                signifier = " " + signifier
                result = result.replace(signifier, "")
        return result

    #returns a list of ints from the length of the lists of parameter possibilities of the expression
    def mapGenome(self, source):
        result = []
        for x in source:
            temp = len(source[x])
            result.append(temp)
        
        return result


"""
testing stuff
"""        
"""
import pprint


pd = "tmp/AdventureDomCopy.pddl"
pp = "tmp/AdventureProbCopycopy.pddl"

pd1 = "RedRidingHoodDom.pddl"
pp1 = "RedRidingHoodProb.pddl"

pp2 = "RedHoodProbTwo.pddl"

tmp = "tmp/"
dna = GiantTortoise(tmp+pd1,tmp+pp1)

pprint.pprint(dna.thesaurus, sort_dicts=False)


for x in dna.goalPredicates:
    print(x)


print(dna.genome)
print()
pprint.pprint(dna.pc.probjects)
print()
pprint.pprint(dna.pc.pddltypes)

"""