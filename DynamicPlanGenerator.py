import time
import random
import Critic
import copy
import json
import PlanApi
import StoryTeller

class DPG():
    def __init__(self, planDomain, planProblem, lexicon, seed = "", api = PlanApi.FD_Api, tensionCurve = ([0,1,2,3,4,5,6],[0,1,2,2.5,3,1.5,0])):
        self.storyTeller = StoryTeller.StoryTeller(planDomain, planProblem, seed, api)
        self.tensionCurve = tensionCurve
        self.lex = lexicon

    def gene_story(self, noS, fnoS = 0, inoS = 0, maxGenerations = 100, acceptanceCriteria = 0.02):
        if (fnoS < 1):
            fnoS = int(noS/4)
        if (inoS < 1):
            inoS = fnoS
          
        temp = self.storyTeller.story_book(inoS)
        storybook = []
        for s in temp:
            storybook.append(s[0])
        
        for gen in range(maxGenerations):
            print(gen)
            arrangedStories = []
            #I don't think this check is nescesary since it is also done when adding new genes
            for s in storybook:
                if not self.contains_duplicate_dna(s,arrangedStories):
                    arrangedStories.append(s)
            """
            arrangedStories = storybook
            """

            arrangedStories.sort(key = self.critic_holder)
            for sto in range(len(arrangedStories)):
                if (sto > len(arrangedStories) - 1):
                    break
                grade = self.critic_holder(arrangedStories[sto])
                #if the grade of the story is sufficiently bad, reject it..
                if (grade >= 2):
                    arrangedStories.pop(sto)
                    continue

                #if a story is good enough end the gene-run early default is 0.02    
                if(grade < acceptanceCriteria):
                    return arrangedStories[:noS]

            genes = copy.deepcopy(arrangedStories[:fnoS])
            genes = genes + self.split_story_dna(arrangedStories[:fnoS])
            nextGen = arrangedStories[:fnoS]

            for tr in range(int(noS)):
                g = random.choice(genes)
                g = self.storyTeller.giantTortoise.mutate_dna(g[2], genes)
                addit = True

                for p in nextGen:
                    if (self.storyTeller.giantTortoise.dna_is_same(p[2], g)):
                        addit = False
                        break

                if addit:
                    g = self.storyTeller.one_act(g, self.storyTeller.startState)
                    if (not g[0] == ''):
                        nextGen.append(g)

            storybook = nextGen

        return arrangedStories

    def critic_holder(self, story):
        plancurve = self.plan_to_curve(story[0])
        if (plancurve == ([0], [0])):
            return 2
        result = Critic.curve_comparer(plancurve,self.tensionCurve)
        
        divi = (len(plancurve[0]))
        result = result/divi
        return result

    def contains_duplicate_dna(self, story, dnaList):
        for i in dnaList:
            if(self.storyTeller.giantTortoise.dna_is_same(i[2],story[2])):
                return True
        return False

    def split_story_dna_full(self, stories):
        dnaNo = len(stories) -1
        result = []
        for strandNo in range(dnaNo):
            if (len(stories[strandNo][2]) > 1):
                temp = copy.deepcopy(stories[strandNo][2])
                for g in temp:
                    story = self.storyTeller.one_act([g], self.storyTeller.startState)
                    result.append(story)
        return result

    #no reason to write out the story when the dna is the active part
    def split_story_dna(self, stories):
        dnaNo = len(stories) -1
        result = []
        for strandNo in range(dnaNo):
            if (len(stories[strandNo][2]) > 1):
                temp = copy.deepcopy(stories[strandNo][2])
                for g in temp:
                    story = ([""],"",[g])
                    result.append(story)
        return result
        
    def story_to_plan_curve(self,story):
        temp = []
        for act in story:
            temp.append(self.plan_to_curve(act[0]))
        result = self.curve_merger(temp)
        return result

    def plan_to_curve(self, plan):
        x = [0]
        y = [0]
        for action in plan:
            a = action.split()[0]
            if (a in self.lex['plan']):
                x.append(x[len(x) -1] + self.lex['plan'][a][0])
                y.append(y[len(y)-1] + self.lex['plan'][a][1])
        result = (x,y)
        #print(result)
        return result

"""
test stuff

"""

pd = "tmp/AdventureDomCopycopy.pddl"
pp = "tmp/AdventureProbCopycopycopy.pddl"

pd1 = "tmp/RedRidingHoodDom.pddl"
pp1 = "tmp/RedHoodProbTwo.pddl"

pd2 = "tmp/CharacterPlanningDom.pddl"
pp2 = "tmp/OVERHERE.pddl"
l = "tmp/Adventurelex.json"
l1 = "tmp/RedRidingLex.json"

t1 = time.time()

thing = DPG(pd1, pp1, json.load(open(l1)))#, api=FD_Api)#, "hoppitty")

#pprint(thing.storyTeller.giantTortoise.thesaurus)

pft = thing.storyTeller.planApi.get_plan()
if pft == "":
    print ("error")
    exit()
