from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import statsmodels.formula.api as smf
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('data_normalized.csv')

scatter_plot = px.scatter(df, x="x dimension", y="y dimension", size="price", color="color", hover_name="carat", log_x=True, size_max=120)

line_plot = px.line(df.groupby(['carat'])['price'].mean().reset_index(), x='carat', y='price')

pie_chart = px.pie(df, names='clarity', title='Population of European continent')

regression_data = pd.read_csv('regression_data.csv')

model = smf.ols(formula="price ~ I(xdimension**2)", data=regression_data).fit()

regression_data["fitted"] = model.fittedvalues

regression_fig = go.Figure()
regression_fig.add_trace(go.Scatter(
    x=regression_data["xdimension"], y=regression_data["price"], name="X Dimension vs Price", mode="markers"))
regression_fig.add_trace(go.Scatter(
    x=regression_data["xdimension"], y=regression_data["fitted"], name="Regression model", mode="lines"))
regression_fig.update_layout(title="Regression line X Dimension vs Price", xaxis_title="X dimension",
    yaxis_title="Price")

app.layout = html.Div([
    html.H2('Scatter plot'),

    html.Div([
        html.Div([
            html.P('X axis'),
            dcc.Dropdown(
                ['carat', 'x dimension', 'y dimension', 'z dimension', 'depth', 'table', 'price'],
                'x dimension',
                id='xaxis-column',
            )
        ],
        style={'width': '33%', 'display': 'inline-block'}),
        html.Div([
            html.P('Y axis'),
            dcc.Dropdown(
                ['carat', 'x dimension', 'y dimension', 'z dimension', 'depth', 'table', 'price'],
                'y dimension',
                id='yaxis-column',
            )
        ],
        style={'width': '33%', 'display': 'inline-block'}),
        html.Div([
            html.P('Z axis'),
            dcc.Dropdown(
                ['carat', 'x dimension', 'y dimension', 'z dimension', 'depth', 'table', 'price'],
                'z dimension',
                id='zaxis-column',
            )
        ], style={'width': '33%', 'display': 'inline-block'}),
    ], style={
        'padding': '10px 5px',
        'display': 'flex',
        'justify-content': 'space-evenly'
    }),

    html.Div([
        html.Div([
            html.P('Category'),
            dcc.Dropdown(
                ['clarity', 'color', 'cut'],
                'cut',
                id='category-column',
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.P('Size'),
            dcc.Slider(
            20,
            120,
            step=None,
            id='size-slider'
        )
        ],
        style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    ], style={
        'padding': '10px 5px'
    }),

    html.Hr(),

    html.Div(
    dcc.Graph(
        id='scatter-plot',
        figure=scatter_plot
    )),

    html.Hr(), 

    html.Div([
        html.H2('Variable/Price plot'),
        html.Div([
            html.P('X axis'),
            dcc.Dropdown(
                ['carat', 'x dimension', 'y dimension', 'z dimension', 'depth', 'table'],
                'x dimension',
                id='xaxis-column-line-plot',
            )
        ], style={'width': '90%'}),
        dcc.Graph(
            id='line-plot',
            figure=line_plot
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),

    html.Div([
        html.H2('Samples by categories count'),
        html.Div([
            html.P('Category'),
            dcc.Dropdown(
                ['clarity', 'color', 'cut'],
                'cut',
                id='category-column-pie-chart',
            )
        ], style={'width': '90%'}),
        dcc.Graph(
            id='pie-chart',
            figure=pie_chart
        )
    ], style={'width': '49%', 'display': 'inline-block'}),

    html.Hr(),

    html.H2('Regression plot'),

    html.Div(
    dcc.Graph(
        id='regression-plot',
        figure=regression_fig
    ))
])

@app.callback(
    Output('scatter-plot', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('zaxis-column', 'value'),
    Input('category-column', 'value'),
    Input('size-slider', 'value'))
def update_scatter_plot(xaxis_column, yaxis_column,
                        zaxis_column, category_column,
                        size):
    fig = px.scatter(df, x=xaxis_column, y=yaxis_column, size=zaxis_column, color=category_column, hover_name=category_column, log_x=True, size_max=size)
    return fig

@app.callback(
        Output('line-plot', 'figure'),
        Input('xaxis-column-line-plot', 'value')
)
def update_line_plot(xaxis_column):
    fig = px.line(df.groupby([xaxis_column])['price'].mean().reset_index(), x=xaxis_column, y='price')
    return fig

@app.callback(
        Output('pie-chart', 'figure'),
        Input('category-column-pie-chart', 'value')
)
def update_pie_chart(category_column):
    fig = px.pie(df, names=category_column)
    return fig

if __name__  == '__main__':
    app.run_server(debug=True)

