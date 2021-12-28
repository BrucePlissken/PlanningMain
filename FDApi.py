import os
import subprocess
import sys
sys.path.append('../')

#magic from fast-downward
DRIVER_DIR = os.path.abspath(os.path.dirname(__file__))
REPO_ROOT_DIR = os.path.dirname(DRIVER_DIR)
BUILDS_DIR = os.path.join(REPO_ROOT_DIR, "builds")

#planner = plan_manager.PlanManager('plannies')
class FD_Api:
    def __init__(self, dom, prob):
        

        self.parameters = [
            #"downward\\misc\\tests\\benchmarks\\gripper\\domain.pddl",
            #"downward\\misc\\tests\\benchmarks\\gripper\\prob01.pddl",
            #"PlanningMain\\tmp\\domdom.pddl",
            #"PlanningMain\\tmp\\probcopy.pddl",
            #"--evaluator",
            #"hff=ff()", 
            #"--evaluator",
            #"hcea=cea()", 
            #"--debug",
            
            "PlanningMain\\tmp\\" +dom,
            "PlanningMain\\tmp\\" +prob,

            "--search-options",

            #"--run all",
            "--search",
            #"lazy_greedy([hff, hcea], preferred=[hff, hcea])"
            
            #"astar(lmcount(lm_rhw()))"
            #"astar(cegar())",
            #"--sas-file"
            #"astar(blind())"

            #"eager(epsilon_greedy(cegar()), verbosity=silent)"

            "astar(cg(max_cache_size=1000000, transform=no_transform(), cache_estimates=true))"
            
            #"merge_and_shrink(transform=no_transform(), cache_estimates=true, merge_strategy, shrink_strategy, label_reduction=<none>, prune_unreachable_states=true, prune_irrelevant_states=true, max_states=-1, max_states_before_merge=-1, threshold_before_merge=-1, verbosity=normal, main_loop_max_time=infinity)"

            #"ff(transform=no_transform(), cache_estimates=true)"

            ]

    #run driver
    def rumBriber(self, par, show = True):
        cmd = [sys.executable, "downward/fast-downward.py"] + par
        result = subprocess.run(cmd, cwd=REPO_ROOT_DIR, capture_output = not show)
        
        return result

#rumBriber(parameters)

#lmcount(lm_factory, admissible=false, optimal=false, pref=false, alm=true, lpsolver=CPLEX, transform=no_transform(), cache_estimates=true)