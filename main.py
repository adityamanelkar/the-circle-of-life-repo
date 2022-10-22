import grapher
import random
import math
import time
import agent


#create a graph
G = grapher.create_graph(50,3,0.5)

# agentNum = int(input("Enter the agent number: "))


# Spawn the agent
a = agent.Agent("Agent1")

# Spawn Prey and Predator
preypos = random.randint(0,49)
predpos = random.randint(0,49)


print("Initial Prey Position: "+str(preypos))
print("Initial Predator Position: "+str(predpos))
print()


a.move_1(G, preypos, predpos)

print("Next position of Agent: "+str(a.node))

grapher.visualise_graph(G)



# Simulate 