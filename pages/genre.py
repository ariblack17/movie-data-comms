##----------------------------------- imports -----------------------------------##
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

from pages._matplotlib_figs import *
from pages._styles import *

##----------------------------------- register page -----------------------------------##
dash.register_page(__name__, path='/genre')

##----------------------------------- styles (temp) -----------------------------------##

##----------------------------------- define elements -----------------------------------##

## graph 21a, box ratings by genre
    #region

graph21a = go.Figure()

## one trace per box/genre
graph21a.add_trace(go.Box(y=df_family['rating'],name=labels[0], boxpoints='suspectedoutliers', marker_color='#FF88B4')) ## dark pink
graph21a.add_trace(go.Box(y=df_crime['rating'],name=labels[1], boxpoints='suspectedoutliers', marker_color='#FFB3D2')) ## pink
graph21a.add_trace(go.Box(y=df_thriller['rating'],name=labels[2], boxpoints='suspectedoutliers', marker_color='#E3E3FF')) ## light purp
graph21a.add_trace(go.Box(y=df_romance['rating'],name=labels[3], boxpoints='suspectedoutliers', marker_color='#BCC0D6')) ## purple
graph21a.add_trace(go.Box(y=df_comedy['rating'],name=labels[4], boxpoints='suspectedoutliers', marker_color='#89C3CF')) ## blue
graph21a.add_trace(go.Box(y=df_action['rating'],name=labels[5], boxpoints='suspectedoutliers', marker_color='#76A7B2')) ## dark blue
graph21a.add_trace(go.Box(y=df_horror['rating'],name=labels[6], boxpoints='suspectedoutliers', marker_color='#FDC899')) ## orange
graph21a.add_trace(go.Box(y=df_scifi['rating'],name=labels[7], boxpoints='suspectedoutliers', marker_color='#FDAB62')) ## dark orange
graph21a.add_trace(go.Box(y=df_mystery['rating'],name=labels[8], boxpoints='suspectedoutliers', marker_color='#CDE4CF')) ## green
graph21a.add_trace(go.Box(y=df_adventure['rating'],name=labels[9], boxpoints='suspectedoutliers', marker_color='#FFEDAE')) ## yellow
graph21a.add_trace(go.Box(y=df_drama['rating'],name=labels[10], boxpoints='suspectedoutliers', marker_color='#FFE072')) ## gold
graph21a.add_trace(go.Box(y=df_other['rating'],name=labels[11], boxpoints='suspectedoutliers', marker_color='#C28F4F')) ## tan

graph21a.update_layout(width=1000, height=800, 
                     margin=dict(l=10, r=20, t=50, b=20),
                     xaxis=dict(title='Genre'),
                     yaxis=dict(title='TMDb Rating'),
                     title='TMDb Ratings by Film Genre',
                     title_x=0.5,
                     showlegend=False,
                     )
    #endregion

## graph 21b, z-score rev by genre
    #region

graph21b = go.Figure()

colors21b = ['#76A7B2']*13
colors21b[12] = '#BCC0D6'
labels21b = [i for i in labels]
if ('Animation' not in labels):
    labels21b.append('Animation')


graph21b.add_trace(go.Bar(
    x=z_scores,
    y=labels21b,
    orientation='h',
    marker_color=colors21b
))

graph21b.update_layout(width=800, height=600, 
                     margin=dict(l=10, r=20, t=50, b=20),
                     yaxis=dict(title='Genre'),
                     xaxis=dict(title='Z-Score'),
                     title='Z-Score of Revenue by Genre',
                     title_x=0.5,
                     showlegend=False,
                     )

    #endregion

##---------------------------- cards ----------------------------##

genre_card = dbc.Card( ## genre trends card
        [
            dbc.CardBody(
                [
                    html.H4(id='genre_card_title', children=['Are there any genres which perform better than others?'], className='card-title',
                            style=CARD_TEXT_STYLE),
                    html.P(id='genre_card_text', children=['Metrics: average TMDb ratings and revenue'], style=CARD_TEXT_STYLE),
                ]
            )
        ]
    )

