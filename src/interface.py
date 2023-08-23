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
            visdcc.Network(
                id = 'net', 
                data = {'nodes': [], 'edges': []},
                style={
                    'position' : 'absolute',
                    'top' : '0px',
                    'right': '0px'
                }
            )
        ],
    ),
    #Menu
    html.Div([
        dbc.Alert(id='nodes', is_open=False, duration=4000),
        dbc.Card(
            dbc.CardBody([
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
                                        dbc.Button(id='submit-button-state', children='Submit', color='success', className='me-1'),
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
                                        dbc.Button(id='Rsubmit-button-state', children='Submit', color='success', className='me-1'),
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
                    style={
                        'padding-bottom' : 'inherit'
                    }
                ),
                dbc.Button(id='update-button', children='Update', color='primary', className='me-1')
            ]),
            style={
                'position' : 'absolute',
                'top' : '0px',
                'right': '0px',
                'bottom': '0px',
                'border-left': '1px solid rgb(238, 241, 246)',
                'justify-content':'start',
                'flex-direction': 'column',
                '-webkit-box-pack': 'start'
            },
        ),
    ]),
])

#Refresh the graph
@app.callback(
    Output('update', 'children'),
    Input('update-button', 'n_clicks'),
    prevent_initial_call=True
)
def update(n_clicks):
    nodes, edges, colorLegends = nd.loadNet()
    return html.Div(
        id = 'update',
        children=[
            visdcc.Network(
                id = 'netUpdated', 
                data = {'nodes': nodes, 'edges': edges}, 
                selection = {'nodes':[], 'edges':[]},
                style={
                    'position' : 'absolute',
                    'top' : '0px',
                    'right': '0px',
                    'bottom': '0px',
                }),
            colorLegends
        ]
    )

#Create new node method
@app.callback(
    Output('outpruebas', 'children'),
    Output('outpruebas', 'is_open'),
    [Input('submit-button-state', 'n_clicks')],
    [State('input-1-state', 'value')],
    [State('input-2-state', 'value')],
    [State('outpruebas', 'is_open')],
    prevent_initial_call=True
)
def sendNode(n_clicks, name, lastname, is_open):
    if n_clicks is not None:
        try:
            connection.createNode(name, lastname)
            return 'Se ha creado el nodo {} {} con éxito'.format(name, lastname), not is_open
        except: return 'Unexpected error'
    return '', False

#Create new relationship method
@app.callback(
    Output('outpruebas2', 'children'),
    Output('outpruebas2', 'is_open'),
    Input('Rsubmit-button-state', 'n_clicks'),
    State('Rinput-1-state', 'value'),
    State('Rinput-2-state', 'value'),
    State('Rinput-3-state', 'value'),
    [State('outpruebas2', 'is_open')],
    prevent_initial_call=True
)
def sendRelation(n_clicks, begin, end, relation, is_open):
    if n_clicks is not None:
        try:
            connection.createRelationship(begin, end, relation)
            return 'Se ha creado la relación {}-{}-{} con éxito'.format(begin, relation, end), not is_open
        except: return 'Unexpected error'
    return '', False

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
    return '', False

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
    return '', False

#Get selected node ID
@app.callback(
    Output('nodes', 'children'),
    Output('nodes', 'is_open'),
    [Input('netUpdated', 'selection')],
    [State('nodes','is_open')], 
    )
def selectNode(x, is_open):
    if len(x['nodes']) > 0: 
        return 'Selected Node ID: ' + str(x['nodes'][0]), not is_open
    return '', False

if __name__ == '__main__':
    app.run_server()