#print(pft)

"""
funk = []

print(thing.storyTeller.giantTortoise.genome)

for k in range(1):
    temp = thing.gene_story(20, fnoS= 5, inoS= 5, maxGenerations= 20, acceptanceCriteria = 0.02)
    funk.append(temp)
    t2 = time.time()
    print(t2 - t1)
    print(k)

for f in funk:
    for s in range(3):
        print()
        print(f[s][0])
        print()

    #for s in f:
    #    print(len(s[2]))

    print()

t2 = time.time()
print(t2 - t1)

gotta rewamp stuff beyond this point
"""

"""
def first_gene_story(acts, noS, maxGen = 1000):
    fnoS = int(noS/4)
    storybook = st.story_book(fnoS, acts)

    for gen in range(maxGen):
        print(gen)

        genes = []
        for n in range(acts):
            arrangedActs = []
            for s in storybook:
                addit = True
                for a in arrangedActs:
                    #pa = st.genePool.makeGoalGene(a[2])
                    #ap = st.genePool.makeGoalGene(s[n][2])
                    if (st.genePool.dna_is_same(a[2],s[n][2])):
                        addit = False
                #if s[n] not in arrangedActs:
                if addit:
                    arrangedActs.append(s[n])

            def dickhole(story):
                return st.asses_act_from_state(story, desiredCurve[n])

            arrangedActs.sort(key = dickhole)
            topActs = arrangedActs[:noS]
            genes.append(topActs)

        stary = [genes[0][0]]
        newGene = []
        newGene.append(genes[1][0][2])
        newGene.append(genes[2][0][2])
        st.write_story(newGene, genes[0][0][1], stary)
        storybook.append(stary)

        storybook.sort(key = st.asses_story_by_states)

        topGrade = st.asses_story_by_states(storybook[0])
        grades = []
        for s in storybook:
            grades.append(st.asses_story_by_states(s))

        print(grades)
        print("")
        print("curve grade:")
        plancurve = st.story_to_plan_curve(storybook[0])
        if(max(plancurve[0]) > 0 and max(plancurve[1]) > 0):
            print(plancurve)
            curveGrade = Critic.curve_comparer(plancurve,([0,1,2,3],[0,1,2,0]))
        else:
            curveGrade = "empty plan curve"
        print(curveGrade)
        print("")
            
        #print(topGrade)
        if(topGrade == 0):
            print("---- Story Time ! ----")
            print(storybook[0][0][0])
            print(storybook[0][1][0])
            print(storybook[0][2][0])
            break

        #print(genes)

        nextGen = []
        #this needs to be made dynamic
        for tr in range(30):
            
            g0 = random.choice(genes[0])
            n = random.randint(0,99)
            if n < 10:
                st.genePool.mutate_dna(g0[2], genes, 0)
                g0 = st.one_act(g0[2], st.startState)
                #print(g0)
            
            n = random.randint(0,99)
            g1 = random.choice(genes[1])[2]
            if n < 10:
                st.genePool.mutate_dna(g1, genes, 1)

            n = random.randint(0,99)        
            g2 = random.choice(genes[2])[2]
            if n < 10:
                st.genePool.mutate_dna(g2, genes, 2)

            newGene = [g1,g2]
            stary = []
            stary.append(g0)
            st.write_story(newGene, g0[1], stary, tr)
            nextGen.append(stary)
            #t1 = threading.Thread(st.write_story(newGene, g0[1], stary, tr))
            #t1.start()

#        for _ in range(10):
#            g0 = random.choice(genes)
#            g1 = random.choice(genes)
#            g2 = random.choice(genes)
#
#            newGene = [g0[0],g1[1],g2[2]]
#            stary = []
#           st.write_story(newGene, st.startState, stary)
#            nextGen.append(stary)
        
        storybook = nextGen + st.story_book(fnoS, acts) + storybook[:fnoS]

    #storybook.sort(key = st.asses_story_by_states)
    #print(st.asses_story_by_states(storybook[0]))
    #print(storybook[0][0][0])
    #print(storybook[0][1][0])
    #print(storybook[0][2][0])
"""


"""
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

#        x = 0
#        for z in xz:
#            print(z)
#            if (other[x] == z):
#                print("z")
#                print(z)
#                result = result / (x+2)
#            x += 1
        
        return result

    def asses_act_from_state(self, story, aim = 0):
        lex = self.lex
        result = 0
        state = story[1]
        if (story[0] == ""):
            return 4
#        print(story[0])
        for key in lex['state']:
            result += state.count(key) * lex['state'][key]
 #       print(aim)
  #      print(result)
        result = abs(aim - result)
   #     print (result)
        return result

    def curve_merger(self, curves):
        x = [0]
        y = [0]
        for curve in curves:
            curve[1].pop(0)
            curve[0].pop(0)
            for t in curve[0]:
                x.append(x[len(x) -1] + t)
            for v in curve[1]:
                y.append(y[len(y) -1] + v)
                
        result = (x,y)
        return result

"""