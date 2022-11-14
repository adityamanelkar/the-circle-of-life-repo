import math
import random
import numpy as np
from graph_utils import Graph

def node_to_survey(current_belief: list, target: str) -> int:
    """
    Returns best node to survey for partial prey/pred
    """
    if target == "prey" or target == "predator":
        # List of nodes with the highest probability of prey/predator
        high_prob_nodes = [node for node in range(len(current_belief)) if current_belief[node] == max(current_belief)]

        return random.choice(high_prob_nodes)

    else:
        raise ValueError("The target for survey needs to be either prey or predator and not {}".format(target))

def node_to_survey_closest(graph: Graph, agent_pos, current_belief: list, target: str) -> int:
    """
    Returns best+closest node to survey for partial prey/pred
    """
    if target == "predator":
        # List of nodes with the highest probability of prey/predator
        high_prob_nodes = [node for node in range(len(current_belief)) if current_belief[node] == max(current_belief)]

        sp_len = math.inf
        node_to_survey = 0

        for node in high_prob_nodes:

            node_len = graph.shortest_path_length(node, agent_pos)            

            if graph.shortest_path_length(node, agent_pos) < sp_len:
                sp_len = node_len
                node_to_survey = node

        return node_to_survey

    elif target == "prey":
        # List of nodes with the highest probability of prey/predator
        high_prob_nodes = [node for node in range(len(current_belief)) if current_belief[node] == max(current_belief)]

        return random.choice(high_prob_nodes)

    else:
        raise ValueError("The target for survey needs to be either prey or predator and not {}".format(target))

def node_to_survey_proximity(graph: Graph, agent_pos, current_belief: list, target: str) -> int:
    """
    Returns best+proximity node to survey for partial prey/pred
    """
    if target == "predator":
        l1_neighbors = graph.neighbors(agent_pos)

        # l2_neighbors = []
        # for neighbor in l1_neighbors:
        #     l2_neighbors.extend(graph.neighbors(neighbor))

        # l1_neighbors.extend(l2_neighbors)

        # list(set(l1_neighbors)) # remove all duplicates

        region = l1_neighbors

        beliefs = {}

        for node in region:
            beliefs[node] = current_belief[node]

        max_prob_in_region = max(list(beliefs.values()))

        if max_prob_in_region > 0:
            # List of nodes with the highest probability of prey/predator
            high_prob_nodes = [node for node, prob in beliefs.items() if prob == max_prob_in_region]
            print("In nodes_to_survey_proximity")
            print(high_prob_nodes)

        else: # follow old closest logic
            # List of nodes with the highest probability of prey/predator
            high_prob_nodes = [node for node in range(len(current_belief)) if current_belief[node] == max(current_belief)]

        sp_len = math.inf
        node_to_survey = 0

        for node in high_prob_nodes:

            node_len = graph.shortest_path_length(node, agent_pos)            

            if graph.shortest_path_length(node, agent_pos) < sp_len:
                sp_len = node_len
                node_to_survey = node

        return node_to_survey

    elif target == "prey":
        # List of nodes with the highest probability of prey/predator
        high_prob_nodes = [node for node in range(len(current_belief)) if current_belief[node] == max(current_belief)]

        return random.choice(high_prob_nodes)

    else:
        raise ValueError("The target for survey needs to be either prey or predator and not {}".format(target))

def node_to_survey_cheating(graph: Graph, agent_pos, prey_belief: list, pred_belief: list, target: str) -> int:
    """
    Returns a cheat node to survey to almost always guarantee a success
    """
    if target == "predator":
        # We want to simulate and see which position we would want to jump to given we are trying to catch a prey
        max_prob_nodes_prey = [node for node, belief in enumerate(prey_belief) if belief == max(prey_belief)]
        sp_len = math.inf
        prey_choices = []

        for prey_node in max_prob_nodes_prey:
            cp_len = graph.shortest_path_length(agent_pos, prey_node)
            if cp_len < sp_len:
                sp_len = cp_len
                prey_choices = [prey_node]
            elif cp_len == sp_len:
                prey_choices.append(prey_node)

        prey_pos = random.choice(prey_choices)

        node_to_survey = 0

        agent_neighbors = set(graph.neighbors(agent_pos))
        agent_neighbors.add(agent_pos)
        print(agent_neighbors)

        path_to_prey = graph.shortest_path(agent_pos, prey_pos)
        path_to_prey = set(path_to_prey)
        print(path_to_prey)

        node_to_survey = list(agent_neighbors.intersection(path_to_prey))[0]

        return node_to_survey

    elif target == "prey":
        # List of nodes with the highest probability of prey/predator
        high_prob_nodes = [node for node in range(len(prey_belief)) if prey_belief[node] == max(prey_belief)]

        return random.choice(high_prob_nodes)

    else:
        raise ValueError("The target for survey needs to be either prey or predator and not {}".format(target))


