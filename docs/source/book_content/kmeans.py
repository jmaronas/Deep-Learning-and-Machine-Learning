import numpy as np
import copy

def assign_data_to_centroids(X, centroids):
    """
    Assigns data X to centroids.
    """
    num_centroids = centroids.shape[0]

    ## compute distance to centroids
    dist = np.sum((X[:,np.newaxis] - centroids)**2,axis=-1)

    ## assign the centroid with lowest distance
    centroids_assigned = np.argmin(dist, axis = -1)

    ## separate data X by assigned centroid
    X_assigned = {}

    for _c in range(num_centroids):
        _x_assign = X[centroids_assigned == _c]
        X_assigned[_c] = _x_assign

    return centroids_assigned, X_assigned

def kmeans_loss_function(X, centroids, X_assigned):
        
    num_centroids = centroids.shape[0]

    loss = 0.0
    for _c in range(num_centroids):
        loss += np.sum((centroids[_c] - X_assigned[_c])**2)

    return loss

class Kmeans:
    def __init__(self, num_centroids : int, plotter = None):
        self.num_centroids = num_centroids
        
        self._run_plotter = True
        if plotter is None:
            self._run_plotter = False
            
        self._plotter = plotter
      
    @property
    def centroids(self):
        return copy.deepcopy(self._centroids)
    
    def _assign_data_to_centroids(self,X, centroids = None):
        """
        Assigns data X to centroids.
        """
        
        if centroids is None:
            centroids = self._centroids
        
        ## compute distance to centroids
        dist = np.sum((X[:,np.newaxis] - centroids)**2,axis=-1)
        
        ## assign the centroid with lowest distance
        centroids_assigned = np.argmin(dist, axis = -1)
        
        ## separate data X by assigned centroid
        X_assigned = {}
        
        for _c in range(self.num_centroids):
            _x_assign = X[centroids_assigned == _c]
            X_assigned[_c] = _x_assign
        
        return centroids_assigned, X_assigned
    
    def _get_new_centroids(self,X):
        centroids_assigned, X_assigned = self._assign_data_to_centroids(X)   
                
        for _c in range(self.num_centroids):           
            _x_assign = X_assigned[_c]
            # if no data then keep old centroid
            if _x_assign.size != 0:
                self._centroids[_c] = np.mean(X_assigned[_c], axis = 0)
                
        return centroids_assigned, X_assigned
            
    def run_iter(self,X):
        return self._get_new_centroids(X)
        
    def run(self,X, num_iters, seed = None):
        
        self.initialize_centroids(X, seed = seed)
        
        for itet in range(num_iters):
            print(f"Running iteration {itet}", end = "\r")
            centroids_old = copy.deepcopy(self.centroids)
            
            centroids_assigned, X_assigned = self.run_iter(X)

            loss = self.loss_function(X, X_assigned = X_assigned)
            
            ## plot 
            if self._run_plotter:
                self._plotter.draw_cluster_assignments(centroids_old,X_assigned)
                self._plotter.draw_loss_function(X, centroids_old)
                self._plotter.draw_new_centroids(self._centroids)
                self._plotter.draw_loss_at_given_centroids(X, centroids_old, self._centroids)
                self._plotter.draw_loss(loss)
            
            print(f"Running iteration {itet} loss {loss:.3f}")

            if np.all(self.centroids == centroids_old):
                break
                
        if self._run_plotter:
            self._plotter.close_video()
                
    def initialize_centroids(self,X, seed = None):
        if seed is not None:
            np.random.seed(seed)
        
        # we start by chosing randomly from X.
        centroids_idx = np.random.randint(0, X.shape[0], size=self.num_centroids)
        
        self._centroids = X[centroids_idx]
        
        if self._run_plotter:
            self._plotter.draw_initial_centroids(self._centroids, X )
            
        return self._centroids
    
    def loss_function(self, X, centroids = None, X_assigned = None):
        
        if centroids is None:
            centroids = self.centroids
            num_centroids = self.num_centroids
        else:
            num_centroids = centroids.shape[0]
        
        if X_assigned is None:
            _, X_assigned = self._assign_data_to_centroids(X, centroids = centroids)
        
        loss = 0.0
        for _c in range(num_centroids):
            loss += np.sum((centroids[_c] - X_assigned[_c])**2)
            
        return loss

