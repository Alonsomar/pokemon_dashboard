# Imports
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
from layout import create_layout, render_radar_chart_layout, render_scatter_plot_layout, render_box_plot_layout, render_stats_bar_chart
from plot_utils import get_type_color, load_pokemon_data, create_pokebola_spinner, TYPE_ICONS
from plotly.subplots import make_subplots

# Initialize the app
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP,
                                      "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"],
                external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.js"],
                suppress_callback_exceptions=True)


# Set the app layout
app.layout = create_layout(app)
app.title = "Pokemon Dashboard"

# Load Pokémon data
df = load_pokemon_data()

# Custom chart layout
chart_layout = dict(
    font=dict(family='Montserrat, sans-serif'),
    title_font=dict(family='Montserrat, sans-serif'),
    template='ggplot2',
    plot_bgcolor='rgba(240,240,240,0.4)',
    paper_bgcolor='rgba(0,0,0,0)',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.03,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=20, r=20, t=30, b=20),
    hoverlabel=dict(
            font=dict(
                family='Montserrat, sans-serif',
                size=12
            )
    )
)

# Funtion to parse stats with icons and image
def get_pokemon_info(pokemon_data):
    type1_icon = TYPE_ICONS.get(pokemon_data['Type 1'], 'fas fa-question')
    type2_icon = TYPE_ICONS.get(pokemon_data['Type 2'], 'fas fa-question') if not pd.isna(pokemon_data['Type 2']) else None

    info = html.Div([
        html.H4(html.B(pokemon_data['Name']), style={'textAlign': 'center'}),
        html.P([html.I(className=type1_icon, style={'margin-right': '5px'}), f"Type 1: {pokemon_data['Type 1']}"], **{'data-tooltip': pokemon_data['Type 1']}, style={'textAlign': 'center'}),
        html.P([html.I(className=type2_icon, style={'margin-right': '5px'}), f"Type 2: {pokemon_data['Type 2']}"], **{'data-tooltip': pokemon_data['Type 2']}, style={'textAlign': 'center'}) if type2_icon else None,
        html.P([html.I(className='fas fa-chart-bar', style={'margin-right': '5px'}), f"Total: {pokemon_data['Total']}"], **{'data-tooltip': 'Total Stats'}, style={'textAlign': 'center'}),
        html.P([html.I(className='fas fa-heartbeat', style={'margin-right': '5px'}), f"HP: {pokemon_data['HP']}"], **{'data-tooltip': 'Health Points'}, style={'textAlign': 'center'}),
        html.P([html.I(className='fas fa-fist-raised', style={'margin-right': '5px'}), f"Attack: {pokemon_data['Attack']}"], **{'data-tooltip': 'Attack'}, style={'textAlign': 'center'}),
        html.P([html.I(className='fas fa-shield-alt', style={'margin-right': '5px'}), f"Defense: {pokemon_data['Defense']}"], **{'data-tooltip': 'Defense'}, style={'textAlign': 'center'}),
        html.P([html.I(className='fas fa-bolt', style={'margin-right': '5px'}), f"Sp. Atk: {pokemon_data['Sp. Atk']}"], **{'data-tooltip': 'Special Attack'}, style={'textAlign': 'center'}),
        html.P([html.I(className='fas fa-bolt', style={'margin-right': '5px'}), f"Sp. Def: {pokemon_data['Sp. Def']}"], **{'data-tooltip': 'Special Defense'}, style={'textAlign': 'center'}),
        html.P([html.I(className='fas fa-tachometer-alt', style={'margin-right': '5px'}), f"Speed: {pokemon_data['Speed']}"], **{'data-tooltip': 'Speed'}, style={'textAlign': 'center'})
    ], style={'textAlign': 'center'} )

    image_src = f'assets/images/{str(pokemon_data["#"]).zfill(3)}.png'

    return info, image_src

