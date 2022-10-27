import math
import random
from graph_utils import Graph


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

    def predator_move_sim(self, graph: Graph, pred_pos, agent_future_pos) -> int:
        """
        The function simulates the predator's movement pattern (used in Agents 2, 4, 6 and 8)
        """
        shortest_path_length = graph.shortest_path_length(pred_pos, agent_future_pos)

        for neighbor in graph.neighbors(pred_pos):
            
            path_length = graph.shortest_path_length(neighbor, agent_future_pos)
            
            if path_length < shortest_path_length:
                shortest_path_length = path_length

        # Just set the current position to the best neighbor (and break ties randomly if there is more than one)
        return shortest_path_length

    def move_1(self, graph: Graph, prey_pos, pred_pos) -> None:
        """
        This function moves the agent 1 according to the strategy mentioned in the write up

        """



        # Shortest Distance from Agent to prey

        # agent_to_prey_path = graph.shortest_path(self.node , prey_pos)
        # print("Path from Agent to Prey: ")
        # print(agent_to_prey_path)
        agent_to_prey = graph.shortest_path_length(self.node , prey_pos)
        

        # print ("Distance of Agent to Prey: "+str(agent_to_prey))  

        


        # Shortest Distance from Agent to Predator

        # agent_to_predator_path = graph.shortest_path(self.node , pred_pos)
        # print("Path from Agent to Predator: ")
        # print(agent_to_predator_path)
        agent_to_predator = graph.shortest_path_length(self.node , pred_pos)

        # print ("Distance of Agent to Predator: "+str(agent_to_predator))


        # List of Neighbors of Agent
        agent_neighbours = graph.neighbors(self.node)

        # print()
        # print("Neighbors of Agent: {}".format(agent_neighbours))

        
        #Distance of shortest path from each neighbour to prey and predator
        dist_neighbors = {}
        # Setting priority for every neighbor according to the order followed by Agent1 
        priority = {}

        


        for neighbor in agent_neighbours:

            # Distance of shortest path from neighbor to prey

            # neighbor_to_prey_path = graph.shortest_path(neighbor , prey_pos)
            # print("Path from Neighbor {} to Prey: {}".format(neighbor,neighbor_to_prey_path))
            neighbor_to_prey = graph.shortest_path_length( neighbor, prey_pos)

            # print("Dist of Neighbor {} to Prey: {} ".format(neighbor,neighbor_to_prey))
            


            # Distance of shortest path from neighbor to predator

            # neighbor_to_predator_path = graph.shortest_path(neighbor , pred_pos)
            # print("Path from Neighbor {} to Predator: {}".format(neighbor,neighbor_to_predator_path))
            neighbor_to_predator = graph.shortest_path_length( neighbor, pred_pos)

            # print("Dist of Neighbor {} to Predator: {} ".format(neighbor,neighbor_to_predator))
            
            


            dist_neighbors[neighbor] = (neighbor_to_prey,neighbor_to_predator)


            if neighbor_to_prey < agent_to_prey and neighbor_to_predator > agent_to_predator:

                priority[neighbor] = 1
                
            elif neighbor_to_prey < agent_to_prey and neighbor_to_predator == agent_to_predator :

                priority[neighbor] = 2
                
            elif neighbor_to_prey == agent_to_prey and neighbor_to_predator > agent_to_predator :

                priority[neighbor] = 3
                
            elif neighbor_to_prey == agent_to_prey and neighbor_to_predator == agent_to_predator :

                priority[neighbor] = 4
                
            elif neighbor_to_predator > agent_to_predator :

                priority[neighbor] = 5
                
            elif neighbor_to_predator == agent_to_predator :

                priority[neighbor] = 6
                
            else :

                priority[neighbor] = 7
                

      
        # print("Distance of every neighbour from prey and predator: ")
        # print(dist_neighbors)

        # print("Priority of every neighbour:")
        # print(priority)

        
        

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
    
    def move_2(self, graph: Graph, prey_pos, pred_pos) -> None:
        """
        Movement logic for Agent 2
        """
        # Shortest Distance from Agent to prey
        agent_to_prey = graph.shortest_path_length(self.node , prey_pos)
        
        # Shortest Distance from Agent to Predator
        agent_to_predator = graph.shortest_path_length(self.node , pred_pos)

        # List of Neighbors of Agent
        agent_neighbours = graph.neighbors(self.node)

        # Distance of shortest path from each neighbour to prey and predator
        dist_neighbors = {}

        # Setting priority for every neighbor according to the order followed by Agent1 
        priority = {}

        for neighbor in agent_neighbours:

            # Distance of shortest path from neighbor to prey
            neighbor_to_prey = graph.shortest_path_length(neighbor, prey_pos)

            # Distance of shortest path from neighbor to predator
            neighbor_to_predator = graph.shortest_path_length( neighbor, pred_pos)

            # Distance of shortest path from neighbor to predator future
            neighbor_to_predator_future = self.predator_move_sim(graph, pred_pos, neighbor) # We just need distance

            dist_neighbors[neighbor] = (neighbor_to_prey, neighbor_to_predator)

            if neighbor_to_prey < agent_to_prey and neighbor_to_predator_future > agent_to_predator:
                priority[neighbor] = 1

            elif neighbor_to_prey < agent_to_prey and neighbor_to_predator_future == agent_to_predator :
                priority[neighbor] = 2

            # elif neighbor_to_prey < agent_to_prey and neighbor_to_predator > agent_to_predator:
            #     priority[neighbor] = 3
                
            # elif neighbor_to_prey < agent_to_prey and neighbor_to_predator == agent_to_predator :
            #     priority[neighbor] = 4
                
            elif neighbor_to_prey == agent_to_prey and neighbor_to_predator_future > agent_to_predator :
                priority[neighbor] = 5
            
            elif neighbor_to_prey == agent_to_prey and neighbor_to_predator_future == agent_to_predator :
                priority[neighbor] = 6

            # elif neighbor_to_prey == agent_to_prey and neighbor_to_predator > agent_to_predator :
            #     priority[neighbor] = 7
                
            # elif neighbor_to_prey == agent_to_prey and neighbor_to_predator == agent_to_predator :
            #     priority[neighbor] = 8

            elif neighbor_to_predator_future > agent_to_predator :
                priority[neighbor] = 9

            elif neighbor_to_predator_future == agent_to_predator :
                priority[neighbor] = 10

            # elif neighbor_to_predator > agent_to_predator :
            #     priority[neighbor] = 11
                
            # elif neighbor_to_predator == agent_to_predator :
            #     priority[neighbor] = 12

            else :
                priority[neighbor] = 13
            
        # Highest priority value out of all the neighbors
        min_val = 13
        min_val = min(priority.values())

        # neighbors with the Highest priority
        if min_val < 13:

            # List of neighbors with highest priority
            Highest_priority_neighbors = [key for key, value in priority.items() if value == min_val]

            # Breaking ties at random
            next_pos = random.choice(Highest_priority_neighbors)

            # Update node for the agent
            self.node = next_pos

        else:
            self.node = self.node

               












   