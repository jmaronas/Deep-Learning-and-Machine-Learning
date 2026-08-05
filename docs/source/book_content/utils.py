import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d


## Display 3D arrows
# source: https://stackoverflow.com/questions/29188612/arrows-in-matplotlib-using-mplot3d
class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        super().__init__((0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))

        return np.min(zs)

## function implementing squared loss function
def squared_loss_function(t,y,*args):
    return (t-y)**2

brier_loss_function = squared_loss_function

def absolute_loss_function(t,y,*args):
    return np.abs(t-y)

## function implementing the loss induced by a Student-t likelihood (nu degrees of freedom, scale sigma2)
def student_t_loss_function(t,y,nu,sigma2=1,*args):
    return np.log(1 + (t-y)**2 / (nu*sigma2))

## function implementing the loss induced by a heteroscedastic Gaussian likelihood (per-point variance v)
def heteroscedastic_loss_function(t,y,v,*args):
    return np.log(v) + (t-y)**2 / v

## funciton implementing binary cross entropy
def bce_loss_function(t,y, clip = None,*args):
    idx_0 = t==0
    idx_1 = ~idx_0

    loss = np.zeros(y.shape)

    loss[idx_1] = np.log(y[idx_1])
    loss[idx_0] = np.log(1-y[idx_0])

    ## add +- 1e12 for numerical stability on infs
    if isinstance(clip,float):
        loss[loss == np.inf] = clip
        loss[loss == -np.inf] = -clip

    return -1*loss

## function implementing an activation function
def activation_function_linear(x):
    return x

## activation function sigmoid
def activation_function_sigmoid(x):
    return 1. / (1. + np.exp(-x))

## activation function ReLU
def activation_function_relu(x):
    return np.maximum(0, x)

## activation function softplus
def activation_function_softplus(x):
    return np.log1p(np.exp(x))

## activation function exponential
def activation_function_exponential(x):
    return np.exp(x)

## function that implements the computational graph
def computation_graph_linear(x,w,b):
    '''
    This function represents a computational graph, a neural network, that implements a linear operation.
    Assumes regression R^D -> R (single output): w has shape (D,1) and b has shape (1,1).
    '''
    # this is the W^0 x from the theory above implemented using a transposition ;)
    y = activation_function_linear(np.matmul(x,w) + b)
    return y

## function that implements the computational graph
def computation_graph_sigmoid(x,w,b):
    ''' This function represents a computational graph, a neural network, that implements a linear operation'''
    # this is the W^0 x from the theory above implemented using a transposition ;)
    y = activation_function_sigmoid(np.matmul(x,w) + b)
    return y

## function that implements the computational graph
def computation_graph_relu(x,w,b):
    ''' This function represents a computational graph, a neural network, that implements a linear operation followed by a ReLU link'''
    y = activation_function_relu(np.matmul(x,w) + b)
    return y

## function that implements the computational graph
def computation_graph_softplus(x,w,b):
    ''' This function represents a computational graph, a neural network, that implements a linear operation followed by a Softplus link'''
    y = activation_function_softplus(np.matmul(x,w) + b)
    return y

## function that implements the computational graph
def computation_graph_exponential(x,w,b):
    ''' This function represents a computational graph, a neural network, that implements a linear operation followed by an Exponential link'''
    y = activation_function_exponential(np.matmul(x,w) + b)
    return y

## function implementing the linear model for the heteroscedastic (per-point) variance
def computation_graph_heteroscedastic_variance(x,w_sigma,b_sigma):
    '''
    This function represents the log-variance model, ie sigma^2(x) = exp(x@w_sigma+b_sigma).
    Assumes regression R^D -> R (single output): w_sigma has shape (D,1) and b_sigma has shape (1,1).
    '''
    z = computation_graph_linear(x,w_sigma,b_sigma)
    return activation_function_exponential(z)

