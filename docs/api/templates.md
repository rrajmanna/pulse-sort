# Templates

::: templates

Spatial template construction and template-matching.

## `build_template(waveforms, spike_indices)`
Averages a set of waveforms into a spatial template for one neuron.

- **waveforms**: all extracted waveforms, shape `(n_spikes, time, channels)`
- **spike_indices**: indices into `waveforms` belonging to one cluster/neuron
- **Returns**: template of shape `(time, channels)`

## `template_match(filtered, template, fs, threshold=0.7)`
Slides a template across the filtered signal thru normalized correlation.

- **filtered**: filtered multi-channel signal, shape `(samples, channels)`
- **template**: spatial template, shape `(time, channels)`
- **fs**: sampling frequency in Hz
- **threshold**: minimum normalized correlation score to count as a match
- **Returns**: tuple of `(spike_times, scores)`
