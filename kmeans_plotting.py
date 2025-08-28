import time
import copy
from IPython.display import display, Video
from io import BytesIO
import os

import numpy as np

import matplotlib.pyplot as plt
import imageio.v2 as imageio

from kmeans import assign_data_to_centroids, kmeans_loss_function

# todo: move to ABC
class PlotterBase:
    def show_plot(self):
        self.fig.canvas.draw()    
        self.fig.canvas.flush_events()
        time.sleep(self.sleep_time)

    def save_video_frame(self):
        buf = BytesIO()
        self.fig.savefig(buf, format="png", dpi=100)

        buf.seek(0)
        frame = imageio.imread(buf) 
        self.writer.append_data(frame)
        
    def show_video(self):
        if self.video_filename is not None:
            display(Video(data=self.video_filename, embed=True))
            os.remove(self.video_filename)
            
    def close_plot(self):
        if self.interactive_plot:
            plt.close(self.fig)
        
    def close_video(self):
        if self.video:
            self.writer.close()     
            
        if not self.interactive_plot:
            plt.close(self.fig)
                         
class Plot1DKmeans(PlotterBase):
    def __init__(self, 
                 video:bool = False, 
                 interactive_plot = False, 
                 sleep_time: float = 0.1, 
                 draw_voronoi : bool = False,
                 loss_fun_optim : bool = False,
                 num_loss_fun_centroids_to_show : int = None,
                ):
        
        self.video = video
        self.interactive_plot = interactive_plot
        self.loss_fun_optim = loss_fun_optim
        self.voronoi = draw_voronoi
        
        if self.video or self.interactive_plot:
            num_row_plot = 1
            figsize = None
            if self.loss_fun_optim:
                self.num_loss_fun_centroids_to_show = num_loss_fun_centroids_to_show
                num_row_plot = 1 + num_loss_fun_centroids_to_show
                figsize = (10,10)
                
            fig, ax = plt.subplots(num_row_plot,2, figsize = figsize )
            
            # to match data structure when num_rows > 1
            if num_row_plot == 1:
                ax = [ax]
            
            # primera fila solo un dibujo
            ax_top = fig.add_subplot(num_row_plot, 1, 1)   
            ax[0][1].remove()               
            ax[0][0].remove()
            
            axs_list = [ax_top]
            
            self.fig = fig
            if num_row_plot == 1:
                self.ax = axs_list
            else:

                for i in range(1, num_row_plot):
                    axs_list.append([ax[i, 0], ax[i, 1]])

                self.ax = axs_list
                
            self.sleep_time = sleep_time
            
            if self.voronoi:
                # to predict with kmeans
                self.predictor = assign_data_to_centroids
                xx = np.linspace(-10, 10, 500)
                self.vor_grid_xx = np.reshape( xx, (xx.shape[0],1))
                
            if self.loss_fun_optim:
                xx = np.linspace(-10, 10, 500)
                self.loss_fun_grid = np.reshape(xx, (xx.shape[0],1) )
        
        # this should be done in a separate class instance.
        self.video_filename = None
        if self.video:
            # Create temporary file for video creation
            self.video_filename = "/tmp/aux.mp4"

            ## video writer
            self.writer = imageio.get_writer(self.video_filename, format="FFMPEG", mode="I", fps=1, codec="libx264")  
            
    def draw_initial_centroids(self,centroids,X):
        
        if self.interactive_plot or self.video:  
            self.ax[0].cla()
            self.ax[0].plot(X,np.zeros_like(X), 'x', color = 'k')

            for idx,cet in enumerate(centroids):
                self.ax[0].plot(cet,0.0, 'o', color = f'C{idx}')

            self.ax[0].set_title("Initial Centroids")     
            
            self.draw_voronoi(centroids)
            
            self.ax[0].legend()
            
        if self.interactive_plot:
            self.show_plot()
        
        if self.video:
            self.save_video_frame()

    def draw_cluster_assignments(self, centroids,X_assigned):
        
        if self.interactive_plot or self.video:  
            num_centroids = centroids.shape[0]

            self.ax[0].cla()

            for idx,cet in enumerate(centroids):
                label = ""
                if idx == 0:
                    label = "Centroid"

                self.ax[0].plot(cet,0.0, 'o', color = f'C{idx}', label = label)

            for _c in range(num_centroids):
                _X = X_assigned[_c]

                self.ax[0].plot(_X,np.zeros_like(_X), 'x',  color = f'C{_c}')
                self.ax[0].set_title("Centroids Assignment")

            self.draw_voronoi(centroids)
            
            self.ax[0].legend()

        if self.interactive_plot:
            self.show_plot()
        
        if self.video:
            self.save_video_frame()
            
    def draw_loss_function(self, X, centroids):

        if self.loss_fun_optim:
            
            if self.interactive_plot or self.video:                 
                
                # obtain loss function of current point
                centroids_assigned_true, X_assigned_true = self.predictor(X, centroids = centroids)
                loss_true = kmeans_loss_function(X, centroids = centroids, X_assigned = X_assigned_true)

                # to separate the cost function within the different assignments
                assigned_regions = {}

                # to keep loss
                loss_acc = {}
                loss_acc_convex = {}

                # to keep region colors
                region_colors = {}

                for cent2change in range(self.num_loss_fun_centroids_to_show):
                    
                    self.ax[cent2change+1][0].cla()
                    self.ax[cent2change+1][1].cla()
                    
                    ## to separate the cost function within the different assignments
                    assigned_regions[cent2change] = []

                    # to keep loss
                    loss_acc[cent2change] = []
                    loss_acc_convex[cent2change] = []
                    
                    # save centroids
                    centroids_run = copy.deepcopy(centroids)

                    # obtain loss function over grid within assignments
                    for _c in self.loss_fun_grid:
                        centroids_run[cent2change,:] = _c

                        centroids_assigned, X_assigned = self.predictor(X, centroids = centroids_run)

                        assigned_regions[cent2change].append(tuple(centroids_assigned))

                        # overlapped loss function
                        loss = kmeans_loss_function(X, centroids = centroids_run, X_assigned = X_assigned)
                        loss_acc[cent2change].append(loss)
                        
                        # convex loss function
                        loss = kmeans_loss_function(X, centroids = centroids_run, X_assigned = X_assigned_true)
                        loss_acc_convex[cent2change].append(loss)

                    unique_assignments = list(set(assigned_regions[cent2change]))
                    region_colors[cent2change] = [f"C{unique_assignments.index(a)}" for a in assigned_regions[cent2change]]
                    
                    ## ==================
                    ## Draw loss function
                    
                    # separate by colors
                    start = 0
                    for i in range(1, len(region_colors[cent2change])):
                        if region_colors[cent2change][i] != region_colors[cent2change][i-1]:
                            self.ax[cent2change+1][0].plot(self.loss_fun_grid[start:i+1], loss_acc[cent2change][start:i+1], color=region_colors[cent2change][i-1])
                            start = i
                        
                    ## Sometimes that exact cluster assignment is not available, probably because the grid is not
                    #  big enough
                    try:
                        color = f"C{unique_assignments.index(tuple(centroids_assigned_true))}"
                    except:
                        color = 'k'
                        
                    self.ax[cent2change+1][1].plot(self.loss_fun_grid, loss_acc_convex[cent2change], color = color)

                    ## ========================================================================================
                    ## Draw current part of the loss function within the location of the corresponding centroid
                    self.ax[cent2change+1][0].plot(centroids[cent2change],loss_true,'x', color = 'k', markersize = 5)
                    self.ax[cent2change+1][1].plot(centroids[cent2change],loss_true,'x', color = 'k', markersize = 5)
                    
                    self.ax[cent2change+1][0].set_xlabel(f"Centroid {cent2change}")
                    self.ax[cent2change+1][1].set_xlabel(f"Centroid {cent2change}")
                
            if self.interactive_plot:
                self.show_plot()

            if self.video:
                self.save_video_frame()
    
    def draw_loss_at_given_centroids(self, X, centroids, centroids_new):
        if self.loss_fun_optim:
            
            if self.interactive_plot or self.video:                 
                
                for cent2change in range(self.num_loss_fun_centroids_to_show):
                    
                    centroids_run = copy.deepcopy(centroids)
                    
                    # check the updated centroid goes into the optimal place of the loss function
                    centroids_run[cent2change] = centroids_new[cent2change]
                    
                    # obtain loss function of current point
                    centroids_assigned, X_assigned = self.predictor(X, centroids = centroids_run)
                    loss_true = kmeans_loss_function(X, centroids = centroids_run, X_assigned = X_assigned)

                    ## ========================================================================================
                    ## Draw current part of the loss function within the location of the corresponding centroid
                    self.ax[cent2change+1][0].plot(centroids_run[cent2change],loss_true,'x', color = 'gray', markersize = 5)
                    self.ax[cent2change+1][1].plot(centroids_run[cent2change],loss_true,'x', color = 'gray', markersize = 5)

            if self.interactive_plot:
                self.show_plot()

            if self.video:
                self.save_video_frame()

    def draw_new_centroids(self,centroids, voronoi_regions = None):

        if self.interactive_plot or self.video:  
            for idx,cet in enumerate(centroids):
                label = ""
                if idx == 0:
                    label = "New centroid"

                self.ax[0].plot(cet,0.0, '*', color = f'C{idx}', markersize = 20, label = label)

            self.ax[0].set_title("New Centroids")
            self.draw_voronoi(centroids, colors = 'gray')
            
            self.ax[0].legend()

        if self.interactive_plot:
            self.show_plot()
        
        if self.video:
            self.save_video_frame()
            
    def draw_loss(self,loss):
        
        if self.interactive_plot or self.video:  
            self.ax[0].set_title(f"Loss {loss :.3f}")

        if self.interactive_plot:
            self.show_plot()
        
        if self.video:
            self.save_video_frame()
            
    def draw_voronoi(self, centroids, colors = 'k'):
        if self.voronoi:
            voronoi_regions, _ = self.predictor(self.vor_grid_xx , centroids)
            voronoi_regions_limits = np.where(np.diff(voronoi_regions) != 0)[0] + 1

            for c in voronoi_regions_limits:
                self.ax[0].axvline(self.vor_grid_xx[c], color=colors, linestyle="--")
                
