import networkx as nx
import matplotlib.pyplot as plt
import random
import math
import time

class cycle:
    def __init__(self, c):
        self._c = c
    
    def set_index(self, idx):
        self._index = idx

    def next(self, k):
        i = self._index
        self._index += k
        if self._index >= len(self._c):
            self._index = k - i - 2
        return self._c[self._index]

    def previous(self, k):
        i = self._index
        self._index -= k
        if self._index < 0:
            self._index = len(self._c) - (k - i)
        return self._c[self._index]

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

# Set the edges with when dimension < 3

print(edges)

# Initialize G as a directed graph
G = nx.Graph()

# Add initial edges
G.add_edges_from(edges)

# Add more edges

# There needs to be some kind of while here
can_add = True
tries = 0
max_tries = 10 ** 5
closed_list = []

while tries < max_tries:
    tries += 1

    print("Try {}".format(tries))
    node_degrees = {node : val for (node, val) in G.degree()}

    random_idx = random.randint(0, 49) # pulls a random index

    if node_degrees[random_idx] > 2 or random_idx in closed_list:
        if random_idx not in closed_list:
            closed_list.append(random_idx)
        continue

    cyc_point.set_index(random_idx)

    if random.random() <= 0.5:
        positive_idx = cyc_point.next(random.randint(2, 5))
        if positive_idx not in closed_list:
            if node_degrees[positive_idx] < 3:
                G.add_edge(random_idx, positive_idx)
            else:
                if positive_idx not in closed_list:
                    closed_list.append(positive_idx)
    else:
        negative_idx = cyc_point.previous(random.randint(2, 5))
        if negative_idx not in closed_list:
            if node_degrees[negative_idx] < 3:
                G.add_edge(random_idx, negative_idx)
            else:
                if negative_idx not in closed_list:
                    closed_list.append(negative_idx)

print("Number of Edges = {}".format(G.number_of_edges()))

print("Time it took to create a graph is: {} seconds".format(time.time() - start_time))

pos = nx.nx_agraph.graphviz_layout(G, prog="neato") # k=5/math.sqrt(G.order())
nx.draw(G, pos=pos, with_labels=True)

plt.show()