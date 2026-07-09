import numpy as np
from templates import template_match


def _template_similarity(t1, t2):
    """Normalized correlation between two templates (flattened)."""
    a = t1.flatten()
    b = t2.flatten()
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def iterative_refine(filtered, initial_indices, waveforms, fs,
                      n_candidates=400, max_iterations=10,
                      stability_threshold=0.9, anchor_similarity=0.5):
    """
    Iteratively rebuild a spike template using a fixed-size pool of
    top-scoring candidates, but ANCHORED to the original seed template:
    any proposed update that drifts too far from the original (similarity
    below anchor_similarity) is rejected, and refinement stops there.
    """
    history = []
    original_waveforms = waveforms[initial_indices]
    original_template = original_waveforms.mean(axis=0)
    template = original_template.copy()

    prev_times = None

    for iteration in range(max_iterations):
        _, scores = template_match(filtered, template, fs, threshold=-np.inf)

        top_order = np.argsort(scores)[::-1][:n_candidates]
        top_times = np.sort(top_order)

        if prev_times is not None:
            overlap = len(set(top_times) & set(prev_times))
            stability = overlap / n_candidates
        else:
            stability = 0.0

        history.append({
            "iteration": iteration,
            "template": template.copy(),
            "selected_times": top_times,
            "stability": stability,
        })

        print(f"iteration {iteration}: stability={stability:.3f}")

        if stability >= stability_threshold:
            print(f"converged at iteration {iteration}")
            break

        # Build the CANDIDATE next template
        window = template.shape[0] // 2
        new_waveforms = []
        for t in top_times:
            if t - window >= 0 and t + window < len(filtered):
                new_waveforms.append(filtered[t - window : t + window, :])
        new_waveforms = np.array(new_waveforms)
        candidate_template = new_waveforms.mean(axis=0)

        # Anchor check: does this candidate still resemble the ORIGINAL seed?
        sim = _template_similarity(candidate_template, original_template)
        print(f"  similarity to original template: {sim:.3f}")

        if sim < anchor_similarity:
            print(f"  rejected: drifted too far from original (similarity={sim:.3f} < {anchor_similarity})")
            print(f"  stopping, keeping template from iteration {iteration}")
            break

        template = candidate_template
        prev_times = top_times

    return history
