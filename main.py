from graph_utils import Graph
import random
import math
import time
import agent
from predator import Predator
from prey import Prey
import statistics

total_vertices = int(input("Enter the total vertices number: "))
agentNum = int(input("Enter the agent number: "))
num_runs = int(input("Enter the number of runs: "))
num_trials = int(input("Enter the number of trials per run: "))

total_success_count = 0
total_failure_1_count = 0
total_failure_2_count = 0

success_rates = []
failure_1_rates = []
failure_2_rates = []

# Run the agent/prey/predator game (based on input params)
for run in range(num_runs):

    success_count = 0
    failure_1_count = 0
    failure_2_count = 0

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
                break

            elif a.node == prey.pos :
                caught_prey = True
                break           

            # MOVE PREY (Randomly)
            prey.move_prey(G)

            # CHECK IF CAUGHT OR NOT
            if a.node == predator.pos :
                caught_us = True
                break

            elif a.node == prey.pos :
                caught_prey = True
                break

            # MOVE PREDATOR (Shortest path to agent)
            predator.move_predator(G, a)

            # CHECK IF CAUGHT OR NOT
            if a.node == predator.pos:
                caught_us = True
                break

            elif a.node == prey.pos:
                caught_prey = True
                break
        
        # End of movement while loop
    
        # Check what was the reason of exiting the while loop and update the counters

        if caught_prey:
            success_count += 1
        
        elif caught_us:
            failure_1_count += 1
        
        elif timeSteps > maxSteps:
            failure_2_count += 1

    # End of trial

    success_rate = success_count / num_trials
    failure_1_rate = failure_1_count / num_trials
    failure_2_rate = failure_2_count / num_trials

    print("For run {} we have the following data:\n".format(run))
    print("Success Rate: [{}] Failure 1 Rate: [{}] Failure 2 Rate: []".format(success_rate, failure_1_rate, failure_2_rate))

    success_rates.append(success_rate)
    failure_1_rates.append(failure_1_rate)
    failure_2_rates.append(failure_2_rate)

    total_success_count += success_count
    total_failure_1_count += failure_1_count
    total_failure_2_count += failure_2_count

# End of runs

print("Success Rate for all runs is: [{}]".format(total_success_count / (num_runs * num_trials)))
print("Failure 1 Rate for all runs is: [{}]".format(total_failure_1_count / (num_runs * num_trials)))
print("Failure 2 Rate for all runs is: [{}]".format(total_failure_2_count / (num_runs * num_trials)))

print("Standard deviation for Success Rates from each of the runs is: [{}]".format(statistics.pstdev(success_rates)))
print("Standard deviation for Failure 1 Rates from each of the runs is: [{}]".format(statistics.pstdev(failure_1_rates)))
print("Standard deviation for Failure 2 Rates from each of the runs is: [{}]".format(statistics.pstdev(failure_2_rates)))