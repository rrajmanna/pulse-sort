# Clustering

::: clustering

## `cluster_hdbscan(features, min_cluster_size=15)`
Clusters spikes in feature space using HDBSCAN, a clustering algorithm that finds the number of clusters automatically.

- **features**: learned feature vectors, shape `(n_spikes, latent_dim)`
- **min_cluster_size**: minimum number of points to form a cluster
- **Returns**: array of cluster labels, one per spike.
