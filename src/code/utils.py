
def filter_vector(vector, condition, threshold):
    return [(idx, val) for idx, val in enumerate(vector) if condition(val, threshold)]

def calculate_intersection(vector1, vector2):
    return [(x, y) for x in vector1 for y in vector2 if x[0] == y[0]]
