# Refinement

::: refine

Iterative, closed-loop template refinement

## `iterative_refine(filtered, initial_indices, waveforms, fs, match_threshold=0.6, top_k=200, max_iterations=10, anchor_similarity=0.5)`

- **filtered**: filtered multi-channel signal
- **initial_indices**: indices into `waveforms` for the starting spike set (e.g. from an initial cluster)
- **waveforms**: all extracted waveforms
- **fs**: sampling frequency in Hz
- **match_threshold**: correlation threshold for matching
- **top_k**: number of top-scoring matches used to rebuild the template each round
- **max_iterations**: maximum number of refinement rounds
- **anchor_similarity**: minimum allowed correlation to the original seed template
- **Returns**: list of per-iteration dicts (iteration index, template, matched spike times)
