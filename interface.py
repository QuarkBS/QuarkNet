from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from numpy import ERR_DEFAULT
import visdcc
import connection
import networkData as nd
import dash_bootstrap_components as dbc

#Call the network data
nodes, edges, colorLegends = nd.loadNet()

#Initialize the dash application
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([

    #Div for the graph
    html.Div(
        id = 'update',
        children=[
            visdcc.Network(id = 'net', data = {'nodes': nodes, 'edges': edges}, selection = {'nodes':[], 'edges':[]}, 
            options = dict(height='auto', width='auto')),
            colorLegends,
            dbc.Button(id='update-button', children='Update', color='secondary', className='me-1')]
    ),

    #Menu
    html.Div(
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        #Add Node
                        dbc.Form(
                            [
                                html.Div(
                                    [
                                        dbc.Label('Name', html_for='input-1-state'),
                                        dbc.Input(id='input-1-state', type='text', placeholder='Enter first name')
                                    ], className='mb-3'
                                ),
                                html.Div(
                                    [
                                        dbc.Label('Last name', html_for='input-2-state'),
                                        dbc.Input(id='input-2-state', type='text', placeholder='Enter last name')
                                    ], className='mb-3'
                                ),
                                dbc.Button(id='submit-button-state', children='Submit', color='primary', className='me-1'),
                                dbc.Alert(id='outpruebas', is_open=False, duration=4000),
                            ]
                        )
                    ], title='Add new node'
                ),
                dbc.AccordionItem(
                    [
                        #Add Relation
                        dbc.Form(
                            [
                                html.Div(
                                    [
                                        dbc.Label('From', html_for='Rinput-1-state'),
                                        dbc.Input(id='Rinput-1-state', type='number', placeholder='Enter ID')
                                    ], className='mb-3'
                                ),
                                html.Div(
                                    [
                                        dbc.Label('To', html_for='Rinput-2-state'),
                                        dbc.Input(id='Rinput-2-state', type='number', placeholder='Enter ID')
                                    ], className='mb-3'
                                ),
                                html.Div(
                                    [
                                        dbc.Label('Type', html_for='Rinput-3-state'),
                                        dbc.Input(id='Rinput-3-state', type='text', placeholder='Enter relationship type')
                                    ], className='mb-3'
                                ),
                                dbc.Button(id='Rsubmit-button-state', children='Submit', color='primary', className='me-1'),
                                dbc.Alert(id='outpruebas2', is_open=False, duration=4000),
                            ]
                        )
                    ], title='Add new relationship'
                ),
                dbc.AccordionItem(
                    [
                        #Delete Relation
                        dbc.Form(
                            [
                                html.Div(
                                    [
                                        dbc.Label('From', html_for='Rdelete-1-state'),
                                        dbc.Input(id='Rdelete-1-state', type='number', placeholder='Enter ID')
                                    ], className='mb-3'
                                ),
                                html.Div(
                                    [
                                        dbc.Label('To', html_for='Rdelete-2-state'),
                                        dbc.Input(id='Rdelete-2-state', type='number', placeholder='Enter ID')
                                    ], className='mb-3'
                                ),
                                html.Div(
                                    [
                                        dbc.Label('Type', html_for='Rdelete-3-state'),
                                        dbc.Input(id='Rdelete-3-state', type='text', placeholder='Enter relationship type')
                                    ], className='mb-3'
                                ),
                                dbc.Button(id='Rdelete-button-state', children='Submit', color='danger', className='me-1'),
                                dbc.Alert(id='outpruebas3', is_open=False, duration=4000),
                            ]
                        )
                    ], title='Delete existing relationship'
                ),
                dbc.AccordionItem(
                    [
                        #Delete Node
                        dbc.Form(
                            [
                                html.Div(
                                    [
                                        dbc.Label('ID', html_for='RNdelete-1-state'),
                                        dbc.Input(id='RNdelete-1-state', type='number', placeholder='Enter ID')
                                    ], className='mb-3'
                                ),
                                dbc.Button(id='RNdelete-button-state', children='Submit', color='danger', className='me-1'),
                                dbc.Alert(id='outpruebas4', is_open=False, duration=4000),
                            ]
                        )
                    ], title='Delete existing node'
                ),
            ],
            style={'height':'auto', 'width':'auto'},
        ),
    ),
    #html.Div(id='nodes'),html.Div(id='edges')
], style={'display': 'flex', 'justify-content':'space-between'})

