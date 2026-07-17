from dataclasses import dataclass


@dataclass
class DetectionConfig:
    low_freq: float = 300
    high_freq: float = 6000
    threshold_factor: float = 8
    refractory_ms: float = 1.0
    combine_method: str = "sum_sq"


@dataclass
class WaveformConfig:
    window_ms: float = 2.0


@dataclass
class AutoencoderConfig:
    latent_dim: int = 8
    epochs: int = 100
    lr: float = 1e-3
    batch_size: int = 64


@dataclass
class ClusteringConfig:
    n_clusters: int = 10
    random_state: int = 42


@dataclass
class RefinementConfig:
    match_threshold: float = 0.6
    top_k: int = 200
    max_iterations: int = 10
    anchor_similarity: float = 0.5