# Transform hex code to rgba string
def hex_to_rgba(hex_color, opacity):
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f'rgba({r}, {g}, {b}, {opacity})'

# Heatmap figure
def render_heatmap():
    correlation_matrix = df[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].corr()
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale='Blues',
        zmin=-1, zmax=1,
        text=correlation_matrix.values.round(2),
        hoverinfo='text',
    ))

    # Add annotations
    annotations = []
    for i, row in enumerate(correlation_matrix.values):
        for j, value in enumerate(row):
            annotations.append(
                dict(
                    x=correlation_matrix.columns[j],
                    y=correlation_matrix.columns[i],
                    text=str(round(value, 2)),
                    showarrow=False,
                    font=dict(color="black" if value < 0.5 else "white"),
                )
            )

    fig_heatmap.update_layout(
        xaxis={'side': 'bottom'},
        yaxis_tickmode='array',
        yaxis_tickvals=list(range(len(correlation_matrix.columns))),
        yaxis_ticktext=correlation_matrix.columns,
        annotations=annotations,
        **chart_layout
    )

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    html.Div("Correlation Heatmap of Pokémon Stats", className="card-header"),
                    dbc.CardBody([
                        dcc.Loading(
                            children=[
                                dcc.Graph(id='heatmap-graph', figure=fig_heatmap, className='graph-container', style={'height': '520px'})
                            ],
                            custom_spinner=create_pokebola_spinner(),
                            fullscreen=True,
                        )
                    ])
                ], className='graph-card')
            ], width=12)
        ])
    ], fluid=True)

# Callback with content
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/heatmap':
        return render_heatmap()
    elif pathname == '/scatter-plot':
        return render_scatter_plot_layout()
    elif pathname == '/bar-chart':
        return render_stats_bar_chart()
    elif pathname == '/box-plot':
        return render_box_plot_layout()
    else:
        return render_radar_chart_layout()


# Callback to
@app.callback(
    Output('stats-graph', 'figure'),
    [Input('pokemon-dropdown', 'value')]
)
def update_bar_chart(selected_pokemon):
    if not selected_pokemon:
        return go.Figure()

    filtered_df = df[df['#'].isin(selected_pokemon)]
    fig = go.Figure()

    for _, row in filtered_df.iterrows():
        fig.add_trace(go.Bar(
            x=['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'],
            y=[row['HP'], row['Attack'], row['Defense'], row['Sp. Atk'], row['Sp. Def'], row['Speed']],
            name=row['Name'],
            marker=dict(cornerradius="15%")
        ))

    fig.update_layout(
        barmode='group',
        xaxis_title='Stats',
        yaxis_title='Values',
        **chart_layout
    )

    return fig


