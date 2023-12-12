
# -----
# 
# # dash
# 
# 

##----------------------------------- imports -----------------------------------##
    #region 


import dash
import dash_bootstrap_components as dbc
from dash import dcc, callback
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
from plotly.tools import mpl_to_plotly
import plotly.graph_objects as go
from dash import dash_table
from PIL import Image
from dash_bootstrap_templates import load_figure_template
from pages._matplotlib_figs import *
from pages._styles import *
from pages._utility import *

#endregion

##----------------------------------- init app -----------------------------------##
    #region
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
load_figure_template('lux')
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX, dbc_css], use_pages=True, suppress_callback_exceptions=True)


    #endregion


##----------------------------------- define elements -----------------------------------##

## sidebar
sidebar = html.Div([
        html.H4("A project by Ari.", className="display-7"),
        html.Hr(),
        ## section 1
        html.P(
            "What trends can we extract from the database?", className="lead"
        ),
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







##---------------------------- cards ----------------------------##

# genre_button = html.Button(id='genre_button', n_clicks=0, children="Show table",
#                     style={'font-size': '12px', 'width': '140px', 'display': 'inline-block', 'margin-bottom': '10px', 'margin-right': '5px', 'height':'25px'})
    
# genre_button = dbc.Button('genre', outline=True, color='secondary', className='me-1')


##---------------------------- rows ----------------------------##



            

##---------------------------- layout ----------------------------##

content = html.Div( ## page content: header and page container
    [
        html.H2('Using Metadata to Predict Success in the Film Industry', style=TEXT_STYLE),
        html.Hr(),
        html.Br(),
        dash.page_container,    ## the contents of the linked page

    ],
        style=CONTENT_STYLE, id='page-content'
    

)

## put everything together
# app.layout = html.Div([content, extra])
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])
# app.layout = html.Div([content])


##---------------------------- callbacks ----------------------------##

## old sidebar stuff
    #region

# @app.callback(Output("page-content", "children"), [Input("url", "pathname")]) ## sidebar
# def render_page_content(pathname):
#     if pathname == "/":
#         return html.P("This is the content of the home page!")
#     elif pathname == "/genre":
#         return html.P("This is the content of page 1. Yay!")
#     elif pathname == "/page-2":
#         return html.P("Oh cool, this is page 2!")
#     # If the user tries to reach a different page, return a 404 message
#     return html.Div(
#         [
#             html.H1("404: Not found", className="text-danger"),
#             html.Hr(),
#             html.P(f"The pathname {pathname} was not recognised..."),
#         ],
#         className="p-3 bg-light rounded-3",
#     )

    #endregion



##---------------------------- start server ----------------------------##

if __name__=='__main__':
    # app.run_server(mode='external', port=8050, host='127.0.0.1')
    print('starting dash...')
    # app.run_server(debug=True, use_reloader=False)
    # app.run_server(debug=True)
    app.run_server()



