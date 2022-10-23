import random
from graph_utils import Graph
from agent import Agent

class Predator:
    
    def __init__(self, graph: Graph) -> None:
        """
        Spawn at some node while initializing the predator object
        """
        self.pos = random.choice(list(graph.graph))
    
    def move_predator(self, graph: Graph, agent: Agent) -> None:
        """
        Move the predator to the most favorable neighbor to catch the agent
        
        The predator could choose to stay if that may be the best option
        """
        best_neighbors = [self.pos]
        shortest_path_length = graph.shortest_path_length(self.pos, agent.node)

        for neighbor in graph.neighbors(self.pos):
            
            path_length = graph.shortest_path_length(neighbor, agent.node)
            
            if path_length < shortest_path_length:
                best_neighbors = [neighbor] # this is done because we have a clear cut best neighbor
            
            elif path_length == shortest_path_length:
                best_neighbors.append(neighbor) # this is done because we have a tie which we need to break randomly

        # Just set the current position to the best neighbor (and break ties randomly if there is more than one)
        self.pos = random.choice(best_neighbors)
