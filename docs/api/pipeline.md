# Pipeline

::: pipeline

Rrun the full pulse-sort pipeline on any recording.

## `run_pulse_sort(recording, fs, detection_config=None, waveform_config=None, autoencoder_config=None, clustering_config=None)`
Runs detection, waveform extraction, autoencoder feature learning, and clustering on any multi-channel recording, using config objects for each stage (see `config.md`).

- **recording**: raw multi-channel voltage traces, shape `(samples, channels)`
- **fs**: sampling frequency in Hz
- Each `*_config` argument is optional; if not provided, sensible defaults are used
- **Returns**: a `PulseSortResult` object containing spike times, waveforms, cluster labels, learned features, and per-cluster spatial templates
