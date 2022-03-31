import time
import random
import Critic
import copy
import json
import PlanApi
from PlanApi import Plan_Api
import StoryTeller

pd = "AdventureDomCopy.pddl"
pp = "AdventureProbCopycopy.pddl"

pd1 = "RedRidingHoodDom.pddl"
#pp1 = "RedRidingHoodProb.pddl"

pp2 = "RedHoodProbTwo.pddl"

l2 = "tmp/Adventurelex.json"
l1 = "tmp/RedRidingLex.json"

lex = json.load(open(l1))

desiredCurve = [1,2,-2]

st = StoryTeller.StoryTeller(pd1, pp2, lex, "", api = PlanApi.Cloud_Planner_Api)

def contains_duplicate_dna(story, dnaList):
    for i in dnaList:
        if(st.genePool.dna_is_same(i[2],story[2])):
            return True
    return False

def split_story_dna_full(stories):
    dnaNo = len(stories) -1
    result = []
    for strandNo in range(dnaNo):
        if (len(stories[strandNo][2]) > 1):
            temp = copy.deepcopy(stories[strandNo][2])
            for g in temp:
                story = st.one_act([g], st.startState)
                result.append(story)
    return result

#no reason to write out the story when the dna is the active part
def split_story_dna(stories):
    dnaNo = len(stories) -1
    result = []
    for strandNo in range(dnaNo):
        if (len(stories[strandNo][2]) > 1):
            temp = copy.deepcopy(stories[strandNo][2])
            for g in temp:
                story = ([""],"",[g])
                result.append(story)
    return result 

def other_gene_story(noS, generations = 100):
    fnoS = int(noS/4)
    temp = st.story_book(int(fnoS))
    storybook = []
    #blackList = []
    for s in temp:
        storybook.append(s[0])

    
    #print(storybook)
    for gen in range(generations):
        print(gen)
    #    print(len(storybook))
        arrangedStories = []
        for s in storybook:
            if not contains_duplicate_dna(s,arrangedStories):
                arrangedStories.append(s)
            """
            addit = True
            for a in arrangedStories:
                if (st.genePool.dna_is_same(a[2],s[0][2])):
                    addit = False
            if addit:
                arrangedStories.append(s[0])
            """

        def critic_holder(story):
            plancurve = st.plan_to_curve(story[0])
            if (plancurve == ([0], [0])):
                return 2
            result = Critic.curve_comparer(plancurve,([0,1,2,3,4,5,6],[0,1,2,2.5,3,1.5,0]))
            
            divi = (len(plancurve[0]))
            #print(divi)
            result = result/divi
            #print(plancurve)
            #print(result)
            return result

        arrangedStories.sort(key = critic_holder)
        for sto in range(len(arrangedStories)):
            if (sto > len(arrangedStories) - 1):
                #print ("kaplah!")
                #print(len(arrangedStories))
                break
            topgrade = critic_holder(arrangedStories[sto])
            if (topgrade == 2):
                arrangedStories.pop(sto)
                continue
            """
            print("---- Story Time ! ----")
            print(st.plan_to_curve(arrangedStories[sto][0]))
            print(topgrade)
            print(st.genePool.makeGoalGene(arrangedStories[sto][2]))
            print(arrangedStories[sto][0])
            print()
            """
                
            if(topgrade < 0.02):
                #print("---- Story Time ! ----")
                #print(arrangedStories[0][0])
                return arrangedStories[:noS]    

        genes = copy.deepcopy(arrangedStories[:fnoS])
        genes = genes + split_story_dna(arrangedStories[:fnoS])
        nextGen = []
        #this needs to be made dynamic
        #while (len(nextGen) < noS -1):
        for tr in range(int(noS)):
            #print(tr)
            g = random.choice(genes)
            #n = random.randint(0,99)
            #if n < 10:
            g = st.genePool.mutate_dna(g[2], genes)
            addit = True
            #print(g)
            for p in nextGen:
                if (st.genePool.dna_is_same(p[2], g)):
                    #print("naddit")
                    addit = False
                    break
            if addit:
                #print("addit")
                g = st.one_act(g, st.startState)
                #print("")
                #print(g)
                if (not g[0] == ''):
                    nextGen.append(g)


        storybook = arrangedStories[:fnoS] + nextGen
        #print(storybook)

    return arrangedStories

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
        
        storybook = nextGen + st.story_book(fnoS, acts) + storybook[:fnoS]

    """
    storybook.sort(key = st.asses_story_by_states)
    print(st.asses_story_by_states(storybook[0]))
    print(storybook[0][0][0])
    print(storybook[0][1][0])
    print(storybook[0][2][0])
    """

t1 = time.time()
funk = []
for k in range(3):
    temp = other_gene_story(20)
    funk.append(temp)
    t2 = time.time()
    print(t2 - t1)
    print(k)

for f in funk:
    print(f[0][0])
    
    #for s in f:
    #    print(len(s[2]))

    print()

t2 = time.time()
print(t2 - t1)
print(k)
