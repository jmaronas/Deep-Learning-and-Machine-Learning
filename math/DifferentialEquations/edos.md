# First order Linear Differential Equations

Since I have started to learn differential equations, here are my notes and exercises. I am focusing on first order linear differential equations since these are the ones I am interested in for the things  I have in mind.

With any loss of generality, beyond changing exponentials for matrix exponentials, we will be assuming vector valued functions, i.e,  we could either have $y : \mathbb{R} \rightarrow \mathbb{R^d}$ or $y : \mathbb{R^n} \rightarrow \mathbb{R^d}$, although for exposition we will be thinking always on functions from the time domain. I like to make time dependence explicit.

## Homogeneous

An homogeneous ode is given by:


$$
\begin{split}
\frac{d y(t)}{d t} &= Fy(t);\\
y(t_0) &= \alpha
\end{split}
$$


where $F$ is an element (scalar, matrix, etc) that does not depend on time and $C$ is any constant value.

The solution to this ODE can be obtained by the method of variable separation and the solution is given by:


$$
y(t) = e^{F(t-t_0)}y(t_0)
$$

## Non Homogeneous ODE

A non-homogeneus ODE is given by:


$$
\begin{split}
\frac{d y(t)}{d t} &= Fy(t) + L w(t) + C;\\
y(t_0) &= \alpha
\end{split}
$$


where $L$ is similar to $F$ and does not depend on time. $C$ denotes a constant and $w$ is any other function of time.

The solution can be obtained by the method of integrating factor, and is given by:


$$
y(t) = e^{F(t-t_0)}y(t_0) + \int^t_{t_0} e^{F(t-\tau)} \left[L w(\tau) + C \right] d\tau;
$$


Note that here the solution has an integral given by the convolution between two signals, and is the reason why Linear Time Invariant systems use the convolution to obtain the output, something I was taught as: "this is like this because I say it" rather than giving out the real reasons. Obviously I need to elaborate further on this claim to show where this really come true for any convolution.

## Homogeneous Time Variant ODE

An homogeneous time variant ODE is given by:


$$
\begin{split}
\frac{d y(t)}{d t} &= F(t)y(t) ;\\
y(t_0) &= \alpha
\end{split}
$$


with solution given by:




$$
y(t) = \Psi(t,t_0) y(t_0)
$$


where the function $\Psi$ must satisfy some properties see the book from Arno Solin equation 2.34.

## Non Homogeneous Time Variant ODE

$$
\begin{split}
\frac{d y(t)}{d t} &= F(t)y(t) + L(t) w(t);\\
y(t_0) &= \alpha
\end{split}
$$

with solution given by:


$$
y(t) = \Psi(t,t_0)y(t_0) + \int^t_{t_0} \Psi(t,\tau) L w(\tau)d\tau;
$$

## Special cases

We can have several special cases from the above solutions that are useful for direct plug in. 

First note that a non-homogeneous ode generalizes homogeneous ode. Basically the solution is the homogeneous one plus the fluctuations introduced by the other function through a convolution. So in other words if we set $L=0$  and $C=0$ we recover the homogeneous solution.

#### Case L = 0

$$
\begin{split}\frac{d y(t)}{d t} &= Fy(t) + C;\\
y(t_0) &= \alpha\end{split}
$$



The solution is:




$$
\begin{split}
&y(t) = e^{F(t-t_0)}y(t_0) + \int^t_{t_0} e^{F(t-\tau)}  C d\tau;\\
&y(t) = e^{F(t-t_0)}y(t_0) -\frac{C}{F}\left[1-e^{F(t-t_0)}\right]
\end{split}
$$

### Case F = 0

$$
\begin{split}
\frac{d y(t)}{d t} &= Lw(t) + C;\\
y(t_0) &= \alpha
\end{split}
$$



The solution is:




$$
\begin{split}
&y(t) = y(t_0) + \int^t_{t_0} \left[L w(\tau) + C \right] d\tau;\\
&y(t) = y(t_0) + C(t-t_0) + L \int^t_{t_0} w(\tau)d\tau;
\end{split}
$$
