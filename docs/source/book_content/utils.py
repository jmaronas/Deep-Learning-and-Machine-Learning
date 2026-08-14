import numpy as np
from scipy.special import digamma, gammaln
from scipy.optimize import brentq
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
## only the part that depends on w,b (valid for optimizing over w,b with sigma2,nu fixed):
## drops the (nu+1)/2 factor, the log(sigma) term and the log-Gamma constants, since none of
## them depend on w,b and therefore do not change where the loss is minimized wrt w,b
def student_t_loss_function(t,y,nu,sigma2=1,*args):
    return np.log(1 + (t-y)**2 / (nu*sigma2))

## full negative log-likelihood of the Student-t model, including the sigma2 and nu dependent
## terms dropped by student_t_loss_function; needed to track the loss when sigma2 and/or nu
## are also being optimized (e.g. joint gradient descent on w,b,sigma2,nu)
def student_t_full_loss_function(t,y,nu,sigma2,*args):
    r = t-y
    return (-gammaln((nu+1)/2) + gammaln(nu/2) + 0.5*np.log(nu*np.pi) + 0.5*np.log(sigma2)
            + (nu+1)/2*np.log(1 + r**2/(nu*sigma2)))

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

## function implementing categorical cross entropy (multiclass generalization of BCE)
def categorical_crossentropy_loss_function(t,y, clip = None,*args):
    '''
    t,y have shape (N,K): t is one-hot (one row per point, a 1 in the true class, 0 elsewhere),
    y is a predicted probability vector per point (e.g. the output of a softmax). Returns the
    per-point loss, shape (N,1).
    '''
    log_y = np.log(y)

    ## add +- 1e12 for numerical stability on infs, same convention as bce_loss_function
    if isinstance(clip,float):
        log_y[log_y == np.inf] = clip
        log_y[log_y == -np.inf] = -clip

    return -np.sum(t*log_y, axis=1, keepdims=True)

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

## activation function softmax
def activation_function_softmax(z):
    '''
    Row-wise softmax. z has shape (N,K); returns y with shape (N,K), each row summing to 1.
    Subtracts the row-wise max before exponentiating for numerical stability (does not
    change the result, since softmax is invariant to adding the same constant to every
    logit in a row).
    '''
    z_shift = z - np.max(z, axis=1, keepdims=True)
    exp_z = np.exp(z_shift)
    return exp_z / np.sum(exp_z, axis=1, keepdims=True)

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
def computation_graph_softmax(x,w,b):
    '''
    This function represents a computational graph, a neural network, that implements a
    linear operation followed by a Softmax link.
    Assumes classification R^D -> K classes: x has shape (N,D), w has shape (D,K), and,
    unlike every other computation_graph_* above, b has shape (1,K) rather than (K,1)
    (we need it to broadcast against the (N,K) result of x@w, one bias per class, not
    one bias per sample). Returns y with shape (N,K), each row a probability vector.
    '''
    z = np.matmul(x,w) + b
    return activation_function_softmax(z)

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

def grad_student_t_loss_wrt_linear_model(x,t,w,b,nu,sigma2,only_sigma=False,only_nu=False):
    """
    Assumes regression R^D -> R (single output): w has shape (D,1) and b has shape (1,1).
    nu (degrees of freedom) and sigma2 (scale) are both required.

    Returns the gradients of the negative log-likelihood wrt w,b (grad_w,grad_b), sigma2
    (grad_sigma2) and nu (grad_nu), reusing the residual r=t-y and denom=nu*sigma2+r**2
    across all of them instead of recomputing the forward pass for each parameter.

    If only_sigma=True, only grad_sigma2 is computed and returned (used when w,b instead
    gets the EM/IRLS step from step_student_t_least_square, and sigma is updated by a
    Generalized EM gradient step). If only_nu=True, only grad_nu is computed and returned.
    """
    N = x.shape[0]

    ## forward operation
    y = computation_graph_linear(x,w,b)

    ## shared terms
    r = t-y
    denom = nu*sigma2 + r**2
    sum_r2_over_denom = np.sum(r**2/denom)

    if only_sigma:
        grad_sigma2 = (N - (nu+1)*sum_r2_over_denom) / (2*sigma2)
        return grad_sigma2

    if only_nu:
        grad_nu = (-0.5*N*digamma((nu+1)/2) + 0.5*N*digamma(nu/2) + N/(2*nu)
                   + 0.5*np.sum(np.log(1 + r**2/(nu*sigma2)))
                   - (nu+1)/(2*nu)*sum_r2_over_denom)
        return grad_nu

    ## backward operation (compute gradients / backpropagation / reverse mode autodiff)

    # dL/dy
    dL_dy = -2*r / denom

    grad_w = np.transpose(np.sum(dL_dy*x, axis = 0, keepdims = True))
    grad_b = np.transpose(np.sum(dL_dy, axis = 0, keepdims = True))

    grad_sigma2 = (N - (nu+1)*sum_r2_over_denom) / (2*sigma2)

    grad_nu = (-0.5*N*digamma((nu+1)/2) + 0.5*N*digamma(nu/2) + N/(2*nu)
               + 0.5*np.sum(np.log(1 + r**2/(nu*sigma2)))
               - (nu+1)/(2*nu)*sum_r2_over_denom)

    return grad_w, grad_b, grad_sigma2, grad_nu

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
    x_sigma are the features fed into the variance model; defaults to x if not given. This allows, for instancce
    using x to parameterize the mean and an different set of basis to parameterize x_sigma.

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


