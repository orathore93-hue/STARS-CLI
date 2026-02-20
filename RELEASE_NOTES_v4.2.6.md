# Release v4.2.6 - RBAC Enforcement & Privacy Controls

## 🔒 Security & Privacy Release

This release adds enterprise-grade security controls with mandatory RBAC enforcement and comprehensive privacy protections for AI features.

## 🎯 Highlights

### RBAC Enforcement (v4.2.5)
- **Mandatory permission checks** before all destructive operations
- Pre-flight RBAC validation for delete, restart, scale, drain
- Clear error messages with actionable guidance
- Comprehensive RBAC requirements documentation

### Privacy Controls (v4.2.6)
- **Explicit consent required** for AI features (first use)
- **Per-command opt-out** via `--no-ai` flag
- New `tars privacy` command for consent management
- Comprehensive privacy policy documentation
- Enhanced logging of external API calls

## 🚀 New Features

### Privacy Management Command
```bash
tars privacy status   # Check AI consent status
tars privacy grant    # Grant consent without prompts
tars privacy revoke   # Revoke consent and disable AI
```

### Per-Command AI Control
```bash
tars health --no-ai           # Disable AI for this command
tars diagnose pod-name --no-ai  # Local analysis only
```

### Consent Prompt
First-time AI feature use shows:
```
⚠️  AI Analysis Privacy Notice
AI features send anonymized cluster data to Google Gemini API for analysis.
Data sent: pod names, status, container info (secrets are redacted)
Use --no-ai flag to disable. See docs/PRIVACY.md for details.

Allow AI analysis? [y/N]:
```

## 🛡️ Security Improvements

### RBAC Enforcement
- `delete_pod()` - Checks delete permission before execution
- `restart_resource()` - Checks patch permission
- `scale_resource()` - Checks patch permission
- `drain_node()` - Checks both node patch AND pod delete permissions
- `delete_from_yaml()` - Checks permission for each resource type

### Privacy by Design
- Default deny (must opt-in)
- Explicit consent required
- Per-command granular control
- Comprehensive audit trail
- Clear data disclosure

## 📚 Documentation

### New Documentation
- **docs/RBAC_REQUIREMENTS.md** - Complete RBAC guide with ClusterRole examples
- **docs/PRIVACY.md** - Comprehensive privacy policy (300+ lines)
- **tests/unit/test_rbac_enforcement.py** - RBAC test coverage

### Updated Documentation
- README.md - Added privacy and RBAC notices
- SECURITY.md - Enhanced with consent and enforcement details
- SECURITY_AUDIT.md - Updated with new security controls

## 🔧 Technical Changes

### API Changes
- `AIAnalyzer.analyze_pod_issue()` - Added `allow_external` parameter
- `AIAnalyzer.analyze_cluster_health()` - Added `allow_external` parameter
- `MonitoringCommands.health_check()` - Added `allow_ai` parameter
- `MonitoringCommands.diagnose_pod()` - Added `allow_ai` parameter

### New Configuration
- `CONSENT_FILE` in `~/.stars/ai_consent`
- Functions: `check_ai_consent()`, `grant_ai_consent()`, `revoke_ai_consent()`

### Enhanced Logging
```python
logger.info(f"Sending pod data to Google Gemini API: {pod_name}")
logger.info("Sending cluster health data to Google Gemini API")
```

## 🎯 Defense in Depth

1. **RBAC Enforcement** (NEW) - Kubernetes permission checks
2. **Explicit Consent** (NEW) - User control over external data
3. **Human Confirmations** (Existing) - Prevent accidents
4. **Data Redaction** (Existing) - Remove secrets
5. **Audit Logging** (Existing) - Track all operations

## ✅ Compliance

### GDPR Ready
- ✅ Explicit consent (Article 6)
- ✅ Data minimization (Article 5)
- ✅ Transparency (Article 12)
- ✅ Right to withdraw consent (Article 7)
- ✅ Privacy by design (Article 25)

### Regulated Industries
- ✅ Can disable AI completely
- ✅ Air-gapped deployment supported
- ✅ Audit trail for compliance
- ✅ RBAC enforcement for access control

## 📦 Installation

```bash
# Upgrade to v4.2.6
pip install --upgrade stars-cli

# Or install from source
git clone https://github.com/orathore93-hue/stars-cli.git
cd stars-cli
git checkout v4.2.6
pip install -e .
```

## 🔄 Migration Guide

### No Breaking Changes
This release is fully backward compatible. Existing commands work as before.

### New Behavior
- **First AI feature use** will prompt for consent
- **Grant consent once** to avoid future prompts
- **Use --no-ai flag** for per-command opt-out

### Recommended Actions
1. Review [RBAC Requirements](docs/RBAC_REQUIREMENTS.md)
2. Verify permissions: `kubectl auth can-i --list`
3. Review [Privacy Policy](docs/PRIVACY.md)
4. Configure AI consent: `tars privacy grant` or `tars privacy revoke`

## 📊 Statistics

- **15 files changed**
- **1,552 insertions, 16 deletions**
- **6 new files created**
- **2 new commands** (privacy management)
- **2 new flags** (--no-ai)
- **500+ lines of documentation**

## 🙏 Credits

This release focuses on enterprise security and privacy requirements, making SSTARS CLI production-ready for regulated industries and compliance-conscious organizations.

## 📝 Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete details.

## 🔗 Links

- **Repository**: https://github.com/orathore93-hue/stars-cli
- **Documentation**: [docs/](docs/)
- **RBAC Guide**: [docs/RBAC_REQUIREMENTS.md](docs/RBAC_REQUIREMENTS.md)
- **Privacy Policy**: [docs/PRIVACY.md](docs/PRIVACY.md)
- **Security**: [SECURITY.md](SECURITY.md)

---

**Full Diff**: https://github.com/orathore93-hue/stars-cli/compare/v4.2.4...v4.2.6
