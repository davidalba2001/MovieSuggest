import sys
sys.path.append('./src/code')
import dash
from dash import dcc, html, Input, Output, State
import recommendation_engine as re

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Diseño de la aplicación


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
