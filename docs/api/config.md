# Config

::: config

Configuration dataclasses for each pipeline stage. Each has  defaults and can be customized

- **`DetectionConfig`**: `low_freq`, `high_freq`, `threshold_factor`, `refractory_ms`, `combine_method`
- **`WaveformConfig`**: `window_ms`
- **`AutoencoderConfig`**: `latent_dim`, `epochs`, `lr`, `batch_size`
- **`ClusteringConfig`**: `n_clusters`, `random_state`
- **`RefinementConfig`**: `match_threshold`, `top_k`, `max_iterations`, `anchor_similarity`
