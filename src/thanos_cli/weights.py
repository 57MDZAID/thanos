import random
from pathlib import Path


def calculate_file_weight(file: Path, weights_config: dict) -> float:
    """
    Calculate elimination probability for a file based on weights.
    Returns a value between 0.0 (protect) and 1.0 (highly likely to eliminate).
    Default is 0.5 (neutral).
    """
    if not weights_config:
        return 0.5

    weight = 0.5

    # Extension-based weights
    ext_weights = weights_config.get("by_extension", {})
    if ext_weights and file.suffix in ext_weights:
        weight = ext_weights[file.suffix]

    return weight


def weighted_random_sample(files: list[Path], weights: list[float], k: int) -> list[Path]:
    """Select k files using weighted random sampling."""
    selected = []
    remaining_files = list(files)
    remaining_weights = list(weights)

    for _ in range(k):
        if not remaining_files:
            break

        # Weighted random choice
        total = sum(remaining_weights)
        if total == 0:
            # Fallback to uniform if all weights are 0
            idx = random.randint(0, len(remaining_files) - 1)
        else:
            r = random.uniform(0, total)
            cumulative = 0
            idx = 0
            for i, w in enumerate(remaining_weights):
                cumulative += w
                if r <= cumulative:
                    idx = i
                    break

        selected.append(remaining_files[idx])
        remaining_files.pop(idx)
        remaining_weights.pop(idx)

    return selected
