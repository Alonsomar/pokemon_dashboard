import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots

from layout import (
    create_layout,
    render_box_plot_layout,
    render_radar_chart_layout,
    render_scatter_plot_layout,
    render_stats_bar_chart,
)
from plot_utils import TYPE_ICONS, create_pokebola_spinner, get_type_color, load_pokemon_data

# Initialize the app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css",
    ],
    external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.js"],
    suppress_callback_exceptions=True,
)


# Set the app layout
app.layout = create_layout(app)
app.title = "Pokemon Dashboard"

# Load Pokémon data
df = load_pokemon_data()

# Definir el layout base
chart_layout = {
    "font": {"family": "Montserrat, sans-serif", "size": 12},
    "title_font": {"family": "Montserrat, sans-serif", "size": 16},
    "plot_bgcolor": "rgba(0,0,0,0)",
    "paper_bgcolor": "rgba(0,0,0,0)",
    "legend": {
        "orientation": "h",
        "yanchor": "bottom",
        "y": 1.02,
        "xanchor": "right",
        "x": 1,
        "bgcolor": "rgba(0,0,0,0)",
        "font": {"size": 10},
    },
    "margin": {"l": 40, "r": 40, "t": 40, "b": 40},
    "hoverlabel": {"font": {"family": "Montserrat, sans-serif", "size": 12}},
}


# Función helper para obtener el layout actualizado según el tema
def get_themed_layout(theme_data):
    layout = chart_layout.copy()
    is_dark = theme_data and theme_data.get("theme") == "dark"

    layout.update(
        template="plotly_dark" if is_dark else "plotly_white",
        title_font_color="white" if is_dark else "#2C3E50",
    )
    return layout


# Callback para actualizar el estilo de las gráficas cuando cambia el tema
@app.callback(
    Output("your-graph-id", "figure"),  # Reemplaza 'your-graph-id' con el ID de tu gráfica
    [Input("theme-store", "data")],
    [State("your-graph-id", "figure")],  # Reemplaza 'your-graph-id' con el ID de tu gráfica
)
def update_graph_theme(theme_data, current_figure):
    if current_figure is None:
        return {}

    fig = go.Figure(current_figure)
    fig.update_layout(get_themed_layout(theme_data))
    return fig


# Funtion to parse stats with icons and image
def get_pokemon_info(pokemon_data):
    type1_icon = TYPE_ICONS.get(pokemon_data["Type 1"], "fas fa-question")
    type2_icon = (
        TYPE_ICONS.get(pokemon_data["Type 2"], "fas fa-question")
        if not pd.isna(pokemon_data["Type 2"])
        else None
    )

    info = html.Div(
        [
            html.H4(html.B(pokemon_data["Name"]), style={"textAlign": "center"}),
            html.P(
                [
                    html.I(className=type1_icon, style={"margin-right": "5px"}),
                    f"Type 1: {pokemon_data['Type 1']}",
                ],
                **{"data-tooltip": pokemon_data["Type 1"]},
                style={"textAlign": "center"},
            ),
            html.P(
                [
                    html.I(className=type2_icon, style={"margin-right": "5px"}),
                    f"Type 2: {pokemon_data['Type 2']}",
                ],
                **{"data-tooltip": pokemon_data["Type 2"]},
                style={"textAlign": "center"},
            )
            if type2_icon
            else None,
            html.P(
                [
                    html.I(className="fas fa-chart-bar", style={"margin-right": "5px"}),
                    f"Total: {pokemon_data['Total']}",
                ],
                **{"data-tooltip": "Total Stats"},
                style={"textAlign": "center"},
            ),
            html.P(
                [
                    html.I(className="fas fa-heartbeat", style={"margin-right": "5px"}),
                    f"HP: {pokemon_data['HP']}",
                ],
                **{"data-tooltip": "Health Points"},
                style={"textAlign": "center"},
            ),
            html.P(
                [
                    html.I(className="fas fa-fist-raised", style={"margin-right": "5px"}),
                    f"Attack: {pokemon_data['Attack']}",
                ],
                **{"data-tooltip": "Attack"},
                style={"textAlign": "center"},
            ),
            html.P(
                [
                    html.I(className="fas fa-shield-alt", style={"margin-right": "5px"}),
                    f"Defense: {pokemon_data['Defense']}",
                ],
                **{"data-tooltip": "Defense"},
                style={"textAlign": "center"},
            ),
            html.P(
                [
                    html.I(className="fas fa-bolt", style={"margin-right": "5px"}),
                    f"Sp. Atk: {pokemon_data['Sp. Atk']}",
                ],
                **{"data-tooltip": "Special Attack"},
                style={"textAlign": "center"},
            ),
            html.P(
                [
                    html.I(className="fas fa-bolt", style={"margin-right": "5px"}),
                    f"Sp. Def: {pokemon_data['Sp. Def']}",
                ],
                **{"data-tooltip": "Special Defense"},
                style={"textAlign": "center"},
            ),
            html.P(
                [
                    html.I(className="fas fa-tachometer-alt", style={"margin-right": "5px"}),
                    f"Speed: {pokemon_data['Speed']}",
                ],
                **{"data-tooltip": "Speed"},
                style={"textAlign": "center"},
            ),
        ],
        style={"textAlign": "center"},
    )

    image_src = f"assets/images/{str(pokemon_data['#']).zfill(3)}.png"

    return info, image_src


