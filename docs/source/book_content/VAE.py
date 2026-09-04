import torch
import torch.nn as nn
from torch.distributions import Normal, kl_divergence


class VAE(nn.Module):
    def __init__(self, encoder_layers, decoder_layers, latent_dim, decoder_type, N):
        """
        encoder_layers: list og tuples (in_dim, out_dim, activation)
        decoder_layers: list of tuples (in_dim, out_dim, activation)
        activation is nn.Module class or None to specify a linear activation
        decoder_type: to specify the observation model p(x|z). For the moment only Gaussian
        is considered
        """
        super().__init__()

        self.latent_dim = latent_dim
        self.decoder_type = decoder_type
        # self.im_shape = im_shape
        self.N = N

        # standard normal prior
        self.p_z = Normal(torch.zeros(latent_dim),torch.ones(latent_dim))

        # for sampling
        self.zero_tensor = torch.tensor(0.0)

        # Definir encoder y decoder
        self.encoder = self.build_encoder(encoder_layers)
        self.decoder = self.build_decoder(decoder_layers)

    def build_encoder(self, layers_config):
        layers = []
        for in_dim, out_dim, activation in layers_config[:-1]:
            layers.append(nn.Linear(in_dim, out_dim))
            if activation is not None:
                layers.append(activation())

        self.enc = nn.Sequential(*layers)
        in_dim, out_dim, activation = layers_config[-1]
        self.enc_mean = nn.Sequential(*[nn.Linear(in_dim, out_dim)])
        self.enc_logvar = nn.Sequential(*[nn.Linear(in_dim, out_dim),nn.Tanh()])

    def build_decoder(self, layers_config):

        layers = []
        for in_dim, out_dim, activation in layers_config[:-1]:
            layers.append(nn.Linear(in_dim, out_dim))
            if activation is not None:
                layers.append(activation())

        self.dec = nn.Sequential(*layers)
        in_dim, out_dim, activation = layers_config[-1]
        self.dec_mean = nn.Linear(in_dim, out_dim)
        self.dec_logvar = nn.Sequential(*[nn.Linear(in_dim, out_dim),nn.Tanh()])

    def encoder_forward(self, x):
        z = self.enc(x)
        return self.enc_mean(z), 5*self.enc_logvar(z)

    def decoder_forward(self, z):
        x = self.dec(z)
        return self.dec_mean(x), 5*self.dec_logvar(x)

    def sample_gaussian(self, mean, logvar, return_mean=False):
        if return_mean:
            return mean
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mean + eps * std

    def ELBO(self, x, mc_samples=1, kld_scale=1.0):
        M = x.size(0)

        # Encoder
        q_mean, q_logvar = self.encoder_forward(x)

        # Encoder distribution
        q_zx = Normal(q_mean, torch.exp(0.5*q_logvar))

        # DKL
        KLD = kld_scale * kl_divergence(q_zx,self.p_z)

        # sum over each training point
        KLD = KLD.sum()

        # Log Likelihood using Monte Carlo. We could vectorize mc_sampling but for academic
        # purposes this is better. Also vectorizing requires taking care of memory.
        LLH = torch.tensor(0.0)
        for _ in range(mc_samples):
            z = self.sample_gaussian(q_mean, q_logvar)
            dec_mean, dec_logvar = self.decoder_forward(z)

            # Sum over training points and over dimensions
            LLH += Normal(dec_mean, torch.exp(0.5*dec_logvar)).log_prob(x).sum()

        ## Monte Carlo Estimation
        LLH /= mc_samples

        ## ELBO
        ELBO = LLH - KLD

        ## Renormalize minibatching for appropidate scale
        ELBO *= self.N / M

        return ELBO, LLH, KLD

    def sample_from_prior(self, n_samples, return_mean=False):
        """Sample from prior via ancestral sampling"""
        z = self.sample_gaussian(self.zero_tensor.expand(n_samples, self.latent_dim),
                               self.zero_tensor.expand(n_samples, self.latent_dim),
                               return_mean=False)

        mean, logvar = self.decoder_forward(z)
        return z, self.sample_gaussian(mean, logvar, return_mean=return_mean)

    def sample_from_posterior(self, x, return_mean=False):
        """Sample from posterior distribution q(z|x)."""
        mean, logvar = self.encoder_forward(x)
        z = self.sample_gaussian(mean, logvar, return_mean=False)
        dec_mean, dec_logvar = self.decoder_forward(z)
        return self.sample_gaussian(dec_mean, dec_logvar, return_mean=return_mean)

    def run_mcmc(self, x, num_steps, n_chains=1, return_mean=False):
        x_chain = []

        batch_size, x_dim = x.shape
        # expand x to [batch_size, n_chains, x_dim] then flatten to [batch_size*n_chains, x_dim]
        x_t = x.unsqueeze(1).repeat(1, n_chains, 1).view(batch_size * n_chains, x_dim)
        x_chain.append(x_t)
        z_chain = []

        for _ in range(num_steps):
            # z_t ~ q(z|x_t)
            q_mean, q_logvar = self.encoder_forward(x_t)
            z_t = self.sample_gaussian(q_mean, q_logvar)

            # x_{t+1} ~ p(x|z_t)
            dec_mean, dec_logvar = self.decoder_forward(z_t)
            x_t = self.sample_gaussian(dec_mean, dec_logvar, return_mean=return_mean)

            x_chain.append(x_t)
            z_chain.append(z_t)

        # stack and reshape to [num_steps, batch_size, n_chains, z_dim] / [num_steps+1, batch_size, n_chains, x_dim]
        z_chain = torch.stack(z_chain, dim=0).view(num_steps, batch_size, n_chains, -1)
        x_chain = torch.stack(x_chain, dim=0).view(num_steps+1, batch_size, n_chains, -1)

        # reshape to [batch_size, n_chains, num_steps, dim]
        z_chain = z_chain.permute(1,2,0,3).contiguous()
        x_chain = x_chain.permute(1,2,0,3).contiguous()

        return z_chain, x_chain