class Plot2DKmeans(PlotterBase):
    
    def __init__(self, 
                 video:bool = False, 
                 interactive_plot = False, 
                 sleep_time: float = 0.1, 
                 draw_voronoi : bool = False,
                 loss_fun_optim : bool = False,
                 num_loss_fun_centroids_to_show : int = None
                ):
        
        self.video = video
        self.interactive_plot = interactive_plot
        self.loss_fun_optim = loss_fun_optim
        self.voronoi = draw_voronoi

        if self.video or self.interactive_plot:
            num_row_plot = 1
            figsize = None
            if self.loss_fun_optim:
                self.num_loss_fun_centroids_to_show = num_loss_fun_centroids_to_show
                num_row_plot = 1 + num_loss_fun_centroids_to_show
                figsize = (10,20)
                
            fig, ax = plt.subplots(num_row_plot,2, figsize = figsize )
            
            # to match data structure when num_rows > 1
            if num_row_plot == 1:
                ax = [ax]
            
            # primera fila solo un dibujo
            ax_top = fig.add_subplot(num_row_plot, 1, 1)   
            ax[0][1].remove()               
            ax[0][0].remove()
            
            axs_list = [ax_top]
            
            self.fig = fig
            if num_row_plot == 1:
                self.ax = axs_list
            else:
                for i in range(1, num_row_plot):
                    axs_list.append([ax[i, 0], ax[i, 1]])

                self.ax = axs_list
                
            self.sleep_time = sleep_time
            
            if self.voronoi:
                # to predict with kmeans
                self.predictor = assign_data_to_centroids
                xx, yy = np.meshgrid(
                            np.linspace(-1, 1, 500),
                            np.linspace(-1, 1, 500)
                        )

                self.vor_grid_xx = xx
                self.vor_grid_yy = yy
        
            if self.loss_fun_optim:
                self.loss_N_grid = 100
                xx, yy = np.meshgrid(
                            np.linspace(-1.2, 1.2, self.loss_N_grid),
                            np.linspace(-1.2, 1.2, self.loss_N_grid)
                        )
                
                self.loss_fun_grid_xx = xx
                self.loss_fun_grid_yy = yy
                self.loss_fun_grid = np.hstack((np.reshape(xx, (self.loss_N_grid**2,1)),np.reshape(yy, (self.loss_N_grid**2,1))))

        
            # this should be done in a separate class instance.
            self.video_filename = None
            if self.video:
                # Create temporary file for video creation
                self.video_filename = "/tmp/aux.mp4"

                ## video writer
                self.writer = imageio.get_writer(self.video_filename, format="FFMPEG", mode="I", fps=1, codec="libx264")  

    def draw_initial_centroids(self,centroids,X):
        
        if self.interactive_plot or self.video:  
            self.ax[0].cla()
            self.ax[0].plot(X[:,0],X[:,1], 'x', color = 'k')

            for idx,cet in enumerate(centroids):
                self.ax[0].plot(cet[0],cet[1], 'o', color = f'C{idx}')

            self.ax[0].set_title("Initial Centroids")     
            
            self.draw_voronoi(centroids)
            
            self.ax[0].legend()
            
        if self.interactive_plot:
            self.show_plot()
        
        if self.video:
            self.save_video_frame()

    def draw_cluster_assignments(self, centroids,X_assigned):
        
        if self.interactive_plot or self.video:  
            num_centroids = centroids.shape[0]

            self.ax[0].cla()

            for idx,cet in enumerate(centroids):
                label = ""
                if idx == 0:
                    label = "Centroid"

                self.ax[0].plot(cet[0],cet[1], 'o', color = f'C{idx}', label = label)

            for _c in range(num_centroids):
                _X = X_assigned[_c]

                self.ax[0].plot(_X[:,0],_X[:,1], 'x',  color = f'C{_c}')
                self.ax[0].set_title("Centroids Assignment")

            self.draw_voronoi(centroids)
            
            self.ax[0].legend()

        if self.interactive_plot:
            self.show_plot()
        
        if self.video:
            self.save_video_frame()
            
    def draw_new_centroids(self,centroids, voronoi_regions = None):

        if self.interactive_plot or self.video:  
            for idx,cet in enumerate(centroids):
                label = ""
                if idx == 0:
                    label = "New centroid"

                self.ax[0].plot(cet[0],cet[1], '*', color = f'C{idx}', markersize = 20, label = label)

            self.ax[0].set_title("New Centroids")
            self.draw_voronoi(centroids, colors = 'gray')
            
            self.ax[0].legend()

        if self.interactive_plot:
            self.show_plot()
        
        if self.video:
            self.save_video_frame()
            
    def draw_loss(self,loss):
        
        if self.interactive_plot or self.video:  
            self.ax[0].set_title(f"Loss {loss :.3f}")

        if self.interactive_plot:
            self.show_plot()
        
        if self.video:
            self.save_video_frame()
            
    def draw_voronoi(self, centroids, colors = 'k'):
        if self.voronoi:
            voronoi_regions, _ = self.predictor(
                np.c_[self.vor_grid_xx.ravel(), self.vor_grid_yy.ravel()], centroids
            )

            voronoi_regions = np.reshape(voronoi_regions,self.vor_grid_xx.shape)
            self.ax[0].contour(self.vor_grid_xx, self.vor_grid_yy, voronoi_regions, colors=colors, linewidths=1)
            
    def draw_loss_function(self, X, centroids):

        if self.loss_fun_optim:
            
            if self.interactive_plot or self.video:  
                
                # obtain loss function of current point
                centroids_assigned_true, X_assigned_true = self.predictor(X, centroids = centroids)
                loss_true = kmeans_loss_function(X, centroids = centroids, X_assigned = X_assigned_true)

                # to separate the cost function within the different assignments
                assigned_regions = {}

                # to keep loss
                loss_acc = {}
                loss_acc_convex = {}

                # to keep region colors
                region_colors = {}

                ## ====================
                ## Parameter to vary ##
                ## There are eight combination
                for cent2change in range(self.num_loss_fun_centroids_to_show):
                    
                    self.ax[cent2change+1][0].cla()
                    self.ax[cent2change+1][1].cla()

                    # to keep loss
                    loss_acc[cent2change] = []
                    loss_acc_convex[cent2change] = []
                    
                    # save centroids
                    centroids_run = copy.deepcopy(centroids)

                    # obtain loss function over grid within assignments
                    for _c in self.loss_fun_grid:
                        centroids_run[cent2change,:] = _c

                        centroids_assigned, X_assigned = self.predictor(X, centroids = centroids_run)

                        # overlapped loss function
                        loss = kmeans_loss_function(X, centroids = centroids_run, X_assigned = X_assigned)
                        loss_acc[cent2change].append(loss)
                        
                        # convex loss function
                        loss = kmeans_loss_function(X, centroids = centroids_run, X_assigned = X_assigned_true)
                        loss_acc_convex[cent2change].append(loss)
                        
                
                    loss_acc_mesh = np.reshape(np.array(loss_acc[cent2change]), (self.loss_N_grid,self.loss_N_grid))
                    loss_acc_convex_mesh = np.reshape(np.array(loss_acc_convex[cent2change]), (self.loss_N_grid,self.loss_N_grid))

                    self.ax[cent2change+1][0].contourf(
                        self.loss_fun_grid_xx, 
                        self.loss_fun_grid_yy, 
                        loss_acc_mesh, 
                        cmap = plt.cm.get_cmap("Oranges")
                    )
                   
                    self.ax[cent2change+1][1].contourf(
                        self.loss_fun_grid_xx, 
                        self.loss_fun_grid_yy, 
                        loss_acc_convex_mesh, 
                        cmap = plt.cm.get_cmap("Oranges")
                    )
                    
               
                    ## ===================================================================================
                    ## Draw current part of the loss function within the location of the corresponding centroid
                    self.ax[cent2change+1][0].plot(centroids[cent2change][0],centroids[cent2change][1],'x', color = 'k', markersize = 10)
                    self.ax[cent2change+1][1].plot(centroids[cent2change][0],centroids[cent2change][1],'x', color = 'k', markersize = 10)


                ## ==============================
                ## Label axis and title and so on
                self.ax[cent2change][0].set_title(f"Centroid {cent2change}")

                self.ax[cent2change][0].set_xlabel(f"Coordinate {0}")
                self.ax[cent2change][0].set_ylabel(f"Coordinate {1}")
                self.ax[cent2change][1].set_xlabel(f"Coordinate {0}")
                self.ax[cent2change][1].set_ylabel(f"Coordinate {1}")
               
            
            if self.interactive_plot:
                self.show_plot()

            if self.video:
                self.save_video_frame()
    
    def draw_loss_at_given_centroids(self, X, centroids, centroids_new):
        if self.loss_fun_optim:
            
            if self.interactive_plot or self.video:                 
                
                for cent2change in range(self.num_loss_fun_centroids_to_show):
                    # we are not 3d plotting hence no loss computation is needed

                    ## ========================================================================================
                    ## Draw current part of the loss function within the location of the corresponding centroid
                    self.ax[cent2change+1][0].plot(centroids_new[cent2change][0],centroids_new[cent2change][1],'x', color = 'gray', markersize = 10)
                    self.ax[cent2change+1][1].plot(centroids_new[cent2change][0],centroids_new[cent2change][1],'x', color = 'gray', markersize = 10)

            if self.interactive_plot:
                self.show_plot()

            if self.video:
                self.save_video_frame()    
