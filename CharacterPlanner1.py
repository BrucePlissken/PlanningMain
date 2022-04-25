import json
import PlanApi
from PlanningMain.PDDLAccessor import changeGoal
import ProblemWriter
import pprint
import random

class CharacterPlanner():
    def __init__(self, world, domain, problem = '', seed = '', planApi = PlanApi.Cloud_Planner_Api):
        self.writer = ProblemWriter.PddlProblemWriter("tmp/" +domain)
        self.planner = planApi(domain, problem)
        self.world_loc = "tmp/" + world
        self.domain = domain
        self.problem = problem
        self.world = self.open_world()
        if (seed != ''):
            random.seed(seed)

    def update_problem_address(self, problem):
        self.planner.prob = problem
        self.planner.updateParams()

    def run_planner(self):
        return self.planner.get_plan()

    def custom_problem(self, new_world, prob_name):
        temp = self.writer.unwrap_dict(new_world)
        self.writer.create_problem_file(prob_name, temp[0], temp[1])

    def open_world(self):        
        result = json.load(open(self.world_loc))
        return result

    def mk_agent(self, world, agent):
        world["- agent"] = [agent]

    def pop_character(self, world, character = ''):
        if (character == ''):
            n = random.randint(0, len(world["- character"]) -1)
            print(len(world["- character"]))
            print(n)
            return world["- character"].pop(n)
        #else:
        #    return world["- character"]
    def get_character(self, world, character = ''):
        if (character == ''):
            n = random.randint(0, len(world["- character"]) -1)
            print(len(world["- character"]))
            print(n)
            return world["- character"][n]
"""
testing stuff
"""

world = "world.json"
dom = "CharacterPlanningDom.pddl"
prob = "OVERHERE.pddl"

cp = CharacterPlanner(world, dom, prob)

plop = cp.pop_character(cp.world)
cp.mk_agent(cp.world, plop)
print(plop)
vict = cp.get_character(cp.world)
cp.custom_problem(cp.world, "OVERHERE")
goal = "(isdead " + vict["name"] + ")"
changeGoal("tmp/" + prob, goal)
#pprint.pprint(cp.world)
plan = cp.run_planner()
print()
print(plan)
"""
"""