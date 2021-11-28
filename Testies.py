import SimplePddlParser
from SimplePddlParser import *
import FDApi
from FDApi import FD_Api
import os

dom = "AdventureDomCopy.pddl"
#prob = "experiments.pddl"
#prob = "AdventureProb.pddl"
prob1 = "AdventureProbCopy.pddl"

prob = "AdventureProbCopycopy.pddl"

sasPlan = "..\sas_plan"
tempPlan = "tempPlan.txt"
tmpDir = "tmp/"

goal1 = "(and\n        (atball ball1 roomb)\n        (atball ball2 roomb)\n        (atball ball3 roomb)\n        (atball ball4 roomb)\n        )"
goal2 = "(and\n        (atball ball1 rooma)\n        (atball ball2 rooma)\n        (atball ball3 rooma)\n        (atball ball4 rooma)\n        )"


goal3 = "(and (ismissing girl) (atloc girl lair))"
goal4 = "(atLoc girl farm) ) (:metric minimize (total-cost)"
goal5 = "(and (havething bailiff goblinhead) )) (:metric minimize (total-cost)"
goal6 = "(and (havething bailiff goblinhead) (not (isMissing girl)) )) (:metric minimize (total-cost)"
goal7 = "(and (havething bailiff vampireheart) (forall (?cha - npc) (not (ismissing ?cha)) ) )) (:metric minimize (total-cost)"
goal8 = "(and (havething bailiff vampireheart) )) \n(:metric minimize (total-cost)"
ap = ActionParser(tmpDir+dom,tmpDir+prob)
changeGoal(tmpDir+prob, goal5)
fdapi = FD_Api(dom, prob)
def applyPlan(plan, writeChange = False):
    openPlan = open(plan)
    while (True):
        planAction = openPlan.readline().partition("\n")[0]
        if (planAction.count(";") > 0):
            break
        if (ap.applyAction(planAction)):# & writeChange):
            
            print("plan-step allowed")
            break
            #ap.writeChange()
    openPlan.close()

def applyPlanAction(plan, writeChange = False):
    openPlan = open(plan, "r")
    planAction = openPlan.read().partition("\n")
    openPlan.close()
    if (planAction[0].count(";") > 0):
        #print("reached end of plan")
        return False
    if (ap.applyAction(planAction[0])):
        #print("plan-step allowed")
        if(writeChange):
            openPlan = open(plan, "w")
            openPlan.write(planAction[2])            
            openPlan.close()
            #ap.writeChange()
    else :
        return False
    return True
    

def printPlan(plan):
    openPlan = open(plan)
    print(openPlan.read())
    openPlan.close()

def savePlan(plan, fileName):
    openPlan = open(plan)
    planString = openPlan.read()
    openPlan.close()
    openPlan = open(fileName, "w")
    openPlan.write(planString)
    openPlan.close()


#SimplePddlParser.changeGoal(prob, goal1)
def runPlanner():

    output = fdapi.rumBriber(fdapi.parameters, False)#.wait()



    if (os.path.exists(sasPlan)):
        savePlan(sasPlan, tempPlan)
        print("plan exists")
        thing = True
        p = True
    else: 
        output = fdapi.rumBriber(fdapi.parameters, True)#.wait()
        print("plan failed")
        thing = False
        p = False

    while (thing):
        thing = applyPlanAction(tempPlan, True)


    if p:
        print()
        printPlan(sasPlan)
        print(ap.state.partition("init")[2])
        os.remove(sasPlan)
        return True

    return False


if (runPlanner()):
    ap.writeChange()
   # changeGoal(tmpDir+prob, goal5)
    #if (runPlanner()):
     #   ap.writeChange()    


savePlan(tmpDir+prob1, tmpDir+prob)

"""
ap.ppActions()
print(output)
print(ap.actions)
for x in ap.actions:
    x.pp()
SimplePddlParser.changeGoal(prob, goal2)
FDApi.rumBriber(FDApi.parameters).wait()
printPlan(sasPlan)
applyPlan(sasPlan)
"""