## function that implements the full computational graph of the heteroscedastic Gaussian model
def computation_graph_heteroscedastic_gaussian(x,w,b,w_sigma,b_sigma,x_sigma=None):
    '''
    This function represents the heteroscedastic Gaussian model: a linear mean model and a
    linear log-variance model, ie t | x ~ N(x@w+b, exp(x_sigma@w_sigma+b_sigma)).
    Assumes regression R^D -> R (single output): w has shape (D,1), w_sigma has shape (D_sigma,1);
    b,b_sigma have shape (1,1).
    x_sigma are the features fed into the variance model; defaults to x (same features as the
    mean model) if not given, but can be a different (eg basis-expanded) feature matrix.
    Returns the mean y and the per-point variance v.
    '''
    if x_sigma is None:
        x_sigma = x
    y = computation_graph_linear(x,w,b)
    v = computation_graph_heteroscedastic_variance(x_sigma,w_sigma,b_sigma)
    return y, v

## function that implements the full computational graph of the heteroscedastic Gaussian model with a softplus mean link
def computation_graph_heteroscedastic_gaussian_softplus(x,w,b,w_sigma,b_sigma,x_sigma=None):
    '''
    This function represents the heteroscedastic Gaussian model with a positive (softplus) mean
    and a log-variance model, ie t | x ~ N(softplus(x@w+b), exp(x_sigma@w_sigma+b_sigma)).
    Assumes regression R^D -> R (single output): w has shape (D,1), w_sigma has shape (D_sigma,1);
    b,b_sigma have shape (1,1).
    x_sigma are the features fed into the variance model; defaults to x (same features as the
    mean model) if not given, but can be a different (eg basis-expanded) feature matrix.
    Returns the mean y and the per-point variance v.
    '''
    if x_sigma is None:
        x_sigma = x
    y = computation_graph_softplus(x,w,b)
    v = computation_graph_heteroscedastic_variance(x_sigma,w_sigma,b_sigma)
    return y, v

## function that initializes the values of a computational graph
def create_computation_graph_linear(n_in,n_out, mean = 0, std = 1):
    ''' Create elements of the computational graph'''
    # parameters
    w = np.random.randn(n_in,n_out) # get a random value from standard normal distribution
    b = np.random.randn(n_out,1) + 1 # get a random value from Gaussian with mean 1 and standard deviation 1.

    w = w * std + mean
    b = b * std + mean

    return w,b

## function that initializes the values of a computational graph at the OLS solution
def create_computation_graph_linear_from_ols(x,t):
    '''
    Create elements of the computational graph, initialized at the OLS solution.
    Assumes regression R^D -> R (single output): x has shape (N,D), t has shape (N,1).
    '''
    # extend x with a column of ones to account for the bias
    x_ext = np.concatenate([x, np.ones((x.shape[0],1))], axis = 1)

    w_ext = fit_norm2_least_square(x_ext,t)

    w = w_ext[:-1]
    b = w_ext[-1:]

    return w,b

def grad_squared_loss_wrt_linear_model(x,t,w,b):
    """
    Assumes regression R^D -> R (single output): w has shape (D,1) and b has shape (1,1).
    """
    ## forward operation
    y = computation_graph_linear(x,w,b)

    ## backward operation (compute gradients / backpropagation / reverse mode autodiff)

    # dL/dy
    dL_dy = -2*(t-y)

    grad_w = np.transpose(np.sum(dL_dy*x, axis = 0, keepdims = True))
    grad_b = np.transpose(np.sum(dL_dy, axis = 0, keepdims = True))

    return grad_w, grad_b

def grad_absolute_loss_wrt_linear_model(x,t,w,b):
    """
    Assumes regression R^D -> R (single output): w has shape (D,1) and b has shape (1,1).

    For absolute value |t-y|, define the derivative as:

     1 if t > y
     0 if t = y
    -1 if t < y

    """
    ## forward operation
    y = computation_graph_linear(x,w,b)

    ## backward operation (compute gradients / backpropagation / reverse mode autodiff)

    # dL/dy
    diff = t - y
    dL_dy = np.ones(y.shape)
    dL_dy[diff < 0] = -1
    dL_dy[diff == 0] = 0

    dL_dy *= -1

    grad_w = np.transpose(np.sum(dL_dy*x, axis = 0, keepdims = True))
    grad_b = np.transpose(np.sum(dL_dy, axis = 0, keepdims = True))

    return grad_w, grad_b

