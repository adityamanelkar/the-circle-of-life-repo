import random
import numpy as np
import probability as prob
from graph_utils import Graph

class Agent:
    """
    Object that has stuff on the agent
    """
    def __init__(self, name, graph: Graph) -> None:
        """
        Initialization
        """
        self.name = name

        # Spawn Agent at a random node (other than the prey and predator spawn nodes)
        self.node = random.choice(graph.node_list())

        total_nodes = len(graph.node_list())

        # Initialize prey probability matrix to (1/49)s
        self.prey_beliefs = []

        for _ in range(total_nodes):
            self.prey_beliefs.append(1 / (total_nodes - 1))

        self.prey_beliefs[self.node] = 0.0

        # Initialize predator probability matrix to 0s
        self.pred_beliefs = []

        for _ in range(total_nodes):
            self.pred_beliefs.append(0.0)

        # For partial prey
        self.prey_transition_matrix = np.zeros((total_nodes, total_nodes), dtype=float)

        # For partial predator
        self.pred_transition_matrix = np.zeros((total_nodes, total_nodes), dtype=float)

        print("Initial Agent Position: " + str(self.node))

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

    def update_prey_trans_matrix(self, graph: Graph) -> None:
        """
        Updates prey transition matrix P(i, j) = Probability of prey at node i at (t + 1) given prey was at node j at (t) i.e. [j -> i]
        """
        graph_nodes = graph.node_list()

        for jnode in graph_nodes:

            neighbors = list(graph.neighbors(jnode))
            prob_each_neighbor = 1 / (len(neighbors) + 1)
    
            # When prey stays at the same node
            self.prey_transition_matrix[jnode, jnode] = prob_each_neighbor

            # When prey moves to a different node
            for inode in neighbors:
                self.prey_transition_matrix[inode, jnode] = prob_each_neighbor

    def update_pred_trans_matrix(self, graph: Graph) -> None:
        """
        Updates predator transition matrix P(i, j) = Probability of predator at node i at (t + 1) given predator was at node j at (t) i.e. [j -> i]
        (for a non-distracted predator)
        """
        graph_nodes = graph.node_list()

        self.pred_transition_matrix = np.zeros((len(graph_nodes), len(graph_nodes)))

        for jnode in graph_nodes:
            prev_path_length = graph.shortest_path_length(jnode, self.node)
            likely_nodes_plan = []

            for neighbor in graph.neighbors(jnode):
                
                path_length = graph.shortest_path_length(jnode, self.node)
                
                if path_length <= prev_path_length:
                    likely_nodes_plan.append(neighbor)

            for inode in likely_nodes_plan:
                self.pred_transition_matrix[inode, jnode] = 1 / len(likely_nodes_plan)


    def update_dist_pred_trans_matrix(self, graph: Graph) -> None:
        """
        Updates predator transition matrix P(i, j) = Probability of predator at node i at (t + 1) given predator was at node j at (t) i.e. [j -> i]
        (for a distracted predator)
        """
        graph_nodes = graph.node_list()

        self.pred_transition_matrix = np.zeros((len(graph_nodes), len(graph_nodes)))

        for jnode in graph_nodes:
            prev_path_length = graph.shortest_path_length(jnode, self.node)
            likely_nodes_plan = []
            likely_nodes_random = graph.neighbors(jnode)

            for neighbor in graph.neighbors(jnode):
                
                path_length = graph.shortest_path_length(jnode, self.node)
                
                if path_length <= prev_path_length:
                    likely_nodes_plan.append(neighbor)

            for inode in likely_nodes_random:
                # When predator moves to a node without being distracted
                if inode in likely_nodes_plan:
                    self.pred_transition_matrix[inode, jnode] = 0.6 / len(likely_nodes_plan) + 0.4 / len(likely_nodes_random)
                else: # when predator is distracted
                    self.pred_transition_matrix[inode, jnode] = 0.4 / len(likely_nodes_random)

    def move_1(self, graph: Graph, prey_pos, pred_pos) -> None:
        """
        This function moves the agent 1 according to the strategy mentioned in the write up
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
            neighbor_to_prey = graph.shortest_path_length( neighbor, prey_pos)

            # Distance of shortest path from neighbor to predator
            neighbor_to_predator = graph.shortest_path_length( neighbor, pred_pos)

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
        
        # Highest priority value out of all the neighbors
        min_val = min(priority.values())

        # Neighbors with the Highest priority
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

        # Neighbors with the Highest priority
        if min_val < 13:
            # List of neighbors with highest priority
            Highest_priority_neighbors = [key for key, value in priority.items() if value == min_val]

            # Breaking ties at random
            next_pos = random.choice(Highest_priority_neighbors)

            # Update node for the agent
            self.node = next_pos

        else:
            self.node = self.node

    def move_3(self, graph: Graph, prey_pos: int, pred_pos: int, time_steps: int) -> bool:
        """
        Movement logic for Agents 3 and 4
        """
        error = 10 ** -5

        if time_steps == 1:
            # Initial transition matrix (not to be altered)
            self.update_prey_trans_matrix(graph)

        elif time_steps > 1:
            # Update beliefs post prey move
            """
            P ( prey at some_node now ) = SUM [ P ( prey at some_node now AND prey was at old_node then ) ]
                ... Marginalization

            P ( prey at some_node now ) = SUM [ P ( prey at old_node then ) * P ( prey at some_node now | prey at old_node then ) ]
                ... Conditional Factoring

            P ( prey at some_node now ) = SUM [ P ( prey at old_node then ) * P ( some_node | old_node ) ]
                ... Simplifying the last probability which is basically the transition probability
            
            New beilief = DOT PRODUCT [ old_belief , row in the transition matrix ]
                ... In terms of what we have
            """

            updated_beliefs_ndarray = np.matmul(self.prey_transition_matrix, np.array(self.prey_beliefs))
            self.prey_beliefs = updated_beliefs_ndarray.tolist()

            if not prob.check_sum_beliefs(self.prey_beliefs):
                raise ValueError("Sum of beliefs error (after prey move update)")

        # Find the best survey pos
        best_survey_node = prob.node_to_survey(self.prey_beliefs, "prey")

        # Perform survey on the best node
        self.prey_beliefs = prob.survey(self.prey_beliefs, best_survey_node, prey_pos)

        if not prob.check_sum_beliefs(self.prey_beliefs):
            raise ValueError("Sum of beliefs error (after node survey)")

        # Find the node for which we have highest belief
        max_prob_nodes = [node for node, belief in enumerate(self.prey_beliefs) if belief == max(self.prey_beliefs)]

        # If more than one, break ties randomly if 
        prob_prey_pos = random.choice(max_prob_nodes)

        print("Highest probable current position of prey is [{}] with probability [{}], so we'll use that info".format(prob_prey_pos, self.prey_beliefs[prob_prey_pos]))

        if self.name == "agent3":
            # Do the actual movement to highest belief node based on agent 1 logic for agent 3
            self.move_1(graph, prob_prey_pos, pred_pos)
        
        elif self.name == "agent4":
            # Do the actual movement to highest belief node based on agent 2 logic for agent 4
            self.move_2(graph, prob_prey_pos, pred_pos)

        # Update beliefs post agent move
        prob.survey(self.prey_beliefs, self.node, prey_pos)

        if not prob.check_sum_beliefs(self.prey_beliefs):
            raise ValueError("Sum of beliefs error (after agent move)")
        
        if 1.0 - error <= max(self.prey_beliefs) <= 1.0 + error:
            return True
        else:
            return False

    def move_5(self, graph: Graph, prey_pos: int, pred_pos: int, time_steps: int) -> bool:
        """
        Movement logic for Agents 5 and 6
        """
        error = 10 ** -5

        if time_steps == 1:
            self.pred_beliefs[pred_pos] = 1.0
            if not prob.check_sum_beliefs(self.pred_beliefs):
                raise ValueError("Sum of beliefs error (initial)")

        elif time_steps > 1:
            # Update beliefs post predator move
            self.update_dist_pred_trans_matrix(graph)

            """
            P ( pred at some_node now ) = SUM [ P ( pred at some_node now AND pred was at old_node then ) ]
                ... Marginalization

            P ( pred at some_node now ) = SUM [ P ( pred at old_node then ) * P ( pred at some_node now | pred at old_node then ) ]
                ... Conditional Factoring

            P ( pred at some_node now ) = SUM [ P ( pred at old_node then ) * P ( some_node | old_node ) ]
                ... Simplifying the last probability which is basically the transition probability
            
            New beilief = DOT PRODUCT [ old_belief , row in the transition matrix ]
                ... In terms of what we have
            """

            updated_beliefs_ndarray = np.matmul(self.pred_transition_matrix, np.array(self.pred_beliefs))
            self.pred_beliefs = updated_beliefs_ndarray.tolist()

            if not prob.check_sum_beliefs(self.pred_beliefs):
                raise ValueError("Sum of beliefs error (after predator move update)")

        # Find the best survey pos
        best_survey_node = prob.node_to_survey(self.pred_beliefs, "predator")

        # Perform survey on the best node
        self.pred_beliefs = prob.survey(self.pred_beliefs, best_survey_node, pred_pos)

        if not prob.check_sum_beliefs(self.pred_beliefs):
            raise ValueError("Sum of beliefs error (after node survey)")

        # Find the node for which we have highest belief
        max_prob_nodes = [node for node, belief in enumerate(self.pred_beliefs) if belief == max(self.pred_beliefs)]

        dist_max_prob = {}

        for node in max_prob_nodes:
            dist_max_prob[node] = graph.shortest_path_length(node, self.node)

        upd_max_prob_nodes = []

        for node in dist_max_prob:
            if dist_max_prob[node] == min(dist_max_prob.values()):
                upd_max_prob_nodes.append(node)

        # If more than one, break ties randomly if 
        prob_pred_pos = random.choice(upd_max_prob_nodes)

        print("Highest probable current position of predator is [{}] with probability [{}], so we'll use that info".format(prob_pred_pos, self.pred_beliefs[prob_pred_pos]))

        if self.name == "agent5":
            # Do the actual movement to highest belief node based on agent 1 logic for agent 5
            self.move_1(graph, prey_pos, prob_pred_pos)
        
        elif self.name == "agent6":
            # Do the actual movement to highest belief node based on agent 2 logic for agent 6
            self.move_2(graph, prey_pos, prob_pred_pos)

        # Update beliefs post agent move
        prob.survey(self.pred_beliefs, self.node, pred_pos)

        if not prob.check_sum_beliefs(self.pred_beliefs):
            raise ValueError("Sum of beliefs error (after agent move)")
        
        if 1.0 - error <= max(self.pred_beliefs) <= 1.0 + error:
            return True
        else:
            return False

    def move_7(self, graph: Graph, prey_pos: int, pred_pos: int, time_steps: int) -> tuple:
        """
        Movement logic for Agents 7 and 8
        """
        error = 10 ** -5

        if time_steps == 1:
            self.pred_beliefs[pred_pos] = 1.0
            if not prob.check_sum_beliefs(self.pred_beliefs):
                raise ValueError("Sum of pred beliefs error (initial)")

            # Initial transition matrix for prey (not to be altered)
            self.update_prey_trans_matrix(graph)

        elif time_steps > 1:
            # Update beliefs post predator move
            self.update_dist_pred_trans_matrix(graph)

            """
            P ( prey/pred at some_node now ) = SUM [ P ( prey/pred at some_node now AND prey/pred was at old_node then ) ]
                ... Marginalization

            P ( prey/pred at some_node now ) = SUM [ P ( prey/pred at old_node then ) * P ( prey/pred at some_node now | prey/pred at old_node then ) ]
                ... Conditional Factoring

            P ( prey/pred at some_node now ) = SUM [ P ( prey/pred at old_node then ) * P ( some_node | old_node ) ]
                ... Simplifying the last probability which is basically the transition probability
            
            New beilief = DOT PRODUCT [ old_belief , row in the transition matrix ]
                ... In terms of what we have
            """

            updated_beliefs_ndarray_prey = np.matmul(self.prey_transition_matrix, np.array(self.prey_beliefs))
            self.prey_beliefs = updated_beliefs_ndarray_prey.tolist()

            if not prob.check_sum_beliefs(self.prey_beliefs):
                raise ValueError("Sum of prey beliefs error (after prey move update)")

            updated_beliefs_ndarray_pred = np.matmul(self.pred_transition_matrix, np.array(self.pred_beliefs))
            self.pred_beliefs = updated_beliefs_ndarray_pred.tolist()

            if not prob.check_sum_beliefs(self.pred_beliefs):
                raise ValueError("Sum of pred beliefs error (after predator move update)")

        # Find the best survey pos.
        # From what Aravind said in OH, we need to see if max belief for any node for predator is greater than or equal to 0.5.
        # If max pred belief < 0.5 we will always survey predator, else we will survey prey.

        if max(self.pred_beliefs) < 0.5:
            # Survey the predator
            best_survey_node = prob.node_to_survey(self.pred_beliefs, "predator")
        else:
            # Survey the prey
            best_survey_node = prob.node_to_survey(self.prey_beliefs, "prey")

        # Perform survey on the best node.
        # But while doing this, we will check the node for both prey and predator, and will update the beliefs of both.

        if self.name == "agent7" or self.name == "agent8":

            self.prey_beliefs = prob.survey(self.prey_beliefs, best_survey_node, prey_pos)
            if not prob.check_sum_beliefs(self.prey_beliefs):
                raise ValueError("Sum of prey beliefs error (after node survey)")

            self.pred_beliefs = prob.survey(self.pred_beliefs, best_survey_node, pred_pos)
            if not prob.check_sum_beliefs(self.pred_beliefs):
                raise ValueError("Sum of pred beliefs error (after node survey)")

        elif self.name == "agent7b" or self.name == "agent8b":

            rand = random.random() # Aravind mentioned if the drone does cannot pinpoint a prey it cannot even pinpoint the predator (meaning random failure should be uniform for both)

            self.prey_beliefs = prob.survey_defective(self.prey_beliefs, best_survey_node, prey_pos, rand)
            if not prob.check_sum_beliefs(self.prey_beliefs):
                raise ValueError("Sum of prey beliefs error (after node defective survey)")

            self.pred_beliefs = prob.survey_defective(self.pred_beliefs, best_survey_node, pred_pos, rand)
            if not prob.check_sum_beliefs(self.pred_beliefs):
                raise ValueError("Sum of pred beliefs error (after node defective survey)")

        # Find the node for which we have highest beliefs for prey
        max_prob_nodes_prey = [node for node, belief in enumerate(self.prey_beliefs) if belief == max(self.prey_beliefs)]

        prob_prey_pos = random.choice(max_prob_nodes_prey)

        print("Highest probable current position of prey is [{}] with probability [{}], so we'll use that info".format(prob_prey_pos, self.pred_beliefs[prob_prey_pos]))

        # Find the node for which we have highest beliefs for predator
        max_prob_nodes_pred = [node for node, belief in enumerate(self.pred_beliefs) if belief == max(self.pred_beliefs)]

        dist_max_prob = {}

        for node in max_prob_nodes_pred:
            dist_max_prob[node] = graph.shortest_path_length(node, self.node)

        upd_max_prob_nodes = []

        for node in dist_max_prob:
            if dist_max_prob[node] == min(dist_max_prob.values()):
                upd_max_prob_nodes.append(node)

        # If more than one, break ties randomly
        prob_pred_pos = random.choice(upd_max_prob_nodes)

        print("Highest probable current position of predator is [{}] with probability [{}], so we'll use that info".format(prob_pred_pos, self.pred_beliefs[prob_pred_pos]))

        if self.name == "agent7" or self.name == "agent7b":
            # Do the actual movement to highest belief node based on agent 1 logic for agent 7/b
            self.move_1(graph, prob_prey_pos, prob_pred_pos)

        elif self.name == "agent8" or self.name == "agent8b":
            # Do the actual movement to highest belief node based on agent 2 logic for agent 8/b
            self.move_2(graph, prob_prey_pos, prob_pred_pos)

        # Update beliefs post agent move (for both prey and predator)

        prob.survey(self.prey_beliefs, self.node, prey_pos)
        if not prob.check_sum_beliefs(self.prey_beliefs):
            raise ValueError("Sum of prey beliefs error (after agent move)")

        prob.survey(self.pred_beliefs, self.node, pred_pos)
        if not prob.check_sum_beliefs(self.pred_beliefs):
            raise ValueError("Sum of pred beliefs error (after agent move)")
        
        prey_found = False

        if 1.0 - error <= max(self.prey_beliefs) <= 1.0 + error:
            prey_found = True

        pred_found = False

        if 1.0 - error <= max(self.pred_beliefs) <= 1.0 + error:
            pred_found = True

        return (prey_found, pred_found)


   