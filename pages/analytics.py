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
from pages._utility import *

##----------------------------------- register page -----------------------------------##
dash.register_page(__name__, path='/analytics') 


##----------------------------------- define elements -----------------------------------##

## top 10 budgets bar graph
    #region
fig_bar_budget = go.Figure()
colors_bar_budget = util_colors[:10]
labels_bar_budget = axU7_labels

fig_bar_budget.add_trace(go.Bar(
    x=df_budget['budget'],
    y=labels_bar_budget,
    orientation='h',
    marker_color=colors_bar_budget,
    opacity=0.7
))
fig_bar_budget.update_layout(width=850, height=600, 
                     margin=dict(l=10, r=20, t=50, b=20),
                     yaxis=dict(title='Film Title'),
                     xaxis=dict(title='Budget'),
                     title='Films with the 10 Highest Budgets',
                     title_x=0.5,
                     showlegend=False,
                     )
    #endregion

## box plot budget/revenue
    #region

fig_box = go.Figure()
util_df = df_movies.copy()
util_df = util_df[['budget', 'revenue']]
util_df['budget'] = df_movies['budget'].div(1000000)
util_df = util_df[util_df['revenue'] != 0]
util_df = util_df[util_df['budget'] != 0]

fig_box.add_trace(go.Box(x=util_df['budget'],name='Budget', boxpoints='suspectedoutliers', marker_color='#76A7B2'))
fig_box.add_trace(go.Box(x=util_df['revenue'].div(1000000),name='Revenue', boxpoints='suspectedoutliers', marker_color='#89C3CF')) 
fig_box.update_layout(width=800, height=600, 
                     margin=dict(l=10, r=20, t=50, b=20),
                     yaxis=dict(title='Metric'),
                     xaxis=dict(title='Value (millions)'),
                     title='Budget and Revenue Across all Films',
                     title_x=0.5,
                     showlegend=False,
                     )
fig_box.update_xaxes(range=[0, 400])

    #endregion

## proportion of each genre across all films
    #region
genre_dfs = [df_family, df_crime, df_thriller, df_romance, df_comedy, df_action, 
             df_horror, df_scifi, df_mystery, df_adventure, df_drama, df_other]
genre_lengths = [len(x) for x in genre_dfs]
total_length = sum(genre_lengths)
genre_labels = ['Family','Crime','Thriller', 'Romance','Comedy', 'Action',
        'Horror', 'Science Fiction','Mystery', 'Adventure','Drama', 'Other' ]
fig_pie = go.Figure()
fig_pie.add_trace(go.Pie(
    values=genre_lengths,
    labels=genre_labels, 
    hole=.75
))
fig_pie.update_layout(title='Film Genre Counts',
                    title_x=0.5,
                    font_size=12,
                    width=700, height=600, 
                    margin=dict(l=10, r=20, t=50, b=20),
                )
colors_pie = util_colors_past[:len(genre_labels)]
fig_pie.update_traces(marker=dict(colors=colors_pie))

    #endregion

##---------------------------- images ----------------------------##
    #region
heatmap_image = './assets/heatmap.jpeg'
pca_image = './assets/kmeans.jpeg'
pca_steps_image = './assets/principalcomponents.jpeg'
kmeans_image = './assets/clustercomponents.jpeg'

pirates_image = './assets/pirates.jpeg'
avatar_image = './assets/avatar.jpg'
shawshank_image = './assets/shawshank.jpeg'

    #endregion


##---------------------------- cards ----------------------------##

## misc findings
misc_card = dbc.Row(
    dbc.Card( 
        [
            dbc.CardBody(
                [
                    html.H4(id='misc_card_title', children=['Interesting miscellaneous findings and analyses'], className='card-title',
                            style=CARD_TEXT_STYLE),
                    html.P(id='misc_card_text', children=["Charts and figures that don't fit within the other categories"], style=CARD_TEXT_STYLE),
                ]
            )
        ]
    )
)

bar_card = dbc.Row(
    dbc.Card( 
        [
            dbc.CardBody(
                [
                    html.H2(id='bar_title', children=['Highest budget'], className='card-title',
                            style=CARD_TEXT_STYLE),
                    html.P(id='bar_card_text1', children=["Pirates of the Caribbean: On Stranger Tides"], style=CARD_TEXT_STYLE),
                    # html.H4(id='bar_card_text2', children=["380 million"], style=CARD_TEXT_STYLE),
                ]
            )
        ]
    )
)

box_card = dbc.Row(
    dbc.Card( 
        [
            dbc.CardBody(
                [
                    html.H2(id='box_title', children=['Highest revenue'], className='card-title',
                            style=CARD_TEXT_STYLE),
                    html.P(id='box_card_text1', children=["Avatar"], style=CARD_TEXT_STYLE),
                    # html.H2(id='box_card_text2', children=["2.8 billion"], style=CARD_TEXT_STYLE),
                    
                ]
            )
        ]
    )
)

