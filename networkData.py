import pandas as pd
import connection
from dash import html
import dash_bootstrap_components as dbc

COLORS = [
    #Relationships colors
    '#117864',
    '#7B241C',
    '#633974',
    '#F87474',
    '#1A5276',
    '#196F3D',
    '#9A7D0A',
    '#935116',
    '#212F3C',
    '#0E6655',
]

#Function to send data to interface file
def loadNet():
    nodes = nodesLoad()
    edges, legends = edgesLoad()
    return nodes, edges, legends

#Load the nodes from the database
def nodesLoad():
    nodes = pd.DataFrame(connection.loadNodes())
    nodes_list = []
    for row in nodes.to_dict(orient='Records'):
        id, name, lastname = row[0], row[1], row[2]
        nodes_list.append({
            'id': str(id),
            'label': name + ' ' + lastname,
            'shape': 'dot',
            'size': 10,
            'color': '#FF2D2D'
        })
    nodes = nodes_list
    return nodes

#Load the relationships from the database
def edgesLoad():
    edges = pd.DataFrame(connection.loadEdges())
    #Defining the color according to relationships
    relations_list = edges[2].unique()
    colors = {}
    for color in range(0, len(relations_list)):
        colors[relations_list[color]] = COLORS[color]
    
    #Variable that contains the color legends in the graph
    colorLegend = edgesLegend(colors)

    edges_list = []
    for row in edges.to_dict(orient='Records'):
        id, source, relation, target = row[0], row[1], row[2], row[3]
        edges_list.append({
            'id': id,
            'from': source,
            'to': target,
            #'label': relation,
            'color' : {
                'highlight':colors[relation],
                'color': colors[relation],
                'inherit': 'false',
                'opacity':1.0}
        })
    edges = edges_list
    return edges, colorLegend

#Creates the color legend for the graph
def edgesLegend(legend):
    rows = []
    legend_items = legend.items()
    for key, value in legend_items:
        rows.append(dbc.Badge(key, color=value, class_name="me-1"))
    rows = html.Span(rows)
    return rows

#edgesLoad()