# Waveforms

::: waveforms

Waveform extraction around detected spike times.

## `extract_waveforms(filtered, spike_times, fs, window_ms=2.0)`
Extracts a multi-channel snippet around each detected spike.

- **filtered**: filtered multi-channel signal, shape `(samples, channels)`
- **spike_times**: detected spike sample indices
- **fs**: sampling frequency in Hz
- **window_ms**: half-window size in milliseconds on each side of the spike
- **Returns**: tuple of `(waveforms, valid_times)`
  - `waveforms`: array of shape `(n_spikes, window_samples*2, channels)`
  - `valid_times`: spike times that had a full window available
