import math
import random
import networkx as nx


# Need to implement some algo for the agent here

# Need to also implement some framework for calling the algo



class Agent():
    """
    Object that has stuff on the agent

    """
    #Spawn Agent at a random node 
    def __init__(self, name) -> None:
        self.name = name
        self.node = random.randint(0,49)

        print("Initial Agent Position: "+str(self.node))


    def move_1(self, graph, prey_pos, pred_pos) -> None:
        """
        This function moves the agent 1 according to the strategy mentioned in the write up

        """



        # Shortest Distance from Agent to prey
        agent_to_prey = nx.shortest_path_length(graph,source = self.node, target = prey_pos)
        print ("Distance of Agent to Prey: "+str(agent_to_prey))  


        # Shortest Distance from Agent to Predator
        agent_to_predator = nx.shortest_path_length(graph,source = self.node, target = pred_pos)
        print ("Distance of Agent to Predator: "+str(agent_to_predator))


        # List of Neighbors of Agent
        agent_neighbours = list(graph.neighbors(self.node))
        print()
        print("Neighbors of Agent: {}".format(agent_neighbours))

        
        

        # Setting priority for every neighbor according to the order followed by Agent1 
        priority = {}


        for i in agent_neighbours:
            # dist = []

            # Distance of shortest path from neighbor to prey
            neighbor_to_prey = nx.shortest_path_length(graph,source = i, target=prey_pos)

            # dist.append(neighbor_to_prey)

            # Distance of shortest path from neighbor to predator
            neighbor_to_predator = nx.shortest_path_length(graph,source = i, target=pred_pos)

            # dist.append(neighbor_to_predator)


            if neighbor_to_prey < agent_to_prey and neighbor_to_predator > agent_to_predator:

                priority[i] = 1
                
            elif neighbor_to_prey < agent_to_prey and neighbor_to_predator == agent_to_predator :

                priority[i] = 2
                
            elif neighbor_to_prey == agent_to_prey and neighbor_to_predator > agent_to_predator :

                priority[i] = 3
                
            elif neighbor_to_prey == agent_to_prey and neighbor_to_predator == agent_to_predator :

                priority[i] = 4
                
            elif neighbor_to_predator > agent_to_predator :

                priority[i] = 5
                
            elif neighbor_to_predator == agent_to_predator :

                priority[i] = 6
                
            else :

                priority[i] = 7
                

        #     print("Distance of neighbor {} to prey and predator".format(i))
        #     print(dist)
        #     print("priority of neighbor "+str(i))
        #     print(priority[i])
        print("Priority of every neighbour:")
        print(priority)

        
        

        # Highest priority value out of all the neighbors
        min_val = min(priority.values())

        # print("Highest priority value out of all the neighbors: "+str(m))

        # neighbors with the Highest priority
        if min_val < 7:
            # List of neighbors with highest priority
            Highest_priority_neighbors = [key for key, value in priority.items() if value == min_val]      

            # Breaking ties at random
            next_pos = random.choice(Highest_priority_neighbors)
            # Update node for the agent
            self.node = next_pos
        else:
            self.node = self.node
    

        
               












   