import numpy as np
from sklearn.decomposition import TruncatedSVD

def create_dataMatrix(ratings_data):
    data_matrix = ratings_data.pivot_table(values="rating",index="user_id",columns="movie_id",fill_value= 0)
    return data_matrix,data_matrix.T

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