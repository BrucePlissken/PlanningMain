import FDApi
from FDApi import FD_Api
import os
import pprint
import GiantTortoise
from GiantTortoise import GiantTortoise
import time
import random
import threading

class StoryTeller:
    def __init__(self, domainF, problemF, lex, seed):
        tmp = "tmp/"
        self.genePool = GiantTortoise(tmp+domainF, tmp+problemF, seed)
        self.pddlController = self.genePool.pc
        self.startState = self.genePool.pc.state
        self.sasPlan = "..\sas_plan"
        self.fdapi = FD_Api(domainF, problemF)
        self.problemF = problemF
        self.lex = lex

    #uhm, problem is a bit of a mess here, it should be like new broblem name or something instead,
    # n describes a number for making multiples, this probably shouldn't recide in this part of the code
    #all these checks should be done in a higher up method that activates these methods..
    def one_act(self, gene, state, problem = "", n = 0):
        act = ""
        if (problem == ""):
            problem = self.problemF.partition(".")
            problem = problem[0] + str(n) + problem[1] + problem[2] 

        copyFile("tmp/"+self.problemF, "tmp/" + problem)

        if (state != ""):
            changeState("tmp/" + problem, state)



        goalGene = ""
        if type(gene) is tuple:
            print("error: ")
            print(gene)
            for g in gene:
                goalGene = goalGene + " " + self.genePool.makeGoalGene(g)
        else:
            goalGene = self.genePool.makeGoalGene(gene)
        
        changeGoal("tmp/"+problem, goalGene)

        self.fdapi.prob = problem
        self.fdapi.updateParams()
        if (os.path.exists(self.sasPlan)):
            os.remove(self.sasPlan)
        
        output = self.fdapi.rumBriber(self.fdapi.parameters, False)
        
        if (os.path.exists(self.sasPlan)):
            act = getPlan(self.sasPlan)
            act = act.splitlines()
            for x in act:
                if (x[0] == ";"):
                    break
                state = self.pddlController.apply_action_to_state(x, state, self.genePool.thesaurus)
                if (state != ""):
                    changeState("tmp/" + problem, state)
            if (act[0][0] == ";"):
                act = ""
        return (act, state, gene)
    
    #input ints for amount of stories and acts of the stories
    #returns a list of random, (but different (first act dependant)) stories (list of acts (tupple: (plan, state, gene)))
    def story_book(self, amount, acts = 1, startState = "", maxRev = 100):
        storybook = []
        rejects = []
        n = 0
        storyStart = ("", "fart", [])

        if (startState == ""):
            startState = self.startState

        while (len(storybook) < amount and n < maxRev):
            story = storyStart
            while (story[0] == ""):
                writeStory = True
                gene1 = self.genePool.mk_random_dna()
                for gene in rejects:
                    k = 1
                    for pos in range(0, len(gene)):
                        if (list(gene1[pos]) == list(gene)[pos]):
                            k += 1
                            if (k == len(gene)):
                                writeStory = False
                            
                if writeStory:
                    story = self.one_act(gene1, startState)
                    if (story != False):
                        rejects.append(gene1)
            newStory = True
            for s in storybook:
                if (list(s[0]) == list(story[0])):
                    newStory = False
                    rejects.append(story[2])
            if newStory:
                #storybook.append(story)
                temp = []
                temp.append(story)
                if (acts > 1):
                    self.add_chapter(story, acts -1, temp)
                #print(n)
                storybook.append(temp)
            n += 1
        return storybook

    #returns a list of acts, that follow an original act
    #the accumulator should be fed in with the first act attatched, if a complete story is desired
    def add_chapter(self, story, n = 1, acc = []):
        if n > 0 :
            n -= 1
            #this is a version of an "empty" act
            act = [""]
            while(act[0] == ""):
                gene1 = self.genePool.mk_random_dna()
                act = self.one_act(gene1, story[1])
            acc.append(act)
            self.add_chapter(act, n, acc)
        else :
            return acc

    #returns a story, from a list of genes
    def write_story(self, genes, state = "", acc = []):
        if (genes == []):
            return acc
        if (state == ""):
            state = self.startState
        gene = genes.pop(0)
        act = self.one_act(gene, state)
        acc.append(act)
        self.write_story(genes, act[1], acc)

    def asses_story_by_states(self, story, startState = "", ideal = [0,1,2,-2], other = [1,1,-1]):
        xy = []
        #xz = []
        result = 0.0
        if (startState == ""):
            startState = self.startState
            startVal = self.asses_act_from_state(["",startState], ideal[0])

        x = 0
        xy.append(startVal)
        state = startState
        for act in story:
            if (state == act[1]):
                result += 1.0
            if (act[0] == ""):
                result += 1
            state = act[1]
            #z = sum(self.asses_act_from_plan(act[0], self.lex))
            result += self.asses_act_from_state(act, ideal[x+1])# - startVal
            #xy.append(y)
            #xz.append(z)
            x += 1

        """
        x = 0
        for z in xz:
            print(z)
            if (other[x] == z):
                print("z")
                print(z)
                result = result / (x+2)
            x += 1
        """
        
        return result

    def asses_act_from_plan(self, plan, lex):
        result = []
        for action in plan:
            n = 0
            for key in lex:
                action.count(key) * lex[key]
            result.append(n)
        return result

    def asses_act_from_state(self, story, aim = 0):
        lex = self.lex
        result = 0
        state = story[1]
        if (story[0] == ""):
            return 4
