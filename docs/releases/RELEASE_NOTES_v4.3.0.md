# Release v4.3.0 - Renamed to STARS

## 🎉 Major Rebrand: TARS → STARS

**S.T.A.R.S** - **S**ite **T**echnical **A**ssistance & **R**eliability **S**ystem

This release renames the project from TARS to STARS to better reflect its purpose as a site reliability tool.

## ⚠️ Breaking Changes

### CLI Command
```bash
# Old
tars health

# New
stars health
```

### Package Name
```bash
# Old
pip install tars-cli

# New
pip install stars-cli
```

### Module Import
```python
# Old
from tars.cli import main

# New
from stars.cli import main
```

### Configuration Directory
```bash
# Old
~/.tars/

# New
~/.stars/
```

## 📦 Migration Guide

### Step 1: Uninstall Old Version
```bash
pip uninstall tars-cli
```

### Step 2: Install New Version
```bash
pip install stars-cli
```

### Step 3: Migrate Configuration (Optional)
```bash
# Preserve your settings and consent
mv ~/.tars ~/.stars
```

### Step 4: Update Scripts
Replace all instances of `tars` command with `stars`:
```bash
# Update shell scripts
sed -i 's/tars /stars /g' your-script.sh

# Update aliases
alias k8s-health='stars health'
```

## 🎨 Visual Changes

### New ASCII Banner
```
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║  ███████╗.████████╗.  █████╗ .  ██████╗ .  ███████╗        ║
║  ██╔════╝.╚══██╔══╝. ██╔══██╗.  ██╔══██╗.  ██╔════╝        ║
║  ███████╗.   ██║   . ███████║.  ██████╔╝.  ███████╗        ║
║  ╚════██║.   ██║   . ██╔══██║.  ██╔══██╗.  ╚════██║        ║
║  ███████║.   ██║   . ██║  ██║.  ██║  ██║.  ███████║        ║
║  ╚══════╝.   ╚═╝   . ╚═╝  ╚═╝.  ╚═╝  ╚═╝.  ╚══════╝        ║
║                                                            ║
║    Site Technical Assistance & Reliability System        ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

## ✨ What's Included

All features from v4.2.6 are included:

### Security Features
- ✅ Mandatory RBAC enforcement
- ✅ Pre-flight permission checks
- ✅ Clear error messages with guidance

### Privacy Features
- ✅ Explicit consent for AI features
- ✅ Per-command `--no-ai` flag
- ✅ `stars privacy` command for consent management
- ✅ Comprehensive privacy policy

### Core Features
- ✅ AI-powered cluster analysis
- ✅ Real-time monitoring
- ✅ Incident response tools
- ✅ Prometheus integration
- ✅ Multi-cluster support

## 📝 Command Reference

All commands remain the same, just use `stars` instead of `tars`:

```bash
# Monitoring
stars health              # Cluster health check
stars pods                # List all pods
stars top                 # Resource usage

# Diagnostics
stars diagnose <pod>      # Diagnose pod issues
stars logs <pod>          # Get pod logs
stars events              # Show cluster events

# Operations
stars restart <pod>       # Restart a pod
stars scale <deploy> 3    # Scale deployment
stars drain <node>        # Drain a node

# Privacy
stars privacy status      # Check AI consent
stars privacy grant       # Enable AI features
stars privacy revoke      # Disable AI features

# AI Features (with consent)
stars health              # With AI analysis
stars diagnose <pod>      # With AI recommendations

# Opt-out per command
stars health --no-ai      # Disable AI for this command
```

## 🔗 Updated Links

- **Repository**: https://github.com/orathore93-hue/stars-cli (will be renamed)
- **PyPI**: https://pypi.org/project/stars-cli/
- **Documentation**: [docs/](docs/)

## 📊 Statistics

- **53 files changed**
- **485 insertions, 292 deletions**
- **Complete rebrand** across all documentation
- **Zero functionality changes** - only naming

## 🙏 Why the Rename?

The name **STARS** (Site Technical Assistance & Reliability System) better reflects the tool's purpose:
- **Site** - Emphasizes site reliability engineering
- **Technical Assistance** - Highlights the AI-powered help
- **Reliability System** - Core focus on system reliability

## ⚡ Quick Start

```bash
# Install
pip install stars-cli

# Setup
export GEMINI_API_KEY='your-key'

# Verify RBAC
kubectl auth can-i --list

# Start using
stars health
stars oncall
```

## 🔄 Backward Compatibility

**None** - This is a breaking change. The `tars` command will no longer work after upgrading.

However, all your data and settings can be migrated by simply renaming the directory:
```bash
mv ~/.tars ~/.stars
```

## 📚 Documentation Updates

All documentation has been updated:
- README.md - Updated branding
- All docs/ files - Updated references
- Code comments - Updated terminology
- Examples - Updated command names

## 🐛 Known Issues

None. This is a pure rename with no functional changes.

## 💬 Feedback

If you have any issues with the migration, please open an issue on GitHub.

---

**Full Diff**: https://github.com/orathore93-hue/stars-cli/compare/v4.2.6...v4.3.0
