from pathlib import Path

import pathspec


def should_protect_file(file: Path, base_path: Path, protected_patterns: set[str]) -> bool:
    """
    Check if a file matches any protection pattern using gitignore-style matching.

    Args:
        file: File path to check
        base_path: Base directory path
        protected_patterns: Set of gitignore-style patterns

    Returns:
        True if file should be protected, False otherwise
    """
    if not protected_patterns:
        return False

    # Resolve both paths to handle absolute/relative path mismatches
    file_resolved = file.resolve()
    base_resolved = base_path.resolve()

    try:
        relative_path = file_resolved.relative_to(base_resolved)
    except ValueError:
        # File is outside base_path - this shouldn't happen in normal operation
        # But if it does, we should protect it to be safe (don't delete files outside target)
        return True

    # Convert to POSIX-style path (forward slashes) for pathspec
    relative_path_str = relative_path.as_posix()

    # Normalize patterns: ensure directory patterns work correctly
    normalized_patterns = []
    for pattern in protected_patterns:
        pattern = pattern.strip()
        if not pattern or pattern.startswith("#"):
            continue

        # For directory patterns (ending with /), we need both the dir and its contents
        if pattern.endswith("/"):
            # Add pattern for the directory itself and everything inside
            dir_name = pattern.rstrip("/")
            normalized_patterns.append(dir_name)
            normalized_patterns.append(f"{dir_name}/**")
        else:
            normalized_patterns.append(pattern)

    # Create a PathSpec object from patterns (gitignore-style)
    spec = pathspec.PathSpec.from_lines("gitwildmatch", normalized_patterns)

    # Check if the file or any of its parent directories match
    # This is crucial for directory-based protection
    if spec.match_file(relative_path_str):
        return True

    # Also check each parent directory component
    # E.g., for ".venv/bin/python", check ".venv", ".venv/bin", ".venv/bin/python"
    parts = relative_path.parts
    for i in range(1, len(parts) + 1):
        partial_path = "/".join(parts[:i])
        if spec.match_file(partial_path):
            return True

    return False
