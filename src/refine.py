import numpy as np
from templates import template_match


def iterative_refine(filtered, initial_indices, waveforms, fs,
                      match_threshold=0.6, top_k=200, max_iterations=10,
                      growth_limit=1.3):
    """
    Iteratively rebuild a spike template using only the top-K highest-scoring
    matches each round. Stops and reverts if the match count grows too fast
    (a sign the template is drifting toward noise rather than converging).
    """
    history = []
    current_waveforms = waveforms[initial_indices]
    template = current_waveforms.mean(axis=0)
    best_template = template.copy()

    prev_n_matches = None

    for iteration in range(max_iterations):
        matched_times, scores = template_match(filtered, template, fs, threshold=match_threshold)
        n_matches = len(matched_times)

        print(f"iteration {iteration}: {n_matches} total matches")

        # Divergence check: if matches grew too fast, the template is drifting toward noise.
        # Stop here and keep the PREVIOUS iteration's template as the final answer.
        if prev_n_matches is not None and n_matches > prev_n_matches * growth_limit:
            print(f"stopping: match count grew too fast ({prev_n_matches} -> {n_matches}), reverting to previous template")
            break

        history.append({
            "iteration": iteration,
            "template": template.copy(),
            "matched_times": matched_times,
            "n_matches": n_matches,
        })
        best_template = template.copy()

        match_scores = scores[matched_times]
        top_order = np.argsort(match_scores)[::-1][:top_k]
        top_times = matched_times[top_order]

        window = template.shape[0] // 2
        new_waveforms = []
        for t in top_times:
            if t - window >= 0 and t + window < len(filtered):
                new_waveforms.append(filtered[t - window : t + window, :])
        new_waveforms = np.array(new_waveforms)
        new_template = new_waveforms.mean(axis=0)

        prev_n_matches = n_matches
        template = new_template

    return history, best_template
