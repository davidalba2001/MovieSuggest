import dash
from dash import Dash, dcc, html, Input, Output, State, ALL, callback_context
from dash.exceptions import PreventUpdate

app = Dash(__name__)

movie_ratings = {}
movie_componet ={}
# Lista de títulos de películas
list_titles = ["Movie 1", "Movie 2", "Movie 3", "Random Title"]

# Función para mostrar las películas que coincidan con la búsqueda


def show_movies(search_query):
    matched_movies = [
        title for title in list_titles if search_query.lower() in title.lower()]
    return matched_movies


# Layout de la aplicación
app.layout = html.Div([
    html.H1("Search Movies"),
    dcc.Input(id='search-input', type='text', value='',
              placeholder="Enter search term..."),
    html.Button('Search', id='search-button', n_clicks=0),
    html.Div(id='output-container-button'),
])


@app.callback(
    Output('output-container-button', 'children'),
    Input('search-button', 'n_clicks'),
    [State('search-input', 'value')]
)
def update_search(n_clicks, input_value):
    print(movie_ratings)
    # Verificar si n_clicks es mayor que 0
    if n_clicks is not None and n_clicks > 0:
        # Llamamos a la función show_movies con el valor de entrada
        movies = show_movies(input_value)

        # Creamos una lista para almacenar los componentes de diseño de las películas
        movie_layouts = []

        # Iteramos sobre cada película y creamos un componente de diseño para ella
        for i, movie in enumerate(movies):
            # Utilizamos la función layout para crear el diseño de la película
            # Pasamos el título de la película como parámetro
            movie_layout = generate_star_rating_component(movie, i)
            movie_layouts.append(movie_layout)
        # Retornamos la lista de componentes de diseño de películas como salida de la devolución de llamada
        return movie_layouts
    else:
        # Si no se ha hecho clic en el botón de búsqueda, no hay actualizaciones
        raise PreventUpdate


def generate_star_rating_component(title, component_id):
    movie_componet[component_id] = title
    rating_div = html.Div([
        html.H2(title, style={'display': 'inline-block'}),
        html.Div([
            html.Div('★', id=f'star-{component_id}-1', n_clicks=0, style={'font-size': '30px',
                     'display': 'inline-block', 'cursor': 'pointer', 'margin-right': '5px'}),
            html.Div('★', id=f'star-{component_id}-2', n_clicks=0, style={'font-size': '30px',
                     'display': 'inline-block', 'cursor': 'pointer', 'margin-right': '5px'}),
            html.Div('★', id=f'star-{component_id}-3', n_clicks=0, style={'font-size': '30px',
                     'display': 'inline-block', 'cursor': 'pointer', 'margin-right': '5px'}),
            html.Div('★', id=f'star-{component_id}-4', n_clicks=0, style={'font-size': '30px',
                     'display': 'inline-block', 'cursor': 'pointer', 'margin-right': '5px'}),
            html.Div('★', id=f'star-{component_id}-5', n_clicks=0, style={
                     'font-size': '30px', 'display': 'inline-block', 'cursor': 'pointer'})
        ], style={'display': 'inline-block'})
    ])
    return rating_div


def generate_star_callback(component_id):
    @app.callback(
        [Output(f'star-{component_id}-{i}', 'style') for i in range(1, 6)],
        [Input(f'star-{component_id}-{i}', 'n_clicks') for i in range(1, 6)]
    )
    def update_stars(*args):
        ctx = callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        gold_style = {'color': 'gold', 'font-size': '30px',
                      'display': 'inline-block', 'cursor': 'pointer'}
        black_style = {'color': 'black', 'font-size': '30px',
                       'display': 'inline-block', 'cursor': 'pointer'}

        if triggered_id.startswith(f'star-{component_id}'):
            last_clicked = int(triggered_id.split('-')[-1])
            movie_ratings[movie_componet[component_id]] = last_clicked  
            return [gold_style if i + 1 <= last_clicked else black_style for i in range(5)]
        else:
            return [black_style] * 5

# Generar los callbacks para las estrellas
for i in range(len(list_titles)):
    generate_star_callback(i)


if __name__ == '__main__':
    app.run_server(debug=True)
