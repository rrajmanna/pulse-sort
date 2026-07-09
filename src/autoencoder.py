import torch
import torch.nn as nn

class WaveformAutoencoder(nn.Module):
    def __init__(self, input_dim, latent_dim):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Linear(64, latent_dim),
        )
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 256),
            nn.ReLU(),
            nn.Linear(256, input_dim),
        )

    def forward(self, x):
        z = self.encoder(x)
        x_hat = self.decoder(z)
        return x_hat, z


def train_autoencoder(model, data, epochs=50, lr=1e-3, batch_size=64):
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.MSELoss()
    losses = []

    n = data.shape[0]
    for epoch in range(epochs):
        permutation = torch.randperm(n)
        epoch_loss = 0
        for i in range(0, n, batch_size):
            idx = permutation[i:i+batch_size]
            batch = data[idx]

            optimizer.zero_grad()
            x_hat, _ = model(batch)
            loss = loss_fn(x_hat, batch)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item() * len(idx)

        losses.append(epoch_loss / n)

    return losses
