"""
Este script realiza el procesamiento de datos para el proyecto MovieSuggest.
"""
import pandas as pd

def load_users_data(users_path):
    users_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
    users_data = pd.read_csv(
        users_path, sep='|', names=users_cols, encoding='latin-1')
    return users_data


def load_movies_data(movies_path):
    movies_cols = ['movie id', 'movie title', 'release date', 'video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure',
                   'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
                   'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    movies_data = pd.read_csv(movies_path, sep='|',names=movies_cols, encoding='latin-1')
    return movies_data


def load_ratings_data(ratings_path):
    ratings_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
    ratings_data = pd.read_csv(
        ratings_path, sep='\t', names=ratings_cols, encoding='latin-1')
    return ratings_data


def get_userId(users_path):
    users_data = load_users_data(users_path)
    #print (users_data.head)
    usersId = users_data[['user_id']]
    return usersId

