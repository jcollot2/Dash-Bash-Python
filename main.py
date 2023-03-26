# -*- coding: utf-8 -*-
""" IMPORTATION LIBRAIRIES """

import dash
from dash import dcc, html
import pandas as pd
import datetime as dt
import numpy as np
import plotly.graph_objs as go
from dash.dependencies import Input, Output

""" INITIALISATION DU DATAFRAME """

# get the data
df = pd.read_csv("data.csv", sep=',')

# remove spaces in data
df[['now', 'close', 'daymin', 'daymax', 'yearmin', 'yearmax']] = df[
    ['now', 'close', 'daymin', 'daymax', 'yearmin', 'yearmax']].replace('\u202f', '', regex=True).astype(float)

# make timestamp readable
df['timestamp'] = df['timestamp'].apply(lambda x: dt.datetime.fromtimestamp(x))

""" CALCUL DES DONNEES """

now = df['now'].iloc[-1]

# vol = round(df.now.std(), 2)
min = df.yearmin.min()
max = df.yearmax.max()

daily_min = 0
daily_max = 0
daily_var = 0
daily_vol = 0
daily_open = 0
daily_close = 0

""" CREATION GRAPHIQUES """

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

""" INITIALISATION DU DASHBOARD """

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
                                html.H2(id="Now", children=f"Cours actuel : {now} €"),
                                dcc.Graph(id='Graph', figure=figure),
                                html.Div(style={'display': 'inline-block', 'width': '100%'}, children=[
                                    html.Div(id="Current", style={'float': 'left', 'width': '50%'}, children=[
                                        html.H2("Données historiques"),
                                        # html.Div(id='Vol', children=f'Volatilité historique : {vol} %'),
                                        html.Div(id='Max', children=f'Maximum historique : {max} €'),
                                        html.Div(id='Min', children=f'Minimum historique : {min} €')]),
                                    html.Div(id="Daily Report", style={'float': 'right', 'width': '50%'}, children=[
                                        html.H2('Rapport journalier'),
                                        html.Div(id='Daily Open', children=f"Prix à l'ouverture : {daily_open} €"),
                                        html.Div(id='Daily Close', children=f"Prix à la clôture : {daily_close} €"),
                                        html.Div(id='Daily Var', children=f'Variation journalier : {daily_var} %'),
                                        html.Div(id='Daily Vol', children=f'Volatilité journalier : {daily_vol} %'),
                                        html.Div(id='Daily Max', children=f'Maximum journalier : {daily_max} €'),
                                        html.Div(id='Daily Min', children=f'Minimum journalier : {daily_min} €')])
                                ]),
                                dcc.Interval(
                                    id='interval-component',
                                    interval=5 * 60 * 1000,  # rafraîchit toutes les 5 minutes
                                    n_intervals=0
                                )
                                ])

""" MISE A JOUR DES DONNEES """


@app.callback([Output('Graph', 'figure'),
               Output(component_id='Now', component_property='children'),
               Output(component_id='Max', component_property='children'),
               Output(component_id='Min', component_property='children'),
               Output(component_id='Daily Open', component_property='children'),
               Output(component_id='Daily Close', component_property='children'),
               Output(component_id='Daily Var', component_property='children'),
               Output(component_id='Daily Vol', component_property='children'),
               Output(component_id='Daily Max', component_property='children'),
               Output(component_id='Daily Min', component_property='children'), ],
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    # get the data
    updated_df = pd.read_csv("data.csv", sep=',')

    # remove spaces in data
    updated_df[['now', 'close', 'daymin', 'daymax', 'yearmin', 'yearmax']] = updated_df[['now', 'close', 'daymin', 'daymax', 'yearmin', 'yearmax']].replace('\u202f', '', regex=True).astype(float)

    # make timestamp readable
    updated_df['timestamp'] = updated_df['timestamp'].apply(lambda x: dt.datetime.fromtimestamp(x))

    now = updated_df['now'].iloc[-1]
    # vol = round(updated_df.now.std(), 2)
    min = updated_df.yearmin.min()
    max = updated_df.yearmax.max()

    # plot
    trace1 = go.Scatter(
        x=updated_df['timestamp'],
        y=updated_df['now'],
        name='Prix actuel'
    )
    trace2 = go.Scatter(
        x=updated_df['timestamp'],
        y=updated_df['close'],
        name='Clôture de la veille'
    )

    trace = go.Scatter(x=np.concatenate([updated_df.timestamp, updated_df.timestamp[::-1]]),
                       y=np.concatenate([updated_df.daymin, updated_df.daymax[::-1]]),
                       fill='tozerox', mode='none', fillcolor='rgba(20,0,50,0.1)',
                       showlegend=False, name='Valeur atteinte la veille')
    data = [trace1, trace2, trace]
    layout = go.Layout(xaxis=dict(title='Date'), yaxis=dict(title='Valeur'),
                       title=dict(text="Cours du CAC40", x=0.5, y=0.9, xanchor='center', yanchor='top'))
    figure = go.Figure(data=data, layout=layout)

    global daily_vol
    global daily_min
    global daily_max
    global daily_open
    global daily_close
    global daily_var

    time = dt.datetime.now()
    if time.hour == 20 and 0 <= time.minute <= 10:
        # création d'un sous dataframe contenant seulement les données du jour
        daily_df = updated_df[updated_df["timestamp"].dt.date == time.date()]
        daily_vol = round(daily_df.now.std(), 2)
        daily_min = daily_df.now.min()
        daily_max = daily_df.now.max()
        daily_open = daily_df.nsmallest(1, 'timestamp').iloc[0]["now"]
        daily_close = daily_df.nlargest(1, 'timestamp').iloc[0]["now"]
        daily_var = round((daily_close - daily_open) / daily_open * 100, 2)

    return [
        figure,
        f"Cours actuel : {now} €",
        f'Maximun historique : {max} €',
        f'Minimum historique : {min} €',
        f"Prix à l'ouverture : {daily_open} €",
        f"Prix à la clôture : {daily_close} €",
        f'Variation journalière : {daily_var} %',
        f'Volatilité journalière : {daily_vol} %',
        f"Maximum journalier : {daily_max} €",
        f'Minimum journalier : {daily_min} €']


""" LANCEMENT DU SERVEUR WEB """

if __name__ == '__main__':
    app.run_server(debug=False, )
