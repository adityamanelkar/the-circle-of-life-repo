from graph_utils import Graph
import random
import math
import time
import agent
from predator import Predator
from prey import Prey
import statistics
import pandas as pd

total_vertices = int(input("Enter the total vertices number: "))
agentNum = int(input("Enter the agent number: "))
num_runs = int(input("Enter the number of runs: "))
num_trials = int(input("Enter the number of trials per run: "))



# Run the agent/prey/predator game (based on input params)
for run in range(num_runs):



    for trial in range(num_trials):

        G = Graph()
        G.create_graph_tcol(total_vertices)

        # Spawn the agent
        a = agent.Agent("agent" + str(agentNum))

        # Spawn Prey and Predator
        prey = Prey(G, a)
        predator = Predator(G, a)

        print("Initial Prey Position: "+str(prey.pos))
        print("Initial Predator Position: "+str(predator.pos))

        # By default set the agent as not caught
        caught_us = False
        caught_prey = False

        success = {}
        fail_predator = {}
        fail_hang = {}

        # Resetting timeSteps (an upper bound of 1000) which is used to make sure agent isn't avoiding ghosts forever
        timeSteps = 0
        maxSteps = 100

        while not caught_us and not caught_prey and timeSteps < maxSteps:

            timeSteps += 1

            # MOVE AGENT
            if a.name == "agent1":
                a.move_1(G, prey.pos, predator.pos)
                print("Next position of Agent: " + str(a.node))

            # CHECK IF CAUGHT OR NOT
            if a.node == predator.pos :
                caught_us = True
                fail_predator[trial] = 1
                break

            elif a.node == prey.pos :
                caught_prey = True
                success[trial] = 1
                break           

            # MOVE PREY (Randomly)
            prey.move_prey(G)

            # CHECK IF CAUGHT OR NOT
            if a.node == predator.pos :
                caught_us = True
                fail_predator[trial] = 1
                break

            elif a.node == prey.pos :
                caught_prey = True
                success[trial] = 1
                break

            # MOVE PREDATOR (Shortest path to agent)
            predator.move_predator(G, a)

            # CHECK IF CAUGHT OR NOT
            if a.node == predator.pos:
                caught_us = True
                fail_predator[trial] = 1
                break

            elif a.node == prey.pos:
                caught_prey = True
                success[trial] = 1
                break
        
        # End of movement while loop
    
        # Check what was the reason of exiting the while loop and update the counters
        if not caught_us and not caught_prey  and timeSteps > maxSteps:
            hang = True
            fail_hang[trial] = 1

    # End of trial

    df = pd.DataFrame()
    df["success"]= success.values()
    df["failure_predator"]= fail_predator.values()
    df["failure_timeout"]= fail_hang.values()
    file_name = "./agent_csv/agent" + str(agentNum) + "/Run" + str(run) + '.csv'
    df.to_csv(file_name, encoding='utf-8')







# End of runs