#Refresh the graph
@app.callback(
    Output('update', 'children'),
    Input('update-button', 'n_clicks')
)
def update(n_clicks):
    nodes, edges, colorLegends = nd.loadNet()
    return html.Div(children=[
        visdcc.Network(id = 'net', data = {'nodes': nodes, 'edges': edges}, selection = {'nodes':[], 'edges':[]},
        options = dict(height='600px', width='900px')),
        colorLegends,
        dbc.Button(id='update-button', children='Update', color='secondary', className='me-1')]
        )

#Create new node method
@app.callback(
    Output('outpruebas', 'children'),
    Output('outpruebas', 'is_open'),
    [Input('submit-button-state', 'n_clicks')],
    [State('input-1-state', 'value')],
    [State('input-2-state', 'value')],
    [State('outpruebas', 'is_open')]
)
def sendNode(n_clicks, name, lastname, is_open):
    if n_clicks is not None:
        try:
            connection.createNode(name, lastname)
            return 'Se ha creado el nodo {} {} con éxito'.format(name, lastname), not is_open
        except: return 'Unexpected error'
    return ' ','is_open'

#Create new relationship method
@app.callback(
    Output('outpruebas2', 'children'),
    Output('outpruebas2', 'is_open'),
    Input('Rsubmit-button-state', 'n_clicks'),
    State('Rinput-1-state', 'value'),
    State('Rinput-2-state', 'value'),
    State('Rinput-3-state', 'value'),
    [State('outpruebas2', 'is_open')]
)
def sendRelation(n_clicks, begin, end, relation, is_open):
    if n_clicks is not None:
        try:
            connection.createRelationship(begin, end, relation)
            return 'Se ha creado la relación {}-{}-{} con éxito'.format(begin, relation, end), not is_open
        except: return 'Unexpected error'
    return ' ','is_open'

#Delete existing node method
@app.callback(
    Output('outpruebas4', 'children'),
    Output('outpruebas4', 'is_open'),
    Input('RNdelete-button-state', 'n_clicks'),
    State('RNdelete-1-state', 'value'),
    [State('outpruebas4', 'is_open')]
)
def deleteNode(n_clicks, idNode, is_open):
    if n_clicks is not None:
        try:
            connection.deleteNode(idNode)
            return 'Se ha borrado el nodo {} con éxito'.format(idNode), not is_open
        except: return 'Unexpected error'
    return ' ','is_open'

#Delete existing relationship method
@app.callback(
    Output('outpruebas3', 'children'),
    Output('outpruebas3', 'is_open'),
    Input('Rdelete-button-state', 'n_clicks'),
    State('Rdelete-1-state', 'value'),
    State('Rdelete-2-state', 'value'),
    State('Rdelete-3-state', 'value'),
    [State('outpruebas3', 'is_open')]
)
def deleteRelation(n_clicks, begin, end, relation, is_open):
    if n_clicks is not None:
        try:
            connection.deleteRelationship(begin, end, relation)
            return 'Se ha borrado la relación {}-{}-{} con éxito'.format(begin, relation, end), not is_open
        except: return 'Unexpected error'
    return ' ','is_open'

#Get selected node ID
#@app.callback(
#    Output('nodes', 'children'),
#    [Input('net', 'selection')])
#def myfun(x):
#    s = 'Selected node : '
#    if len(x['nodes']) > 0 : s += str(x['nodes'][0])
#    return s

#Get selected edge ID
#@app.callback(
#    Output('edges', 'children'),
#    [Input('net', 'selection')])
#def myfun(x):
#    s = 'Selected edges : '
#    if len(x['edges']) > 0 : s = [s] + [html.Div(i) for i in x['edges']]
#    return s

if __name__ == '__main__':
    app.run_server()