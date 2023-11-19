# tested on python 3.11.2
import csv
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import re

"""
find_nodes function
Input:  Filepath (string) that leads to county.csv
Output: List containing all of Colorado's counties sorted in alphabetical order
"""
def find_nodes(input_path: str):
    
    """
    Use a hashset to track all of Colorado's counties w/out duplicates
    Hashsets have O(1) average lookup time.
    """
    seen = set()
    
    with open(input_path, "r") as input_file:
        
        # skip the header
        # if you don't do this, then you'll insert "County" as a node
        next(input_file, None)
        
        for line in input_file:
            try:
                
                """
                For each row, add each county (that's first listed) into
                the hashset. Since each pair [a, b] has a pair [b, a] in
                the CSV, we don't need to add both column values for each row.
                """
                row = line.split(",")
                seen.add(row[0])                
            
            # if something broke, print what went wrong
            except Exception as e:
                print(str(e))
    
    """
    Return a list in sorted order.
    Nodes and counties will be considered the same thing.
    """
    nodes = list(seen)
    nodes.sort()
    
    # O(nlogn) time for sorting counties, where n = number of counties
    # O(n) extra space for hashset and list
    return nodes


"""
find_edges function
Input:  Filepath (string) that leads to county.csv
Output: Adjacency list containing all of Colorado's edges (as hashmap/dict)
"""
def find_edges(input_path: str):
    
    """
    Create an adjacency list, represented as a hashmap/dict
    Key:   County name (type: string)
    Value: List of county names (type: List[str])
    """
    adj_list = dict()
    
    with open(input_path, "r") as input_file:
        
        # skip the header
        next(input_file, None)
        
        for line in input_file:
            try:
                
                """
                For each row, we can get values [a, b]. Add a as a key if it
                doesn't already exist. Then, add b to the adjacency list.
                """
                line = re.sub('[\n]', '', line)
                a, b = line.split(",")
                if a not in adj_list:
                    adj_list[a] = []
                adj_list[a].append(b)               
            
            # if something broke, print what went wrong
            except Exception as e:
                print(str(e))
    
    # return the adjancency list
    # O(n) time for traversing CSV, where n = number of counties
    # O(n) extra space for adjacency list
    return adj_list


"""
find_population_and_leans function
Inputs: input_path: Filepath (string) that leads to data_by_county.csv
        nums:       Dictionary that maps county names to integer IDs
Output: Dictionary containing all of Colorado's county IDs, and (population, pvi) as a value
"""
def find_population_and_leans(input_path: str, nums):
    
    # store the populations and PVIs as dictionaries
    populations = dict()
    partisan_leans = dict()
    
    with open(input_path, "r") as input_file:
        
        # skip the header
        # if you don't do this, then something will probably crash
        next(input_file, None)
        
        for line in input_file:
            try:
                
                """
                For each row, extract each county's name.
                
                Use the county_name to find the assigned integer county_id.
                Then, add the pop and pvi to their respective dictionaries. 
                """
                row = line.split(",")
                county_name = row[0]
                
                county_id = nums[county_name]
                pvi = int(row[1])
                pop = int(row[2])
                
                populations[county_id] = pop
                partisan_leans[county_id] = pvi
            
            # if something broke, print what went wrong
            except Exception as e:
                print(str(e))
    
    """
    Return both dictionaries through a tuple.
    """
    return (populations, partisan_leans)

"""
get_colorado_graph function
INPUT:  None
OUTPUT: networkX undirected graph containing all nodes and edges
        Each node represents a county and contains the following attributes:
            - name
            - population
            - PVI

"""
def get_colorado_graph(edge_path = "county.csv", node_path = "data_by_county.csv"):
    
    """
    STEP 1:
    Extract ALL nodes from the CSV file.
    Store the list of nodes in the variable county_nodes
    """
    input_path = edge_path
    county_nodes = find_nodes(input_path)

    """
    STEP 2:
    Assign an ID number to each county.
    This way, we don't need to refer to each county by its name.
    
    nums is a hashmap/dict, with the following {key: value} pairs:
    key   = county name
    value = ID number
    """
    nums = dict()

    # assign a number to each node
    for i, county_name in enumerate(county_nodes):
        nums[county_name] = i
        
    
    """
    STEP 3:
    Extract an adjacency list from the CSV.
    This way, we know what nodes connect to one another.
    """
    adj_list = find_edges(input_path)


    """
    STEP 4:
    Extract all the edges from the adjacency list.
    If the edge (a, b) exists in the list, so does (b, a).
    """
    edges = []
    for key in adj_list:
        
        # find the target county
        a = nums[key]
        
        # create an edge for every one of its neighbors
        for neighbor in adj_list[key]:
            b = nums[neighbor]
            edges.append((a, b))
            
    """
    STEP 5:
    Extract the population and partisan leans (i.e., PVI) from the graph.
    They will stored in lists, and each county has a population and PVI value.
    """
    input_path = node_path
    populations, partisan_leans = find_population_and_leans(input_path, nums)
    
    """
    STEP 6:
    Now that we have node IDs, edges, names, populations, and PVIs,
    we can finally create the graph.
    """
    graph = nx.Graph()
    n = len(county_nodes)
    for i in range(n):
        graph.add_node(i)

    # set the attributes for each node
    attrs = {}
    for i in range(n):
        attrs[i] = {"name": county_nodes[i], "population": populations[i], 
                "PVI": partisan_leans[i]}
    nx.set_node_attributes(graph, attrs)

    graph.add_edges_from(edges)
    
    """
    STEP 7:
    Return the graph
    """
    return graph
