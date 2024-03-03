from networkx import dfs_labeled_edges
import numpy as np
from sklearn.decomposition import TruncatedSVD
import pandas as pd

def create_dataMatrix(ratings_data):
    data_matrix = ratings_data.pivot_table(values="rating",index="user_id",columns="movie_id",fill_value= 0)
    return data_matrix,data_matrix.T

def create_new_user_ratings_vector(ratings, new_user_id):
    # Crear un DataFrame con las puntuaciones
    df_rating = pd.DataFrame(ratings, columns=['rating'])
    
    # Añadir el ID del usuario y el ID de la película al DataFrame
    df_rating['user_id'] = new_user_id
    df_rating['movie_id'] = df_rating.index
    
    # Asegurarse de que el DataFrame de las calificaciones del nuevo usuario esté en el formato correcto
    # y que los IDs de usuario y película coincidan con los de la matriz de datos
    dfs_labeled_edgesrating = df_rating.rename(columns={'user_id': 'user_id', 'movie_id': 'movie_id', 'rating': 'rating'})
    
    # Añadir las calificaciones del nuevo usuario a la matriz de datos
    new_user_ratings_vector = df_rating.set_index('movie_id')['rating']
    
    return new_user_ratings_vector
    
def add_new_user_ratings(data_matrix, new_user_ratings):
    # Asegurarse de que el DataFrame de las calificaciones del nuevo usuario esté en el formato correcto
    # y que los IDs de usuario y película coincidan con los de la matriz de datos
    new_user_ratings = new_user_ratings.rename(columns={'user_id': 'user_id', 'movie_id': 'movie_id', 'rating': 'rating'})
    
    # Añadir las calificaciones del nuevo usuario a la matriz de datos
    data_matrix = data_matrix.append(new_user_ratings.set_index(['user_id', 'movie_id']), ignore_index=False)
    
    # Asegurarse de que la matriz de datos tenga valores para todas las combinaciones de usuario y película
    data_matrix = data_matrix.fillna(0)
    
    return data_matrix


def calculate_svd(matrix, n_components):
    svd = TruncatedSVD(n_components = n_components, random_state = 42)
    resultant_matrix = svd.fit_transform(matrix)
    return resultant_matrix, svd

def simplify_information(SVD, num_sv=10):
    """
    Simplifica la información utilizando los primeros num_sv vectores singulares.

    Parámetros:
    SVD: objeto TruncatedSVD ya ajustado
    num_sv: número de componentes principales a mantener (por defecto )

    Devuelve:
    Porcentaje de información conservada
    """
    percent_info_retained = 100 * (SVD.singular_values_[:num_sv].sum() / SVD.singular_values_.sum())
    print('Porcentaje de información conservada con los primeros %d vectores singulares:' % num_sv)
    print('%.1f%%' % percent_info_retained)
    return percent_info_retained

def calculate_correlation_matrix(matrix):
    return np.corrcoef(matrix)