def grad_student_t_loss_wrt_linear_model(x,t,w,b,nu,sigma2=1):
    """
    Assumes regression R^D -> R (single output): w has shape (D,1) and b has shape (1,1).
    nu (degrees of freedom) is required, sigma2 (scale) defaults to 1.
    """
    ## forward operation
    y = computation_graph_linear(x,w,b)

    ## backward operation (compute gradients / backpropagation / reverse mode autodiff)

    # dL/dy
    diff = t-y
    dL_dy = -2*diff / (nu*sigma2 + diff**2)

    grad_w = np.transpose(np.sum(dL_dy*x, axis = 0, keepdims = True))
    grad_b = np.transpose(np.sum(dL_dy, axis = 0, keepdims = True))

    return grad_w, grad_b

def grad_heteroscedastic_loss_wrt_linear_model(x,t,w,b,w_sigma,b_sigma,only_sigma=False,x_sigma=None):
    """
    Gradients of the heteroscedastic Gaussian negative log-likelihood wrt the mean model
    (w,b) and the log-variance model (w_sigma,b_sigma).

    Assumes regression R^D -> R (single output): w has shape (D,1), w_sigma has shape (D_sigma,1);
    b,b_sigma have shape (1,1). Mean is x@w+b, per-point variance is exp(x_sigma@w_sigma+b_sigma).
    x_sigma are the features fed into the variance model; defaults to x if not given.

    If only_sigma=True, only the gradients wrt (w_sigma,b_sigma) are computed and returned
    (used by Algorithm 2, where (w,b) instead gets the exact update from fit_ols_heteroscedastic).
    """
    if x_sigma is None:
        x_sigma = x

    ## forward operation
    y, v = computation_graph_heteroscedastic_gaussian(x,w,b,w_sigma,b_sigma,x_sigma=x_sigma)
    a = t - y

    ## backward operation (compute gradients / backpropagation / reverse mode autodiff)

    # dL/dz, with z = x_sigma@w_sigma+b_sigma. Theory notebook gives
    # nabla_wvecsigma = Xt @ diag(v) @ (v_inv - v_inv*v_inv*a*a); the diag(v) is what multiplies
    # v_inv and v_inv*v_inv elementwise, and diag(v)@v_inv=1, diag(v)@(v_inv*v_inv)=v_inv,
    # so it simplifies to:
    v_inv = 1./v
    dL_dz = 1 - a*a*v_inv

    grad_w_sigma = np.transpose(np.sum(dL_dz*x_sigma, axis = 0, keepdims = True))
    grad_b_sigma = np.transpose(np.sum(dL_dz, axis = 0, keepdims = True))

    if only_sigma:
        return grad_w_sigma, grad_b_sigma

    # dL/dy
    dL_dy = -2*a/v

    grad_w = np.transpose(np.sum(dL_dy*x, axis = 0, keepdims = True))
    grad_b = np.transpose(np.sum(dL_dy, axis = 0, keepdims = True))

    return grad_w, grad_b, grad_w_sigma, grad_b_sigma

