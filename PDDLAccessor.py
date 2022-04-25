"""
Methods for accessing the pddl files
Auth: Jakob Ehlers
"""

import IntermediateParser

#returns a file as string opening and closing    
def fileToString(fileName):
    temp = open(fileName)
    result = temp.read().lower()
    temp.close()
    return result

#returns a given section by counting parenthesis, n value should be set to 0 if starting outside a parenthesis
def getSection(name, target, n = 1):
    temp = target.partition(name)[2].lstrip()
    result = ""
    for x in temp:
        result = result + x
        if (x == "("):
            n += 1
        elif (x == ")"):
            n -= 1
        if (n < 1):
            break
    return result

#returns a dict modelled on "PDDL (:action..."
def parseAction(name, domain):
    actionString = getSection("action " + name, domain)
    if (actionString == ""):
        print("no such action")

    parameters = getSection("parameters", actionString, 0)
    precondition = getSection("precondition", actionString, 0)
    effect = getSection("effect", actionString,0)

    params = IntermediateParser.whiteSpaceMatters(parameters)
    preco = IntermediateParser.parsePddlExpression(precondition)
    effe = IntermediateParser.parsePddlExpression(effect)

    action =   {"name" : name,
                "parameters" : params,
                "precondition" : preco,
                "effect" : effe
                }
    return action


def copyFile(source, newFile):
    openFile = open(source)
    fileContent = openFile.read()
    openFile.close()
    openFile = open(newFile, "w")
    openFile.write(fileContent)
    openFile.close()

def changeGoal(prob, newGoal, newFile = ""):
    if (newFile == ""):
        newFile = prob
    file = open(prob)
    tmp = file.read()
    file.close()
    tmp = tmp.partition("(:goal")
    result = tmp[0] + tmp[1] + "\n    (and " + newGoal + ")\n  )\n)"
    #print(result)
    file = open(newFile, "w")
    file.write(result)
    file.close()

def changeState(prob, newState, newFile = ""):
    if (newFile == ""):
        newFile = prob
    file = open(prob)
    tmp = file.read()
    file.close()
    tmp = tmp.partition("(:init")
    result = tmp[0] + tmp[1] + "\n" + newState + ")\n(:goal" + tmp[2].partition("(:goal")[2]
    file = open(newFile, "w")
    file.write(result)
    file.close()

def printPlan(plan):
    openPlan = open(plan)
    print(openPlan.read())
    openPlan.close()
"""
#testing stuff beyond this point

import pprint
domainF = "tmp/AdventureDomCopy.pddl"
problemF = "tmp/AdventureProbCopycopy.pddl"

domain = fileAsString(domainF)
actions = []
n = domain.count("action")
tempDom = domain
while (n > 0):
    tempDom = tempDom.partition("action ")[2]
    action = parseAction(tempDom.partition("\n")[0], domain)
    actions.append(action)
    n -= 1

for x in actions:
    pprint.pprint(x, sort_dicts= False)
    pass
"""