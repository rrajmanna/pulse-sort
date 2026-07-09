import numpy as np

def build_template(waveforms, spike_indices):
    """Average the waveforms belonging to one cluster to build its spatial template."""
    cluster_waveforms = waveforms[spike_indices]
    template = cluster_waveforms.mean(axis=0)  # shape: (time, channels)
    return template


def template_match(filtered, template, fs, threshold=0.7):
    """
    Slide the template across the filtered signal (per channel) and find
    points where the normalized cross-correlation with the template is high.
    Returns candidate spike times.
    """
    n_samples, n_channels = filtered.shape
    window = template.shape[0]
    half_window = window // 2

    # Flatten template for correlation
    template_flat = template.flatten()
    template_norm = template_flat / np.linalg.norm(template_flat)

    scores = np.zeros(n_samples)
    for t in range(half_window, n_samples - half_window):
        snippet = filtered[t - half_window : t + half_window, :]
        if snippet.shape[0] != window:
            continue
        snippet_flat = snippet.flatten()
        norm = np.linalg.norm(snippet_flat)
        if norm == 0:
            continue
        score = np.dot(snippet_flat, template_norm) / norm
        scores[t] = score

    candidate_times = np.where(scores > threshold)[0]

    # Simple refractory period to avoid duplicate detections
    refractory_samples = int(0.001 * fs)
    spike_times = []
    last_spike = -refractory_samples
    for t in candidate_times:
        if t - last_spike >= refractory_samples:
            spike_times.append(t)
            last_spike = t

    return np.array(spike_times), scores
