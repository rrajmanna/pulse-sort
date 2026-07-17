from pathlib import Path

from spikeinterface.sorters import BaseSorter
from spikeinterface.core import NumpySorting

from pipeline import run_pulse_sort
from config import DetectionConfig, WaveformConfig, AutoencoderConfig, ClusteringConfig


class PulseSortSorter(BaseSorter):
    sorter_name = "pulse_sort"
    installed = True

    _default_params = {
        "low_freq": 300,
        "high_freq": 6000,
        "threshold_factor": 8,
        "refractory_ms": 1.0,
        "window_ms": 2.0,
        "latent_dim": 8,
        "epochs": 100,
        "n_clusters": 10,
    }

    _params_description = {
        "low_freq": "Bandpass filter low cutoff (Hz)",
        "high_freq": "Bandpass filter high cutoff (Hz)",
        "threshold_factor": "Detection threshold, in std devs above median",
        "refractory_ms": "Refractory period (ms) between detected spikes",
        "window_ms": "Half-window size (ms) for waveform extraction",
        "latent_dim": "Autoencoder latent feature dimension",
        "epochs": "Autoencoder training epochs",
        "n_clusters": "Number of clusters for k-means",
    }

    installation_mesg = """
    pulse_sort is bundled with this SpikeInterface integration.
    See: https://github.com/rrajmanna/pulse-sort
    """

    @classmethod
    def get_sorter_version(cls):
        return "0.1.0"

    @classmethod
    def is_installed(cls):
        return True

    @classmethod
    def _setup_recording(cls, recording, output_folder, params, verbose):
        traces = recording.get_traces().astype("float32")
        fs = recording.get_sampling_frequency()
        import numpy as np
        np.save(Path(output_folder) / "traces.npy", traces)
        np.save(Path(output_folder) / "fs.npy", fs)

    @classmethod
    def _run_from_folder(cls, output_folder, params, verbose):
        import numpy as np
        traces = np.load(Path(output_folder) / "traces.npy")
        fs = float(np.load(Path(output_folder) / "fs.npy"))

        detection_config = DetectionConfig(
            low_freq=params["low_freq"],
            high_freq=params["high_freq"],
            threshold_factor=params["threshold_factor"],
            refractory_ms=params["refractory_ms"],
        )
        waveform_config = WaveformConfig(window_ms=params["window_ms"])
        autoencoder_config = AutoencoderConfig(
            latent_dim=params["latent_dim"],
            epochs=params["epochs"],
        )
        clustering_config = ClusteringConfig(n_clusters=params["n_clusters"])

        result = run_pulse_sort(
            traces, fs,
            detection_config=detection_config,
            waveform_config=waveform_config,
            autoencoder_config=autoencoder_config,
            clustering_config=clustering_config,
        )

        np.save(Path(output_folder) / "spike_times.npy", result.spike_times)
        np.save(Path(output_folder) / "cluster_labels.npy", result.cluster_labels)

    @classmethod
    def _get_result_from_folder(cls, output_folder, register_recording=True, sorting_info=None):
        import numpy as np
        spike_times = np.load(Path(output_folder) / "spike_times.npy")
        cluster_labels = np.load(Path(output_folder) / "cluster_labels.npy")
        fs = float(np.load(Path(output_folder) / "fs.npy"))

        units_dict = {}
        for cluster_id in np.unique(cluster_labels):
            units_dict[str(int(cluster_id))] = spike_times[cluster_labels == cluster_id]

        sorting = NumpySorting.from_unit_dict(units_dict, sampling_frequency=fs)
        return sorting
