#
# 
# TOP FILMS PAGE
# 
# 


##----------------------------------- imports -----------------------------------##

import dash
import dash_bootstrap_components as dbc
from dash import dcc, callback
from dash import html
from dash.dependencies import Input, Output
from plotly.tools import mpl_to_plotly
import plotly.graph_objects as go
from dash import dash_table
from PIL import Image
from pages._matplotlib_figs import *
from pages._styles import *


##----------------------------------- register page -----------------------------------##

dash.register_page(__name__, path='/top_films')


##----------------------------------- define elements -----------------------------------##

## graph 11, lollipop popularity
    #region
graph11 = mpl_to_plotly(fig11) ## directly convert
y11 = [ x.get_text() for x in ax11.get_yticklabels() ]
graph11.update_layout(width=1100, height=750, title_x=0.7,
                     margin=dict(l=10, r=20, t=50, b=20),
                     yaxis=dict(tickmode='array', 
                                tickvals=[i for i in range(0, 50)],
                                ticktext=y11),
                     
                     )
graph11.update_yaxes(type='category')
# graph11.show();

    #endregion

## graph 12, lollipop rating
    #region

graph12 = mpl_to_plotly(fig12) ## directly convert
y12 = [ x.get_text() for x in ax12.get_yticklabels() ]
graph12.update_layout(width=1100, height=750, title_x=0.7,
                     margin=dict(l=10, r=20, t=50, b=20),
                     yaxis=dict(tickmode='array', 
                                tickvals=[i for i in range(0, 50)],
                                ticktext=y12),
                     
                     )
# graph12.show();

    #endregion

## graph 13a, lollipop top (pop)
    #region

## recreate color code
for i in range(len(colors_pop50)): 
    if colors_pop50[i] == 'k':
        # colors_pop50[i] = 'rgb(100,100,100)'
        colors_pop50[i] = '#E3E3FF'
    else:
        colors_pop50[i] = '#76A7B2'
        
## create figure
graph13a = go.Figure(graph11)
# graph13a = graph12.copy()

## add traces
graph13a.add_trace(go.Scatter(
        x=graph11.data[0]['x'],
        y=graph11.data[0]['y'],
        mode='markers',
        marker=dict(color=colors_pop50), 
        # labels={x:'pop', y:'title'},
    ))


    #endregion

## graph 13b, lollipop top (rating)
    #region

## recreate color code
for i in range(len(colors_vote50)):
    if colors_vote50[i] == 'k':
        colors_vote50[i] = '#E3E3FF'
    else:
        colors_vote50[i] = '#76A7B2'

        
## create figure
graph13b = go.Figure(graph12)

## add traces
graph13b.add_trace(go.Scatter(
        x=graph12.data[0]['x'],
        y=graph12.data[0]['y'],
        mode='markers',
        marker=dict(color=colors_vote50), 
    ))

    #endregion

## table 13, table top
    #region

# df_popvote50
table13 = dash_table.DataTable(data=df_popvote50.to_dict('records'), 
                               columns = [{"name": i, 'id': i} for i in df_popvote50.columns if i!='id'],
                               # columns=[{'id': c, 'name': c} for c in df.columns if c!="Pressure"]
                                style_data={
                                    'whiteSpace': 'normal',
                                    'height': 'auto',
                                  },
                                fill_width=False,
                               style_cell={
                                   'fontSize':13, 
                                   'font-family':'sans-serif', 
                                   'text-align': 'left',},
                               
                                style_header={
                                    'text-align': 'center',
                                },
                              )

    #endregion

## graph 14a, bar top budget
    #region

graph14a = mpl_to_plotly(fig14a) ## directly convert
y14a = [ x.get_text() for x in ax14a.get_yticklabels() ]
graph14a.update_layout(width=650, height=600, title_x=0.9,
                     margin=dict(l=10, r=20, t=50, b=20),
                     yaxis=dict(tickmode='array', 
                                tickvals=[i for i in range(0, 13)],
                                ticktext=y14a,
                                # tickwidth=10
                                # ticklen=10
                               ),
                                
                     )