#        print(story[0])
        for key in lex:
            result += state.count(key) * lex[key]
 #       print(aim)
  #      print(result)
        result = abs(aim - result)
   #     print (result)
        return result

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

def getPlan(plan):
    openPlan = open(plan)
    result = openPlan.read()
    openPlan.close()
    return result

pd = "tmp/AdventureDomCopy.pddl"
pp = "tmp/AdventureProbCopycopy.pddl"

pd1 = "RedRidingHoodDom.pddl"
#pp1 = "RedRidingHoodProb.pddl"

pp2 = "RedHoodProbTwo.pddl"

t1 = time.time()

lex = {
        "isswallowed" : 1,
        "issaved" : -1,
        "(swallow" : 1,
        "(slay" : -1
        }

st = StoryTeller(pd1, pp2, lex, "")
"""
import numpy
import matplotlib.pyplot as plt
import scipy.optimize

plah = numpy.poly([0.0, 0.6, 0.8, 0.9, 1.0])
print(plah)
curb = numpy.polyfit([0.0,0.33,0.66,1.0], [0,0.5,1,0], 3)
print(curb)
plah = numpy.diff(plah)
print(plah)
plt.figure(num=0,dpi=120)
N = 50
xlist = numpy.linspace(0,1,N)
ylist = numpy.polyval(plah,xlist)

plt.plot(xlist,ylist)

def normalize_curve(curve):
    maxy = max(curve)
    maxx = len(curve) -1
    print(maxx)
    x = []
    y = []
    n = 0
    for point in curve:
        y.append(point/maxy)
        x.append(n/maxx)
        n+=1
    return x,y

curvay = normalize_curve([0,1,2,2,2,3,3,4,1,6,0])
print(curvay)


curvsy = numpy.polyfit(curvay[0],curvay[1], 5)
#curv = scipy.optimize.curve_fit(f, curvay[0], curvay[1], (0,0,0,0,0), sigma=sigma)
#curv = scipy.optimize.curve_fit(f, curvay[0], curvay[1], (0,0,0,0,0))
ylist1 = numpy.polyval(curvsy,xlist)
#plt.plot(xlist,f(xlist,*curv))
plt.plot(xlist,ylist1)

"""
acts = 3

storybook = st.story_book(10, acts)

desiredCurve = [1,2,-2]

for gen in range(100):
    print(gen)

    storybook.sort(key = st.asses_story_by_states)

    genes = []
    for n in range(acts):
        arrangedActs = []
        for s in storybook:
            arrangedActs.append(s[n])

        def dickhole(story):
            return st.asses_act_from_state(story, desiredCurve[n])

        arrangedActs.sort(key = dickhole)
        topActs = arrangedActs[:20]
        genes.append(topActs)
    topGrade = st.asses_story_by_states(storybook[0])
    print("---- Story Time ! ----")
    print(storybook[0][0][0])
    print(storybook[0][1][0])
    print(storybook[0][2][0])
    print(topGrade)
    if(topGrade == 0):
        break
    """
    for g in genes[0]:
        print(g)


    print(st.asses_story_by_states(storybook[0]))



    fart = []
    for s in storybook:
        fart.append(st.asses_story_by_states(s))
    
    print(fart)

    bestStories = storybook[:10]
    genes = []
    for s in bestStories:
        gene = []
        for g in s:
            gene.append(g[2])
        genes.append(gene)
    """

    #print(genes)

    nextGen = []

    for tr in range(100):
        n = random.randint(0,99)
        if n < 15:
            g0 = st.genePool.mk_random_dna()
        else:
            g0 = random.choice(genes[0])[2]
        if 14 < n < 30:
            g1 = st.genePool.mk_random_dna()
        else:
            g1 = random.choice(genes[1])[2]
        if 29 < n < 45:
            g2 = st.genePool.mk_random_dna()
        else:
            g2 = random.choice(genes[2])[2]

        newGene = [g0,g1,g2]
    #    print(newGene)
        stary = []

        st.write_story(newGene, st.startState, stary)
        nextGen.append(stary)

    """
    
    for _ in range(10):
        g0 = random.choice(genes)
        g1 = random.choice(genes)
        g2 = random.choice(genes)

        newGene = [g0[0],g1[1],g2[2]]
        stary = []
        st.write_story(newGene, st.startState, stary)
        nextGen.append(stary)
    """    
    
    storybook = nextGen


