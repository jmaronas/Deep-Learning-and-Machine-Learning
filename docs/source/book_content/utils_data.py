import numpy as np

from utils import computation_graph_linear

## generate polinomial features.
def generate_poly_features(x, poly_degree, add_bias = True):
    feat = []
    
    for i in range(poly_degree+1):
        feat.append(x**i)
        
    # remove bias term (ones) if requested 
    if not add_bias:
        feat = feat[1:]
        
    return np.column_stack(tuple(feat))


## generate fourier (sin/cos) features.
def generate_fourier_features(x, n_frequencies, add_bias = True):
    feat = [np.ones_like(x)]

    for k in range(1, n_frequencies+1):
        feat.append(np.sin(k*x))
        feat.append(np.cos(k*x))

    # remove bias term (ones) if requested
    if not add_bias:
        feat = feat[1:]

    return np.column_stack(tuple(feat))


## Generates sinusoidal data
def generate_sinusoidal_data(xmin, xmax, frequency, noise_var, N, seed = None):
    if seed is not None:
        np.random.seed(seed)
    x_train = (xmax - xmin) * np.random.random_sample((N,1)) + xmin
    t_train = np.sin(frequency*x_train) + 0.3 * x_train
    t_train += np.random.normal(0, noise_var, size=x_train.shape)
    return x_train, t_train

## generates polinomial data
def generate_polinomial_data(xmin, xmax, poly_degree, noise_var, N, w_true = None, seed = None):
    if seed is not None:
        np.random.seed(seed)
    if w_true is None:
        w_true = np.array([[2],[-1.5],[0.9]])
    x_train = (xmax - xmin) * np.random.random_sample((N,1)) + xmin
    X_feats = generate_features(x_train, poly_degree)
    t_train = computation_graph_linear(X_feats, w_true, b = 0) + np.random.normal(0, noise_var, size=x_train.shape[0])[:,np.newaxis]
    return x_train, t_train

##
def sinusoidal_fun(x_locs, frequency):
    return np.sin(frequency*x_locs) + 0.3 * x_locs

## alias: the reference notebook calls this generate_features
generate_features = generate_poly_features

def norm_data(X, mean = None, std = None ):
    if mean is None:
        mean = np.mean(X, axis = 0)
        std  = np.std(X, axis = 0)

    return  (X - mean) / std, mean, std