@app.callback(
    [Output('pokemon-info-1', 'children'),
     Output('pokemon-image-1', 'src'),
     Output('pokemon-info-1', 'style'),
     Output('pokemon-info-2', 'children'),
     Output('pokemon-image-2', 'src'),
     Output('pokemon-info-2', 'style'),
     Output('radar-graph-comparison', 'figure')],
    [Input('pokemon-dropdown-1', 'value'),
     Input('pokemon-dropdown-2', 'value')]
)
def update_radar_chart(pokemon1, pokemon2):
    pokemon_data_1 = df[df['#'] == pokemon1].iloc[0]
    pokemon_data_2 = df[df['#'] == pokemon2].iloc[0]

    info_1, image_src_1 = get_pokemon_info(pokemon_data_1)
    info_2, image_src_2 = get_pokemon_info(pokemon_data_2)

    color_1 = hex_to_rgba(get_type_color(pokemon_data_1['Type 1']), 0.4)
    color_2 = hex_to_rgba(get_type_color(pokemon_data_2['Type 1']), 0.4)

    style_1 = {'backgroundColor': color_1, 'borderRadius': '10px', 'padding': '10px'}
    style_2 = {'backgroundColor': color_2, 'borderRadius': '10px', 'padding': '10px'}

    max_stat = max(pokemon_data_1[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].max(),
                   pokemon_data_2[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].max())

    fig_radar = go.Figure()

    line_dash_2 = 'dash' if pokemon_data_1['Type 1'] == pokemon_data_2['Type 1'] else 'solid'

    fig_radar.add_trace(go.Scatterpolar(
        r=[pokemon_data_1['HP'], pokemon_data_1['Attack'], pokemon_data_1['Defense'],
           pokemon_data_1['Sp. Atk'], pokemon_data_1['Sp. Def'], pokemon_data_1['Speed'], pokemon_data_1['HP']],
        theta=['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'HP'],
        mode='lines+markers',
        name=pokemon_data_1['Name'],
        line_color= get_type_color(pokemon_data_1['Type 1'])
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=[pokemon_data_2['HP'], pokemon_data_2['Attack'], pokemon_data_2['Defense'],
           pokemon_data_2['Sp. Atk'], pokemon_data_2['Sp. Def'], pokemon_data_2['Speed'], pokemon_data_2['HP']],
        theta=['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'HP'],
        mode='lines+markers',
        name=pokemon_data_2['Name'],
        line=dict(color=get_type_color(pokemon_data_2['Type 1']), dash=line_dash_2)
    ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor="rgba(240, 240, 240, 0.3)",
            radialaxis=dict(visible=True, range=[0, max(100, max_stat)])
        ),
        showlegend=True,
        **chart_layout,

    )

    return info_1, image_src_1, style_1, info_2, image_src_2, style_2, fig_radar


@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('scatter-xaxis', 'value'),
     Input('scatter-yaxis', 'value'),
     Input('pokemon-dropdown', 'value')]
)
def update_scatter_plot(xaxis, yaxis, selected_pokemon):
    fig = go.Figure()

    for pokemon_type in df['Type 1'].unique():
        type_color = get_type_color(pokemon_type)
        type_data = df[df['Type 1'] == pokemon_type]
        fig.add_trace(go.Scatter(
            x=type_data[xaxis],
            y=type_data[yaxis],
            mode='markers',
            marker=dict(color=type_color, size=8, line=dict(color='rgba(0, 0, 0, 0.5)', width=1)),
            text=type_data['Name'],
            name=pokemon_type
        ))

    if selected_pokemon:
        selected_data = df[df['#'].isin(selected_pokemon)]
        fig.add_trace(
            go.Scatter(
                x=selected_data[xaxis],
                y=selected_data[yaxis],
                mode='markers',
                marker=dict(color='red', size=12, line=dict(color='black', width=2)),
                text=selected_data['Name'],
                name='Selected Pokémon'
            )
        )

    fig.update_layout(
        xaxis_title=xaxis,
        yaxis_title=yaxis,
        showlegend=True,
        **chart_layout
    )

    return fig


@app.callback(
    Output('box-plot', 'figure'),
    [Input('url', 'pathname')]
)
def update_violin_plot(pathname):
    if pathname != '/box-plot':
        return go.Figure()

    fig = make_subplots(
        rows=6,
        cols=1,
        shared_xaxes=True,
        subplot_titles=['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'],
        vertical_spacing=0.03  # Reduce vertical spacing
    )

    stats = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']

    for i, stat in enumerate(stats, start=1):
        for pokemon_type in df['Type 1'].unique():
            type_color = get_type_color(pokemon_type)
            violin_trace = go.Violin(
                x=df[df['Type 1'] == pokemon_type]['Type 1'],
                y=df[df['Type 1'] == pokemon_type][stat],
                name=pokemon_type,
                line_color=type_color,
                box_visible=True,
                meanline_visible=True,
                points='all'
            )
            fig.add_trace(violin_trace, row=i, col=1)

    fig.update_layout(
        height=1200,
        showlegend=False,
        **chart_layout
    )

    return fig


# Run the server
if __name__ == '__main__':
    app.run_server(debug=False)
