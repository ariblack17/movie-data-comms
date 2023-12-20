#
# 
# HOME PAGE
# 
# 


##----------------------------------- imports -----------------------------------##

import dash
import dash_bootstrap_components as dbc
from dash import html
from pages._matplotlib_figs import *
from pages._styles import *


##----------------------------------- register page -----------------------------------##

dash.register_page(__name__, path='/')


##---------------------------- images ----------------------------##

    #region
slate_image = './assets/slate1.jpg'
tmdb_image = './assets/tmdb_home.jpeg'
    #endregion


##---------------------------- rows ----------------------------##

## four cards row
content_first_row = dbc.Row([ ## row 1
    dbc.Col(
        dbc.Card( ## card 1
            [
                dbc.CardBody(
                    [
                        html.H4(id='card_title_1', children=['Source'], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html.P(id='card_text_1', children=['Metadata from 5000 films scraped from TMDb: The Movie Database'], style=CARD_TEXT_STYLE),
                    ]
                )
            ]
        ),
        md=3
    ),
    dbc.Col(
        dbc.Card( ## card 2
            [
                dbc.CardBody(
                    [
                        html.H4('Relevancy', className='card-title', style=CARD_TEXT_STYLE),
                        html.P('Entries from the early 1990s to 2017, and predominantly first released in English', style=CARD_TEXT_STYLE),
                    ]
                ),
            ]

        ),
        md=3
    ),
    dbc.Col(
        dbc.Card( ## card 3
            [
                dbc.CardBody(
                    [
                        html.H4('Key Metrics', className='card-title', style=CARD_TEXT_STYLE),
                        html.P('Popularity (based on user interaction), and Vote Average (based on user votes)', style=CARD_TEXT_STYLE),
                    ]
                ),
            ]

        ),
        md=3
    ),
    dbc.Col(
        dbc.Card( ## card 4
            [
                dbc.CardBody(
                    [
                        html.H4('Size', className='card-title', style=CARD_TEXT_STYLE),
                        html.P('Data split across two csv files with over 20,000 data entries each', style=CARD_TEXT_STYLE),
                    ]
                ),
            ]
        ),
        md=3
    )
])

content_goals = dbc.Row([
    html.Hr(),
    html.H2('Goals for this project', style=TEXT_STYLE),
    html.Hr(),
    html.Br(),
    ## developmental goals
    html.H4('Developmental', style=GENRE_TEXT_STYLE),
    html.P('Identify and answer guiding research questions, including: what factors affect how well a film is recieved, and can we predict anything about a film before its release?', style=GENRE_TEXT_STYLE),
    html.P('Extract and present interesting information from a large dataset, converting it into a digestible form', style=GENRE_TEXT_STYLE),

    ## personal goals
    html.H4('Personal', style=GENRE_TEXT_STYLE),
    html.P("Develop better data communication skills in a way that interests me", style=GENRE_TEXT_STYLE),
    html.P("Produce a final product which showcases my familiarity with data visualization tools", style=GENRE_TEXT_STYLE),



])


image_row1 = dbc.Row([
        html.Div(html.Img(src=slate_image, style={'height':'70%', 'width':'70%'}), 
                 style={'textAlign':'center'}),], style={'align-items':'center', 'display':'flex'})


image_row2 = dbc.Row([
        html.Div(html.Img(src=tmdb_image, style={'height':'90%', 'width':'90%'}), 
                 style={'textAlign':'center'}),], style={'align-items':'center', 'display':'flex', 'margin-bottom':'2rem'})



this_dataset = dbc.Row([
    html.Hr(),
    html.H2('The dataset', style=TEXT_STYLE),
    html.Hr(),
    html.Br(),
    image_row2,
    html.Br(),
    html.Br(),
    html.Br(),
    content_first_row

])

project_extensions = dbc.Row([
    html.Hr(),
    html.H2('Future extensions', style=TEXT_STYLE),
    html.Hr(),
    html.Br(),
    ## prediction model
    html.H4('Prediction model', style=GENRE_TEXT_STYLE),
    html.P("Use machine learning to generate and train a prediction model which can evaluate a film's potential success prior to its release", style=GENRE_TEXT_STYLE),
    html.P('Propel this project beyond data communication and visualization, and into data mining', style=GENRE_TEXT_STYLE),
    ## explore other factors
    html.H4('Divulging new trends', style=GENRE_TEXT_STYLE),
    html.P("Go deeper into film research, and push beyond finding trends within a single dataset", style=GENRE_TEXT_STYLE),
    html.P('Uncover more trends regarding film analytics, considering factors which are not present in the current database', style=GENRE_TEXT_STYLE),

])




##---------------------------- layout ----------------------------##

layout = html.Div([
    image_row1,
    html.Br(),
    html.Br(),
    content_goals,
    html.Br(),
    this_dataset,
    html.Br(),
    project_extensions
])


##---------------------------- callbacks ----------------------------##


