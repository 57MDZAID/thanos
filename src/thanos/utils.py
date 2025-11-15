from pathlib import Path


def get_files(directory: str, recursive: bool = False) -> list[Path]:
    """Get all files in the directory."""
    path = Path(directory)

    if not path.exists():
        raise FileNotFoundError(f"Directory '{directory}' does not exist")

    if not path.is_dir():
        raise NotADirectoryError(f"'{directory}' is not a directory")

    if recursive:
        files = [f for f in path.rglob("*") if f.is_file()]
    else:
        files = [f for f in path.iterdir() if f.is_file()]

    return files
