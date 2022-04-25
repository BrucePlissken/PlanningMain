import os
import PDDLAccessor
from PDDLAccessor import *
import GiantTortoise
from GiantTortoise import GiantTortoise

class StoryTeller:
    def __init__(self, domainF, problemF, seed, api):
        tmp = "tmp/"
        problemS = PDDLAccessor.fileToString(tmp + problemF)
        self.giantTortoise = GiantTortoise(tmp+domainF, problemS, seed)
        self.pddlController = self.giantTortoise.pc
        self.startState = self.get_state(problemS)
        self.sasPlan = "..\sas_plan"
        self.planApi = api(domainF, problemF)
        self.problemF = problemF

    #uhm, "problem" is a bit of a mess, as a keyword here, it should be like new problem name or something instead,
    # n describes a number for making multiples, this probably shouldn't recide in this part of the code
    #all these checks should be done in a higher up method that activates these methods..
    def one_act(self, gene, state, n = 0, problem = ""):
        act = ""
        if (problem == ""):
            problem = self.problemF.partition(".")
            problem = problem[0] + str(n) + problem[1] + problem[2] 

        copyFile("tmp/"+self.problemF, "tmp/" + problem)

        if (state != ""):
            changeState("tmp/" + problem, state)

        goalGene = ""
        if type(gene) is str:
            goalGene = gene
        else:
            goalGene = self.giantTortoise.makeGoalGene(gene)
        
        changeGoal("tmp/"+problem, goalGene)

        self.planApi.prob = problem
        self.planApi.updateParams()

        output = self.planApi.get_plan(show = False)
        
        #in current configuration this isn't nescesarry(only because it is requested higher up) , it is useful for making multiple acts/bigger stories, but maybe that should be handled somewhere else in a different maner
        
        if (output != ""):
            act = output.splitlines()
            for x in act:
                if (x[0] == ";"):
                    break
                state = self.pddlController.apply_action_to_state(x, state, self.giantTortoise.thesaurus)
                if (state != ""):
                    changeState("tmp/" + problem, state)
            if (act[0][0] == ";"):
                act = ""

        os.remove("tmp/" + problem)
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
                gene1 = self.giantTortoise.mk_random_dna()
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
                gene1 = self.giantTortoise.mk_random_dna()
                act = self.one_act(gene1, story[1])
            acc.append(act)
            self.add_chapter(act, n, acc)
        else :
            return acc

    #returns a story, from a list of genes
    def write_story(self, genes, state = "", acc = [], n = 0):
        if (genes == []):
            return acc
        if (state == ""):
            state = self.startState
        gene = genes.pop(0)
        act = self.one_act(gene, state, n = n)
        acc.append(act)
        self.write_story(genes, act[1], acc, n)

        #returns a state e.g. the init section of a problem
    def get_state(self, problemString):
        return "    " + PDDLAccessor.getSection("init", problemString).rpartition(")")[0]
    
