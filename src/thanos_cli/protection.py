import fnmatch
from pathlib import Path


def should_protect_file(file: Path, base_path: Path, protected_patterns: set[str]) -> bool:
    """Check if a file matches any protection pattern."""
    # Resolve both paths to handle absolute/relative path mismatches
    file_resolved = file.resolve()
    base_resolved = base_path.resolve()

    try:
        relative_path = file_resolved.relative_to(base_resolved)
    except ValueError:
        # If file is not under base_path, don't protect it
        return False

    for pattern in protected_patterns:
        # Handle directory patterns
        if pattern.endswith("/**"):
            dir_pattern = pattern[:-3]
            if str(relative_path).startswith(dir_pattern):
                return True

        # Handle exact matches
        elif pattern == str(relative_path):
            return True

        # Handle wildcard patterns
        elif "*" in pattern:
            if fnmatch.fnmatch(str(relative_path), pattern):
                return True
            if fnmatch.fnmatch(file.name, pattern):
                return True

    return False
