import torch.nn as nn


class DenoisingAutoencoder(nn.Module):
    def __init__(self, encoder_layers, decoder_layers):
        """
        encoder_layers: list og tuples (in_dim, out_dim, activation)
        decoder_layers: list of tuples (in_dim, out_dim, activation)
        activation is nn.Module class or None to specify a linear activaiton
        """
        super().__init__()

        self.encoder = self._build_net(encoder_layers)
        self.decoder = self._build_net(decoder_layers)

    def _build_net(self, layers_config):
        layers = []
        for in_dim, out_dim, activation in layers_config:
            layers.append(nn.Linear(in_dim, out_dim))
            if activation is not None:
                layers.append(activation())
        return nn.Sequential(*layers)

    def forward(self, x):
        z = self.encoder(x)
        x_hat = self.decoder(z)
        return x_hat
