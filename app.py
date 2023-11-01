import webbrowser
import networkx as nx
import dash_daq as daq
from pyvis.network import Network
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State

PAGE_TITLE = "Example Graph Network Visualization"
RED = "#e64360"
BLUE = "#34a1eb"

external_stylesheets = ["custom-styles.css"]

app = Dash(__name__, external_stylesheets = external_stylesheets)

####################
##### APP BODY #####
####################
app.layout = html.Div([
    # page header
    html.H1(PAGE_TITLE),

    # frame for displaying graph
    html.Iframe(srcDoc = "", width="70%", height="500", id = "graph-display",
                style = {"display": "inline-block", "width": "75%",
                         "height": "750px"}),

    # sidebar for graph settings
    html.Div([
        # sliders
        html.Label("Number of nodes:"),
        dcc.Slider(min = 1, max = 20, step = 1, value = 10, id = "node-slider",
                   marks = {i: str(i) for i in [1, 5, 10, 15, 20]}),

        html.Label("Probability of an edge forming:"),
        dcc.Slider(min = 0, max = 1, step = .1, value = .2, id = "p-slider",
                   marks = {i: str(i) for i in [0, .2, .4, .6, .8, 1]}),

        html.Label("Proportion of color 1:"),
        dcc.Slider(min = 0, max = 1, step = .1, value = .2, id = "p-red-slider",
                   marks = {i: str(i) for i in [0, .2, .4, .6, .8, 1]}),


        # color picker text inputs
        html.Div([
            html.Label("Color 1:", style = {"width": "45%"}),
            html.Div(
                daq.ColorPicker(
                    id = "color1-input", 
                    value = {"hex": RED}
                ),
                style = {"width": "30%"}
            )]),

        html.Div([
            html.Label("Color 2:", style = {"width": "45%"}),
            html.Div(
                daq.ColorPicker(
                    id = "color2-input", 
                    value = {"hex": BLUE}
                ),
                style = {"width": "30%"}
            )])],

        style = {"display": "inline-block", "width": "20%", 
                 "vertical-align": "top"}
    )
])


#####################
##### CALLBACKS #####
#####################
"""
Create test graph with n nodes with probability p of an edge between them.
For this test graph, 50% of the nodes are red, and the others blue. This is a
simple graph to be used only for troubleshooting or proof of concept
"""
@app.callback(
    Output("graph-display", "srcDoc"),
    Input("node-slider", "value"),
    Input("p-slider", "value"),
    Input("p-red-slider", "value"),
    Input("color1-input", "value"),
    Input("color2-input", "value")
)
def generate_test_graph(n, p, p_color1, color1, color2):
    G = nx.erdos_renyi_graph(n, p)
    num_color1 = int(n * p_color1)

    for i in range(len(G.nodes())):
        if i < num_color1:
            G.nodes[i]["color"] = color1["hex"]
        else:
            G.nodes[i]["color"] = color2["hex"]

    net = Network(notebook = True, height = "1000px", cdn_resources = "in_line")
    net.from_nx(G)
    net.show("temp-net.html")

    with open("temp-net.html", "r") as file:
        content = file.read()

    return content


###################
##### RUN APP #####
###################
if __name__ == '__main__':
    app.run(debug=True)
