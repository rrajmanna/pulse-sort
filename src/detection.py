import numpy as np
from scipy.signal import butter, filtfilt

def bandpass_filter(signal, fs, low=300, high=6000):
    nyq = fs / 2
    b, a = butter(4, [low/nyq, high/nyq], btype='band')
    return filtfilt(b, a, signal, axis=0)

def combined_signal(filtered, method="sum_sq"):
    if method == "sum_sq":
        return np.sum(filtered ** 2, axis=1)
    elif method == "max_abs":
        return np.max(np.abs(filtered), axis=1)

def detect_spikes(combo, fs, threshold_factor=8, refractory_ms=1.0):
    threshold = np.median(combo) + threshold_factor * np.std(combo)
    refractory_samples = int((refractory_ms / 1000) * fs)
    above_threshold = combo > threshold
    crossings = np.where(above_threshold)[0]
    spike_times = []
    last_spike = -refractory_samples
    for idx in crossings:
        if idx - last_spike >= refractory_samples:
            spike_times.append(idx)
            last_spike = idx
    return np.array(spike_times)