def grad_heteroscedastic_loss_wrt_softplus_model(x,t,w,b,w_sigma,b_sigma,only_sigma=False,x_sigma=None):
    """
    Gradients of the heteroscedastic Gaussian negative log-likelihood wrt the mean model
    (w,b), now with a softplus link (positive mean), and the log-variance model (w_sigma,b_sigma).

    Assumes regression R^D -> R (single output): w has shape (D,1), w_sigma has shape (D_sigma,1);
    b,b_sigma have shape (1,1). Mean is softplus(x@w+b), per-point variance is exp(x_sigma@w_sigma+b_sigma).
    x_sigma are the features fed into the variance model; defaults to x if not given.

    The w_sigma,b_sigma gradient is identical to grad_heteroscedastic_loss_wrt_linear_model (it only
    depends on the residual a=t-y, not on how y was computed). The w,b gradient picks up an extra
    dy/dz=sigmoid(z) factor from the softplus link. There is no exact coordinate update for (w,b)
    here (the softplus link breaks the weighted-OLS closed form used by fit_ols_heteroscedastic),
    so both (w,b) and (w_sigma,b_sigma) must be fit by gradient descent.

    If only_sigma=True, only the gradients wrt (w_sigma,b_sigma) are computed and returned.
    """
    if x_sigma is None:
        x_sigma = x

    ## forward operation
    z = computation_graph_linear(x,w,b)
    y = activation_function_softplus(z)
    v = computation_graph_heteroscedastic_variance(x_sigma,w_sigma,b_sigma)
    a = t - y

    ## backward operation (compute gradients / backpropagation / reverse mode autodiff)

    # dL/dz_sigma, with z_sigma = x_sigma@w_sigma+b_sigma (see grad_heteroscedastic_loss_wrt_linear_model)
    v_inv = 1./v
    dL_dz_sigma = 1 - a*a*v_inv

    grad_w_sigma = np.transpose(np.sum(dL_dz_sigma*x_sigma, axis = 0, keepdims = True))
    grad_b_sigma = np.transpose(np.sum(dL_dz_sigma, axis = 0, keepdims = True))

    if only_sigma:
        return grad_w_sigma, grad_b_sigma

    # dL/dy, then chain through dy/dz = sigmoid(z) (derivative of softplus)
    dL_dy = -2*a/v
    dy_dz = activation_function_sigmoid(z)
    dL_dz = dL_dy*dy_dz

    grad_w = np.transpose(np.sum(dL_dz*x, axis = 0, keepdims = True))
    grad_b = np.transpose(np.sum(dL_dz, axis = 0, keepdims = True))

    return grad_w, grad_b, grad_w_sigma, grad_b_sigma

def grad_bce_loss_wrt_sigmoid_model(x,t,w,b):
    """
    Applies chain rule.
    """
    ## forward operation
    z = computation_graph_linear(x,w,b)
    y = activation_function_sigmoid(z)

    ## backward operation (compute gradients / backpropagation / reverse mode autodiff)
    idx_0 = t==0
    idx_1 = ~idx_0

    dL_dy = np.zeros(y.shape)

    # dL/dy. 1e-12 is added/substracted for stability on +-inf values
    dL_dy[idx_0] = - 1/(1-y[idx_0])
    dL_dy[idx_1] = 1/y[idx_1]
    dL_dy[dL_dy == np.inf] = 1e12
    dL_dy[dL_dy == -np.inf] = -1e12

    dL_dy *= -1

    # dy/dz
    dy_dz = activation_function_sigmoid(z)*(1-activation_function_sigmoid(z))

    grad_w = np.transpose(np.sum(dL_dy*dy_dz*x, axis = 0, keepdims = True))
    grad_b = np.transpose(np.sum(dL_dy*dy_dz, axis = 0, keepdims = True))

    return grad_w, grad_b


def grad_brier_loss_wrt_sigmoid_model(x,t,w,b):
    """
    Applies chain rule.
    """
    ## forward operation
    z = computation_graph_linear(x,w,b)
    y = activation_function_sigmoid(z)

    ## backward operation (compute gradients / backpropagation / reverse mode autodiff)

    # dL/dy
    dL_dy = -2*(t-y)

    # dy/dz
    dy_dz = activation_function_sigmoid(z)*(1-activation_function_sigmoid(z))

    grad_w = np.transpose(np.sum(dL_dy*dy_dz*x, axis = 0, keepdims = True))
    grad_b = np.transpose(np.sum(dL_dy*dy_dz, axis = 0, keepdims = True))

    return grad_w, grad_b


def grad_squared_loss_wrt_relu_model(x,t,w,b):
    """
    Applies chain rule.

    For ReLU dy/dz, define the derivative as:

     1 if z > 0
     0 if z <= 0

    """
    ## forward operation
    z = computation_graph_linear(x,w,b)
    y = activation_function_relu(z)

    ## backward operation (compute gradients / backpropagation / reverse mode autodiff)

    # dL/dy
    dL_dy = -2*(t-y)

    # dy/dz
    dy_dz = np.zeros(z.shape)
    dy_dz[z > 0] = 1

    grad_w = np.transpose(np.sum(dL_dy*dy_dz*x, axis = 0, keepdims = True))
    grad_b = np.transpose(np.sum(dL_dy*dy_dz, axis = 0, keepdims = True))

    return grad_w, grad_b