storybook.sort(key = st.asses_story_by_states)
print(st.asses_story_by_states(storybook[0]))
print(storybook[0][0][0])
print(storybook[0][1][0])
print(storybook[0][2][0])




"""
fart = []
for s in storybook:
    fart.append(st.asses_story_by_states(s, startVal))

print(fart)

"""



t2 = time.time()

print(t2 - t1)




"""
for s in storybook:
    for c in s:
        print(c[0])
"""



"""
tempo = []
for s in storybook[0]:
    tempo.append(s[2])
fart = []
st.write_story(tempo, "", fart)

for farts in fart:
    print(farts[0])



bigBook = []
n = 2
#bigBook.append(storybook)
for s in storybook:
    temp = []
    temp.append(s)
    st.add_chapter(s,n, temp)
    #story = []
    #print(s[0])
    #nextChapter = st.story_book(n,s[1])
    #story.append(s)

    #hump = []
    #for p in nextChapter:
    #    lastChapter = st.story_book(n,p[1])
    #    stairy = BranchingBook(p, lastChapter)
    #    stairy.children = lastChapter
    #    hump.append(stairy)

    #temp = BranchingBook(s)
    #print(temp)
    #print(temp.get_stories())
    #temp.children = hump

#    print(hump[0].get_stories())
    #print(s[0])
    #print(nextChapter[0][0])
    #spleen = st.genePool.makeGoalGene(s[2])
    #print(spleen)
#    print(temp)
#    print("fart")
    bigBook.append(temp)

#print (bigBook)

for b in bigBook:
#    print(b)
    #print(b.get_stories())
    print("---- Story Time ! ----")
    for s in b:
        print(s[0])
       # pass
"""

"""
storybook = st.multiple_act(3)


print(storybook)

for s in storybook:
    print(s[0])

storybook = []

rejects = []
n= 0
while (len(storybook) < 10 and n < 100):
    story = storyStart
    while (story[0] == ""):
        writeStory = True
        gene1 = st.genePool.mk_random_dna()
        for gene in rejects:
            k = 1
            for pos in range(0, len(gene)):
                if (list(gene1[pos]) == list(gene)[pos]):
                    k += 1
                    if (k == len(gene)):
                        #print("duplicate ")
                        writeStory = False
                    
        #gene2 = st.genePool.mk_random_dna()
        #gene3 = st.genePool.mk_random_dna()
        if writeStory:
            story = st.one_act(gene1, st.startState)
            if (story[0] == ""):
                rejects.append(gene1)
        #print(gene1)
        #story = st.multiple_act([gene1,gene2,gene3])
    newStory = True
    for s in storybook:
        if (list(s[0]) == list(story[0])):
            newStory = False
            rejects.append(story[2])
    if newStory:
        storybook.append(story)
        print(n)
    n += 1
"""


#pprint.pprint(storybook)
"""
gene1 = [[3, 4, 1, 7, 0, 5, 2, 6], [1, 2, 0], [0, 3, 1, 2], [0, 1, 2]]
gene2 = [[3, 4, 1, 7, 0, 5, 2, 6], [1, 2, 0], [1, 0, 3, 2], [0, 1, 2]]
gene3 = [[1, 3, 2, 5, 4, 0], [0, 1, 2], [0, 1, 3, 2], [2, 1, 0]]
big bad wolf at grannies house [[1, 0, 6, 7, 5, 2, 4, 3], [2, 0, 1], [2, 1, 0, 3], [2, 0, 1]]
"""

#geneus = [[7, 0, 1, 5, 2, 4, 3, 6], [0, 2, 1], [1, 2, 3, 0], [1, 2, 0]]
#geneus = [[1, 0, 1, 5, 2, 4, 3, 6], [0, 2, 1], [0, 2, 3, 0], [2, 2, 0]]
#geneus = [[3, 0, 2, 6, 7, 4, 5, 1], [1, 0, 2], [0, 2, 1, 3], [1, 2, 0]]

#print(st.genePool.makeGoalGene(geneus))
#story = st.one_act((gene1,gene2), st.startState)

#print(st.genePool.makeGoalGene(gene2))
#print(st.genePool.makeGoalGene(gene3))
#print(gene1)
#print(story[0])

"""
tmp = "tmp/"
dna = GiantTortoise(tmp+pd1,tmp+pp1)
n = 0
p=0
fdapi = FD_Api(pd1, pp2)

while (n < 100):
    gene = dna.makeGene(dna.mk_random_dna(), dna.goalPredicates)

    changeGoal(tmp+pp1, gene, tmp+pp2)

    output = fdapi.rumBriber(fdapi.parameters, False)#.wait()

    sasPlan = "..\sas_plan"
    if (os.path.exists(sasPlan)):
        printPlan(sasPlan)
        print(gene)
        p += 1
        print(p)
    n +=1

"""
