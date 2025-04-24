# Solving First order Linear Differential Equations

### Integrating factor method to solve ODE

This method of integration can be used to construct the solution to an non-homogeneous ODE.


$$
\begin{split}
\frac{d y(t)}{d t} &= Fy(t) + L w(t);\\
\frac{d y(t)}{d t} - Fy(t) &=  L w(t);\\
\end{split}
$$


Multiply both sides by the integrating factor given by:


$$
\begin{split}
e^{\int -Fdt} = e^{-Ft}\\
e^{-Ft}\frac{d y(t)}{d t} - e^{-Ft}Fy(t) &=   e^{-Ft} L w(t);\\
\end{split}
$$



Note that the left hand side is the derivative of a product. Namely:


$$
\frac{d e^{-Ft}y(t)}{dt} = e^{-Ft}\frac{d y(t)}{d t} - Fe^{-Ft}y(t)
$$


So we can write:


$$
\begin{split}
\frac{d e^{-Ft}y(t)}{dt} &=   e^{-Ft} L w(t);\\
\int^t_{t_0}\frac{d e^{-F\tau}y(\tau)}{d\tau}d\tau &=  \int^t_{t_0} e^{-F\tau} L w(\tau)d\tau;\\
\end{split}
$$


Since the integral of the derivative is the argument itself we have:


$$
\begin{split}
&\int^t_{t_0}\frac{d e^{-F\tau}y(\tau)}{d\tau}d\tau =  \int^t_{t_0} e^{-F\tau} L w(\tau)d\tau;\\
&e^{-Ft}y(t) - e^{-Ft_0}y(t_0) = \int^t_{t_0} e^{-F\tau} L w(\tau)d\tau;\\
&e^{Ft}\left( e^{-Ft}y(t) \right) = e^{Ft}\left( e^{-Ft_0}y(t_0) + \int^t_{t_0} e^{-F\tau} L w(\tau)d\tau;\right)\\
&y(t) = e^{F(t-t_0)}y(t_0) + e^{Ft}\int^t_{t_0} e^{-F\tau} L w(\tau)d\tau;\\
&y(t) = e^{F(t-t_0)}y(t_0) + \int^t_{t_0} e^{F(t-\tau)} L w(\tau)d\tau;
\end{split}
$$


where we push last exponential into the integral since it is constant wrt the argument of integration.
