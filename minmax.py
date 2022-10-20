import networkx as nx
import random
import time

class cycle:
    def __init__(self, c):
        self._c = c
    
    def set_index(self, idx):
        self._index = idx

    def next(self, k):
        self._index += k
        if self._index >= len(self._c):
            self._index = (self._index % 49) - 1
        return self._c[self._index]

    def previous(self, k):
        i = self._index
        self._index -= k
        if self._index < 0:
            self._index = len(self._c) - (k - i)
        return self._c[self._index]

edges_array = []

for x in range(5000):

    start_time = time.time()

    # Create a list
    vertices = [i for i in range(50)]

    cyc_point = cycle(vertices)

    edges = []

    cyc_point.set_index(0)

    # Set normal edges
    for i in range(50):
        edges.append((i, cyc_point.next(1)))

    cyc_point.set_index(0)

    # Initialize G as a directed graph
    G = nx.Graph()

    # Add initial edges
    G.add_edges_from(edges)

    # Add more edges
    tries = 0
    max_tries = 10 ** 3

    while tries < max_tries:
        
        tries += 1

        degree_two_nodes = {node : val for (node, val) in G.degree() if val < 3}

        random_idx = random.randint(0, 49) # pulls a random index

        if random_idx not in degree_two_nodes:
            continue

        cyc_point.set_index(random_idx)

        if random.random() <= 0.5:
            positive_idx = cyc_point.next(random.randint(2, 5))
            if positive_idx in degree_two_nodes:
                G.add_edge(random_idx, positive_idx)

        else:
            negative_idx = cyc_point.previous(random.randint(2, 5))
            if negative_idx in degree_two_nodes:
                G.add_edge(random_idx, negative_idx)

    print("Number of Edges for run {} = {}".format(x + 1, G.number_of_edges() - 50))

    edges_array.append(G.number_of_edges() - 50)

print("The min number of edges we could add over 5000 graphs was: {}".format(min(edges_array)))
print("The max number of edges we could add over 5000 graphs was: {}".format(max(edges_array)))