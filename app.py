import dash
import json
import networkx as nx
import plotly.graph_objs as go
import numpy as np
from mcmc_driver import *
from generate_data import get_colorado_graph
from dash import dcc, html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

# Create a Dash app
app = dash.Dash(__name__, suppress_callback_exceptions = True)

# necessary constants
PAGE_TITLE = "Working Project Site, CS 333"
ITERATION_INTERVAL_MS = 1000

# static functin for format text that appears when hovering over a node
def format_hover_text(node) -> str:
    name = node["name"]
    pop = node["population"]
    output = f"{name} County<br>Population: {pop}"
    return output

# get a list of all node colors for displaying on the graph
def get_node_colors(G) -> list:
    # colors = [G.nodes()[n]["color"] for n in G.nodes()]
    colors = [np.random.choice(["red", "green", "blue"], p = (0.3, 0.3, 0.4)) for
              _ in G.nodes()]
    return colors

# Create a sample NetworkX graph
G = get_colorado_graph()

# set initial positions of nodes, which remain static
pos = nx.spring_layout(G)

# Create a layout with a plotly subplot
app.layout = html.Div([
    html.H1(PAGE_TITLE),
    dcc.Graph(id = 'graph-animation'),
    dcc.Interval(
        id = 'interval-component',
        interval = ITERATION_INTERVAL_MS,
        n_intervals = 0
    )
])

# Define callback to update graph colors over time
@app.callback(
    Output('graph-animation', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    # Create a subplot with NetworkX graph and update node colors
    fig = make_subplots(rows=1, cols=1)

    # display the graph nodes
    node_trace = go.Scatter(
        x = [pos[node][0] for node in G.nodes()],
        y = [pos[node][1] for node in G.nodes()],
        text = [format_hover_text(G.nodes()[i]) for i in G.nodes()],
        mode = 'markers',
        hoverinfo = 'text',
        marker = dict(
            size = 15,
            color = get_node_colors(G)
        ),
        hoverlabel = dict(font = {"color": "white"})
    )

    # display the graph edges
    edges_trace = go.Scatter(
        x = [],
        y = [],
        line = dict(width = 1.5, color = "gray"),
        hoverinfo = 'none',
        mode = 'lines'
    )

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edges_trace['x'] += tuple([x0, x1, None])
        edges_trace['y'] += tuple([y0, y1, None])

    # add visualizations to figure
    fig.add_trace(edges_trace)
    fig.add_trace(node_trace)
    fig.update_layout(
        showlegend = False,
        hovermode = 'closest',
        margin = dict(b = 0, l = 0, r = 0, t = 0),
        xaxis = dict(showgrid = False, zeroline = False, showticklabels = False),
        yaxis = dict(showgrid = False, zeroline = False, showticklabels = False),
        plot_bgcolor = "rgba(0,0,0,0)",
        paper_bgcolor = "rgba(0,0,0,0)"
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

