from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
from plot_utils import load_pokemon_data, create_pokebola_spinner, create_pokebola_sidebar


# Load Pokémon data
df = load_pokemon_data()

# App Layout
def create_layout(app):
    return dbc.Container([
        html.Div(id='p5-container', style={'position': 'fixed', 'top': 0, 'left': 0, 'width': '100%', 'height': '100%', 'zIndex': -1}),
        dcc.Location(id='url', refresh=False),
        dbc.Row([
            dbc.Col([
                dbc.Nav([
                    create_pokebola_sidebar(),
                    dbc.NavLink(
                        [
                            html.I(className="fas fa-spider me-2"),
                            html.Span("Radar Chart")
                        ],
                        href="/",
                        id="link-radar-chart",
                        active="exact"
                    ),
                    dbc.NavLink(
                        [
                            html.I(className="fas fa-chart-bar me-2"),
                            html.Span("Stats Bar Chart")
                        ],
                        href="/bar-chart",
                        id="link-bar-chart",
                        active="exact"
                    ),
                    dbc.NavLink(
                        [
                            html.I(className="fas fa-chart-line me-2"),
                            html.Span("Scatter Plot")
                        ],
                        href="/scatter-plot",
                        id="link-scatter-plot",
                        active="exact"
                    ),
                    dbc.NavLink(
                        [
                            html.I(className="fas fa-th me-2"),
                            html.Span("Heatmap")
                        ],
                        href="/heatmap",
                        id="link-heatmap",
                        active="exact"
                    ),
                    dbc.NavLink(
                        [
                            html.I(className="fas fa-box me-2"),
                            html.Span("Box Plot")
                        ],
                        href="/box-plot",
                        id="link-box-plot",
                        active="exact"
                    )
                ],
                vertical=True,
                pills=True,
                className="sidebar")
            ], width=2),
            dbc.Col([
                html.H1('Pokémon Dashboard', className='text-center shine-effect', **{'data-text': 'Pokémon Dashboard'}),
                html.Div(id='page-content', className="content")
            ], width=10)
        ], className='row-centered', style={'marginTop': '20px'}),
        dbc.Row([
            dbc.Col([
                html.Div("by Alonso Valdés",
                         style={'fontSize': '10px', 'color': 'white', 'marginBottom': '20px'})
            ])
        ])
    ], fluid=True)


def render_radar_chart_layout():
    random_pokemons = df.sample(n=2)['#'].tolist()
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    html.Div("Select First Pokémon", className="card-header"),
                    dbc.CardBody([
                        dcc.Dropdown(
                            id='pokemon-dropdown-1',
                            options=[{'label': row['Name'], 'value': row['#']} for _, row in df.iterrows()],
                            value=random_pokemons[0],
                            clearable=False,
                            style={'marginBottom': '20px'}
                        ),
                        html.Img(id='pokemon-image-1', className='pokemon-image'),
                        html.Div(id='pokemon-info-1', className='pokemon-info', style={})  # Ensure style is an empty dict by default
                    ])
                ], className='pokemon-details')
            ], width=3, style={'padding-left': '15px', 'padding-right': '15px'}),
            dbc.Col([
                dbc.Card([
                    html.Div("Pokémon Radar Chart Comparison", className="card-header"),
                    dbc.CardBody([
                        dcc.Loading(
                            children=[
                                html.Div(dcc.Graph(id='radar-graph-comparison', className='graph-container'))
                            ],
                            custom_spinner=create_pokebola_spinner(),
                            fullscreen=True,
                        )
                    ])
                ], className='graph-card', style={'height': '100%'})
            ], width=6, style={'padding-left': '15px', 'padding-right': '15px'}),
            dbc.Col([
                dbc.Card([
                    html.Div("Select Second Pokémon", className="card-header"),
                    dbc.CardBody([
                        dcc.Dropdown(
                            id='pokemon-dropdown-2',
                            options=[{'label': row['Name'], 'value': row['#']} for _, row in df.iterrows()],
                            value=random_pokemons[1],
                            clearable=False,
                            style={'marginBottom': '20px'}
                        ),
                        html.Img(id='pokemon-image-2', className='pokemon-image'),
                        html.Div(id='pokemon-info-2', className='pokemon-info', style={})
                    ])
                ], className='pokemon-details')
            ], width=3, style={'padding-left': '15px', 'padding-right': '15px'})
        ], className='row-centered', style={'marginTop': '10px', 'height': '600px'})
    ], fluid=True)


