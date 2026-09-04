import torch
import torch.nn as nn
from torch.distributions import Normal, Independent


class CouplingLayer(nn.Module):
    def __init__(self, dim, hidden_dim, flip=False):
        super().__init__()

        self.dim = dim
        self.flip = flip

        # Partition
        self.d1 = dim // 2

        # m(x) network
        self.m = nn.Sequential(
            nn.Linear(self.d1, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, dim - self.d1)
        )

    def forward(self, x):
        """
        Forward transformation.
        """
        x1 = x[:, :self.d1]
        x2 = x[:, self.d1:]

        if not self.flip:
            y1 = x1
            y2 = x2 + self.m(x1)
        else:
            y1 = x1 + self.m(x2)
            y2 = x2

        return torch.cat([y1, y2], dim=1)

    def inverse(self, y):
        """
        Exact inverse transformation.
        """
        y1 = y[:, :self.d1]
        y2 = y[:, self.d1:]

        if not self.flip:
            x1 = y1
            x2 = y2 - self.m(y1)
        else:
            x1 = y1 - self.m(y2)
            x2 = y2

        return torch.cat([x1, x2], dim=1)

    def log_det_jacobian(self,x):
        return torch.zeros(x.size(0), device = x.device)


class CouplingLayerNVP(nn.Module):
    # https://arxiv.org/abs/1605.08803
    def __init__(self, dim, hidden_dim, flip=False):
        super().__init__()

        self.dim = dim
        self.flip = flip

        # Partition
        self.d1 = dim // 2

        # scale factor for s()
        self.s_scale_factor = 1.5

        # t(x) and s(x) networks
        self.t = nn.Sequential(
            nn.Linear(self.d1, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, dim - self.d1)
        )

        self.s = nn.Sequential(
            nn.Linear(self.d1, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, dim - self.d1),
            nn.Tanh(),
        )

        ## Initialize flow to the
        nn.init.zeros_(self.t[-1].weight)
        nn.init.zeros_(self.t[-1].bias)

        nn.init.zeros_(self.s[-2].weight)  # -2 porque el último es Tanh
        nn.init.zeros_(self.s[-2].bias)


    def forward(self, x):
        """
        Forward transformation.
        """
        x1 = x[:, :self.d1]
        x2 = x[:, self.d1:]

        if not self.flip:
            y1 = x1
            y2 = x2 * torch.exp(self.s(x1)*self.s_scale_factor) + self.t(x1)
        else:
            y1 = x1 * torch.exp(self.s(x2)*self.s_scale_factor) + self.t(x2)
            y2 = x2

        return torch.cat([y1, y2], dim=1)

    def inverse(self, y):
        """
        Exact inverse transformation.
        """
        y1 = y[:, :self.d1]
        y2 = y[:, self.d1:]

        if not self.flip:
            x1 = y1
            x2 = (y2 - self.t(x1))*torch.exp(-self.s(x1)*self.s_scale_factor)
        else:
            x2 = y2
            x1 = (y1 - self.t(x2))*torch.exp(-self.s(x2)*self.s_scale_factor)


        return torch.cat([x1, x2], dim=1)

    def log_det_jacobian(self,x):
        if not self.flip:
            x1 = x[:, :self.d1]
            log_det_jacobian = torch.sum(self.s(x1)*self.s_scale_factor, dim = 1)
        else:
            x2 = x[:, self.d1:]
            log_det_jacobian = torch.sum(self.s(x2)*self.s_scale_factor, dim = 1)
        return log_det_jacobian

class DiagonalScalingMatrixLayer(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.S = nn.Parameter(torch.ones(dim,))

    def forward(self, x):
        """
        Forward transformation.
        """
        return self.S * x

    def inverse(self, y):
        """
        Exact inverse transformation.
        """
        return 1/self.S * y

    def log_det_jacobian(self,x):
        log_det_jacobian = torch.sum(torch.log(torch.abs(self.S)))
        return log_det_jacobian.expand(x.size(0))

class _FlowModel(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.dim = dim

    def x_to_z(self, x):
        z = x
        for layer in self.layers:
            z = layer(z)
        return z

    def z_to_x(self, z):
        for layer in reversed(self.layers):
            z = layer.inverse(z)
        return z

    def log_likelihood(self, x):
        """
        Compute log p(x) = log p(f(x)) + log|det J|

        It uses forward computation ie starts from x maps to z.
        Thus, each step in the Jacobian computation starts from x_{k-1}

        """
        z = x
        log_det_jacobian = torch.zeros(x.size(0), dtype = x.dtype)
        for layer in self.layers:
            ## call first log_det_jacobian since it receives x_{k-1}
            log_det_jacobian += layer.log_det_jacobian(z)
            z = layer(z)

        # Prior log-probability
        log_pz = self.prior.log_prob(z)

        return log_pz + log_det_jacobian

    def generate_sample(self, num_samples):
        """
        Sample from flow model
        """
        # draw a sample from p(z)
        z = self.prior.sample((num_samples,))

        # draw a sample through the mapping
        x = self.z_to_x(z)
        return x, z

    def inference(self, x):
        """
        Compute latent assignment z
        """
        # encode
        z = self.x_to_z(x)
        return z

class NICEVP(_FlowModel):
    """
    Volume Preserving NICE
    """
    def __init__(self, dim, hidden_dim, num_coupling_layers=4):
        super().__init__(dim)

        # Coupling layers with alternating flip
        layers = []
        for i in range(num_coupling_layers):
            flip = (i % 2 == 1)
            layers.append(CouplingLayer(dim, hidden_dim, flip=flip))
        self.layers = nn.ModuleList(layers)

        # Prior distribution
        self.prior = Independent(Normal(torch.zeros(dim), torch.ones(dim)), 1)


class NICE(NICEVP):
    """
    Non Volume Preserving NICE
    """
    def __init__(self, dim, hidden_dim, num_coupling_layers=4):
        super().__init__(dim = dim, hidden_dim=hidden_dim, num_coupling_layers = num_coupling_layers)
        
        # add diagonal scaling
        self.layers.append(DiagonalScalingMatrixLayer(dim))

class RealNVP(_FlowModel):
    """
    Real NVP (non volume preserving)
    """
    def __init__(self, dim, hidden_dim, num_coupling_layers=4):
        super().__init__(dim)

        # Coupling layers with alternating flip
        layers = []
        for i in range(num_coupling_layers):
            flip = (i % 2 == 1)
            layers.append(CouplingLayerNVP(dim, hidden_dim, flip=flip))
        self.layers = nn.ModuleList(layers)

        # Prior distribution
        self.prior = Independent(Normal(torch.zeros(dim), torch.ones(dim)), 1)
