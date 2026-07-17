import hdbscan
import numpy as np
from numpy.typing import NDArray


def cluster_hdbscan(features: NDArray, min_cluster_size: int = 15) -> NDArray:
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size)
    labels = clusterer.fit_predict(features)
    return labels