"""


import os
import subprocess


import sys
sys.path.append('../')

import os.path

import argparse

from planning import *
from planning_graph.planning_graph import *
from planning_graph.planning_graph_planner import GraphPlanner

from downward.driver import tests
from downward.driver import run_components
from downward.driver import plan_manager
from downward.driver import arguments
from downward.driver import main

#magic from fast-downward
DRIVER_DIR = os.path.abspath(os.path.dirname(__file__))
REPO_ROOT_DIR = os.path.dirname(DRIVER_DIR)
BUILDS_DIR = os.path.join(REPO_ROOT_DIR, "builds")


#planner = plan_manager.PlanManager('plannies')

parameters = [
    #"downward\\misc\\tests\\benchmarks\\gripper\\domain.pddl",
    #"downward\\misc\\tests\\benchmarks\\gripper\\prob01.pddl",
    "PlanningMain\\tmp\\dom.pddl",
    "PlanningMain\\tmp\\prob.pddl",
    "--search-options",
    #"--evaluator",
    #"hff=ff()", 
    #"--evaluator",
    #"hcea=cea()", 
    #"--debug",
     
    #"--run all",
    "--search",
    #"lazy_greedy([hff, hcea], preferred=[hff, hcea])"
    
    "astar(cegar())",
    #"--sas-file"
    

    # casual graph virker ikke so far
    # "cg(max_cache_size=1000000, transform=no_transform(), cache_estimates=true)"
    
    #"merge_and_shrink(transform=no_transform(), cache_estimates=true, merge_strategy, shrink_strategy, label_reduction=<none>, prune_unreachable_states=true, prune_irrelevant_states=true, max_states=-1, max_states_before_merge=-1, threshold_before_merge=-1, verbosity=normal, main_loop_max_time=infinity)"

    #"ff(transform=no_transform(), cache_estimates=true)"

    ]

def rumBriber(par):
    cmd = [sys.executable, "downward/fast-downward.py"] + par
    return subprocess.check_call(cmd, cwd=REPO_ROOT_DIR)

rumBriber(parameters)

#tests.run_driver(parameters)



tests.test_commandline_args()
tests.test_aliases()
tests.test_automatic_domain_file_name_computation()
tests.translate()
tests.cleanup()

cmd = [sys.executable, "fast-downward.py"] + parameters
subprocess.check_call(cmd, cwd=REPO_ROOT_DIR)

" ".join([os.path.basename(sys.argv[0])] + parameters)
args = arguments.parse_args()

#args = run_components.run_translate(args)

run_components.run_search(args)


thing = '(print "testLisp.lisp")'
but = hy_parse(thing)

butt = hy.eval(but)
#print(butt)




#bait = _hy_code_from_file("testLisp.lisp")

domain = "tmp/dwr.pddl"
problem = "tmp/dwrp.pddl"

#def RunPlan():
planning_graph = PlanningGraph(domain, 
                            problem,
                            visualize=True)

graph = planning_graph.create(max_num_of_levels=10)
graph.visualize_png("generated_graph.png")


goal = planning_graph.goal
graph_planner = GraphPlanner()
layered_plan = graph_planner.plan(graph, goal)
if(layered_plan != None):
    print(layered_plan.data)
    for k in layered_plan.data:
        for o in (layered_plan.data[k]._plan) :
            print(o.operator_name + ": ")
            print (o.variable_list.values())
            print(o.effect_pos)
else: 
    print("whap whap")

print(planning_graph.initial_state)
print(planning_graph.goal)


n = 0
while n < 10:
    RunPlan()
    n = n+1


blah = pddlpy.DomainProblem(domain,problem)
blah.vargroundspace


data = json.load(open('LongSnake\Baker.json','r'))
init = data['initial']
goal = data['goal']
dom = data['domain']

action = []


for k in data['actions']:
    a = Action(k, data['actions'][k]['PRECONDITION'],data['actions'][k]['EFFECT'],data['actions'][k]['DOMAIN'])
    action.append(a)




pp = PlanningProblem(initial = init,goals = goal,actions = action, domain = dom)


print(GraphPlan(pp).execute())


#print(socks_and_shoes_graphPlan())

i = 0


poper = PartialOrderPlanner(pp)
#pop = poper.execute()




print(pp.goal_test())

pp.act(expr('Walk(Baker, Home, Mill)'))
pp.act(expr('Take(Baker, Flour, Mill)'))
pp.act(expr('Walk(Baker, Mill, Bakery)'))
pp.act(expr('Take(Baker, Water, Bakery)'))


pp.act(expr('MixDough(Baker, Flour, Water)'))
pp.act(expr('Walk(Baker, Bakery, Home)'))



print(pp.initial)




#print(pp.expand_actions())



print(pp.goal_test())





st = socks_and_shoes()
fpp = PartialOrderPlanner(st)

flop = GraphPlan(st)

#print(flop.extract_solution(pp.goals, 0))

pop.execute()
fpp.execute()

print(st.initial)
print(st.goals)

print(pp.initial)
print(pp.goals)
print(pp.actions)

print(pop.causal_links)
print(pop.constraints)
print(pop.actions)

print(fpp.causal_links)
print(fpp.constraints)
print(fpp.actions)

PartialOrderPlanner(st).execute()
#print(pp.domain)



#rwpp = RealWorldPlanningProblem(init,goal,actions)




"""


"""
PartialOrderPlanner(pp).execute()
pop.execute()

print(GraphPlan(pp).execute())
print(PartialOrderPlanner(pp).causal_links)

st = spare_tire()

bl = three_block_tower()
poppy = PartialOrderPlanner(bl)
poppy.execute()
#print(consLinks[0])
#print(consLinks[1])


#print(socks_and_shoes_graphPlan())
print(spare_tire_graphPlan())

#plan = PartialOrderPlanner(pp)
#plan.execute
"""



