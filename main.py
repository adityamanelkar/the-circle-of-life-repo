import time
import pandas as pd
from graph_utils import Graph
from agent import Agent
from predator import Predator
from prey import Prey

total_vertices = int(input("Enter the total vertices number: "))
agentNum = int(input("Enter the agent number: "))

agentChar = ""
if agentNum == 7 or agentNum == 8:
    agentChar = str(input("Enter a space if normal agent 7 or 8, else enter b: ")).strip()

num_runs = int(input("Enter the number of runs: "))
num_trials = int(input("Enter the number of trials per run: "))
max_steps = int(input("Enter the max number of steps each trial should run for: "))

start_time = time.time()

total_success = 0

# Run the agent/prey/predator game (based on input params)
for run in range(num_runs):

    success = {}
    fail_predator = {}
    fail_hang = {}

    time_steps = {}
    times_prey_known = {}
    times_pred_known = {}

    for trial in range(num_trials):
        success[trial] = fail_predator[trial] = fail_hang[trial] = 0

    for trial in range(num_trials):

        G = Graph()
        G.create_graph_tcol(total_vertices)

        # Spawn the agent
        a = Agent("agent" + str(agentNum) + agentChar, G)

        # Spawn Prey and Predator
        prey = Prey(G, a)
        predator = Predator(G, a)

        print("Initial Prey Position: "+str(prey.pos))
        print("Initial Predator Position: "+str(predator.pos))

        # By default set the agent as not caught
        caught_us = False
        caught_prey = False

        # Resetting time_steps - an upper bound of max_steps is used to make sure agent isn't running forever
        time_steps[trial] = 0
        times_prey_known[trial] = 0
        times_pred_known[trial] = 0

        while not caught_us and not caught_prey and time_steps[trial] < max_steps:

            time_steps[trial] += 1

            # MOVE AGENT
            if a.name == "agent1":
                a.move_1(G, prey.pos, predator.pos)
                times_pred_known[trial] += 1
                times_prey_known[trial] += 1
                print("Next position of Agent: " + str(a.node))


            elif a.name == "agent2":
                a.move_2(G, prey.pos, predator.pos, distracted=False)
                times_pred_known[trial] += 1
                times_prey_known[trial] += 1
                print("Next position of Agent: " + str(a.node))

            elif a.name == "agent3":
                if a.move_3(G, prey.pos, predator.pos, time_steps[trial]):
                    times_prey_known[trial] += 1
                times_pred_known[trial] += 1
                print("Next position of Agent: " + str(a.node))

            elif a.name == "agent4":
                if a.move_3(G, prey.pos, predator.pos, time_steps[trial]):
                    times_prey_known[trial] += 1
                times_pred_known[trial] += 1
                print("Next position of Agent: " + str(a.node))

            elif a.name == "agent5":
                if a.move_5(G, prey.pos, predator.pos, time_steps[trial]):
                    times_pred_known[trial] += 1
                times_prey_known[trial] += 1
                print("Next position of Agent: " + str(a.node))

            elif a.name == "agent6":
                if a.move_5(G, prey.pos, predator.pos, time_steps[trial]):
                    times_pred_known[trial] += 1
                times_prey_known[trial] += 1
                print("Next position of Agent: " + str(a.node))

            elif a.name == "agent7":
                (prey_known, pred_known) = a.move_7(G, prey.pos, predator.pos, time_steps[trial])
                if prey_known:
                    times_prey_known[trial] += 1
                if pred_known:
                    times_pred_known[trial] += 1
                print("Next position of Agent: " + str(a.node))

            elif a.name == "agent8":
                (prey_known, pred_known) = a.move_7(G, prey.pos, predator.pos, time_steps[trial])
                if prey_known:
                    times_prey_known[trial] += 1
                if pred_known:
                    times_pred_known[trial] += 1
                print("Next position of Agent: " + str(a.node))

            elif a.name == "agent7b":
                (prey_known, pred_known) = a.move_7(G, prey.pos, predator.pos, time_steps[trial])
                if prey_known:
                    times_prey_known[trial] += 1
                if pred_known:
                    times_pred_known[trial] += 1
                print("Next position of Agent: " + str(a.node))

            elif a.name == "agent8b":
                (prey_known, pred_known) = a.move_7(G, prey.pos, predator.pos, time_steps[trial])
                if prey_known:
                    times_prey_known[trial] += 1
                if pred_known:
                    times_pred_known[trial] += 1
                print("Next position of Agent: " + str(a.node))

            elif a.name == "agent9":
                (prey_known, pred_known) = a.move_9(G, prey.pos, predator.pos, time_steps[trial])
                if prey_known:
                    times_prey_known[trial] += 1
                if pred_known:
                    times_pred_known[trial] += 1
                print("Next position of Agent: " + str(a.node))

            elif a.name == "agent10":
                (prey_known, pred_known) = a.move_10(G, prey.pos, predator.pos, time_steps[trial])
                if prey_known:
                    times_prey_known[trial] += 1
                if pred_known:
                    times_pred_known[trial] += 1
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
            if a.name in ["agent1", "agent2", "agent3", "agent4"]:
                predator.move_predator(G, a)
            else:
                predator.move_distracted_predator(G, a)

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
        if not caught_us and not caught_prey and time_steps[trial] == max_steps:
            fail_hang[trial] = 1

    # End of trial

    df = pd.DataFrame()
    df["success"]= success.values()
    df["failure_predator"]= fail_predator.values()
    df["failure_timeout"]= fail_hang.values()
    file_name = "./agent_csv/agent" + str(agentNum) + agentChar + "/Run" + str(run) + '.csv'
    df.to_csv(file_name, encoding='utf-8')

    total_success += sum(list(success.values()))

    df_2 = pd.DataFrame()
    df_2["times_prey_known"] = times_prey_known.values()
    df_2["times_pred_known"] = times_pred_known.values()
    df_2["time_steps"] = time_steps.values()
    file_name_2 = "./know_csv/agent" + str(agentNum) + agentChar + "/Run" + str(run) + '.csv'
    df_2.to_csv(file_name_2, encoding='utf-8')

# End of runs

print("The total success percentage for the run was: [{}%]".format((total_success * 100) / (num_runs * num_trials)))

print("The time taken for {} runs ({} trials per run) was: [{}] seconds".format(num_runs, num_trials, round(time.time() - start_time, 2)))