import pddlpy
import planning
from planning import *

domain = "tmp/dom.pddl"
problem = "tmp/prob.pddl"
blah = pddlpy.DomainProblem(domain,problem)

"""
st = spare_tire()

bl = three_block_tower()
poppy = PartialOrderPlanner(bl)
poppy.execute()
"""
st = socks_and_shoes()
#print(consLinks[0])
#print(consLinks[1])

pop = PartialOrderPlanner(st)
consLinks = pop.execute()

print(socks_and_shoes_graphPlan())
#print(spare_tire_graphPlan())

#plan = PartialOrderPlanner(pp)
#plan.execute



