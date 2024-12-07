# login_layout.py
# DASH Framework for Jupyter
from jupyter_dash import JupyterDash
from dash import dcc
from dash import html
from dash import State
from dash.dependencies import Input, Output
from UserManager import UserManager 
from AnimalShelters import AnimalShelter
import pandas as pd

# URL Lib to make sure that our input is 'sane'
import urllib.parse

from main_layout import create_main_layout, register_callback, register_button

user_manager = UserManager()

login_layout = html.Div([
    html.H1("Login or Register"),
    
    dcc.Input(
        id="input_user",
        type="text",
        placeholder="Enter Username"),
    
    dcc.Input(
        id="input_passwd",
        type="password",
        placeholder="Enter Password"),
    
    # Login button
    html.Button('Login', id='submit-login', n_clicks=0),
    
    # Register button
    html.Button('Register', id='submit-register', n_clicks=0),
    
    html.Hr(),
    html.Div(id="query-out", style={'whiteSpace': 'pre-line'})
])

def register_login_callback(app):
    @app.callback(
        [Output('page-content', 'children'),
         Output('url', 'pathname'), # Set pathname to switch layout after login
         Output('query-out', 'children')],  
        [Input('submit-login', 'n_clicks'),
         Input('submit-register','n_clicks')],
        State('input_user', 'value'),
        State('input_passwd', 'value')
    )
    
    def render_layout(n_clicks_login, n_clicks_register, inputUser, inputPasswd):
        
        if n_clicks_login == 0 and n_clicks_register == 0:
            return login_layout, '/login',""
        
        if n_clicks_login > 0:
            if inputUser and inputPasswd:
                username = inputUser
                password = inputPasswd
                # Validate user credentials via UserManager
                animal_shelter = user_manager.validate_user(username, password)
                
                if isinstance(animal_shelter, AnimalShelter):
                    app.db = animal_shelter
                    
                    # Create main layout and register callbacks
                    main_layout = create_main_layout(app, username, password)
                    register_callback(app)
                    register_button(app, app.db)
                    return main_layout, '/main',""
                else: 
                    return login_layout, '/login', "Invalid username or password" 
        if n_clicks_register > 0:
            
            if inputUser and inputPasswd:
                username = inputUser
                password = inputPasswd
                # Register the user via UserManager
                register_result = user_manager.register_user(username, password)
                
                if "successfully" in register_result:
                    # Show a message to inform the user that they can log in now
                    return login_layout,'/login', "Registration successful! You can now log in using the Login button."
                else:
                    return login_layout, '/login', register_result        
                      
        return login_layout, '/login', "Please enter both username and password."
