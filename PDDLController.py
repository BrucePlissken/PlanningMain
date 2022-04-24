"""
Class for holding domain info and applying it to pddl problems stuff
auth: Jakob Ehlers
"""
import PDDLAccessor
import IntermediateParser
from IntermediateParser import *

#I decoupled the problem from this part of the code, if there is residue it is merely superstition on the coders part... this should be split into a domain holder and a problem controller
class PDDLController:
    def __init__(self, domain):#, prob):
        self.domainFile = domain
        #self.problemFile = prob
        self.domain = PDDLAccessor.fileToString(domain)
        #self.problem = PDDLAccessor.fileToString(prob)
        #
        #self.state = self.get_state(self.problem)

        #set up dicts for nested domain types
        self.pddltypes = self.mapTyps2("types", self.domain)
        #self.probjects = self.mapTyps("objects", self.problem)
        
        #loop for creating the list of dicts of actions
        self.actions = []
        n = self.domain.count("action")
        tempDom = self.domain
        while (n > 0):
            tempDom = tempDom.partition("action ")[2]
            action = PDDLAccessor.parseAction(tempDom.partition("\n")[0], self.domain)
            self.actions.append(action)
            n -= 1
        #loop for creating the list of domain predicates
        pred = PDDLAccessor.getSection("predicates", self.domain)
        predicates = pred.split('\n')
        self.predicates = []
        for x in predicates:
            temp = x.strip()
            if (len(temp) > 1):
                self.predicates.append(temp)

    #itterates the list of actions and returns an action with a matching name
    def getAction(self, name):
        for x in self.actions:
            if (x.get("name") == name):
                return x
        print("error: no such action name: " + name)

    #returns a dict with concrete parameters for replacing the variables
    def adjustParameters(self, action, params):
        paramargs = action.get("parameters") 
        result = {}
        params = params.partition(" ")[2]
        n = paramargs.count("?")
        x = 0
        while (x < n):
            paramargs = paramargs.partition("?")[2]

            if (paramargs.count(" ") > 0):
                s = "?" + paramargs.partition(" ")[0]
                result[s] = params.partition(" ")[0].replace(")", "")
            elif (paramargs.count(")") > 0):
                s = "?" + paramargs.partition(")")[0]
                result[s] = params.partition(")")[0]

            params = params.partition(" ")[2]
            x += 1

        return result

    #returns a dict of the different types in the domain, well actually only the super and sub-types
    def mapTyps(self, section, target):
        typs = PDDLAccessor.getSection(section, target)
        result = {}
        i = typs.count("-")
        while (i > 0):
            kvpair = typs.partition("-")
            k = "-" + kvpair[2].partition("\n")[0]
            v = kvpair[0].rpartition("\n")[2].split()
            result[k] = v
            typs = typs.partition(k)[2]
            i -=1
        
        return result

    def mapTyps2(self, section, target):
        typs = PDDLAccessor.getSection(section, target).partition(')')[0].strip().split('\n')
        result = {}
        for l in typs:
            if (l.__contains__("-")):
                kvpair = l.partition("-")
                k = "-" + kvpair[2].partition("\n")[0]
                v = kvpair[0].rpartition("\n")[2].split()
                result[k] = v
                #typs = typs.partition(k)[2]
            else:
                result['- '+(l.strip())] = []

        return result


    """
    #applies an action from an action string expression eg. (actionName arg1 arg2) with the variables filled out
    def applyAction(self, actionString, thesaurus):
        name = actionString.partition("(")[2].partition(" ")[0]
        action = self.getAction(name)
        #adds a dict with substitutions for the action parameters to the excisting dict of pddl types
        lookUpBook = {**self.adjustParameters(action, actionString), **thesaurus}#self.pddltypes}
        
        #check for precondition satisfaction
        if (applyFunction(action.get("precondition"), lookUpBook, precondCheck, self.state,True,andOp)):
            #applying the allowed change to self.state
            self.state = applyFunction(action.get("effect"), lookUpBook, applyEffect, self.state, self.state, andOp)
            return True
        #on failure:
        print("action "+ actionString + " NOT allowed")
        return False
    """

    #a flexible version of applyAction, that applies an action to a given state
    def apply_action_to_state(self, actionString, state, thesaurus):
        name = actionString.partition("(")[2].partition(" ")[0]
        action = self.getAction(name)
        #adds a dict with substitutions for the action parameters to the excisting dict of pddl types
        lookUpBook = {**self.adjustParameters(action, actionString), **thesaurus}
        #print(lookUpBook)
        #check for precondition satisfaction
        if (applyFunction(action.get("precondition"), lookUpBook, precondCheck, state,True,andOp)):
            #applying the allowed change to state
            state = applyFunction(action.get("effect"), lookUpBook, applyEffect, state, state, andOp)
            return state
        #on failure:
        print("action "+ actionString + " NOT allowed" )
        return ""

    #applies the current state (:init...) to the pddl problem file
    #can and should be disconnected from the class
    def writeChange(self):
        tmp = self.problem
        tmpfirst = tmp.partition("init")[0]+"init"
        tmplast = tmp.partition("(:goal")[2]
        result = tmpfirst + "\n" + self.state + ")\n(:goal" + tmplast
        file = open(self.problemFile, "w")
        file.write(result)
        file.close()

    #change the goal of the problem
    #was moved from this section of the code to StoryTeller.py
    
"""
#testing stuff beyond this point

import pprint
domainF = "tmp/AdventureDomCopy.pddl"
problemF = "tmp/AdventureProbCopycopy.pddl"

pc = PDDLController(domainF, problemF)

print("\npredicates:")
pprint.pprint(pc.predicates)
print("\ntypes:")
pprint.pprint(pc.pddltypes)
print("\nobjects:")
pprint.pprint(pc.probjects, sort_dicts= False)
"""