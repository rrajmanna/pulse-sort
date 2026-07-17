# Autoencoder

::: autoencoder

A small autoencoder for learning compressed spike waveform features, replacing PCA.

## `WaveformAutoencoder(input_dim, latent_dim)`
Autoencoder that compresses a flattened waveform into a low-dimensional latent representation.

- **input_dim**: size of the flattened input waveform (time * channels)
- **latent_dim**: size of the compressed latent representation
- **forward(x)**: returns `(reconstruction, latent_features)`

## `train_autoencoder(model, data, epochs=50, lr=1e-3, batch_size=64)`
Trains the autoencoder with MSE reconstruction loss.

- **model**: a `WaveformAutoencoder` instance
- **data**: training data tensor, shape `(n_samples, input_dim)`
- **epochs, lr, batch_size**: standard training hyperparameters
- **Returns**: list of average reconstruction loss per epoch