# Transform hex code to rgba string
def hex_to_rgba(hex_color, opacity):
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"rgba({r}, {g}, {b}, {opacity})"


# Definir el callback fuera de la función render_heatmap
@app.callback(Output("heatmap-graph", "figure"), [Input("theme-store", "data")])
def update_heatmap(theme_data):
    correlation_matrix = df[["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]].corr()

    fig_heatmap = go.Figure(
        data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.columns,
            colorscale="RdBu",
            zmin=-1,
            zmax=1,
            text=correlation_matrix.values.round(2),
            texttemplate="%{text}",
            textfont={"size": 10},
            hoverongaps=False,
            hovertemplate="%{x} vs %{y}<br>Correlation: %{z:.2f}<extra></extra>",
        )
    )

    # Añadir anotaciones con mejor contraste
    annotations = []
    for i, row in enumerate(correlation_matrix.values):
        for j, value in enumerate(row):
            text_color = "white" if abs(value) > 0.4 else "black"
            annotations.append(
                {
                    "x": correlation_matrix.columns[j],
                    "y": correlation_matrix.columns[i],
                    "text": str(round(value, 2)),
                    "showarrow": False,
                    "font": {"color": text_color, "size": 10},
                }
            )

    # Obtener el layout temático base
    themed_layout = get_themed_layout(theme_data)

    # Actualizar el layout con configuraciones específicas del heatmap
    themed_layout.update(
        title="Correlation Heatmap of Pokémon Stats",
        xaxis={"side": "bottom", "tickangle": 45, "tickfont": {"size": 10}},
        yaxis={"tickfont": {"size": 10}},
        annotations=annotations,
        height=600,
        margin={"l": 60, "r": 30, "t": 50, "b": 80},
    )

    fig_heatmap.update_layout(themed_layout)

    return fig_heatmap


# Función de renderizado separada
def render_heatmap():
    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    html.Div(
                                        "Correlation Heatmap of Pokémon Stats",
                                        className="card-header",
                                    ),
                                    dbc.CardBody(
                                        [
                                            dcc.Loading(
                                                children=[
                                                    dcc.Graph(
                                                        id="heatmap-graph",
                                                        className="graph-container",
                                                        style={"height": "520px"},
                                                    )
                                                ],
                                                custom_spinner=create_pokebola_spinner(),
                                                fullscreen=True,
                                            )
                                        ]
                                    ),
                                ],
                                className="graph-card",
                            )
                        ],
                        width=12,
                    )
                ]
            )
        ],
        fluid=True,
    )