genre_box_card1 = dbc.Card( ## highest rated genres card
        [
            dbc.CardBody(
                [
                    html.H4(id='genre_box_card1_title', children=['Highest rated genres'], className='card-title',
                            style=CARD_TEXT_STYLE),
                    # html.P(id='genre_box_card_text', children=[''], style=CARD_TEXT_STYLE),
                ]
            )
        ]
    )

genre_box_card2 = dbc.Card( ## lowest rated genres card
        [
            dbc.CardBody(
                [
                    html.H4(id='genre_box_card2_title', children=['Lowest rated genres'], className='card-title',
                            style=CARD_TEXT_STYLE),
                    # html.P(id='genre_box_card2_text', children=[''], style=CARD_TEXT_STYLE),
                ]
            )
        ]
    )

genre_box_card3 = dbc.Card( ## highest performing genres card
        [
            dbc.CardBody(
                [
                    html.H4(id='genre_box_card3_title', children=['Highest performing genres'], className='card-title',
                            style=CARD_TEXT_STYLE),
                    # html.P(id='genre_box_card3_text', children=[''], style=CARD_TEXT_STYLE),
                ]
            )
        ]
    )

genre_box_card4 = dbc.Card( ## lowest rev genres card
        [
            dbc.CardBody(
                [
                    html.H4(id='genre_box_card4_title', children=['Lowest performing genres'], className='card-title',
                            style=CARD_TEXT_STYLE),
                    # html.P(id='genre_box_card4_text', children=[''], style=CARD_TEXT_STYLE),
                ]
            )
        ]
    )

genre_note_card = dbc.Card( ## lowest rev genres card
        [
            dbc.CardBody(
                [
                    html.H4(id='genre_note_card_title', children=['Note:'], className='card-title',
                            style=CARD_TEXT_STYLE),
                    html.P(id='genre_note_card_text', children=[
                        'The "Animation" category is actually part of "Other," but is shown separately here for comparison.'], style=CARD_TEXT_STYLE),
                ]
            )
        ], color='success', outline='True'
    )
##---------------------------- rows ----------------------------##
content_seventh_row = dbc.Row( ## row: genre box plot and cards
    [
        dbc.Col( [
            genre_card,
            dbc.Row ([
                dbc.Col(dcc.Graph(figure=graph21a), style={'margin-top':'30px'}),
                dbc.Col([
                    genre_box_card1,
                    html.P('Drama', style=GENRE_TEXT_STYLE),
                    html.P('Animation', style=GENRE_TEXT_STYLE),
                    html.P('Crime', style=GENRE_TEXT_STYLE),
                    genre_box_card2,
                    html.P('Horror', style=GENRE_TEXT_STYLE),
                    html.P('Comedy', style=GENRE_TEXT_STYLE),
                    html.P('Thriller', style=GENRE_TEXT_STYLE),
                    
                ])
            ], style={'align-items':'center'})
            # dcc.Graph(figure=graph21a), width=6 
            # table13, width=6
        ]),

    ]
)

content_eighth_row = dbc.Row( ## row: z-score chart
    [
        dbc.Col( [
            dbc.Row([
                dbc.Col([
                    genre_box_card3,
                    html.P('Animation, Drama, Adventure', style=GENRE_TEXT_STYLE),
                    # html.P('Drama', style=GENRE_TEXT_STYLE),
                    # html.P('Adventure', style=GENRE_TEXT_STYLE),
                    genre_box_card4,
                    html.P('Family, Crime, Thriller', style=GENRE_TEXT_STYLE),
                    genre_note_card,
                    # html.P('Crime', style=GENRE_TEXT_STYLE),
                    # html.P('Thriller', style=GENRE_TEXT_STYLE),
                ]),
                dbc.Col(dcc.Graph(figure=graph21b), style={'margin-top':'30px'}),
            ], style={'align-items':'center', 'justify':'center'})
        ]),

    ]
)



##---------------------------- layout ----------------------------##
    #    content_seventh_row,
    #     content_eighth_row,

layout = html.Div([
    content_seventh_row,
    content_eighth_row

])


##---------------------------- callbacks ----------------------------##


