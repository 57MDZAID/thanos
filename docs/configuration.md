# Configuration Reference

## `.thanosignore` Patterns

Follows gitignore syntax:

```gitignore
# Comments start with #

# Exact filename
.env

# Wildcard
*.log
*.tmp

# Directory (trailing slash)
logs/
cache/

# All files with extension in any directory
**/*.pyc

# Directory contents recursively
node_modules/**

# Negation (don't protect)
!debug.log

# Character ranges
file[0-9].txt

# Question mark (single character)
file?.txt
```

## `.thanosrc.json` Schema

```json
{
  "weights": {
    "by_extension": {
      "<extension>": <0.0-1.0>
    },
    "by_age_days": {
      "<range>": <0.0-1.0>
    },
    "by_size_mb": {
      "<range>": <0.0-1.0>
    }
  }
}
```

#### Example
```json
{
  "weights": {
    "by_extension": {
      ".log": 0.9,
      ".tmp": 0.95,
      ".py": 0.3
    },
    "by_age_days": {
      "0-7": 0.3,
      "30+": 0.9
    },
    "by_size_mb": {
      "0-1": 0.4,
      "100+": 0.8
    }
  }
}
```
**Range formats:**
- `"min-max"` - Inclusive min, exclusive max
- `"min+"` or `"min-"` - Min or greater

---

**Remember**: Thanos is a powerful tool. With great power comes great responsibility. Always preview with `--dry-run` first! 🫰✨
