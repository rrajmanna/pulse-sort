# pulse-sort

A spike sorting pipeline built on in-vivo Neuropixel recordings; extending the basic single-channel pipeline from my [fund-spike-sort](https://github.com/rrajmanna/fund-spike-sort) with multi-channel detection, autoencoder features, and iterations.

## Data

This project uses in-vivo data from the [Kampff Lab ground-truth dataset](https://github.com/kampff-lab/sc.io) (cell `c37`). This data came from a 384-channel Neuropixel recording, giving 601 ground-truth spikes from a sample cortical neuron.

## Pipeline

1. **Multi-channel detection**: spikes were detected using a combined signal across 40-channels, which improves sensitivity to the target neuron.
2. **Multi-channel waveform extraction**: each detected spike is captured as a (time × channel) snippet
3. **Autoencoder feature learning**: a small autoencoder compressed each waveform snippet into a learned feature vector
4. **Clustering**: spikes are grouped in the learned feature space (k-means clustering)
5. **Template construction**: the cluster best matching the ground-truth neuron is averaged into a template.
6. **Template matching**: the template is correlated against the full recording to find more matching spikes.
7. **Iterative refinement**: the template is repeatedly redone from more matches, which I used to converge on a more accurate representation of the neuron

## Installation

\`\`\`bash
git clone git@github.com:rrajmanna/pulse-sort.git
cd pulse-sort
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
\`\`\`

## Usage

Each stage of the pipeline lives in `src/` as an importable module, run step by step in the notebooks under `notebooks/`.

### Detection (`src/detection.py`)
- `bandpass_filter`: isolates the frequency range where spikes are (300-6000 Hz)
- `combined_signal`: merges multiple channels into one detection signal
- `detect_spikes`: locates spike times using thresholds

### Waveform extraction (`src/waveforms.py`)
- `extract_waveforms`: pulls a multi-channel (time × channel) snippet around each detected spike

### Feature learning (`src/autoencoder.py`)
- `WaveformAutoencoder`: an autoencoder that compresses waveform snippets into a learned feature vector
- `train_autoencoder`: trains the autoencoder on extracted waveforms

Latent dimension (8) was chosen by checking 2-32 dimensions and comparing reconstruction loss:

<img src="figures/latent_size.png" width="440">

### Clustering and templates (`src/templates.py`)
- `build_template`: averages a cluster's waveforms into a template for one neuron
- `template_match`: correlates a template against the recording to find matching spikes

### Iterative refinement (`src/refine.py`)
- `iterative_refine`: iteratively rebuilds the template from its own best matches

Several refinement methods were implemented (naive rebuild, top-K selection, fixed candidate pool, anchored to seed template). See `src/refine.py` for more; this stage converges but does not improve on single-pass template matching for this dataset (limitation).

## Results

Autoencoder features outperforms PCA at the same dimensionality:

| Method | Best cluster purity |
|---|---|
| PCA (8 components) | 53.9% |
| Autoencoder (8 latent dims) | **64.5%** |

<img src="figures/clusters.png" width="440">

Spatial template for the isolated neuron:

<img src="figures/template.png" width="440">

Precision/recall by pipeline stage:

| Method | Precision | Recall |
|---|---|---|
| Raw multi-channel detection | 13.5% | 59.9% |
| Autoencoder + clustering | 64.5% | 39.9% |
| Template matching (0.6) | 37.4% | 42.6% |

<img src="figures/final_comparison.png" width="480">

## Project structure

\`\`\`
pulse-sort/
├── notebooks/
│   ├── 01_load_data.ipynb
│   ├── 02_detect_spikes.ipynb
│   ├── 03_waveforms.ipynb
│   ├── 04_autoencoder.ipynb
│   ├── 05_templates.ipynb
│   └── 06_refine.ipynb
├── src/
│   ├── detection.py
│   ├── waveforms.py
│   ├── autoencoder.py
│   ├── templates.py
│   └── refine.py
├── figures/
└── requirements.txt
\`\`\`

## Acknowledgments

Ground-truth data from the [Kampff Lab](http://www.kampff-lab.org/) paired recordings dataset. Built with PyTorch, scikit-learn, NumPy, and SciPy.