pie_card = dbc.Row(
    dbc.Card( 
        [
            dbc.CardBody(
                [
                    html.H2(id='pie_title', children=['Largest Proportion'], className='card-title',
                            style=CARD_TEXT_STYLE),
                    html.P(id='pie_card_text2', children=["Drama"], style=CARD_TEXT_STYLE),
                    # html.P(id='pie_card_text1', children=["(number of films which have drama listed as one of their subgenres; 2297 of 4804)"], style=CARD_TEXT_STYLE),
                    
                ]
            )
        ]
    )
)

## analytics

analytics_card = dbc.Row(
    dbc.Card( ## genre trends card
        [
            dbc.CardBody(
                [
                    html.H4(id='analytics_card_title', children=['What other, more complex trends can we find within the movie data?'], className='card-title',
                            style=CARD_TEXT_STYLE),
                    html.P(id='analytics_card_text', children=['Considering deeper forms of analyses'], style=CARD_TEXT_STYLE),
                ]
            )
        ]
    )
)

heatmap_card1 = dbc.Row(
    dbc.Card( ## genre trends card
        [
            dbc.CardBody(
                [
                    html.H4(id='heatmap_card_title', children=['Numerical features heatmap'], className='card-title',
                            style=CARD_TEXT_STYLE),
                    html.P('Displays the Pearson correlation coefficient values for each pair of features', style=GENRE_TEXT_STYLE),

                ]
            )
        ], color='success', outline='True'
    )
)

highlights_card = dbc.Row(
    dbc.Card( ## genre trends card
        [
            dbc.CardBody(
                [
                    html.H4(id='heatmap2_card_title', children=['Highlights'], className='card-title',
                            style=CARD_TEXT_STYLE),

                ]
            )
        ], 
    )
)

hypotheses_card = dbc.Row(
    dbc.Card( ## genre trends card
        [
            dbc.CardBody(
                [
                    html.H4(id='heatmap3_card_title', children=['Hypotheses'], className='card-title',
                            style=CARD_TEXT_STYLE),

                ]
            )
        ], 
    )
)

pca_card1 = dbc.Row(
    dbc.Card( ## pca card
        [
            dbc.CardBody(
                [
                    html.H4(id='pca_card_title', children=['Principle Component Analysis'], className='card-title',
                            style=CARD_TEXT_STYLE),
                    html.P('Summarizes all features (values) in the dataset into a single graph with two axes (principal components)', style=GENRE_TEXT_STYLE),

                ]
            )
        ], color='success', outline='True'
    )
)

interpretation_card = dbc.Row(
    dbc.Card( ## genre trends card
        [
            dbc.CardBody(
                [
                    html.H4(id='heatmap3_card_title', children=['Interpretation'], className='card-title',
                            style=CARD_TEXT_STYLE),

                ]
            )
        ], 
    )
)

pca_steps_card1 = dbc.Row(
    dbc.Card( ## pca card
        [
            dbc.CardBody(
                [
                    html.H4(id='pca_card_title', children=['Plotting explained variance ratio for PCA'], className='card-title',
                            style=CARD_TEXT_STYLE),
                    html.P('Examines how many principal components (categories) we can break the dataset into for analysis', style=GENRE_TEXT_STYLE),

                ]
            )
        ], color='success', outline='True'
    )
)

kmeans_card1 = dbc.Row(
    dbc.Card( ## pca card
        [
            dbc.CardBody(
                [
                    html.H4(id='kmeans_card_title', children=['K-Means Cluster Analysis'], className='card-title',
                            style=CARD_TEXT_STYLE),
                    html.P('Summarizes all features (values) in the dataset into individual graphs showing the relationships amongst the components (categories)', style=GENRE_TEXT_STYLE),

                ]
            )
        ], color='success', outline='True'
    )
)

##---------------------------- rows ----------------------------##

tabs_row = dbc.Row( ## row: lollipop charts
    [
        dbc.Col(

            html.Div([
                dcc.Tabs(id="tabs-misc", value='bar', children=[
                    dcc.Tab(label='Highest Budgets', value='bar'),
                    dcc.Tab(label='Budget and Revenue Across all Films', value='box'),
                    dcc.Tab(label='Genre Counts', value='pie'),
                ]),
                html.Div(id='tabs-misc-chart')
            ]),
        )

    ])

heatmap_row = dbc.Row([
    dbc.Col([
        dbc.Row(html.H3('Studying correlation'), style={'textAlign':'center'}),
        html.Br(),
        heatmap_card1,
]),
    dbc.Col(
        html.Div(html.Img(src=heatmap_image, style={'height':'39rem', 'width':'51rem'}), 
                 style={'textAlign':'center', 'width':'100%'})),

    dbc.Col([
        highlights_card,
        html.P('High correlation: budget/revenue, popularity/revenue', style=GENRE_TEXT_STYLE),
        html.P('Low correlation: budget/average rating, revenue/average rating', style=GENRE_TEXT_STYLE),
        hypotheses_card,
        html.P('A higher budget and greater popularity indicates that a film may have a higher revenue', style=GENRE_TEXT_STYLE),
        html.P('A higher average rating is not indicative of the budget or revenue of a film', style=GENRE_TEXT_STYLE),
])
                 
    ], style={'align-items':'center', 'display':'flex', 'height':'100%'})

