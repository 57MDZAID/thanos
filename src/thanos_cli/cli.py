"""Console script for thanos_cli."""

import random
from typing import Annotated, Optional

import typer
from rich.console import Console

from .utils import get_files

app = typer.Typer(
    name="thanos",
    help="🫰 Thanos - Eliminate half of all files with a snap. Perfectly balanced, as all things should be.",
    add_completion=False,
)
console = Console()


def snap(
    directory: str = ".",
    recursive: bool = False,
    dry_run: bool = False,
    seed: Optional[int] = None,
):
    """
    The Snap - Eliminates half of all files randomly.

    Args:
        directory: Target directory (default: current directory)
        recursive: Include subdirectories
        dry_run: Show what would be deleted without actually deleting
        seed: Random seed for reproducible file selection
    """
    print("🫰 Initiating the Snap...")

    # Set random seed if provided for reproducible results
    if seed is not None:
        random.seed(seed)
        print(f"🎲 Using random seed: {seed}")

    files = get_files(directory, recursive)
    total_files = len(files)

    if total_files == 0:
        print("No files found. The universe is empty.")
        return

    # Calculate how many files to eliminate
    files_to_eliminate = total_files // 2

    # Randomly select files for elimination
    eliminated = random.sample(files, files_to_eliminate)

    print("\n📊 Balance Assessment:")
    print(f"   Total files: {total_files}")
    print(f"   Files to eliminate: {files_to_eliminate}")
    print(f"   Survivors: {total_files - files_to_eliminate}")

    if dry_run:
        print("\n🔍 DRY RUN - These files would be eliminated:")
        for file in eliminated:
            print(f"   💀 {file}")
        print("\n⚠️  This was a dry run. No files were harmed.")
        if seed is None:
            print("💡 Tip: Use --seed <number> to get the same file selection on the next run.")
        else:
            print(f"💡 Run 'thanos --seed {seed}' to delete these exact files.")
        return

    # Show preview of files to be deleted
    print("\n📋 Files selected for elimination:")
    for file in eliminated:
        print(f"   💀 {file}")

    # Confirm before destruction
    print("\n⚠️  WARNING: This will permanently delete the files listed above!")
    confirm = input("Type 'snap' to proceed: ")

    if confirm.lower() != "snap":
        print("Snap cancelled. The universe remains unchanged.")
        return

    # Execute the snap
    print("\n💥 Snapping...")
    eliminated_count = 0

    for file in eliminated:
        try:
            file.unlink()
            eliminated_count += 1
            print(f"   ✓ Eliminated: {file}")
        except Exception as e:
            print(f"   ❌ Failed to eliminate {file}: {e}")

    print("\n✨ The snap is complete.")
    print(f"   {eliminated_count} files eliminated.")
    print("   Perfectly balanced, as all things should be.")


@app.command()
def main(
    directory: Annotated[
        Optional[str],
        typer.Argument(
            help="Target directory to snap (default: current directory)",
            show_default=False,
        ),
    ] = ".",
    recursive: Annotated[
        bool,
        typer.Option(
            "--recursive",
            "-r",
            help="Include files in subdirectories recursively",
        ),
    ] = False,
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run",
            "-d",
            help="Preview what would be deleted without actually deleting",
        ),
    ] = False,
    seed: Annotated[
        Optional[int],
        typer.Option(
            "--seed",
            "-s",
            help="Random seed for reproducible file selection (use same seed to get same files)",
        ),
    ] = None,
):
    """
    🫰 Eliminate half of all files in a directory with a snap.

    Thanos randomly selects and deletes exactly half of the files in the specified
    directory. Use with caution - deleted files cannot be recovered!

    The file selection is random by default. Use --seed with the same number to get
    the same selection across runs.

    Examples:

        # Preview with a random selection
        $ thanos --dry-run

        # Preview with a specific seed (reproducible)
        $ thanos --dry-run --seed 12345

        # Delete using the same seed from dry run
        $ thanos --seed 12345

        # Snap a specific directory
        $ thanos /path/to/directory --seed 999

        # Include subdirectories with seed
        $ thanos --recursive --seed 42
    """
    try:
        snap(directory, recursive, dry_run, seed)
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    app()
