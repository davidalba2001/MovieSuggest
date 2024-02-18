import sys
sys.path.append('./src/code')
import dash
from dash import dcc, html, Input, Output, State
import recommendation_engine as re

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Diseño de la aplicación
app.layout = html.Div([
    # Encabezado
    html.H1("Sistema de Recomendaciones de Películas", style={'text-align': 'center', 'margin-bottom': '30px'}),

    # Formulario de inicio de sesión
    html.Div([
        html.H2("Inicio de Sesión", style={'margin-bottom': '15px'}),
        dcc.Input(id='input-usuario', type='text', placeholder='Usuario', style={'margin-bottom': '10px'}),
        html.Button('Iniciar Sesión', id='boton-login', n_clicks=0, style={'margin-bottom': '10px'}),
        html.Div(id='output-login')
    ], style={'width': '50%', 'margin': 'auto', 'text-align': 'center', 'padding': '20px', 'border': '1px solid #ccc', 'border-radius': '10px', 'box-shadow': '0px 0px 10px 0px rgba(0,0,0,0.1)'}),

    # Sección de recomendaciones de películas
    html.Div(id='recomendaciones-container', style={'display': 'none', 'margin-top': '30px'}),
    html.H3("Recomendaciones de Películas", style={'text-align': 'center', 'margin-bottom': '15px'}),
    html.Div(id='recomendaciones')
])

# Callback para manejar el inicio de sesión
@app.callback(
    Output('output-login', 'children'),
    Output('recomendaciones-container', 'style'),
    Input('boton-login', 'n_clicks'),
    State('input-usuario', 'value')
)
def log_in(n_clicks, usuario):
    if n_clicks > 0:
        try:
            user_id = int(usuario)
        except ValueError:
            return "Por favor, ingrese un número entero válido.", {'display': 'none'}

        if re.exist_userid(user_id):
            return f"Bienvenido, {user_id}!", {'display': 'block'}
        else:
            return "Usuario incorrecto. Por favor, intente nuevamente.", {'display': 'none'}

# Callback para obtener recomendaciones de películas
@app.callback(
    Output('recomendaciones', 'children'),
    Input('boton-login', 'n_clicks'),
    State('input-usuario', 'value')
)
def obtener_recomendaciones(n_clicks, usuario):
    if n_clicks > 0:
        user_id = int(usuario)
        movies = re.get_topn_movies(user_id, 20)
        recomendaciones = [html.Div(movie) for movie in movies]
        return recomendaciones

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
