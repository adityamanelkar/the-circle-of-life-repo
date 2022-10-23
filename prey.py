import random
from graph_utils import Graph

class Prey:
    
    def __init__(self, graph: Graph) -> None:
        """
        Spawn at some node while initializing the prey object
        """
        self.pos = random.choice(list(graph.graph))
    
    def move_prey(self, graph: Graph) -> None:
        """
        Randomly move the prey to one of its neighbors or stay in the same spot
        """
        possible_pos = [self.pos]
        possible_pos = possible_pos.extend(graph.neighbors(self.pos))

        # Just set the current position with equal random chance
        self.pos = random.choice(possible_pos)
