import pandas as pd
from dash import html

# Constants
TYPE_COLORS = {
        'Grass': '#78C850',
        'Poison': '#A040A0',
        'Fire': '#F08030',
        'Water': '#6890F0',
        'Bug': '#A8B820',
        'Normal': '#A8A878',
        'Flying': '#A890F0',
        'Electric': '#F8D030',
        'Ground': '#E0C068',
        'Fairy': '#EE99AC',
        'Fighting': '#C03028',
        'Psychic': '#F85888',
        'Rock': '#B8A038',
        'Steel': '#B8B8D0',
        'Ice': '#98D8D8',
        'Ghost': '#705898',
        'Dragon': '#7038F8',
        'Dark': '#705848'
    }

TYPE_ICONS = {
    'Grass': 'fas fa-seedling',
    'Poison': 'fas fa-skull-crossbones',
    'Fire': 'fas fa-fire',
    'Water': 'fas fa-tint',
    'Bug': 'fas fa-bug',
    'Normal': 'fas fa-star',
    'Flying': 'fas fa-feather-alt',
    'Electric': 'fas fa-bolt',
    'Ground': 'fas fa-mountain',
    'Fairy': 'fas fa-magic',
    'Fighting': 'fas fa-fist-raised',
    'Psychic': 'fas fa-brain',
    'Rock': 'fas fa-gem',
    'Steel': 'fas fa-shield-alt',
    'Ice': 'fas fa-snowflake',
    'Ghost': 'fas fa-ghost',
    'Dragon': 'fas fa-dragon',
    'Dark': 'fas fa-moon'
}


def get_type_color(pokemon_type):
    """
    Returns the color associated with the given Pokémon type.
    """
    return TYPE_COLORS.get(pokemon_type, '#343a40')


def load_pokemon_data():
    """
    Carga y procesa los datos de los Pokémon.
    """
    df = pd.read_csv('data/pokemon_stats.csv')
    df = df.drop_duplicates(subset=['#'], keep='first')
    return df



# Definir la Pokebola como HTML
def create_pokebola_spinner():
    return html.Div(
        className='pokebola-container pokebola-loading',
        children=[
            html.Div(
                className='item',
                children=[
                    html.Div(className='ball'),
                    html.Div(className='half-ball'),
                    html.Div(className='half-ball-top'),
                    html.Div(className='big-button'),
                    html.Div(className='small-button'),
                    html.Div(className='horizon')
                ]
            )
        ]
    )

def create_pokebola_sidebar():
    return html.Div(
        className='pokebola-container pokebola-sidebar',
        children=[
            html.Div(
                className='item',
                children=[
                    html.Div(className='ball'),
                    html.Div(className='half-ball'),
                    html.Div(className='half-ball-top'),
                    html.Div(className='big-button'),
                    html.Div(className='small-button'),
                    html.Div(className='horizon')
                ]
            )
        ]
    )