pca_row = dbc.Row([
    dbc.Col([
        dbc.Row(html.H3('Studying clusters (2)'), style={'textAlign':'center'}),
        html.Br(),
        pca_card1,
    ]),
    dbc.Col(
        html.Div(html.Img(src=pca_image, style={'height':'35rem', 'width':'50rem'}),
                 style={'textAlign':'center', 'width':'100%'})),
    dbc.Col([
        highlights_card,
        html.P('No real discernable clusters between the first two components', style=GENRE_TEXT_STYLE),
        interpretation_card,
        html.P('Principal component analysis may not be the best way to visualize component clusters', style=GENRE_TEXT_STYLE),
        html.P('Other methods, like K-Means analysis, might produce more interesting results', style=GENRE_TEXT_STYLE),
    ])
], style={'align-items':'center', 'display':'flex', 'height':'100%'})

pca_steps_row = dbc.Row([
    dbc.Col([
        dbc.Row(html.H3('Studying clusters (1)'), style={'textAlign':'center'}),
        html.Br(),
        pca_steps_card1,
    ]),
    dbc.Col(
        html.Div(html.Img(src=pca_steps_image, style={'height':'31rem', 'width':'50rem'}),
                 style={'textAlign':'center', 'width':'100%'})),
    dbc.Col([
        highlights_card,
        html.P('90% of the data variance can be explained with three principal components', style=GENRE_TEXT_STYLE),
        interpretation_card,
        html.P('The overall dataset can be accurately divided into three main components (categories), dependent on a large variety of factors', style=GENRE_TEXT_STYLE),
        html.P('We should use three components for our later analyses', style=GENRE_TEXT_STYLE),
    ])
], style={'align-items':'center', 'display':'flex', 'height':'100%'})

kmeans_row = dbc.Row([
    dbc.Col([
        dbc.Row(html.H3('Studying clusters (3)'), style={'textAlign':'center'}),
        html.Br(),
        kmeans_card1,
    ]),
    dbc.Col(
        html.Div(html.Img(src=kmeans_image, style={'height':'38rem', 'width':'47rem'}),
                 style={'textAlign':'center', 'width':'100%'})),
    dbc.Col([
        highlights_card,
        html.P("While we can't see any major distinctions in clusters, comparing components 0 and 2 produce the clearest subgroups", style=GENRE_TEXT_STYLE),
        interpretation_card,
        html.P('The data can generally be split into three components (with component 3 being the most distinct)', style=GENRE_TEXT_STYLE),
    ])
], style={'align-items':'center', 'display':'flex', 'height':'100%'})

##---------------------------- layout ----------------------------##
    #    content_seventh_row,
    #     content_eighth_row,

layout = html.Div([
    ## misc findings
    misc_card,
    tabs_row,
    ## complex analytics
    analytics_card,
    html.Hr(),
    heatmap_row,
    html.Hr(),
    pca_steps_row,
    html.Hr(),
    pca_row,
    html.Hr(),
    kmeans_row,
])


##---------------------------- callbacks ----------------------------##
'''
pirates_image = './assets/pirates.jpeg'
avatar_image = './assets/avatar.jpg'
shawshank_image = './assets/shawshank.jpeg'
'''

@callback(Output('tabs-misc-chart', 'children'), 
              Input('tabs-misc', 'value', ))
def render_content(tab):
    if tab == 'bar':
        return dbc.Row([
                dbc.Col(dcc.Graph(id='f1', figure=fig_bar_budget)), 
                dbc.Col([bar_card, 
                        html.Div(html.Img(src=pirates_image, style={'height':'80%', 'width':'80%'}), 
                                 style={'textAlign':'center'}),
                                 ], style={'justify':'center'})
        ], style={'align-items':'center'})
    elif tab == 'box':
        return dbc.Row([
                dbc.Col(dcc.Graph(id='f2', figure=fig_box)),
                dbc.Col([box_card,
                        html.Div(html.Img(src=avatar_image, style={'height':'80%', 'width':'80%'}), 
                                style={'textAlign':'center'}),
                                ], style={'justify':'center'})
        ], style={'align-items':'center'})
    elif tab == 'pie':
        return dbc.Row([
                dbc.Col(dcc.Graph(id='f3', figure=fig_pie)),
                dbc.Col([pie_card,
                        html.Div(html.Img(src=shawshank_image, style={'height':'80%', 'width':'80%'}), 
                                style={'textAlign':'center'}),
                                ], style={'justify':'center'})
        ], style={'align-items':'center'})

