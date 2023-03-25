# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 08:42:27 2023

@author: collo
"""

import dash
from dash import dcc, html
import pandas as pd
import datetime as dt
import numpy as np
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# get the data
df = pd.read_csv("data.csv", sep=',')

# remove spaces in data
df[['now', 'close', 'daymin', 'daymax', 'yearmin', 'yearmax']] = df[
    ['now', 'close', 'daymin', 'daymax', 'yearmin', 'yearmax']].replace('\u202f', '', regex=True).astype(float)

# make timestamp readable
df['timestamp'] = df['timestamp'].apply(lambda x: dt.datetime.fromtimestamp(x))

print(df.head())
print(df.tail())

# calcul
now = df['now'].iloc[-1]

# vol = round(df.now.std(), 2)
min = df.now.min()
max = df.now.max()

daily_min = 0
daily_max = 0
daily_vol = 0

# plot
trace1 = go.Scatter(
    x=df['timestamp'],
    y=df['now'],
    name='Prix actuel'
)
trace2 = go.Scatter(
    x=df['timestamp'],
    y=df['close'],
    name='Clôture de la veille'
)

trace = go.Scatter(x=np.concatenate([df.timestamp, df.timestamp[::-1]]),
                   y=np.concatenate([df.daymin, df.daymax[::-1]]),
                   fill='tozerox', mode='none', fillcolor='rgba(20,0,50,0.1)',
                   showlegend=False, name='Valeur atteinte la veille')
data = [trace1, trace2, trace]
layout = go.Layout(xaxis=dict(title='Date'), yaxis=dict(title='Valeur'),
                   title=dict(text="Cours du CAC40", x=0.5, y=0.9, xanchor='center', yanchor='top'))
figure = go.Figure(data=data, layout=layout)

# initialisation dash
app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1(children="Dashboard CAC40", style={'textAlign': 'center'}),
                                html.Div(children=(
                                    html.Div(f"""Le CAC40 est un indice boursier qui reflète la performance des 40 
                                    plus grandes entreprises cotées en bourse en France. Il est considéré comme l'un 
                                    des indices les plus importants et les plus influents en Europe. Le CAC40 est 
                                    utilisé comme indicateur de l'évolution du marché boursier français et est 
                                    souvent considéré comme un baromètre de l'économie française dans son ensemble."""),
                                    html.Br(),
                                    html.Div("""Les entreprises incluses dans le CAC40 sont sélectionnées en fonction 
                                    de leur capitalisation boursière, de leur liquidité et de leur représentativité 
                                    sectorielle. Les secteurs les plus représentés sont la finance, l'énergie, 
                                    les matériaux de base, les produits de consommation courante et les services aux 
                                    collectivités. Le CAC40 est calculé en temps réel et est basé sur la 
                                    capitalisation boursière pondérée des 40 entreprises incluses dans l'indice."""))),
                                html.Br(),
                                html.H3(id="Now", children=f"Cours actuel : {now} €"),
                                dcc.Graph(id='Graph', figure=figure),
                                html.Div(style={'display': 'inline-block', 'width': '100%'}, children=[
                                    html.Div(id="Current", style={'float': 'left', 'width': '50%'}, children=[
                                        html.H2("Données historiques"),
                                        # html.Div(id='Vol', children=f'Volatilité historique : {vol} %'),
                                        html.Div(id='Max', children=f'Maximum historique : {max} €'),
                                        html.Div(id='Min', children=f'Minimum historique : {min} €')]),
                                    html.Div(id="Daily Report", style={'float': 'right', 'width': '50%'}, children=[
                                        html.H2('Rapport journalier'),
                                        html.Div(id='Daily Vol', children=f'Volatilité journalier : {daily_vol} %'),
                                        html.Div(id='Daily Max', children=f'Maximum journalier : {daily_max} €'),
                                        html.Div(id='Daily Min', children=f'Minimum journalier : {daily_min} €')])
                                ]),
                                dcc.Interval(
                                    id='interval-component',
                                    interval=1 * 1000,  # rafraîchit toutes les 5 minutes
                                    n_intervals=0
                                )
                                ])


# Update data
@app.callback([Output('Graph', 'figure'),
               Output(component_id='Now', component_property='children'),
               Output(component_id='Max', component_property='children'),
               Output(component_id='Min', component_property='children'),
               Output(component_id='Daily Vol', component_property='children'),
               Output(component_id='Daily Max', component_property='children'),
               Output(component_id='Daily Min', component_property='children')],
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    # get the data
    df = pd.read_csv("data.csv", sep=',')

    # remove spaces in data
    df[['now', 'close', 'daymin', 'daymax', 'yearmin', 'yearmax']] = df[ ['now', 'close', 'daymin', 'daymax', 'yearmin', 'yearmax']].replace('\u202f', '', regex=True).astype(float)

    # make timestamp readable
    df['timestamp'] = df['timestamp'].apply(lambda x: dt.datetime.fromtimestamp(x))

    now = df['now'].iloc[-1]
    # vol = round(df.now.std(), 2)
    min = df.now.min()
    max = df.now.max()

    # plot
    trace1 = go.Scatter(
        x=df['timestamp'],
        y=df['now'],
        name='Prix actuel'
    )
    trace2 = go.Scatter(
        x=df['timestamp'],
        y=df['close'],
        name='Clôture de la veille'
    )

    trace = go.Scatter(x=np.concatenate([df.timestamp, df.timestamp[::-1]]),
                       y=np.concatenate([df.daymin, df.daymax[::-1]]),
                       fill='tozerox', mode='none', fillcolor='rgba(20,0,50,0.1)',
                       showlegend=False, name='Valeur atteinte la veille')
    data = [trace1, trace2, trace]
    layout = go.Layout(xaxis=dict(title='Date'), yaxis=dict(title='Valeur'),
                       title=dict(text="Cours du CAC40", x=0.5, y=0.9, xanchor='center', yanchor='top'))
    figure = go.Figure(data=data, layout=layout)

    global daily_vol
    global daily_min
    global daily_max
    time = dt.datetime.now()
    if time.hour == 20 and 0 <= time.minute <= 10:
        daily_df = df[df["timestamp"].dt.date == time.date()]
        daily_vol = round(daily_df.now.std(), 2)
        daily_min = daily_df.now.min()
        daily_max = daily_df.now.max()

    return figure, f"Cours actuel : {now} €", f'Maximun historique : {max} €', \
           f'Minimum historique : {min} €', f'Volatilité journalière : {daily_vol} %', \
           f"Maximum journalier : {daily_max} €", f'Minimum journalier : {daily_min} €'


if __name__ == '__main__':
    app.run_server(debug=False)
