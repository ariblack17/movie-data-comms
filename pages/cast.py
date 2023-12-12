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
dash.register_page(__name__, path='/cast')


##----------------------------------- define elements -----------------------------------##

## mpl to plotly
# revenue chart
# fig_cast_rev = mpl_to_plotly(fig_cast_rev)
# x_r = [ x.get_text() for x in axU1.get_xticklabels() ]
# fig_cast_rev.update_layout(width=1100, height=750, title_x=0.8,
#                            xaxis=dict(tickmode='array', 
#                                 tickvals=[i for i in range(0, 5)],
#                                 ticktext=x_r))


# axU1.bar(x=cast_r, height=vals_r, color='#76A7B2')
# plt.xlabel("Lead actor", fontsize=14)
# plt.ylabel("Number of films", fontsize=14)
# plt.title('Actors who Appear Multiple Times Amongst the 50 Highest Revenue Films', fontsize=15)
# plt.yticks([0, 1, 2, 3])




## graph objects
fig_cast_rev = go.Figure()
# colors_cast_rev = util_colors[:(len(cast_r))]
colors_cast_rev = ['#E3E3FF', '#BCC0D6', '#76A7B2', '#89C3CF']
# colors_cast_rev = util_colors_past[:(len(cast_g))]
# colors_cast_rev = [util_colors_past[2],util_colors_past[5],util_colors_past[10],util_colors_past[1]]

labels_cast_rev = cast_r

fig_cast_rev.add_trace(go.Bar(
    x=vals_r,
    y=labels_cast_rev,
    orientation='h',
    marker_color=colors_cast_rev,
    opacity=0.7
))
fig_cast_rev.update_layout(width=850, height=600, 
                     margin=dict(l=10, r=20, t=50, b=20),
                     yaxis=dict(title='Number of films'),
                     xaxis=dict(title='Lead actor'),
                     title='Actors who Appear Multiple Times Amongst the 50 Highest Revenue Films',
                     title_x=0.5,
                     showlegend=False,
                     
                     )

'''
x
'''



# profit chart
# fig_cast_g = mpl_to_plotly(fig_cast_g)
# x_g = [ x.get_text() for x in axU2.get_xticklabels() ]
# fig_cast_g.update_layout(width=1100, height=750, title_x=0.8,
#                            xaxis=dict(tickmode='array', 
#                                 tickvals=[i for i in range(0, 9)],
#                                 ticktext=x_g))
# y_g = [ x.get_text() for x in axU2.get_yticklabels() ]




fig_cast_g = go.Figure()
# colors_cast_g = util_colors[:(len(cast_g))]
colors_cast_g = util_colors_past[:(len(cast_g))]
labels_cast_g = cast_g

fig_cast_g.add_trace(go.Bar(
    x=vals_g,
    y=labels_cast_g,
    orientation='h',
    marker_color=colors_cast_g,
    opacity=0.7
))
fig_cast_g.update_layout(width=850, height=600, 
                     margin=dict(l=10, r=20, t=50, b=20),
                     yaxis=dict(title='Number of films'),
                     xaxis=dict(title='Lead actor'),
                     title='Actors who Appear Multiple Times Amongst the 50 Highest Profiting Films',
                     title_x=0.5,
                     showlegend=False,
                     
                     )


##---------------------------- cards ----------------------------##

cast_card = dbc.Row(
    dbc.Card( ## genre trends card
        [
            dbc.CardBody(
                [
                    html.H4(id='cast_card_title', children=['How important is it to have a highly-accomplished cast?'], className='card-title',
                            style=CARD_TEXT_STYLE),
                    html.P(id='cast_card_text', children=['Metrics: revenue, profit'], style=CARD_TEXT_STYLE),
                ]
            )
        ]
    )
)

cast_card_r = dbc.Row(
    dbc.Card( ## genre trends card
        [
            dbc.CardBody(
                [
                    html.H4(id='cast_card_title', children=['Revenue'], className='card-title',
                            style=CARD_TEXT_STYLE),
                    html.P(id='cast_card_text', children=['Choice of lead cast has a sizable impact on profit; the impact may be lower than expected, as more influential cast members typically inflate costs'], style=CARD_TEXT_STYLE),
                ]
            )
        ]
    )
)

cast_card_g = dbc.Row(
    dbc.Card( ## genre trends card
        [
            dbc.CardBody(
                [
                    html.H4(id='cast_card_title', children=['Profit'], className='card-title',
                            style=CARD_TEXT_STYLE),
                    html.P(id='cast_card_text', children=['Choice of lead cast has a sizable impact; several popular actors appear in multiple high-profiting films'], style=CARD_TEXT_STYLE),
                ]
            )
        ]
    )
)

##---------------------------- rows ----------------------------##

row1 = dbc.Row([
    dbc.Col([
        html.Div([
            dcc.Graph(figure=fig_cast_rev)
        ])
    ], style={'justify':'center'}),
    dbc.Col([
        cast_card_r
    ], style={'justify':'center'})
], style={'align-items':'center'})

row2 = dbc.Row([
    dbc.Col([
        html.Div([
            dcc.Graph(figure=fig_cast_g)
        ]),
    ], style={'justify':'center'}),
    dbc.Col([
        cast_card_g
    ], style={'justify':'center'})
], style={'align-items':'center'})

##---------------------------- layout ----------------------------##
    #    content_seventh_row,
    #     content_eighth_row,

layout = html.Div([
    cast_card,
    html.Hr(),
    row1,
    html.Hr(),
    row2

])


##---------------------------- callbacks ----------------------------##