graph14a.update_yaxes(type='category')

    #endregion


## graph 14b, bar top rev
    #region

graph14b = mpl_to_plotly(fig14b) ## directly convert
y14b = [ x.get_text() for x in ax14b.get_yticklabels() ]
graph14b.update_layout(width=650, height=600, title_x=0.9,
                     margin=dict(l=10, r=20, t=50, b=20),
                     yaxis=dict(tickmode='array', 
                                tickvals=[i for i in range(0, 13)],
                                ticktext=y14b),
                     )
graph14b.update_yaxes(type='category')

    #endregion

## graph 14c, violin other budget
    #region

graph14c = go.Figure()
graph14c.add_trace(go.Violin(
    x=df_nottop50["budget"][(np.abs(stats.zscore(df_nottop50['budget'])) < 3)].div(1000000),
    line_color='#76A7B2'
))
graph14c.add_vline(x=med_12b, line_width=1,  annotation_text=' top films median', line_dash="dash")

graph14c.update_layout(width=600, height=600, 
                     margin=dict(l=10, r=20, t=50, b=20),
                     xaxis=dict(title='Budget (millions)'),
                     yaxis=dict(title=' '),
                     title='Budget for Films not in Top 50 Most Popular or Highest Rated',
                     title_x=0.9,
                     
                     )
graph14c.update_traces(name="")

    #endregion

## graph 14d, violin other rev
    #region

graph14d = go.Figure()
graph14d.add_trace(go.Violin(
    x=df_nottop50["revenue"][(np.abs(stats.zscore(df_nottop50['revenue'])) < 3)].div(1000000),
    line_color='#BCC0D6'
))
graph14d.add_vline(x=med_12r, line_width=1,  annotation_text=' top films median', line_dash="dash")


# graph14d.add_trace(go.Scatter(x=[avg_12r], y=[0, 10], mode='lines', name='avg'))
# ax14d.axvline(x=avg_12r, color='#00224B', linestyle='--')
graph14d.update_layout(width=600, height=600, 
                     margin=dict(l=10, r=20, t=50, b=20),
                     xaxis=dict(title='Revenue (millions)'),
                     yaxis=dict(title=' '),
                     title='Revenue for Films not in Top 50 Most Popular or Highest Rated',
                     title_x=0.9,
                     
                     )
graph14d.update_traces(name="")

    #endregion

## graph 14e, donut top production
    #region

graph14e = go.Figure()
graph14e.add_trace(go.Pie(
    values=arr_production_counts,
    labels=arr_production_tmp, 
    # colors=colors,
    hole=.75
))
graph14e.update_layout(title='Production Companies with Multiple Films Amongst<br>the Highest Rated and Most Popular',
                      title_x=0.9,
                        font_size=10,
                      )
graph14e.update_traces(marker=dict(colors=['#CDE4CF', '#89C3CF', '#BCC0D6', '#FDC899']))

    #endregion



##---------------------------- logo images ----------------------------##
    #region

wb_image = Image.open("./assets/warnerbros.png")
syn_image = Image.open("./assets/syncopy.png")
par_image = Image.open("./assets/paramount.png")
leg_image = Image.open("./assets/legendary.png")

    #endregion

##---------------------------- other images ----------------------------##

dancer_image = './assets/dancer.jpeg'
inter_image = './assets/interstellar.jpeg'


##---------------------------- cards ----------------------------##

