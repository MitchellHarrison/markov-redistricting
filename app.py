import networkx as nx
import random
import webbrowser
from pyvis.network import Network
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State

app = Dash(__name__)

"""
Create test graph with n nodes with probability p of an edge between them.
For this test graph, 50% of the nodes are red, and the others blue. This is a
simple graph to be used only for troubleshooting or proof of concept
"""
def generate_test_graph(n, p):
    G = nx.erdos_renyi_graph(n, p)
    color_map = []
    i = 0
    for node in G.nodes():
        if i % 2 == 0:
            G.nodes[node]["color"] = "blue"
        else:
            G.nodes[node]["color"] = "red"
        i += 1
    return G

# generate a static test graph for visualizations
test_n = 10
test_p = 0.3
G = generate_test_graph(test_n, test_p)
net = Network(notebook = True)
net.from_nx(G)

net.show("example.html")

app.layout = html.Div([
    html.H1("# Example Graph Network Visualization"),
    html.Iframe(srcDoc=open("example.html", 'r').read(),
                width="100%", height="500"),
    html.Div(id='slider-output')
])

if __name__ == '__main__':
    webbrowser.open_new("http://127.0.0.1:8050/")
    app.run(debug=True)