def grad_categorical_crossentropy_loss_wrt_softmax_model(x,t,w,b):
    """
    Applies chain rule. x has shape (N,D), t (one-hot) and y have shape (N,K),
    w has shape (D,K), b has shape (1,K) (see computation_graph_softmax).

    The softmax Jacobian dy/dz is not diagonal (every y_k depends on every z_j), and
    neither is the loss's own dL/dy; but exactly as for BCE, the two combine and
    collapse into the same clean residual, dL/dz = y-t (derived in the theory notebook).
    """
    ## forward operation
    y = computation_graph_softmax(x,w,b)

    ## backward operation (compute gradients / backpropagation / reverse mode autodiff)

    # dL/dz, already simplified (see above)
    dL_dz = y-t

    grad_w = np.matmul(np.transpose(x), dL_dz)
    grad_b = np.sum(dL_dz, axis = 0, keepdims = True)

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

def student_t_e_step(x,t,w,b,nu,sigma2):
    """
    E step of the EM/ECME algorithm for the Student-t likelihood: computes the exact
    expected precision weight, pi_n = E[tau_n] = (nu+1)*sigma2/(nu*sigma2+r_n**2), from
    the Gaussian scale-mixture representation of the Student-t, given the current
    (w,b,nu,sigma2). Computed once per iteration and reused, unchanged, by the three
    M-steps below (student_t_m_step_w, student_t_m_step_sigma2, student_t_m_step_nu).

    While computation of r could be reused by the m_step for sigma2 I have prefer to keep it
    separately for clarity.

    Assumes regression R^D -> R (single output): w has shape (D,1) and b has shape (1,1).
    """
    y = computation_graph_linear(x,w,b)
    r = t-y
    return (nu+1)*sigma2 / (nu*sigma2 + r**2)

def student_t_m_step_w(x,t,pi):
    """
    Coordinate M-step for w,b: weighted least squares using the E-step weight pi
    (student_t_e_step), holding sigma2 and nu fixed.
    """
    # extend x with a column of ones to account for the bias
    x_ext = np.concatenate([x, np.ones((x.shape[0],1))], axis = 1)

    x_ext_w = x_ext * pi
    XtWX = np.transpose(x_ext_w) @ x_ext
    XtWT = np.transpose(x_ext_w) @ t

    w_ext = np.linalg.solve(XtWX, XtWT)

    w_new = w_ext[:-1]
    b_new = w_ext[-1:]

    return w_new, b_new

def student_t_m_step_sigma2(x,t,w,b,pi):
    """
    Coordinate M-step for sigma2: weighted average of the squared residuals, reusing
    the very same E-step weight pi (student_t_e_step) used by student_t_m_step_w, not
    recomputed. (w,b) here are the freshly updated values from student_t_m_step_w, so
    the residual reflects the latest w,b while pi stays frozen at its E-step value.
    """
    y = computation_graph_linear(x,w,b)
    r = t-y
    return np.mean(pi * r**2)

def student_t_nu_score(nu,x,t,w,b,sigma2):
    """
    Left-hand side of Equation (30) in Liu and Rubin (1995) (the ECME CM-step for nu,
    specialized to our univariate, fully-observed regression case), rewritten in terms
    of the E-step weight pi_n(nu)=(nu+1)*sigma2/(nu*sigma2+r_n**2). Its unique root in
    nu (the function is strictly monotonic, see the "Optimizing wrt nu" notebook cell)
    is the M-step update for nu, given (w,b,sigma2) fixed. Used internally by
    student_t_m_step_nu; unlike the other two M-steps, this one has to recompute the
    weight itself, at every candidate nu tried during the search.
    """
    pi = student_t_e_step(x,t,w,b,nu,sigma2)
    return (digamma((nu+1)/2) - digamma(nu/2) + 1 + np.log(nu/(nu+1))
            + np.mean(np.log(pi) - pi))

def student_t_m_step_nu(x,t,w,b,sigma2,bracket=(1e-3,1000.0)):
    """
    Coordinate M-step for nu: unlike student_t_m_step_w and student_t_m_step_sigma2
    (which maximize the frozen-weight Q-function), this one maximizes the actual
    log-likelihood directly, given (w,b,sigma2) fixed; solved via Brent's method on
    student_t_nu_score.
    """
    return brentq(student_t_nu_score, bracket[0], bracket[1], args=(x,t,w,b,sigma2))
