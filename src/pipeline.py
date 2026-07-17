from dataclasses import dataclass, field
from typing import Optional

import numpy as np
from numpy.typing import NDArray
from sklearn.cluster import KMeans

from config import (
    AutoencoderConfig,
    ClusteringConfig,
    DetectionConfig,
    WaveformConfig,
)
from detection import bandpass_filter, combined_signal, detect_spikes
from waveforms import extract_waveforms
from autoencoder import WaveformAutoencoder, train_autoencoder
from templates import build_template

import torch


@dataclass
class PulseSortResult:
    spike_times: NDArray
    waveforms: NDArray
    cluster_labels: NDArray
    features: NDArray
    templates: dict
    detection_config: DetectionConfig = field(repr=False)


def run_pulse_sort(
    recording: NDArray,
    fs: float,
    detection_config: Optional[DetectionConfig] = None,
    waveform_config: Optional[WaveformConfig] = None,
    autoencoder_config: Optional[AutoencoderConfig] = None,
    clustering_config: Optional[ClusteringConfig] = None,
) -> PulseSortResult:
    detection_config = detection_config or DetectionConfig()
    waveform_config = waveform_config or WaveformConfig()
    autoencoder_config = autoencoder_config or AutoencoderConfig()
    clustering_config = clustering_config or ClusteringConfig()

    filtered = bandpass_filter(recording, fs, detection_config.low_freq, detection_config.high_freq)
    combo = combined_signal(filtered, method=detection_config.combine_method)
    spike_times = detect_spikes(
        combo, fs,
        threshold_factor=detection_config.threshold_factor,
        refractory_ms=detection_config.refractory_ms,
    )

    waveforms, valid_times = extract_waveforms(filtered, spike_times, fs, waveform_config.window_ms)

    n_spikes = waveforms.shape[0]
    flattened = waveforms.reshape(n_spikes, -1)
    normalized = (flattened - flattened.mean()) / flattened.std()
    data_tensor = torch.tensor(normalized, dtype=torch.float32)

    model = WaveformAutoencoder(flattened.shape[1], autoencoder_config.latent_dim)
    train_autoencoder(model, data_tensor, epochs=autoencoder_config.epochs, lr=autoencoder_config.lr)
    model.eval()
    with torch.no_grad():
        _, features = model(data_tensor)
    features = features.numpy()

    kmeans = KMeans(n_clusters=clustering_config.n_clusters, random_state=clustering_config.random_state, n_init=10)
    cluster_labels = kmeans.fit_predict(features)

    templates = {}
    for cluster_id in np.unique(cluster_labels):
        indices = np.where(cluster_labels == cluster_id)[0]
        templates[int(cluster_id)] = build_template(waveforms, indices)

    return PulseSortResult(
        spike_times=valid_times,
        waveforms=waveforms,
        cluster_labels=cluster_labels,
        features=features,
        templates=templates,
        detection_config=detection_config,
    )
