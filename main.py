import grapher
import random
import math
import time
import agent

total_vertices = int(input("Enter the total vertices number: "))
max_degree = int(input("Enter the maximum degree of each node in the graph: "))


agentNum = int(input("Enter the agent number: "))


# Run the agent/prey/predator game (based on input params)
for i in range(1):
    for j in range(1):

        G = grapher.create_graph(total_vertices,max_degree,0.5)


        # Spawn the agent
        a = agent.Agent("agent" + str(agentNum))

        # Spawn Prey and Predator
        preypos = random.randint(0,49)
        predpos = random.randint(0,49)


        print("Initial Prey Position: "+str(preypos))
        print("Initial Predator Position: "+str(predpos))
        print()




        # By default set the agent as not caught
        caught_us = False
        caught_prey = False


        # Resetting timeSteps (an upper bound of 1000) which is used to make sure agent isn't avoiding ghosts forever
        timeSteps = 0
        maxSteps = 1000

        while not caught_us and not caught_prey  and timeSteps < maxSteps:
            # MOVE AGENT
            if a.name == "agent1":

                a.move_1(G, preypos, predpos)
                print("Next position of Agent: "+str(a.node))

                # grapher.visualise_graph(G)

            # CHECK IF CAUGHT OR NOT
            if a.node == predator.node :
                caught_us = True
                break
            elif a.node == prey.node :
                caught_prey = True
                break

            

            # MOVE PREY (Randomly)





            # CHECK IF CAUGHT OR NOT
            if a.node == predator.node :
                caught_us = True
                break
            elif a.node == prey.node :
                caught_prey = True
                break

            # MOVE PREDATOR (Shortest path to agent)






            # CHECK IF CAUGHT OR NOT
            if a.node == predator.node :
                caught_us = True
                break
            elif a.node == prey.node :
                caught_prey = True
                break