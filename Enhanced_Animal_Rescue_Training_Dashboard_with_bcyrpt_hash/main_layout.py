# main_layout.py
# Setup the Jupyter version of Dash
from jupyter_dash import JupyterDash

# Configure the necessary Python module imports
import dash_leaflet as dl
from dash import Dash
from dash import dcc
from dash import html
import plotly.express as px
from dash import dash_table
from dash.dependencies import Input, Output, State
import base64

# Configure OS routines
import os

# change animal_shelter and AnimalShelter to match your CRUD Python module file name and class name
from AnimalShelters import AnimalShelter

# Configure the plotting routines
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


###########################
# Data Manipulation / Model
###########################



# Debug
# print(len(df.to_dict(orient='records')))
# print(df.columns)
#print(df)



def create_main_layout(app, username, password):
    image_filename = 'Grazioso Salvare Logo.png' # Graziosos Salvare Logo
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())  
    app.previous_clicks = {'button0': 0, 'button1': 0, 'button2': 0, 'button3': 0}
   
    #  username and password and CRUD Python module name.
    #db = AnimalShelter(username, password)
    #df = pd.DataFrame.from_records(app.db.read({}))
    #df.drop(columns=['_id'], inplace=True)
    
    # Ensure app.db is initialized
    if app.db is not None:
        df = pd.DataFrame.from_records(app.db.read({}))
        df.drop(columns=['_id'], inplace=True)
    else:
        return html.Div("Database connection not established.")
    
    main_layout = html.Div([
        html.Div(id='hidden-div', style={'display': 'none'}),
        html.Center(html.B(html.H1('KaLee Li Dashboard'))),
        html.Hr(),
        html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'height': '20%', 'width': '20%'}), 
        html.Div(className='buttonRow', 
                 style={'display': 'flex'},
                 children=[
                     html.Button(id='submit-button-zero', n_clicks=0, children='Reset To All', style={'fontSize': '20px'}),
                     html.Button(id='submit-button-one', n_clicks=0, children='Water', style={'fontSize': '20px'}),
                     html.Button(id='submit-button-two', n_clicks=0, children='Mountain/Wilderness', style={'fontSize': '20px'}),
                     html.Button(id='submit-button-three', n_clicks=0, children='Disaster/Individual Tracking', style={'fontSize': '20px'})
                 ]),
        dash_table.DataTable(
            id='datatable-id',
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": True}
                for i in df.columns
            ],
            data=df.to_dict('records'),
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable=False,
            row_selectable="single",
            row_deletable=False,
            selected_columns=[],
            selected_rows=[0],
            page_action="native",
            page_current=0,
            page_size=10
        ),
        html.Br(),
        html.Hr(),
        # This sets up the dashboard so that chart and your geolocation chart are side-by-side
        html.Div(className='row',
                 style={'display': 'flex'},
                 children=[
                     html.Div(id='graph-id', className='col s12 m6'),
                     html.Div(id='map-id', className='col s12 m6'),
                 ])
    ], style={'textAlign': 'center'})
     
    return main_layout

#############################################
# Interaction Between Components / Controller
#############################################

def register_callback(app):
    print("Callback triggered")
    # This callback will highlight a row on the data table when the user selects it
    @app.callback(
        Output('datatable-id', 'style_data_conditional'),
        Input('datatable-id', 'selected_columns')
    )
    def update_styles(selected_columns):
        return [{
            'if': {'column_id': i},
            'background_color': '#D2F3FF'
        } for i in selected_columns]
    
    # This callback will update the geo-location chart for the selected data entry
    @app.callback(
        Output('map-id', "children"),
        Input('datatable-id', "derived_virtual_data"),
        Input('datatable-id', "derived_virtual_selected_rows")
    )
    def update_map(viewData, index):
        print("Callback triggered 2")
        dff = pd.DataFrame.from_dict(viewData)

        if dff.empty:
            return []

        row = index[0] if index else 0

        return [
            dl.Map(style={'width': '1000px', 'height': '500px'},
                   center=[30.75, -97.48], zoom=10, children=[
                dl.TileLayer(id="base-layer-id"),
                dl.Marker(position=[dff.iloc[row, 13], dff.iloc[row, 14]], 
                          children=[
                              dl.Tooltip(dff.iloc[row, 4]),
                              dl.Popup([
                                  html.H1("Animal Name"),
                                  html.P(dff.iloc[row, 9])
                              ])
                          ])
            ])
        ]
    # Display the breeds of animal based on quantity represented in the data table
    @app.callback(
        Output('graph-id', "children"),
        Input('datatable-id', "derived_viewport_data")
    )
    def update_graphs(viewData):

        dff = pd.DataFrame.from_dict(viewData)
        

        if dff.empty:
            return []

        return [
            dcc.Graph(
                figure=px.pie(dff, names='breed', title='Preferred Animals'),
            )
        ]
def register_button(app, db):
    # This callback will filter breed and age based on training expertise
    @app.callback(
        Output('datatable-id', "data"),
        Input('submit-button-zero', 'n_clicks'),
        Input('submit-button-one', 'n_clicks'),
        Input('submit-button-two', 'n_clicks'),
        Input('submit-button-three', 'n_clicks')
    )
    def on_click(button0, button1, button2, button3):
      
        df = pd.DataFrame.from_records(db.read({}))
        
        # Filter Logic
        if button0:
            df = pd.DataFrame.from_records(db.read({}))
            #pass
       
        elif button1:
            df = pd.DataFrame.from_records(db.read({
                "breed": {"$in": ["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"]},
                "sex_upon_outcome": "Intact Female",
                "age_upon_outcome_in_weeks": {"$gte": 26.0, "$lt": 156.0}
            }))
        elif button2:
            df = pd.DataFrame.from_records(db.read({
                "breed": {"$in": ["German Shepherd", "Alaskan Malamute", "Old English Sheepdog", "Siberian Husky", "Rottweiler"]},
                "sex_upon_outcome": "Intact Male",
                "age_upon_outcome_in_weeks": {"$gte": 26.0, "$lt": 156.0}
            }))
        elif button3:
            df = pd.DataFrame.from_records(db.read({
                "breed": {"$in": ["Doberman Pinscher", "German Shepherd", "Golden Retriever", "Bloodhound", "Rottweiler"]},
                "sex_upon_outcome": "Intact Male",
                "age_upon_outcome_in_weeks": {"$gte": 20.0, "$lt": 300.0}
            }))

        # Cleanup Mongo _id field
        df.drop(columns=['_id'], inplace=True)

        return df.to_dict('records')
