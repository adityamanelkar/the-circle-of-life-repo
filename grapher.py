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
            self._index = (self._index%len(self._c))
        return self._c[self._index]

    def previous(self, k):
        i = self._index
        self._index -= k
        if self._index < 0:
            self._index = len(self._c) - (k - i)
        return self._c[self._index]

def create_graph(total_vertices,max_degree, p_forward):

    vertices = [i for i in range(total_vertices)]

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

    cyc_point.set_index(0)

# There needs to be some kind of while here
    tries = 0
    max_tries = 1000

    while tries < max_tries:
        tries += 1

        # print("Try {}".format(tries))

        random_idx = random.randint(0, 49) # pulls a random index

        if G.degree(random_idx) < max_degree:
            cyc_point.set_index(random_idx)
            if random.random() <= p_forward:
                positive_idx = cyc_point.next(random.randint(2, 5))
                if G.degree(positive_idx) < max_degree:
                    G.add_edge(random_idx, positive_idx)
            else:
                negative_idx = cyc_point.previous(random.randint(2, 5))
                if G.degree(negative_idx) < max_degree:
                    G.add_edge(random_idx, negative_idx)

    print("Maximum no of Edges added :"+str(G.number_of_edges()-50))
    return G


def visualise_graph(graph):  
    pos = nx.nx_agraph.graphviz_layout(graph, prog="neato") # k=5/math.sqrt(G.order())
    nx.draw(graph, pos=pos, with_labels=True)
    plt.show()






# edges_f = []
# degree = []

# for i in range(1000):
#     start_time = time.time()
#     if i%100 == 0:
#         print("Graph: "+str(i))
#     graph = create_graph(50,3,0.5)
#     edges_f.append(graph.number_of_edges()-50)
#     degree.append(max([i[1]for i in graph.degree()]))

# print("maximum no of edges added :"+str(max(edges_f)))
# print("minimum no of edges added :"+str(min(edges_f)))
# # print(max(degree))
# print("Time it took to create {} graphs is: {} seconds".format(1000,(time.time() - start_time)))