def survey(current_belief: list, node_surveyed: int, target_pos: int) -> list:
    """
    The function performs a "survey" and subsequent belief updates on the node_surveyed
    Every time an agent moves to a node it essentially surveys its new position (i.e. node_surveyed = agent.node)
    """
    # Check if prey/pred found at node_surveyed or not 
    if node_surveyed == target_pos:
        found = True
    else:
        found = False

    # If prey/pred is NOT at node surveyed
    if not found:
        """
        Formula used:
            P ( prey/pred at node | survey did not find prey/pred at node_surveyed )
                = P ( prey/pred at node AND survey did not find prey/pred at node_surveyed ) / P ( survey did not find prey/pred at node_surveyed )
                    ... Definition of Conditional Probability

                = P ( prey/pred at node ) * P ( survey did not find prey/pred at node_surveyed | prey/pred at node ) / P ( survey did not find prey/pred at node_surveyed )
                    ... Conditional Factoring
                
                = P ( prey/pred at node ) * 1 / P ( prey/pred not at node_surveyed )
                    ... P ( survey did not find prey/pred at node_surveyed | prey/pred at node ) = 1 ; since we know prey/pred was not found at node_surveyed
        """
        denominator = (1 - current_belief[node_surveyed])

        # Update probabilities
        for node in range(len(current_belief)):  
            if node == node_surveyed: # set probability of surveyed node = 0 since prey/pred is not there
                current_belief[node_surveyed] = 0 
            else: # update all the other probabilities
                current_belief[node] = current_belief[node] / denominator 

    else: # prey/pred is at node surveyed
        for node in range(len(current_belief)):  
            if node == node_surveyed: # set probability of surveyed node to 1 since prey/pred is there
                current_belief[node_surveyed] = 1
            else: # update all the other probabilities
                current_belief[node] = 0

    return current_belief

def survey_defective(current_belief: list, node_surveyed: int, target_pos: int, rand: float) -> list:
    """
    The function performs a "defective survey" and subsequent belief updates on the node_surveyed
    This is only used for agents 7b and 8b
    """
    # Check if prey/pred found at node_surveyed or not 
    if node_surveyed == target_pos:
        if rand <= 0.9: # 90% of the time the survey correctly finds a prey/pred
            found = True
        else: # 10% of the time there is a false negative
            found = False
    else:
        found = False

    # If prey/pred is NOT at node surveyed
    if not found:
        """
        Formula used:
            P ( prey/pred at node | survey did not find prey/pred at node_surveyed )
                = P ( prey/pred at node AND survey did not find prey/pred at node_surveyed ) / P ( survey did not find prey/pred at node_surveyed )
                    ... Definition of Conditional Probability

                = P ( prey/pred at node ) * P ( survey did not find prey/pred at node_surveyed | prey/pred at node ) / P ( survey did not find prey/pred at node_surveyed )
                    ... Conditional Factoring
                
                = P ( prey/pred at node ) * 1 / P ( prey/pred not at node_surveyed )
                    ... P ( survey did not find prey/pred at node_surveyed | prey/pred at node ) = 1 ; since we know prey/pred was not found at node_surveyed
                        ... (and the defect does not result in any false positives)

            Where - 
            P ( prey/pred not at node_surveyed ) = P ( prey/pred not found node_surveyed AND prey/pred at node_surveyed ) + P ( prey/pred not found node_surveyed AND prey/pred not at node_surveyed )
                = P ( prey/pred at node_surveyed ) * P ( prey/pred not found at node_surveyed | prey/pred at node_surveyed ) + P ( prey/pred not found at node_surveyed )
                    ... Conditional Factoring / Simplification of last probability

                = P ( prey/pred at node_surveyed ) * 0.1 + ( 1 - P ( prey/pred found at node_surveyed ) )
                    ... Values known to us
        """
        denominator = current_belief[node_surveyed] * 0.1 + (1 - current_belief[node_surveyed])

        # Update probabilities
        for node in range(len(current_belief)):  
            if node == node_surveyed:
                # set probability of surveyed node P ( prey/pred at node_surveyed ) * P ( prey/pred not found at node_surveyed | prey/pred at node_surveyed ) / denominator
                # since prey/pred is not found there
                current_belief[node_surveyed] = current_belief[node_surveyed] * 0.1 / denominator
            else:
                # update all the other probabilities
                current_belief[node] = current_belief[node] / denominator 

    else: # prey/pred is at node surveyed
        for node in range(len(current_belief)):  
            if node == node_surveyed: # set probability of surveyed node to 1 since prey/pred is there
                current_belief[node_surveyed] = 1
            else: # update all the other probabilities
                current_belief[node] = 0

    return current_belief

def check_sum_beliefs(beliefs: list) -> bool:
    """
    Checks if beliefs add up to 1
    """
    error = 10 ** -5

    if 1 - error <= sum(beliefs) <= 1 + error:
        return True
    else:
        print("Oops! Sum of beliefs not equal to 1. Instead they are: " + str(sum(beliefs)))
        return False