# Callback with content
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/heatmap":
        return render_heatmap()
    elif pathname == "/scatter-plot":
        return render_scatter_plot_layout()
    elif pathname == "/bar-chart":
        return render_stats_bar_chart()
    elif pathname == "/box-plot":
        return render_box_plot_layout()
    else:
        return render_radar_chart_layout()


# Callback to
@app.callback(
    Output("stats-graph", "figure"),
    [Input("pokemon-dropdown", "value"), Input("theme-store", "data")],
)
def update_bar_chart(selected_pokemon, theme_data):
    if not selected_pokemon:
        return go.Figure()

    filtered_df = df[df["#"].isin(selected_pokemon)]
    fig = go.Figure()

    for _, row in filtered_df.iterrows():
        fig.add_trace(
            go.Bar(
                x=["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"],
                y=[
                    row["HP"],
                    row["Attack"],
                    row["Defense"],
                    row["Sp. Atk"],
                    row["Sp. Def"],
                    row["Speed"],
                ],
                name=row["Name"],
                marker={"cornerradius": "15%"},
            )
        )

    fig.update_layout(
        barmode="group", xaxis_title="Stats", yaxis_title="Values", **get_themed_layout(theme_data)
    )

    return fig


@app.callback(
    [
        Output("pokemon-info-1", "children"),
        Output("pokemon-image-1", "src"),
        Output("pokemon-info-1", "style"),
        Output("pokemon-info-2", "children"),
        Output("pokemon-image-2", "src"),
        Output("pokemon-info-2", "style"),
        Output("radar-graph-comparison", "figure"),
    ],
    [
        Input("pokemon-dropdown-1", "value"),
        Input("pokemon-dropdown-2", "value"),
        Input("theme-store", "data"),
    ],
)
def update_radar_chart(pokemon1, pokemon2, theme_data):
    pokemon_data_1 = df[df["#"] == pokemon1].iloc[0]
    pokemon_data_2 = df[df["#"] == pokemon2].iloc[0]

    info_1, image_src_1 = get_pokemon_info(pokemon_data_1)
    info_2, image_src_2 = get_pokemon_info(pokemon_data_2)

    color_1 = hex_to_rgba(get_type_color(pokemon_data_1["Type 1"]), 0.3)
    color_2 = hex_to_rgba(get_type_color(pokemon_data_2["Type 1"]), 0.3)

    style_1 = {
        "backgroundColor": color_1,
        "borderRadius": "15px",
        "padding": "15px",
        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
        "backdropFilter": "blur(10px)",
        "WebkitBackdropFilter": "blur(10px)",
        "transition": "all 0.3s ease",
    }
    style_2 = {
        "backgroundColor": color_2,
        "borderRadius": "15px",
        "padding": "15px",
        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
        "backdropFilter": "blur(10px)",
        "WebkitBackdropFilter": "blur(10px)",
        "transition": "all 0.3s ease",
    }

    max_stat = max(
        pokemon_data_1[["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]].max(),
        pokemon_data_2[["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]].max(),
    )

    fig_radar = go.Figure()

    line_dash_2 = "dash" if pokemon_data_1["Type 1"] == pokemon_data_2["Type 1"] else "solid"

    fig_radar.add_trace(
        go.Scatterpolar(
            r=[
                pokemon_data_1["HP"],
                pokemon_data_1["Attack"],
                pokemon_data_1["Defense"],
                pokemon_data_1["Sp. Atk"],
                pokemon_data_1["Sp. Def"],
                pokemon_data_1["Speed"],
                pokemon_data_1["HP"],
            ],
            theta=["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed", "HP"],
            mode="lines+markers",
            name=pokemon_data_1["Name"],
            line_color=get_type_color(pokemon_data_1["Type 1"]),
        )
    )
    fig_radar.add_trace(
        go.Scatterpolar(
            r=[
                pokemon_data_2["HP"],
                pokemon_data_2["Attack"],
                pokemon_data_2["Defense"],
                pokemon_data_2["Sp. Atk"],
                pokemon_data_2["Sp. Def"],
                pokemon_data_2["Speed"],
                pokemon_data_2["HP"],
            ],
            theta=["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed", "HP"],
            mode="lines+markers",
            name=pokemon_data_2["Name"],
            line={"color": get_type_color(pokemon_data_2["Type 1"]), "dash": line_dash_2},
        )
    )

    themed_layout = get_themed_layout(theme_data)
    themed_layout.update(
        polar={
            "bgcolor": "rgba(240, 240, 240, 0.3)",
            "radialaxis": {"visible": True, "range": [0, max(100, max_stat)]},
        }
    )
    fig_radar.update_layout(**themed_layout)

    return info_1, image_src_1, style_1, info_2, image_src_2, style_2, fig_radar


@app.callback(
    Output("scatter-plot", "figure"),
    [
        Input("scatter-xaxis", "value"),
        Input("scatter-yaxis", "value"),
        Input("pokemon-dropdown", "value"),
        Input("theme-store", "data"),
    ],
)
def update_scatter_plot(xaxis, yaxis, selected_pokemon, theme_data):
    fig = go.Figure()

    for pokemon_type in df["Type 1"].unique():
        type_color = get_type_color(pokemon_type)
        type_data = df[df["Type 1"] == pokemon_type]
        fig.add_trace(
            go.Scatter(
                x=type_data[xaxis],
                y=type_data[yaxis],
                mode="markers",
                marker={
                    "color": type_color,
                    "size": 8,
                    "line": {"color": "rgba(0, 0, 0, 0.5)", "width": 1},
                },
                text=type_data["Name"],
                name=pokemon_type,
            )
        )

    if selected_pokemon:
        selected_data = df[df["#"].isin(selected_pokemon)]
        fig.add_trace(
            go.Scatter(
                x=selected_data[xaxis],
                y=selected_data[yaxis],
                mode="markers",
                marker={"color": "red", "size": 12, "line": {"color": "black", "width": 2}},
                text=selected_data["Name"],
                name="Selected Pokémon",
            )
        )

    fig.update_layout(
        xaxis_title=xaxis, yaxis_title=yaxis, showlegend=True, **get_themed_layout(theme_data)
    )

    return fig


@app.callback(
    Output("box-plot", "figure"), [Input("url", "pathname"), Input("theme-store", "data")]
)
def update_violin_plot(pathname, theme_data):
    if pathname != "/box-plot":
        return go.Figure()

    fig = make_subplots(
        rows=6,
        cols=1,
        shared_xaxes=True,
        subplot_titles=["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"],
        vertical_spacing=0.03,
    )

    stats = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]

    for i, stat in enumerate(stats, start=1):
        for pokemon_type in df["Type 1"].unique():
            type_color = get_type_color(pokemon_type)
            violin_trace = go.Violin(
                x=df[df["Type 1"] == pokemon_type]["Type 1"],
                y=df[df["Type 1"] == pokemon_type][stat],
                name=pokemon_type,
                line_color=type_color,
                box_visible=True,
                meanline_visible=True,
                points="all",
            )
            fig.add_trace(violin_trace, row=i, col=1)

    themed_layout = get_themed_layout(theme_data)
    themed_layout.update(height=1200)
    fig.update_layout(**themed_layout)

    return fig


# Añadir este callback después de los existentes
@app.callback(
    [
        Output("theme-store", "data"),
        Output("theme-switch", "children"),
        Output("body-container", "data-theme"),
        Output("p5-container", "data-theme"),
    ],
    [Input("theme-switch", "n_clicks")],
    [State("theme-store", "data")],
)
def toggle_theme(n_clicks, current_theme):
    if n_clicks is None:
        return {"theme": "light"}, html.I(className="fas fa-moon"), "light", "light"

    if current_theme is None or current_theme.get("theme") == "light":
        return {"theme": "dark"}, html.I(className="fas fa-sun"), "dark", "dark"

    return {"theme": "light"}, html.I(className="fas fa-moon"), "light", "light"


# Añadir este callback para aplicar el tema

# Run the server
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=False)
