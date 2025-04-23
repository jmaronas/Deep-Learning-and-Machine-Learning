# Coupled Systems of First Order Linear Differential Equations

We might be interested in systems of ordinary differential equations, and how to solve them. A coupled system of first order linear differential equations is a system of equations involving 0 and first derivative, linear terms and where the equations are coupled since changes in one term involve changes in the other equations. Let's see how we can solve them.

Consider the coupled system given by:
$$
\begin{cases}
\frac{d x(t)}{dt} &= y(t) - x(t)\\
\frac{d y(t)}{dt} &= x(t) - y(t)\\
\end{cases}
$$
with initial conditions $x(t_0), y(t_0)$

## Direct method option 1

The direct method I came with is a nightmare and I am not sure if there are better ways of arriving at this, since, to be honest, most of the things I have found so far use the follow up techniques to solve these systems of differential equations.

We can start by looking at each of the differential equations from the system, separately.

From:
$$
\frac{d x(t)}{dt} &= y(t) - x(t)\\
$$
we recognize a non-homogeneous differential equation with $F=-1$; $L=1$; $C=0$ and $w(t) = y(t)$. The solution is.
$$
x(t) = e^{-(t-t_0)}x(t_0) + \int^t_{t_0} e^{-(t-\tau)}y(\tau) d\tau
$$
However, the solution is still coupled since it depends on the form of $y(\tau)$ which is unkown. If we solve the other differential equation:
$$
\frac{d y(t)}{dt} &= x(t) - y(t)\\
$$
with the same terms as above gives:
$$
y(t) = e^{-(t-t_0)}y(t_0) + e^{-t}\int^t_{t_0} e^\tau x(\tau) d\tau
$$
We can now substitute one of the solutions into the other yielding:
$$
y(t) = e^{-(t-t_0)}y(t_0) + e^{-t}\int^t_{t_0} e^\tau \left[e^{-(\tau-t_0)}x(t_0) +  e^{-\tau}\int^\tau_{\tau_0} e^{-\tau'}y(\tau') d\tau'\right] d\tau\\
%
%
y(t) = e^{-(t-t_0)}y(t_0) + e^{-t}\int^t_{t_0} e^\tau e^{-(\tau-t_0)}x(t_0)d\tau + e^{-t}\int^t_{t_0} e^\tau  e^{-\tau}\int^\tau_{\tau_0} e^{-\tau'}y(\tau') d\tau'd\tau\\
%
%
y(t) = e^{-(t-t_0)}y(t_0) + e^{-t}\int^t_{t_0} e^{t_0}x(t_0)d\tau + e^{-t}\int^t_{t_0} \int^\tau_{\tau_0} e^{-\tau'}y(\tau') d\tau'd\tau\\
%
%
y(t) = e^{-(t-t_0)}y(t_0) + e^{-t+t_0}x(t_0)(t-t_0) + e^{-t}\int^t_{t_0} \int^\tau_{\tau_0} e^{-\tau'}y(\tau') d\tau'd\tau\\
$$
I might have make small errors because haven¡t double check properly reason. However, I am not particularly interested in solving the equation through this form. We will now continue subsituting $y(\tau')$. And this has remembered me what we see in [1] around equations 2.12 to 2.15. So it looks like this will end up in a series that is the Taylor expansion of the function giving the solutions I am going to calculate later. I am not sure this will end up in that, but it looks like we end up in a very similar proceedure. In any case, this method of solving the system is not interesting.



## Direct method option 2

See https://resource.download.wjec.co.uk/vtc/2018-19/wjec18-19_1.3/eng/coupled-differential-equations-unit-4.pdf



## Sustitution or change of variables

Sustitution works by finding a function that simplifies the system. In this case the following sustitution will decouple the system.
$$
c(t) = x(t)-y(t)\\
c(t_0) = x(t_0)-y(t_0)\\
$$
we can take derivative on both sides yielding:
$$
\frac{d c(t)}{dt} &= \frac{d x(t)}{dt} - \frac{d y(t)}{dt}\\
$$
since from the system we know the expressions for $\frac{d y(t)}{dt}$ and $\frac{d x(t)}{dt}$ we can substitute them.
$$
\begin{split}
\frac{d c(t)}{dt} &= y(t) - x(t) - x(t) + y(t)\\
\frac{d c(t)}{dt} &= 2y(t) - 2x(t) \\
\frac{d c(t)}{dt} &= -2c \\
\end{split}
$$
yielding a decoupled system since know the differential equation only depends on itself. We recognize an homogeneous time invariant ODE with $F = -2$ solution:
$$
c(t) = e^{-2(t-t_0)}c(t_0)
$$
Once we have solved $c(t)$ we need to recover back both $x(t)$ and $y(t)$. Using the fact that: $c(t) = x(t)-y(t)$ we know that:
$$
x(t)-y(t) = c(t) \\
\frac{d y(t)}{dt} = e^{-2(t-t_0)}c(t_0) = e^{2t_0}c(t_0)e^{-2t}
$$
which can be recognized as a non homogeneous ODE with $F=0$, $C=0$, $L=c(t_0)e^{2t_0}$ and $w(t) = e^{-2t}$. The solution is thus:
$$
y(t) = y(t_0) + c(t_0)e^{2t_0}\int^t_{t_0} e^{-2\tau} d\tau;\\
y(t) = y(t_0) + c(t_0)e^{2t_0}\frac{1}{-2}\left[e^{-2t}-e^{-2t_0}\right];\\
y(t) = y(t_0) -\frac{1}{2}c(t_0)\left[e^{-2(t-t_0)}-1\right];\\
y(t) = y(t_0) + \frac{1}{2}c(t_0)\left[1-e^{-2(t-t_0)}\right];\\
$$
Finally substituting initial condition $c(t_0) = x(t_0)-y(t_0)$, yields:
$$
y(t) = y(t_0) + \frac{1}{2}\left[x(t_0)-y(t_0)\\\right]\left[1-e^{-2(t-t_0)}\right];\\
y(t) = y(t_0) + \left[\frac{1}{2}x(t_0)-\frac{1}{2}y(t_0)\\\right]\left[1-e^{-2(t-t_0)}\right];\\
y(t) = y(t_0) + \frac{1}{2}x(t_0)-\frac{1}{2}y(t_0) -\frac{1}{2}x(t_0)e^{-2(t-t_0)} +\frac{1}{2}y(t_0)e^{-2(t-t_0)};\\
y(t) = \frac{1}{2}y(t_0) + \frac{1}{2}y(t_0)e^{-2(t-t_0)}+\frac{1}{2}x(t_0) -\frac{1}{2}x(t_0)e^{-2(t-t_0)};\\
$$
We now solve for $x(t)$ to show how different option yield different ways to arrive at the same solution, with different complexity.

#### Solving for x(t) option 1 (super easy)

Using the fact that $c(t) = x(t) - y(t)$, we know that $x(t) = c(t) + y(t)$.  Since we know $c(t)$ and $y(t)$ we can substitute. This yields:
$$
x(t) = c(t) + y(t) \\
x(t) = c(t_0)e^{-2(t-t_0)} + \frac{1}{2}y(t_0) + \frac{1}{2}y(t_0)e^{-2(t-t_0)}+\frac{1}{2}x(t_0) -\frac{1}{2}x(t_0)e^{-2(t-t_0)}; \\
x(t) = \left[x(t_0) - y(t_0)\right]e^{-2(t-t_0)} + \frac{1}{2}y(t_0) + \frac{1}{2}y(t_0)e^{-2(t-t_0)} + \frac{1}{2}x(t_0)  - \frac{1}{2}x(t_0)e^{-2(t-t_0)};\\
x(t) = x(t_0)e^{-2(t-t_0)}  - y(t_0)e^{-2(t-t_0)} + \frac{1}{2}y(t_0) + \frac{1}{2}y(t_0)e^{-2(t-t_0)} + \frac{1}{2}x(t_0)  - \frac{1}{2}x(t_0)e^{-2(t-t_0)};\\
x(t) = \frac{1}{2}x(t_0)e^{-2(t-t_0)}  - \frac{1}{2}y(t_0)e^{-2(t-t_0)} + \frac{1}{2}y(t_0)  + \frac{1}{2}x(t_0) ;
$$


So the solution to the system gives:
$$
\mathbf{y(t) = \frac{1}{2}y(t_0) + \frac{1}{2}y(t_0)e^{-2(t-t_0)}+\frac{1}{2}x(t_0) -\frac{1}{2}x(t_0)e^{-2(t-t_0)};}\\
\mathbf{x(t) = \frac{1}{2}x(t_0) +\frac{1}{2}x(t_0)e^{-2(t-t_0)} +\frac{1}{2}y(t_0) - \frac{1}{2}y(t_0)e^{-2(t-t_0)};}
$$
where the only reason to using bold notation is to highlight the solution.



#### Solving for x(t) option 2 (easy)

Once $c(t)$ is solved, we could use the fact that $c(t) = x(t)-y(t)$  is true, in a different way. Rather than noting that:
$$
\frac{d y(t)}{dt} &= x(t) - y(t)\\
\frac{d y(t)}{dt} &= c(t)\\
$$
we could use the fact that:
$$
\frac{d x(t)}{dt} &= y(t) - x(t)\\
\frac{d x(t)}{dt} &= -c(t)\\
\frac{d x(t)}{dt} &= -e^{-2(t-t_0)}c(t_0)\\
$$
which is basically the same differential equation we solved in step above but noting that  $F=0$, $C=0$, $L=-c(t_0)e^{2t_0}$ and $w(t) = e^{-2t}$. The solution is thus, the same as above but changing the sign of the term on the rightest part of the equation:
$$
x(t) = x(t_0) - c(t_0)e^{2t_0}\int^t_{t_0} e^{-2\tau} d\tau;\\
x(t) = x(t_0) - \frac{1}{2}c(t_0)\left[1-e^{-2(t-t_0)}\right];\\
$$
substituting initial conditions yields:
$$
x(t) = x(t_0) - \frac{1}{2}c(t_0)\left[1-e^{-2(t-t_0)}\right];\\
x(t) = x(t_0) - \frac{1}{2}\left[x(t_0) - y(t_0)\right]\left[1-e^{-2(t-t_0)}\right];\\
$$
which again is very similarly solve by considering that just one sign is changing:
$$
x(t) = x(t_0) - \frac{1}{2}x(t_0)+\frac{1}{2}y(t_0) +\frac{1}{2}x(t_0)e^{-2(t-t_0)} -\frac{1}{2}y(t_0)e^{-2(t-t_0)};\\
x(t) = \frac{1}{2}x(t_0) +\frac{1}{2}x(t_0)e^{-2(t-t_0)} +\frac{1}{2}y(t_0) - \frac{1}{2}y(t_0)e^{-2(t-t_0)} ;\\
$$
So the solution to the system gives:
$$
\mathbf{y(t) = \frac{1}{2}y(t_0) + \frac{1}{2}y(t_0)e^{-2(t-t_0)}+\frac{1}{2}x(t_0) -\frac{1}{2}x(t_0)e^{-2(t-t_0)};}\\
\mathbf{x(t) = \frac{1}{2}x(t_0) +\frac{1}{2}x(t_0)e^{-2(t-t_0)} +\frac{1}{2}y(t_0) - \frac{1}{2}y(t_0)e^{-2(t-t_0)};}
$$
where the only reason to using bold notation is to highlight the solution.

#### Solving for x(t) option 3 (you'll better take a beer)

Once we have solved for $y(t)$ we can substitute into $\frac{d x(t)}{dt} = y(t) - x(t)$ and solve the resulting differential equation. This gives:
$$
\frac{d x(t)}{dt} =  y(t_0) + \frac{1}{2}c(t_0)\left[1-e^{-2(t-t_0)}\right] - x(t);\\
$$
where I have substitute $y(t)$ without substituting $c(t_0)$ to lighten the initial number of terms considered. Note that we could reorganize this equation as follows:
$$
\frac{d x(t)}{dt} =  y(t_0) + \frac{1}{2}c(t_0) -\frac{1}{2}c(t_0)e^{2t_0}e^{-2t} - x(t);\\
$$
which we recognize as linear time invariant inhomogeneous ode with: $C =  y(t_0) + \frac{1}{2}c(t_0)$, $L=-\frac{1}{2}c(t_0)e^{2t_0}$, $w(t) = e^{-2t}$  and $F = -1$. We know the solution to this ODE is given by:
$$
x(t) = x(t_0)e^{F(t-t_0)} + \int^{t}_{t_0} e^{F(t-\tau)}\left[Lw(\tau) + C\right]d \tau;\\
%
%
x(t) = x(t_0)e^{t_0-t} + \int^{t}_{t_0} e^{\tau-t}\left[-\frac{1}{2}c(t_0)e^{2t_0}e^{-2\tau} + C\right]d \tau;\\
%
%
x(t) = x(t_0)e^{t_0-t} -\frac{1}{2}c(t_0)e^{2t_0-t}\int^{t}_{t_0}e^{-\tau}d\tau+Ce^{-t}\int^t_{t_0} e^{\tau}d\tau;
$$
 We now solve each integral separately:
$$
-\frac{1}{2}c(t_0)e^{2t_0-t}\int^{t}_{t_0}e^{-\tau}d\tau = \frac{1}{2}c(t_0)\left[e^{2t_0-2t} - e^{t_0-t}\right]
$$
and
$$
Ce^{-t}\int^t_{t_0} e^{\tau}d\tau = C e^{-t}\left[e^t - e^{t_0}\right] = C \left[1-e^{t_0-t}\right]
$$
Substituting back into the solution for $x(t)$ and substituting initial condition $c(t_0)$ we have:
$$
x(t) = x(t_0)e^{t_0-t} +\frac{1}{2}c(t_0)\left[e^{2t_0-2t} - e^{t_0-t}\right]+  C \left[1-e^{t_0-t}\right];\\
x(t) = x(t_0)e^{t_0-t} +\frac{1}{2}\left[x(t_0) - y(t_0)\right]\left[e^{2t_0-2t} - e^{t_0-t}\right]+ \left[ y(t_0) + \frac{1}{2}x(t_0) - \frac{1}{2}y(t_0)\right] \left[1-e^{t_0-t}\right];\\
%
%
x(t) = \cancel{x(t_0)e^{t_0-t}} +\frac{1}{2}x(t_0)e^{2t_0-2t} -\frac{1}{2}y(t_0)e^{2t_0-2t}  \cancel{-\frac{1}{2}x(t_0) e^{t_0-t}} +\cancel{\frac{1}{2}y(t_0)e^{t_0-t}} + y(t_0) + \frac{1}{2}x(t_0) - \frac{1}{2}y(t_0) \cancel{-y(t_0)e^{t_0-t}} \cancel{-\frac{1}{2}x(t_0)e^{t_0-t}} + \cancel{\frac{1}{2}y(t_0)e^{t_0-t}};\\
%
%
x(t) = \frac{1}{2}x(t_0) +\frac{1}{2}x(t_0)e^{2(t_0-t)} + \frac{1}{2}y(t_0) -\frac{1}{2}y(t_0)e^{2(t_0-t)}\\
%
%
x(t) = \frac{1}{2}x(t_0) +\frac{1}{2}x(t_0)e^{-2(t-t_0)} + \frac{1}{2}y(t_0) -\frac{1}{2}y(t_0)e^{-2(t-t_0)}
$$
So the final solution is given as always:
$$
\mathbf{y(t) = \frac{1}{2}y(t_0) + \frac{1}{2}y(t_0)e^{-2(t-t_0)}+\frac{1}{2}x(t_0) -\frac{1}{2}x(t_0)e^{-2(t-t_0)};}\\
\mathbf{x(t) = \frac{1}{2}x(t_0) +\frac{1}{2}x(t_0)e^{-2(t-t_0)} +\frac{1}{2}y(t_0) - \frac{1}{2}y(t_0)e^{-2(t-t_0)};}
$$


## Linear Algebra

It turns out that we can compute the solution to a system of differential equations, using linear algebra. The idea is to express the system using matrices (as commonly done with normal systems) and by diagonalizing the matrix we can end up in a change of variables that provides a system of decoupled differential equations. These differential equations end up being simple homogeneous equations so there is no need to start solving convolutions and so on, as we have previously done.

Note that since we can define the vector $z(t)=[x(t),y(t)]^T$ . Then, the system:
$$
\begin{cases}
\frac{d x(t)}{dt} &= y(t) - x(t)\\
\frac{d y(t)}{dt} &= x(t) - y(t)\\
\end{cases}
$$
can be rewritten as:
$$
\frac{d z(t)}{dt} = A z(t) \\
$$
with:
$$
A = \begin{pmatrix}
-1 & 1 \\
1 & -1
\end{pmatrix}
$$
The initial conditions are now $z(t_0)=[x(t_0),y(t_0)]^T$ 

### Diagonalizing A

We can write $A = PDP^{-1}$

where $D$ is a diagonal matrix where each element in the diagonal is an eigenvalue of $A$, and $P$ is a matrix with columns given by the eigenvectors.

##### Computing eigenvalues $\lambda_i$

The eigenvalues are obtained by solving:
$$
\det(A-\lambda I) = 0\\
\det\begin{pmatrix}
-1 - \lambda & 1 \\
1 & -1 - \lambda
\end{pmatrix} = 0 \\
(-1-\lambda)^2 - 1 = 0\\
1 +2\lambda + \lambda^2 -1 = 0\\
\lambda(\lambda+2)=0
$$
So the eigenvalues are $\lambda_1=-2$ and $\lambda_2=0$

##### Computing eigenvectors $\lambda_i$

Eigenvectors $v_i$ are those who solve $Av_i=\lambda_i v_i$

For the first eigenvalue $\lambda_1 = -2$ the eigenvector $v_1$ is obtained by:
$$
\begin{pmatrix}
-1 & 1 \\
1 & -1
\end{pmatrix}
\begin{pmatrix}
v_{11} \\
v_{12}
\end{pmatrix} = 
%
%
-2 \begin{pmatrix}
v_{11} \\
v_{12}
\end{pmatrix}
$$

$$
\begin{cases}
-v_{11} + v_{12} &= -2v_{11} \\
v_{11}-v_{12} &= -2v_{12} 
\end{cases}
$$

which gives: $v_{11} = -v_{12}$ in both equations. So the associated eigenvector is $v_1 = [1,-1]^T$

For the other eigenvalue it can be shown in a similar way that the eigenvector is given by $v_2 = [1,1]^T$ 

So $A=PDP^{-1}$ can be written as:
$$
\begin{pmatrix}
-1 & 1 \\
1 & -1
\end{pmatrix} = 
\begin{pmatrix}
1 & 1 \\
-1 & 1
\end{pmatrix}
\begin{pmatrix}
-2 & 0 \\
0 & 0
\end{pmatrix}
\frac{1}{2}\begin{pmatrix}
1 & -1 \\
1 & 1
\end{pmatrix}
$$
In other words we have:


$$
P = \begin{pmatrix}
1 & 1 \\
-1 & 1
\end{pmatrix}\\
D = \begin{pmatrix}
-2 & 0 \\
0 & 0
\end{pmatrix}\\
P^{-1}=\frac{1}{2}\begin{pmatrix}
1 & -1 \\
1 & 1
\end{pmatrix}
$$


### Turning a coupled system into a decoupled one

Once we have express $A$ in terms of a diagonal matrix, we note that the system can be rewritten as:
$$
\frac{d z(t)}{dt} = A z(t) \\
\frac{d z(t)}{dt} =  PDP^{-1}z(t) \\
\frac{d P^{-1}z(t)}{dt} = DP^{-1}z(t) \\
$$
if we know make the change of variables $u(t) = P^{-1}z(t)$. We end up having:
$$
\frac{d u(t)}{dt} = Du(t) \\
$$
It is clear that $u(t)$ is a vector with the same number of components as $z(t)$. This is easily shown by noting that:
$$
u(t) = \frac{1}{2}\begin{pmatrix}
1 & -1 \\
1 & 1
\end{pmatrix}
\begin{pmatrix}
z_1(t)\\
z_2(t)
\end{pmatrix}\\
=\frac{1}{2}\begin{pmatrix}
1 & -1 \\
1 & 1
\end{pmatrix}
\begin{pmatrix}
x(t)\\
y(t)
\end{pmatrix}
$$
So the change of variables in terms of $x(t)$ and $y(t)$, which are our variables of interest is given by:
$$
u_1(t) = \frac{1}{2}\left(x(t) - y(t)\right)\\
u_2(t) = \frac{1}{2}\left(x(t) + y(t)\right)\\
$$
So noting that $u(t)$ is a vector valued function of two dimensions, the system of differential equations is given by:
$$
\begin{pmatrix}
\frac{d u_1(t)}{dt} \\
\frac{d u_2(t)}{dt} 
\end{pmatrix} = \begin{pmatrix}
-2 & 0 \\
0 & 0
\end{pmatrix}\begin{pmatrix}
u_1(t) \\
u_2(t)\end{pmatrix}
$$
Which gives the system:
$$
\begin{cases}
\frac{d u_1(t)}{dt} = -2 u_1(t) \\
\frac{d u_2(t)}{dt} = 0 u_2(t) \\
\end{cases}
$$
We have know two decoupled differential equations. The 0 multiplying $u_2(t)$ is to make clear that the solution is just the initial condition. Now, since these differential equations are homogeneous with $F = -2$ and $F = 0$, and assuming initial conditions $u_1(t_0)$, and $u_2(t_0)$, we have:
$$
u_1(t) = u_1(t_0)e^{-2(t-t_0)}\\
u_2(t) = u_2(t_0)\cancelto{1}{e^{0(t-t_0)}}\\
$$

##### Removing the change of variables

To return to the solution in terms of $z(t)= [x(t),y(t)]^T$ we revert the change of variables $u(t) = P^{-1}z(t)$ to get $z(t)$ in terms of $u(t)$. To do so, since $Pu(t)=z(t)$ we have:
$$
\begin{pmatrix}
1 & 1 \\
-1 & 1
\end{pmatrix}\begin{pmatrix}u_1(t) \\ u_2(t)\end{pmatrix} = 
\begin{pmatrix}
u_1(t) + u_2(t)\\ 
-u_1(t) + u_2(t)
\end{pmatrix} = z(t) = 
\begin{pmatrix}
x(t)\\
y(t)
\end{pmatrix} 
$$
So we have:


$$
x(t) = u_1(t) + u_2(t) = u_1(t_0)e^{-2(t-t_0)} + u_2(t_0)\\
y(t) = -u_1(t) + u_2(t) = -u_1(t_0)e^{-2(t-t_0)} + u_2(t_0)
$$

##### Setting up initial conditions.

To get the initial conditions, we need to obtain $u(t_0)$  from $z(t_0)$ to replace in the solution. So now instead of getting $z(t)$ from $u(t)$ as we have just done to get the solution, we need the opposite.

The change of variables applies to initial conditions as well, which means: $u(t) = P^{-1}z(t)$. This implies: $u(t_0) = P^{-1}z(t_0)$, which is an operation I have done above to justify the dimensionality of $u(t)$. So:
$$
u(t_0) = \frac{1}{2}\begin{pmatrix}
1 & -1 \\
1 & 1
\end{pmatrix}
z(t_0)\\
=\frac{1}{2}\begin{pmatrix}
1 & -1 \\
1 & 1
\end{pmatrix}
\begin{pmatrix}
x(t_0)\\
y(t_0)
\end{pmatrix}
$$

$$
u_1(t_0) = \frac{1}{2}\left(x(t_0) - y(t_0)\right)\\
u_2(t_0) = \frac{1}{2}\left(x(t_0) + y(t_0)\right)\\
$$

##### Solution

$$
\begin{split}
x(t) &= \frac{1}{2}\left(x(t_0) - y(t_0)\right)e^{-2(t-t_0)} +  \frac{1}{2}\left(x(t_0) + y(t_0)\right)\\
%
%
&=\frac{1}{2}x(t_0) + \frac{1}{2}y(t_0) + \frac{1}{2}x(t_0)e^{-2(t-t_0)} - \frac{1}{2}y(t_0)e^{-2(t-t_0)} \\
%
%
&= \frac{1}{2}x(t_0) + \frac{1}{2}x(t_0)e^{-2(t-t_0)}  + \frac{1}{2}y(t_0) - \frac{1}{2}y(t_0)e^{-2(t-t_0)}
\end{split}
$$




$$
\begin{split}
y(t) &=-u_1(t_0)e^{-2(t-t_0)} + u_2(t_0) \\
&= -\frac{1}{2}\left(x(t_0) - y(t_0)\right)e^{-2(t-t_0)} + \frac{1}{2}\left(x(t_0) + y(t_0)\right)\\
%
%
&= \frac{1}{2}x(t_0) + \frac{1}{2}y(t_0) -\frac{1}{2}x(t_0)e^{-2(t-t_0)} + \frac{1}{2} y(t_0)e^{-2(t-t_0)} \\
%
%
&=  \frac{1}{2}y(t_0) + \frac{1}{2} y(t_0)e^{-2(t-t_0)} + \frac{1}{2}x(t_0) -\frac{1}{2}x(t_0)e^{-2(t-t_0)}  \\
\end{split}
$$
In summary we have:
$$
\mathbf{y(t) = \frac{1}{2}y(t_0) + \frac{1}{2}y(t_0)e^{-2(t-t_0)}+\frac{1}{2}x(t_0) -\frac{1}{2}x(t_0)e^{-2(t-t_0)};}\\
\mathbf{x(t) = \frac{1}{2}x(t_0) +\frac{1}{2}x(t_0)e^{-2(t-t_0)} +\frac{1}{2}y(t_0) - \frac{1}{2}y(t_0)e^{-2(t-t_0)};}
$$
Recovering the same solutions as we have been recovering in all cases.

# References

[1] https://users.aalto.fi/~asolin/sde-book/sde-book.pdf
