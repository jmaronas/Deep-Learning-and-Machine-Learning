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
def squared_loss_function(t,y):
    return (t-y)**2

brier_loss_function = squared_loss_function

def absolute_loss_function(t,y):
    return np.abs(t-y)

## funciton implementing binary cross entropy
def bce_loss_function(t,y, clip = None):
    idx_0 = t==0
    idx_1 = ~idx_0

    loss = np.zeros(y.shape)

    loss[idx_1] = np.log(y[idx_1])
    loss[idx_0] = np.log(1-y[idx_0])

    ## add +- 1e12 for numerical stability on infs
    if isinstance(clip,float):
        loss[loss == np.inf] = 1e12
        loss[loss == -np.inf] = -1e12

    return - loss

## function implementing an activation function
def activation_function_linear(x):
    return x

## activation function sigmoid
def activation_function_sigmoid(x):
    return 1. / (1. + np.exp(-x))

## function that implements the computational graph
def computation_graph_linear(x,w,b):
    ''' This function represents a computational graph, a neural network, that implements a linear operation'''
    # this is the W^0 x from the theory above implemented using a transposition ;)
    y = activation_function_linear(np.matmul(x,w) + b)
    return y

## function that implements the computational graph
def computation_graph_sigmoid(x,w,b):
    ''' This function represents a computational graph, a neural network, that implements a linear operation'''
    # this is the W^0 x from the theory above implemented using a transposition ;)
    y = activation_function_sigmoid(np.matmul(x,w) + b)
    return y

## function that initializes the values of a computational graph
def create_computation_graph_linear(n_in,n_out):
    ''' Create elements of the computational graph'''
    # parameters
    w = np.random.randn(n_in,n_out) # get a random value from standard normal distribution
    b = np.random.randn(n_out,) + 1 # get a random value from Gaussian with mean 0 and standard deviation 5.

    return w,b

def grad_squared_loss_wrt_linear_model(x,t,w,b):
    ## forward operation
    y = computation_graph_linear(x,w,b)

    ## backward operation (compute gradients / backpropagation / reverse mode autodiff)

    # dL/dy
    dL_dy = -2*(t-y)

    grad_w = np.sum(dL_dy*x, axis = 0, keepdims = True)
    grad_b = np.sum(dL_dy, axis = 0, keepdims = True)

    return grad_w, grad_b

def grad_absolute_loss_wrt_linear_model(x,t,w,b):
    """
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

    grad_w = np.sum(dL_dy*x, axis = 0, keepdims = True)
    grad_b = np.sum(dL_dy, axis = 0, keepdims = True)

    return grad_w, grad_b
