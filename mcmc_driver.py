import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import copy
import plotly.graph_objects as go
from IPython.display import display, HTML
from generate_data import *
seed_value=46

# generate colorado graph
graph = get_colorado_graph()
n = len(graph.nodes)
graph_nodes = graph.nodes

# divide the colorado into subgraphs representing districts
def divide_into_subgraphs(graph, n) -> list:
    # Ensure n is a positive integer less than or equal to the number of nodes 
    if not isinstance(n, int) or n <= 0 or n > len(graph.nodes):
        error = """
        Invalid value for n. It should be a positive integer less than or equal 
        to the number of nodes in the graph.
        """
        raise ValueError(error)

    # Get the list of nodes in the graph
    all_nodes = list(graph.nodes)

    # Calculate the number of nodes in each subgraph
    nodes_per_subgraph = len(all_nodes) // n

    # Initialize empty subgraph list
    subgraphs = []

    # possible colors
    colors = ["orange", "green", "red", "blue", "yellow", "pink"]

    # Divide nodes into n subgraphs, coloring nodes accordingly
    for i in range(n):
        start_index = i * nodes_per_subgraph
        end_index = (i + 1) * nodes_per_subgraph if i < n - 1 else len(all_nodes)
        subgraph_nodes = all_nodes[start_index:end_index]
        for node in subgraph_nodes:
            graph.nodes[node]["color"] = colors[i]

        subgraph = graph.subgraph(subgraph_nodes)
        subgraphs.append(subgraph)

    return subgraphs


# return a list of tuples representing edges that connect subgraphs
def get_edges_between_subgraphs(graph, subgraphs) -> list:
    edges_between_subgraphs = []
    for i in range(len(subgraphs)):
        for j in range(i + 1, len(subgraphs)):
            edges_between_subgraphs.extend(
                    nx.edge_boundary(graph, subgraphs[i], subgraphs[j])
                )
    return edges_between_subgraphs


# randomly select an edge connecting two subgraphs
def get_random_edge_between_subgraphs(graph, subgraphs) -> tuple:
    edges_between_subgraphs = get_edges_between_subgraphs(graph, subgraphs)
    if edges_between_subgraphs:
        return random.choice(edges_between_subgraphs)
    else:
        return None


# create a proposed map, creating updated subgraphs and border edges
def create_proposed_state(graph, subgraphs, conflicted_edge):
    # Create deep copies of the graph and subgraphs
    modified_graph = copy.deepcopy(graph)
    modified_subgraphs = [subgraph.copy() for subgraph in subgraphs]

    # Get the nodes connected by the conflicted edge
    node1, node2 = conflicted_edge

    # Choose one of the nodes randomly
    node_to_move = random.choice([node1, node2])

    # Find the index of the subgraph containing the node to move
    index_with_node = next((i for i, subgraph in enumerate(modified_subgraphs) 
        if node_to_move in subgraph), None)

    # Find the node not selected in the random choice
    node_not_selected = node2 if node_to_move == node1 else node1

    if index_with_node is not None:
        # Remove the node from its current subgraph
        modified_subgraphs[index_with_node].remove_node(node_to_move)

        # Find the index of the subgraph not containing the node
        index_other_node = next((i for i, subgraph in enumerate(modified_subgraphs) 
            if node_not_selected in subgraph), None)

        # Add the node to the other subgraph
        mod_sub = modified_subgraphs[index_other_node]
        new_color = mod_sub.nodes[list(mod_sub.nodes())[0]]["color"]
        mod_sub.add_node(node_to_move)
        mod_sub.nodes[node1]["color"] = new_color
        

    return modified_graph, modified_subgraphs


# sum total population over entire graph
def calculate_total_population(graph) -> int:
    total_population = sum(graph.nodes[node]['population'] for node in graph.nodes)
    return total_population


# population score function for calculating transition probabilities
def populationscore(graph,subgraphs, c_pop = 0.3) -> float:
    totalsum=0
    districtaverage=total_population/len(subgraphs)
    for i, subgraph in enumerate(subgraphs, start=1):
        # Calculate the sum of populations for each subgraph
        population_sum = sum(graph.nodes[node]['population'] for node in subgraph.nodes)
        totalsum+=(population_sum-districtaverage)**2
    return(c_pop*totalsum)


# MCMC score function
def totalscorefunction(graph,subgraph, lambda_J = 1) -> float:
    pop_score = populationscore(graph, subgraph)
    pvi_score = PVIscore(graph, subgraph)
    score = (lambdaJ * pop_score) + ((1 - lambda_J) * pvi_score)
    return score


# perform a single iteration of MCMC sampling
def one_iteration_of_MCMC(graph,subgraphs, beta = 0.002):
    border_edges = get_edges_between_subgraphs(graph,subgraphs)
    con1 = len(border_edges)
    conflicted_edge = get_random_edge_between_subgraphs(graph, subgraphs)

    proposed_graph, proposed_subgraphs = create_proposed_state(
            test_graph, testsubgraphs, conflicted_edge)


    new_border_edges = get_edges_between_subgraphs(proposed_graph,
                                                   proposed_subgraphs)
    con2 = len(new_border_edges)

    new_score = totalscorefunction(proposed_graph, proposed_subgraphs)
    old_score = totalscorefunction(graph, subgraphs)
    probfromscorefunctions = np.exp(-1*beta*(new_score - old_score)) 

    transitionprobability = min(1, con1/con2, float(probfromscorefunctions))

    # optional: print transition probability at each iteration
    # print(transitionprobability)

    # Generate a random number between 0 and 1
    random_number = np.random.rand()

    # Check if the random number is less than the transition probability
    if random_number < transitionprobability:
        return proposed_graph, proposed_subgraphs
    else:
        return graph, subgraphs


# perform full redistricting MCMC algorithm by iterating num_iterations times
def Redistricting_MCMC(graph, subgraphs, num_iterations):
    # Perform MCMC iterations
    for _ in range(num_iterations):
        # Call one_iteration_of_MCMC for each iteration
        graph, subgraphs = one_iteration_of_MCMC(graph, subgraphs)
    return graph, subgraphs
