"""Minimal example: run pulse-sort on a synthetic multi-channel recording."""

import sys
sys.path.append("../src")

import numpy as np
from pipeline import run_pulse_sort

fs = 30000
duration_sec = 5
n_channels = 8
recording = np.random.randn(fs * duration_sec, n_channels).astype(np.float32) * 0.05

result = run_pulse_sort(recording, fs)

print(f"Detected {len(result.spike_times)} spikes")
print(f"Found {len(result.templates)} clusters")