content_card_1 = dbc.Row([ ## top films card

        dbc.Card( ## card 1
            [
                dbc.CardBody(
                    [
                        html.H4(id='card_1_title', children=['What are the top films in the database?'], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html.P(id='card_1_text', children=['Metrics: popularity and average TMDb rating'], style=CARD_TEXT_STYLE),
                        # html.P(id='card_1_text', children=['Metrics: popularity and average TMDb rating']),

                    ]
                )
            ]
        ),

])

content_card_2 = dbc.Row([ ## top films trends card

        dbc.Card( ## card 1
            [
                dbc.CardBody(
                    [
                        html.H4(id='card_2_title', children=['Which of the top films are both popular and highly rated?'], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html.P(id='card_2_text', children=['Metrics: popularity and average TMDb rating'], style=CARD_TEXT_STYLE),
                    ]
                )
            ]
        ),

])

content_card_3 = dbc.Row([ ## top films trends card

        dbc.Card( ## card 1
            [
                dbc.CardBody(
                    [
                        html.H4(id='card_3_title', children=['What similarities exist among the most popular and highest rated films?'], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html.P(id='card_3_text', children=['Metrics: popularity and average TMDb rating'], style=CARD_TEXT_STYLE),
                    ]
                )
            ]
        ),

], style={'margin-top': '20px'})

prod_companies_card = dbc.Card( ## top production companies card
        [
            dbc.CardBody(
                [
                    html.H4(id='prod_companies_card_title', children=[''], className='card-title',
                            style=CARD_TEXT_STYLE),
                    html.P(id='prod_companies_card_text', children=['Most of the top films were produced by four major production companies.'], style=CARD_TEXT_STYLE),
                ]
            )
        ]
    )

inter_card = dbc.Card([ ## interstellar card
    dbc.CardBody(
        [
            html.H4(id='inter_card_title', children=['Interstellar'], className='card-title',
                    style=CARD_TEXT_STYLE),
            # html.P(id='prod_companies_card_text', children=['Most of the top films were produced by four major production companies.'], style=CARD_TEXT_STYLE),
        ]
    )]
)

dancer_card = dbc.Card( ## dancer, texas pop. 81 card
    dbc.CardBody(
        [
            html.H4(id='dancer_card_title', children=['Dancer, Texas Pop. 81'], className='card-title',
                    style=CARD_TEXT_STYLE),
            # html.P(id='prod_companies_card_text', children=['Most of the top films were produced by four major production companies.'], style=CARD_TEXT_STYLE),
        ]
    )
)

##---------------------------- rows ----------------------------##

content_second_row = dbc.Row( ## row: lollipop charts
    [
        dbc.Col(
            # dcc.Graph(id='graph_1'), md=4
            # dcc.Graph(figure=graph11), width=6
        ),
        
        
        html.Div([
            dcc.Tabs(id="tabs-graph", value='popularity-12', children=[
                dcc.Tab(label='Popularity', value='popularity-12'),
                dcc.Tab(label='Rating', value='rating-12'),
            ]),
            html.Div(id='tabs-content-example-graph')
        ]),

    ])

content_second_row2 = dbc.Row( ## row: lollipop charts top
    [        
        
        dbc.Col(
        
            html.Div([
                dcc.Tabs(id="tabs-graph2", value='popularity-13a', children=[
                    dcc.Tab(label='Popularity', value='popularity-13a'),
                    dcc.Tab(label='Rating', value='rating-13b'),
                ]),
                html.Div(id='tabs-content-example-graph2')
            ]),
        ),


    ]
)

content_third_row = dbc.Row( ## row: empty 
    [
        dbc.Col(
            # genre_button
            # dcc.Graph(id='graph_4'), md=12,
            # dcc.Graph(figure=graph13a), width=6,
        ),
    ])

content_third_row2 = dbc.Row( ## row: empty
    [
        dbc.Col(
            # dcc.Graph(figure=graph13b), width=6,
        ),
    ])

content_fourth_row = dbc.Row( ## row: revenue charts
    [
        dbc.Col(
            # dcc.Graph(id='graph_5'), md=6
            # dcc.Graph(figure=graph14b), width=5.5
            dcc.Graph(figure=graph14b), md=6
        ),
        dbc.Col(
            # dcc.Graph(figure=graph14a), width=6,
            # dcc.Graph(figure=graph14d), width=4.5,
            dcc.Graph(figure=graph14d), md=3,
        )
    ], style={'margin-top': '20px'})

content_fifth_row = dbc.Row( ## row: budget charts
    [
        dbc.Col(
            # dcc.Graph(id='graph_5'), md=6
            # table13, width=6
            dcc.Graph(figure=graph14a), md=6,
        ),
        dbc.Col(
            # dcc.Graph(id='graph_6'), md=6
             dcc.Graph(figure=graph14c), md=3,
        )
    ], style={'margin-top': '20px'})

content_sixth_row = dbc.Row( ## row: donut chart
    [ 
        dbc.Col( [
            prod_companies_card,
            dbc.Row( 
                [
                    dbc.Col(html.Img(src=wb_image, style={'height':'16vh', 'width':'18vh'}),
                            style={'justify': 'center', 'margin-left':'10vh', 'margin-top':'1vh'}),
                    dbc.Col(html.Img(src=par_image, style={'height':'15vh', 'width':'28vh'}),
                            style={'justify': 'center', 'margin-left':'0vh'}),
                ], style={'margin-top': '20px', 'justify' : 'center'}),
            dbc.Row( 
                [
                    dbc.Col(html.Img(src=leg_image, style={'height':'16vh', 'width':'25vh'}),
                            style={'justify': 'center', 'margin-left':'7vh', 'margin-top':'5vh'}),
                    dbc.Col(html.Img(src=syn_image, style={'height':'7vh', 'width':'32vh'}),
                            style={'justify': 'center', 'margin-top':'9vh'}),
                ], style={'justify': 'center'})
        ] ),
        dbc.Col(
            dcc.Graph(figure=graph14e), md=6
        ),
    ], style={'margin-top': '20px', 'justify' : 'center'})
    


##---------------------------- layout ----------------------------##
    #    content_seventh_row,
    #     content_eighth_row,

layout = html.Div([
        # content_third_row,
        content_card_1,
        content_second_row,
        content_card_2,
        content_second_row2,
        content_card_3,
# content_third_row,
        # content_third_row2,
        content_fourth_row,
        content_fifth_row,
        content_sixth_row,

])


##---------------------------- callbacks ----------------------------##

@callback(Output('tabs-content-example-graph', 'children'), ## lollipop charts
              Input('tabs-graph', 'value'))
def render_content(tab):
    if tab == 'popularity-12':
        return dbc.Row([
                dbc.Col(dcc.Graph(figure=graph11)), 
                dbc.Col([html.Div(html.Img(src=inter_image, style={'height':'80%', 'width':'80%'}), 
                                 style={'textAlign':'center'}),
                                 inter_card,
                                 ], style={'justify':'center'})
        ], style={'align-items':'center'})
            
    elif tab == 'rating-12':
        return dbc.Row([
                dbc.Col(dcc.Graph(id='graph-2-tabs-dcc',figure=graph12)),
                dbc.Col([html.Div(html.Img(src=dancer_image, style={'height':'80%', 'width':'80%'}), 
                                    style={'textAlign':'center'}),
                                    dancer_card,
                                    ], style={'justify':'center'})
        ], style={'align-items':'center'})

@callback(Output('tabs-content-example-graph2', 'children'), ## lollipop charts top films
              Input('tabs-graph2', 'value'))
def render_content(tab):
    if tab == 'popularity-13a':
        return dbc.Row([
            dbc.Col([
                dcc.Graph(figure=graph13a),
            ]),
            dbc.Col([
                table13
            ]),
        ],
            align="center",
            justify="center",
            # style={"height": "100vh"},
        )
    elif tab == 'rating-13b':
        return dbc.Row([
            dbc.Col([
                dcc.Graph(figure=graph13b),
            ]),
            dbc.Col([
                table13
            ]),
            
        ],
            align="center",
            justify="center",
            # style={"height": "100vh"},
        )