def render_scatter_plot_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div("Select X Axis", className="card-header"),
                dcc.Dropdown(
                    id='scatter-xaxis',
                    options=[
                        {'label': 'HP', 'value': 'HP'},
                        {'label': 'Attack', 'value': 'Attack'},
                        {'label': 'Defense', 'value': 'Defense'},
                        {'label': 'Sp. Atk', 'value': 'Sp. Atk'},
                        {'label': 'Sp. Def', 'value': 'Sp. Def'},
                        {'label': 'Speed', 'value': 'Speed'}
                    ],
                    value='HP',
                    clearable=False,
                    style={'marginBottom': '20px'}
                )
            ], width=6),
            dbc.Col([
                html.Div("Select Y Axis", className="card-header"),
                dcc.Dropdown(
                    id='scatter-yaxis',
                    options=[
                        {'label': 'HP', 'value': 'HP'},
                        {'label': 'Attack', 'value': 'Attack'},
                        {'label': 'Defense', 'value': 'Defense'},
                        {'label': 'Sp. Atk', 'value': 'Sp. Atk'},
                        {'label': 'Sp. Def', 'value': 'Sp. Def'},
                        {'label': 'Speed', 'value': 'Speed'}
                    ],
                    value='Attack',
                    clearable=False,
                    style={'marginBottom': '20px'}
                )
            ], width=6)
        ]),
        dbc.Row([
            dbc.Col([
                html.Div("Select Pokémon to Highlight", className="card-header"),
                dcc.Dropdown(
                    id='pokemon-dropdown',
                    options=[{'label': row['Name'], 'value': row['#']} for _, row in df.iterrows()],
                    value=[],
                    multi=True,
                    style={'marginBottom': '20px'}
                )
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    html.Div("Scatter Plot of Pokémon Stats", className="card-header"),
                    dbc.CardBody([
                        dcc.Loading(
                            children=[
                                dcc.Graph(id='scatter-plot', className='graph-container', style={'height': '400px'})
                            ],
                            custom_spinner=create_pokebola_spinner(),
                            fullscreen=True,
                        )
                    ])
                ], className='graph-card')
            ], width=12)
        ])
    ], fluid=True)

def render_box_plot_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    html.Div("Violin Plot of Pokémon Stats by Type 1", className="card-header"),
                    dbc.CardBody([
                        dcc.Loading(
                            children=[
                                dcc.Graph(id='box-plot', className='graph-container', style={'height': '1200px'})
                            ],
                            custom_spinner=create_pokebola_spinner(),
                            fullscreen=True,
                        )
                    ])
                ], className='graph-card')
            ], width=12)
        ])
    ], fluid=True)


def render_stats_bar_chart():
    random_pokemons = df.sample(n=3)['#'].tolist()
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    html.Div("Pokémon Stats Bar Chart", className="card-header"),
                    dbc.CardBody([
                        dcc.Dropdown(
                            id='pokemon-dropdown',
                            options=[{'label': row['Name'], 'value': row['#']} for _, row in df.iterrows()],
                            value=random_pokemons,
                            multi=True,
                            style={'marginBottom': '20px'}
                        ),
                        dcc.Loading(
                            children=[
                                dcc.Graph(id='stats-graph', className='graph-container', style={'height': '500px'})
                            ],
                            custom_spinner=create_pokebola_spinner(),
                            fullscreen=True,
                        )
                    ])
                ], className='graph-card')
            ], width=12)
        ])
    ], fluid=True)