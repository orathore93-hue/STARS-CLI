# GitHub Repository Rename Instructions

## Step 1: Rename Repository on GitHub

1. Go to: https://github.com/orathore93-hue/stars-cli
2. Click **Settings** tab
3. Scroll down to **Repository name**
4. Change `tars-cli` to `stars-cli`
5. Click **Rename**

GitHub will automatically:
- Redirect old URLs to new repository
- Update clone URLs
- Preserve all issues, PRs, releases

## Step 2: Update Local Repository

After renaming on GitHub:

```bash
cd ~/Desktop/work/tars-cli

# Update remote URL
git remote set-url origin https://github.com/orathore93-hue/stars-cli.git

# Verify
git remote -v

# Optional: Rename local directory
cd ~/Desktop/work
mv tars-cli stars-cli
cd stars-cli
```

## Step 3: Update Documentation URLs

The following files reference the old repo URL and should be updated after rename:

- pyproject.toml (Homepage, Repository, Issues URLs)
- README.md (badges, links)
- CONTRIBUTING.md (repository links)
- All docs/*.md files with GitHub links

Run this after renaming:

```bash
# Update all GitHub URLs
find . -type f \( -name "*.md" -o -name "*.toml" \) -exec sed -i '' 's|orathore93-hue/stars-cli|orathore93-hue/stars-cli|g' {} \;

# Commit changes
git add -A
git commit -m "docs: Update repository URLs after rename"
git push origin main
```

## Step 4: Update PyPI Package (Future)

When publishing to PyPI:
- Package name is already `stars-cli` in setup.py
- No changes needed for PyPI

## Verification

After completing all steps:

```bash
# Check remote URL
git remote -v
# Should show: https://github.com/orathore93-hue/stars-cli.git

# Test clone
cd /tmp
git clone https://github.com/orathore93-hue/stars-cli.git
cd stars-cli
python3 -m stars.cli --help
```

## Notes

- Old URLs will redirect automatically (GitHub feature)
- All releases, tags, and history are preserved
- No data loss during rename
- Contributors' commits remain intact
