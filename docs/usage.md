# 📚 Thanos Usage Guide

Complete guide for using Thanos CLI tool.

## Table of Contents

- [Basic Usage](#basic-usage)
- [Command Options](#command-options)
- [Common Scenarios](#common-scenarios)
- [Safety Guidelines](#safety-guidelines)
- [Advanced Usage](#advanced-usage)
- [Troubleshooting](#troubleshooting)

## Basic Usage

### Getting Help

```bash
# Display help message
thanos --help
```

### Simple Snap

```bash
# Snap current directory (with confirmation)
thanos

# Snap a specific directory
thanos /path/to/directory
```

### Dry Run (Recommended First Step)

Always start with a dry run to see what would be deleted:

```bash
# Preview deletion in current directory
thanos --dry-run

# Preview deletion in specific directory
thanos /path/to/directory --dry-run
```

### Deterministic Preview Using --seed

Use `--seed` to get reproducible file selections:

```bash
# Same preview every time
thanos --dry-run --seed 42

# Use same seed again to delete the exact same files
thanos --seed 42
```

## Command Options

### Directory Argument

```bash
thanos [DIRECTORY]
```

- **Default**: Current directory (`.`)
- **Description**: The target directory where files will be eliminated
- **Examples**:
  ```bash
  thanos                    # Current directory
  thanos ~/Downloads        # Home Downloads folder
  thanos /tmp/test-files    # Absolute path
  thanos ../parent-folder   # Relative path
  ```

### `--recursive` / `-r`

Include files in subdirectories.

```bash
thanos --recursive
thanos -r
thanos /path/to/dir --recursive
```

**Behavior**:
- Without flag: Only files in the immediate directory
- With flag: All files in directory and all subdirectories

**Example**:
```bash
# Directory structure:
# project/
# ├── file1.txt
# ├── file2.txt
# └── subdir/
#     ├── file3.txt
#     └── file4.txt

# Without --recursive: Only file1.txt and file2.txt considered
thanos project/

# With --recursive: All 4 files considered
thanos project/ --recursive
```

### `--dry-run` / `-d`

Preview what would be deleted without actually deleting.

```bash
thanos --dry-run
thanos -d
thanos /path/to/dir --dry-run --recursive
```

**Output includes**:
- Total file count
- Number of files that would be eliminated
- List of files that would be deleted
- No actual deletion occurs

## Common Scenarios

### Scenario 1: Cleaning Test Data

```bash
# 1. Check what's in your test directory
ls -la test-data/

# 2. See what would be deleted
thanos test-data/ --dry-run --seed 99   # preview reproducibly

# 3. Proceed with deletion
thanos test-data/ --seed 99            # delete same selection
# Type 'snap' when prompted
```

### Scenario 2: Reducing Large Download Folders

```bash
# Preview deletion including subdirectories
thanos ~/Downloads --recursive --dry-run --seed 150

# If satisfied, proceed
thanos ~/Downloads --recursive --seed 150
```

### Scenario 3: Cleaning Temporary Files

```bash
# Clean temp directory
thanos /tmp/my-temp-files --dry-run
thanos /tmp/my-temp-files
```

### Scenario 4: Development Testing

```bash
# Create test environment
mkdir test-snap
cd test-snap
for i in {1..20}; do echo "test $i" > file$i.txt; done

# Test the snap
thanos --dry-run --seed 150
thanos --seed 150
```

## Safety Guidelines

### ⚠️ Always Use Dry Run First

```bash
# GOOD: Check first
thanos --dry-run
thanos

# RISKY: Directly snapping without preview
thanos  # Don't do this without dry run first!
```

### 🔒 Confirmation Required

Thanos requires you to type `snap` to confirm deletion:

```
⚠️  WARNING: This will permanently delete files!
Type 'snap' to proceed: snap
```

**Cancellation**:
```
Type 'snap' to proceed: no
Snap cancelled. The universe remains unchanged.
```

### 💾 Backup Important Data

Before using Thanos on important directories:

```bash
# Create a backup
tar -czf backup.tar.gz /path/to/important-directory/

# Then use Thanos
thanos /path/to/important-directory/ --dry-run
```

### 🎯 Target Specific Directories

Don't run Thanos from your home directory or root:

```bash
# DANGEROUS
cd ~
thanos --recursive  # DON'T DO THIS!

# SAFE
thanos ~/specific-folder
```

## Advanced Usage

### Combining Options

```bash
# Dry run with recursive
thanos /data --recursive --dry-run --seed 123
thanos /data -r -d --seed 123

# Real snap with recursive (requires confirmation)
thanos /data --recursive
thanos /data -r
```

### Working with Different Directory Types

```bash
# Current directory
thanos

# Relative paths
thanos ./subdirectory
thanos ../sibling-directory

# Absolute paths
thanos /absolute/path/to/directory

# Home directory shortcuts
thanos ~/Documents/old-files
thanos $HOME/tmp
```

### Integration with Other Commands

```bash
# Count files before and after
ls | wc -l
thanos --dry-run
thanos
ls | wc -l

# Verify directory size
du -sh /path/to/dir
thanos /path/to/dir --dry-run
thanos /path/to/dir
du -sh /path/to/dir
```

### Scripting (Use with Extreme Caution!)

```bash
#!/bin/bash
# Example: Clean multiple test directories

TEST_DIRS=("test1" "test2" "test3")

for dir in "${TEST_DIRS[@]}"; do
    echo "Processing $dir..."
    thanos "$dir" --dry-run
    # Manual confirmation still required per directory
done
```

## Understanding the Output

### Dry Run Output

```
🫰 Initiating the Snap...

📊 Balance Assessment:
   Total files: 100
   Files to eliminate: 50
   Survivors: 50

🔍 DRY RUN - These files would be eliminated:
   💀 /path/to/file1.txt
   💀 /path/to/file2.jpg
   ...

⚠️  This was a dry run. No files were harmed.
```

### Actual Snap Output

```
🫰 Initiating the Snap...

📊 Balance Assessment:
   Total files: 100
   Files to eliminate: 50
   Survivors: 50

⚠️  WARNING: This will permanently delete files!
Type 'snap' to proceed: snap

💥 Snapping...
   💀 /path/to/file1.txt
   💀 /path/to/file2.jpg
   ❌ Failed to eliminate /path/to/protected.txt: Permission denied
   ...

✨ The snap is complete.
   49 files eliminated.
   Perfectly balanced, as all things should be.
```

## Troubleshooting

### "No such file or directory"

```bash
# Error
thanos /nonexistent/path

# Solution: Verify path exists
ls /nonexistent/path
thanos /correct/path
```

### "Permission denied"

```bash
# Some files may be protected
# Thanos will skip them and report errors

# Check permissions
ls -la /path/to/directory

# Run with sudo (use extreme caution!)
sudo thanos /protected/directory
```

### "No files found"

```bash
# Directory is empty or contains only subdirectories
thanos /empty/directory
# Output: "No files found. The universe is empty."

# Use --recursive if files are in subdirectories
thanos /directory --recursive
```

### Odd Number of Files

```bash
# If you have 11 files:
# - 5 will be deleted (11 // 2 = 5)
# - 6 will remain

# If you have 1 file:
# - 0 will be deleted (1 // 2 = 0)
# - 1 will remain
```

## Best Practices

1. **Always dry run first**: `thanos --dry-run`
2. **Start with small, safe directories**: Test on `/tmp` first
3. **Use `--seed` when you want predictable behavior**
3. **Know your file count**: Check with `ls | wc -l`
4. **Backup important data**: Better safe than sorry
5. **Read the confirmation prompt**: Make sure you're in the right directory
6. **Use specific paths**: Avoid running from important system directories
7. **Check permissions**: Ensure you have rights to delete files
8. **Understand randomness**: Each snap produces different results

## Examples by Use Case

### Development: Cleaning Test Fixtures

```bash
cd my-project/tests/fixtures
thanos --dry-run
thanos
```

### Data Science: Reducing Dataset Size

```bash
thanos ./training-data/images --dry-run
thanos ./training-data/images
```

### System Admin: Cleaning Logs

```bash
thanos /var/log/old-logs --dry-run
thanos /var/log/old-logs
```

### Personal: Organizing Downloads

```bash
thanos ~/Downloads --recursive --dry-run
# Review the list carefully
thanos ~/Downloads --recursive
```

---

**Remember**: Thanos is a powerful tool. Use it wisely and always preview with `--dry-run` first! 🫰
