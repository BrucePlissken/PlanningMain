import re

def prsExp(expstr):

    if (expstr[0:4] == "and "):
        result = andOrLoop(expstr)
        #print("ending *and")
        return {"and" : result}
    
    if (expstr[0:4] == "not "):
        #print("hit 'not'")
        return {"not" : prsExp(nextExpr(expstr)[1])}

    if (expstr[0:3] == "or "):
        #print("hit 'or'")
        result = andOrLoop(expstr)
        return {"or" : result}

    if (expstr[0:7] == "exists "):
        #print("hit exists-loop")
        result = andOrLoop(expstr)
        return {"exists" : result}

    if (expstr[0:7] == "forall "):
        #print("hit forall-loop")
        result = andOrLoop(expstr)
        return {"forall" : result}

    if (expstr[0:9] == "increase "):
        #print("hit increase")
        return {"increase" : prsExp(nextExpr(expstr)[1])}

    if (isSingleExpr(expstr)):
        return expstr
    #print("reached end")
    return "not intended"

#check to see if the string contains a bare-bones expression statement
def isSingleExpr(expstr):
    if (expstr.count("(") == 0):
        return True
    return False

#loops through expressions comming in line
def andOrLoop(expstr):
    result = []
    expr = nextExpr(expstr)
    while (True):
        #print(result)
        result.append(prsExp(expr[1]))
        if (expr[2] == ")"):
            break
        expr = nextExpr(expr[2])

    return result
#strips outer parenthensis and returns the next expression in line
def nextExpr(exprString):
    i = 1
    result = ""

    for x in exprString.partition("(")[2]:
        if (x == "("):
            i += 1
        if (x == ")"):
            i -= 1
        if (i == 0):
            if (result != ""):
                thingy = exprString.partition(result)
                return thingy
            else:
                print("Kurt Carpenter")
                return False
        result += x

#outer method for convenience of running the parser
def parsePddlExpression(expression):
    return prsExp(nextExpr(whiteSpaceMatters(expression))[1])

#removes most of the whitespace between expressions
def whiteSpaceMatters(expression):
    result = re.sub("\s*\(", "(", expression)
    result = re.sub("\)\s*", ")", expression)
    return result

"""
pfff = " (and (not (atloc ?char ?from)) (atloc ?char ?to)\n    (increase (total-cost) 2)\n    ))\n"
pff = "(and (atLoc ?char1 ?from) (atLoc ?char2 ?from) (not (isSecret ?to))\n(isAvailable ?char2) (or (and (not (isSus ?char2)) (not (isBound ?char2))) (and (isSus ?char2) (isBound ?char2))) (exists (?sus - monster) (or (not (atLoc ?sus ?from)) (isDead ?sus)\n)))\n)"
#print(whiteSpaceMatters(pfff))
#print(parsePddlExpression(pfff))
pf = "(and (atLoc ?char1 ?from) (atLoc ?char2 ?from) (isAvailable ?char2))"
p = "(atLoc ?char1 ?from)"
f ="(not (isSecret ?to))"    
"""