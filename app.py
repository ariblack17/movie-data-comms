
#
# 
# DASH APP LAYOUT / MAIN FUNCTION
# 
# 


##----------------------------------- imports -----------------------------------##

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash_bootstrap_templates import load_figure_template
from pages._matplotlib_figs import *
from pages._styles import *
from pages._utility import *


##----------------------------------- init app -----------------------------------##

    #region
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
load_figure_template('lux')
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX, dbc_css], use_pages=True, 
                suppress_callback_exceptions=True)

    #endregion


##----------------------------------- define elements -----------------------------------##

## sidebar
sidebar = html.Div([
    ## headers
        html.H4("A project by Ari.", className="display-7"),
        html.Hr(),
        html.P(
            "What trends can we extract from the database?", className="lead"
        ),
        ## links to pages
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Top films", href="/top_films", active="exact"),
                dbc.NavLink("Genres", href="/genre", active="exact"),
                dbc.NavLink("Cast", href="/cast", active="exact"),
                dbc.NavLink("Other analytics", href="/analytics", active="exact"),

            ],
            vertical=True,
            pills=True,
        ),
        
    ],
    style=SIDEBAR_STYLE,
)            


##---------------------------- layout ----------------------------##

## layout of content for all pages
content = html.Div( ## page content: header and page container
    [
        ## title
        html.H2('Using Metadata to Predict Success in the Film Industry', style=TEXT_STYLE), 
        html.Hr(),
        html.Br(),
        ## the contents of the linked page
        dash.page_container,    
    ],
        style=CONTENT_STYLE, id='page-content'
    

)

## put everything together
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


##---------------------------- start server ----------------------------##

if __name__=='__main__':
    print('starting dash...')
    app.run_server(debug=True) ## debug to enable automatic reload

