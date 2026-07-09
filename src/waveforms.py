import numpy as np

def extract_waveforms(filtered, spike_times, fs, window_ms=2.0):
    window_samples = int((window_ms / 1000) * fs)
    waveforms = []
    valid_times = []
    for t in spike_times:
        if t - window_samples >= 0 and t + window_samples < len(filtered):
            snippet = filtered[t - window_samples : t + window_samples, :]
            waveforms.append(snippet)
            valid_times.append(t)
    return np.array(waveforms), np.array(valid_times)
