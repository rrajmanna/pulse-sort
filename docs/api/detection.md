# Detection

::: detection
Functions for multi-channel spike detection: filtering, channel combination, and thresholding.

## `bandpass_filter(signal, fs, low=300, high=6000)`
Applies a 4th-order Butterworth bandpass filter to isolate relevant frequencies.

- **signal**: raw voltage traces, shape `(samples, channels)`
- **fs**: sampling frequency in Hz
- **low, high**: cutoff frequencies in Hz
- **Returns**: filtered signal, same shape as input

## `combined_signal(filtered, method="sum_sq")`
Combines multiple channels into a single  signal.

- **filtered**: filtered multi-channel signal, shape `(samples, channels)`
- **method**: `"sum_sq"` (sum of squared amplitude) or `"max_abs"` (max amplitude across channels)
- **Returns**: 1D combined signal, shape `(samples,)`

## `detect_spikes(combo, fs, threshold_factor=8, refractory_ms=1.0)`
Detects spike times thru thresholding on a combined signal.

- **combo**: 1D combined detection signal
- **fs**: sampling frequency in Hz
- **threshold_factor**: number of standard deviations above the median used as the detection threshold
- **refractory_ms**: minimum time (ms) between two detected spikes
- **Returns**: array of detected spike sample indices
