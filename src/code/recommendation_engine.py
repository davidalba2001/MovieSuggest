'''
 Recommendation Engine
'''
import data_processing as dp
import utils as utl
import matrix_operations as op
import sys
sys.path.append('/home/d4v3_S145/repos/MovieSuggest/src/code')

USERS_PATH = 'src/datasets/ml-100k/u.user'
MOVIES_PATH = 'src/datasets/ml-100k/u.item'
RATINGS_PATH = 'src/datasets/ml-100k/u.data'

data_usersId = dp.get_userId(USERS_PATH)

def exist_userid(user_id: int) -> bool:
    print(data_usersId)
    ''' Revisa si existe user id en los datos del sistema '''
    return user_id in data_usersId['user_id']


data_movie = dp.load_movies_data(MOVIES_PATH)
data_ratings = dp.load_ratings_data(RATINGS_PATH)

n_users = data_ratings.user_id.unique().shape[0]
n_movies = data_ratings.movie_id.unique().shape[0]
n_components = min(n_users, n_movies)
data_usermovie, data_movieuser = op.create_dataMatrix(data_ratings)

def test_simplify_information(n_components, porcent):
    (_, svd1) = op.calculate_svd(
        data_usermovie, n_components=n_components)
    (_, svd2) = op.calculate_svd(
        data_movieuser, n_components=n_components)
    print(len(svd1.singular_values_))
    n_sv = 0
    percent_info_retained = 0

    for value in range(n_components, 0, -1):
        n_sv = n_components - \
            len(list(filter(lambda x: x < value, svd1.singular_values_)))
        percent_info_retained = op.simplify_information(svd1, n_sv)
        if (percent_info_retained > porcent):
            break
    print("___________________________________________________________________________________________________")
    print(f"Con {n_sv} valores singulares se conservada el {percent_info_retained}% de la información  ")
    print("___________________________________________________________________________________________________")
    return n_sv

'''
Este test en este caso lanza 589 por lo que lo he comentado ya que conozco el resultado
'''
# test_simplify_information(n_components,90)

resultant_usermovie, _ = op.calculate_svd(data_usermovie, 590) 
resultant_movieuser, _ = op.calculate_svd(data_movieuser, 590)

correlation_usermovie = op.calculate_correlation_matrix(resultant_usermovie)
correlation_movieuser = op.calculate_correlation_matrix(resultant_movieuser)


def test_decendent_sorted(vector_item):
    return all(vector_item[i] >= vector_item[i + 1] for i in range(len(vector_item) - 1))

def test_correlation_sorted(correlation_matrix):
    for i in range(len(correlation_matrix)-1):
        if (not (test_decendent_sorted(correlation_matrix[i]))):
            return False

    return True
'''
La matriz de correlacion esta desordenada por default
'''
# print(test_correlation_sorted(correlation_usermovie))

def get_similar_items(items_id, correlation_matrix, threshold_low, threshold_high):
    similar_items = []
    items_row = correlation_matrix[items_id]
    # Crear una lista de tuplas (ID del elemento, correlación)
    similar_items_with_correlation = [(idx, correlation) for idx, correlation in enumerate(items_row)
                                      if threshold_low < correlation < threshold_high]
    # Ordenar la lista de tuplas por correlación de mayor a menor
    similar_items_with_correlation.sort(key=lambda x: x[1], reverse=True)
    return similar_items_with_correlation

def get_user_similarity_recommendations(user_id,similar_users,similar_user):
    vector_user = data_usermovie[user_id]
    #similar_users = get_similar_items(user_id,correlation_usermovie,0.95,0.99)
    similar_userid = similar_users[similar_user][0]
    vector_most_similar = data_usermovie[similar_userid]
    unrated_movies = utl.filter_vector(vector_user,lambda x,y : True if(x == y) else False,0)
    best_rated_movies = utl.filter_vector(vector_most_similar,lambda x,y : True if(x >= y) else False,5)
    recomend_movies = utl.calculate_intersection(unrated_movies,best_rated_movies)
    movie_ids = [tupla[0][0] for tupla in recomend_movies]
    return get_movie_names(movie_ids,data_movie)

def get_movie_names(movie_ids, movies_dataframe):
    movie_names = []
    for movie_id in movie_ids:
        # Buscar el nombre de la película correspondiente al ID de la película
        movie_name = movies_dataframe.loc[movies_dataframe['movie id'] == movie_id, 'movie title'].values
        # Comprobar si se encontró un nombre para la película
        if len(movie_name) > 0:
            movie_names.append(movie_name[0])
        else:
            movie_names.append("Película no encontrada")  # O cualquier mensaje que desees para películas no encontradas
    return movie_names

def get_topn_movies(user_id, n):
    top_movies = []
    similar_users = get_similar_items(user_id, correlation_usermovie, 0.35, 0.99)
    similar_userid = 0
    while True:
        if similar_userid >= len(similar_users):
            break
        movie_names = get_user_similarity_recommendations(user_id, similar_users, similar_userid)
        similar_userid += 1
        top_movies.extend(movie_names)  # Usar extend() para agregar películas individualmente
        if len(top_movies) > n:
           break
    
    return top_movies[:n]

def save_ratings_newuser(vect_rating):
    n_users += 1
    new_user_ratings = op.create_new_user_ratings_vector(vect_rating,n_users+1)
    data_usermovie = op.add_new_user_ratings(data_usermovie, new_user_ratings)
    return n_users

