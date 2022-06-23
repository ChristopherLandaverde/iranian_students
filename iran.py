import dash
from dash import html,dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd


df=pd.read_csv('iranian_students.csv')

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


## filtered dataframes
fig = px.bar(df,x=df['Years'],y=df['Girls Middle School'],barmode="group")
girls = df[['Girls Kindergarten','Girls Grade School','Girls Middle School','Girls High School']]
boys = df[['Boys Kindergarten','Boys Grade School','Boys Middle School','Boys High School']]

### Static Bar Charts
boys_lines = px.bar(df,x=df['Years'],y=list(girls),barmode="group")
girls_lines = px.bar(df,x=df['Years'],y=list(boys),barmode="group")




app.layout = dbc.Container([
    dbc.Container([
          html.H1('Iranian Students from 1968 to 2017',className='display-3 mb-4'),
          dcc.Markdown('''
                       data source: https://www.kaggle.com/chubak/iranian-students-from-1968-to-2017

''')
    ]),
        dbc.Card([
        dcc.Dropdown(options=df.columns[1:9].unique(),
                            value='Boys Grade School',
                            multi=False,
                            id='geo-dropdown'),]),
            dbc.Row([
                    dcc.Graph(id='price-graph'),
                    dbc.Col(html.Div([html.H2('Boys'),
                                      dcc.RadioItems(options=list(boys),value='Boys Kindergarten',
                                     id='boys-dropdown',labelStyle={'display':'block'})])),
                      dbc.Col(
                          html.Div([html.H2('Girls'), (dcc.RadioItems(options=list(girls),
                            value='Girls Kindergarten',
                            id='girls-dropdown',
                            labelStyle={'display':'block'}))
                      ]))
            ]),
               dbc.Row([
                    dcc.Graph(id='duelchats',figure=fig),
               ]),
                dbc.Row(
            [
                html.H2(children='Boys vs Girls'),
                dbc.Col(html.Div(dcc.Graph(id='barcharts',figure=boys_lines),)),
                dbc.Col(html.Div( dcc.Graph(id='girlcharts',figure=girls_lines)))
            ]
        )

])


@app.callback(
    Output(component_id='price-graph', component_property='figure'),
    Input(component_id='geo-dropdown', component_property='value')
)
def update_firstgraph(selected_iran):
    ''' Filters out the graph based on the selected demographics'''
    filtered_df = df[selected_iran]
    line_fig = px.bar(df,
                       x=df['Years'],
                       y=filtered_df
                       )
    return line_fig


@app.callback(
    Output(component_id='duelchats', component_property='figure'),
    [Input(component_id='girls-dropdown', component_property='value'),
    Input(component_id='boys-dropdown', component_property='value')]
)
def update_histogram(xaxis,yaxis):
    """ Updates the histogram with boys and girls demographics"""
    duel_fig = px.histogram(df,
                       x=df['Years'],
                       y=[xaxis,yaxis]

                       )
    return duel_fig



if __name__ == '__main__':
    app.run_server(debug=True)