def grad_squared_loss_wrt_softplus_model(x,t,w,b):
    """
    Applies chain rule.
    """
    ## forward operation
    z = computation_graph_linear(x,w,b)
    y = activation_function_softplus(z)

    ## backward operation (compute gradients / backpropagation / reverse mode autodiff)

    # dL/dy
    dL_dy = -2*(t-y)

    # dy/dz. Derivative of softplus is the sigmoid.
    dy_dz = activation_function_sigmoid(z)

    grad_w = np.transpose(np.sum(dL_dy*dy_dz*x, axis = 0, keepdims = True))
    grad_b = np.transpose(np.sum(dL_dy*dy_dz, axis = 0, keepdims = True))

    return grad_w, grad_b


def grad_squared_loss_wrt_exponential_model(x,t,w,b):
    """
    Applies chain rule.
    """
    ## forward operation
    z = computation_graph_linear(x,w,b)
    y = activation_function_exponential(z)

    ## backward operation (compute gradients / backpropagation / reverse mode autodiff)

    # dL/dy
    dL_dy = -2*(t-y)

    # dy/dz. Derivative of exp(z) is exp(z) itself, i.e. y.
    dy_dz = y

    grad_w = np.transpose(np.sum(dL_dy*dy_dz*x, axis = 0, keepdims = True))
    grad_b = np.transpose(np.sum(dL_dy*dy_dz, axis = 0, keepdims = True))

    return grad_w, grad_b


def fit_norm2_least_square(X,T, lam = 0):

    # Obtain optimum model
    XtX = np.transpose(X) @ X
    Xty = np.transpose(X) @ T

    XtX += lam * np.eye(XtX.shape[0])

    # withouth regularization
    w_opt = np.linalg.solve(XtX, Xty)

    return w_opt

def fit_ols_heteroscedastic(x,t,w_sigma,b_sigma,x_sigma=None):
    """
    Closed-form weighted least squares update for the mean model (w,b), given a fixed
    log-variance model (w_sigma,b_sigma): the exact coordinate update in Algorithm 2.
    Weights are 1/exp(x_sigma@w_sigma+b_sigma), ie the inverse of the per-point variance.

    Assumes regression R^D -> R (single output): x has shape (N,D), t has shape (N,1);
    w_sigma has shape (D_sigma,1), b_sigma has shape (1,1).
    x_sigma are the features fed into the variance model; defaults to x if not given.
    """
    if x_sigma is None:
        x_sigma = x

    v_inv = 1. / computation_graph_heteroscedastic_variance(x_sigma,w_sigma,b_sigma)

    # extend x with a column of ones to account for the bias
    x_ext = np.concatenate([x, np.ones((x.shape[0],1))], axis = 1)

    x_ext_w = x_ext * v_inv
    XtWX = np.transpose(x_ext_w) @ x_ext
    XtWT = np.transpose(x_ext_w) @ t

    w_ext = np.linalg.solve(XtWX, XtWT)

    w_new = w_ext[:-1]
    b_new = w_ext[-1:]

    return w_new, b_new

def step_student_t_least_square(x,t,w,b,nu,sigma2=1):
    """
    EM Algorithm (coincides with IRLS (Iteratively Reweighted Least Squares))
    for the Student-t likelihood. Performs a single step (E step + M step).

    Assumes regression R^D -> R (single output): w has shape (D,1) and b has shape (1,1).
    nu (degrees of freedom) is required, sigma2 (scale) defaults to 1.

    E step computes the expected precision weights, pi_n, from the residuals
    of the current fit; M step updates the model by solving the induced
    weighted least squares problem.
    """
    ## forward operation
    y = computation_graph_linear(x,w,b)

    ## E step: expected precision weights given the current residuals
    r = t-y
    pi = 1 / (nu*sigma2 + r**2)

    ## M step: weighted least squares update

    # extend x with a column of ones to account for the bias
    x_ext = np.concatenate([x, np.ones((x.shape[0],1))], axis = 1)

    x_ext_w = x_ext * pi
    XtWX = np.transpose(x_ext_w) @ x_ext
    XtWT = np.transpose(x_ext_w) @ t

    w_ext = np.linalg.solve(XtWX, XtWT)

    w_new = w_ext[:-1]
    b_new = w_ext[-1:]

    return w_new, b_new
