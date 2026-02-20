# Privacy Policy - SSTARS CLI

## Overview

SSTARS CLI is designed with privacy in mind. This document explains what data is collected, where it goes, and how you can control it.

## Data Collection

### Local Data Only (Default Operations)

Most STARS commands operate **entirely locally** and never send data externally:

- `tars pods` - Lists pods from your cluster
- `tars logs` - Retrieves logs locally
- `tars top` - Shows resource usage
- `tars events` - Displays cluster events
- `tars describe` - Shows resource details
- `tars restart` - Restarts resources
- `tars scale` - Scales deployments
- `tars delete` - Deletes resources

**No external data transmission for these commands.**

### AI-Powered Features (Optional External Data)

The following commands **may send data to Google Gemini API** if AI features are enabled:

- `tars health` - Cluster health analysis
- `tars diagnose` - Pod issue diagnosis
- `tars analyze` - Cluster analysis
- `tars oncall` - On-call dashboard with AI insights

## What Data is Sent to Google Gemini

When AI features are used, the following **anonymized** data is sent:

### Pod Analysis
```json
{
  "name": "my-app-pod-xyz",
  "status": "CrashLoopBackOff",
  "containers": [
    {
      "name": "app",
      "ready": false,
      "restarts": 5
    }
  ]
}
```

### Cluster Health
```json
{
  "nodes": {
    "total": 3,
    "ready": 2,
    "not_ready": 1
  },
  "pods": {
    "total": 50,
    "running": 45,
    "failed": 5
  }
}
```

## What is NOT Sent

STARS **never** sends:

- ❌ Secrets or ConfigMap contents
- ❌ Environment variables
- ❌ API tokens or credentials
- ❌ Private keys
- ❌ Full pod specifications
- ❌ Log contents
- ❌ Network policies
- ❌ RBAC configurations
- ❌ Service account tokens
- ❌ Image pull secrets

All sensitive data is **redacted before transmission** using pattern matching.

## Data Redaction

Before sending any data to external APIs, STARS applies comprehensive redaction:

```python
# Patterns automatically redacted:
- password: ***
- token: ***
- api_key: ***
- secret: ***
- AWS_ACCESS_KEY_ID: ***
- AWS_SECRET_ACCESS_KEY: ***
- GOOGLE_APPLICATION_CREDENTIALS: ***
- authorization: ***
- bearer tokens
- private keys
```

See `src/tars/utils.py` for complete redaction patterns.

## Consent Management

### First Use Prompt

On first use of AI features, you'll see:

```
⚠️  AI Analysis Privacy Notice
AI features send anonymized cluster data to Google Gemini API for analysis.
Data sent: pod names, status, container info (secrets are redacted)
Use --no-ai flag to disable. See docs/PRIVACY.md for details.

Allow AI analysis? [y/N]:
```

### Managing Consent

```bash
# Check current consent status
tars privacy status

# Grant consent (skip prompts)
tars privacy grant

# Revoke consent (disable AI)
tars privacy revoke
```

Consent is stored locally in `~/.stars/ai_consent` (chmod 600).

## Disabling AI Features

### Per-Command Opt-Out

```bash
# Disable AI for specific command
tars health --no-ai
tars diagnose my-pod --no-ai
```

### Global Disable

```bash
# Don't set GEMINI_API_KEY
# AI features will be completely disabled

# Or revoke consent
tars privacy revoke
```

### Air-Gapped Environments

STARS works perfectly in air-gapped environments:

1. Don't set `GEMINI_API_KEY`
2. All core features work without AI
3. AI commands gracefully degrade

## Third-Party Services

### Google Gemini API

- **Service**: Google Gemini 2.0 Flash
- **Purpose**: AI-powered cluster analysis
- **Data Sent**: Anonymized pod/cluster metrics (see above)
- **Data Retention**: Per Google's API terms
- **Privacy Policy**: https://policies.google.com/privacy
- **Terms**: https://ai.google.dev/terms

### No Other External Services

STARS does **not** use:
- Analytics or telemetry
- Crash reporting services
- Usage tracking
- Phone-home mechanisms
- Update checks

## Data Storage

### Local Storage Only

All STARS data is stored locally in `~/.stars/`:

```
~/.stars/
├── config.yaml       # User configuration (chmod 600)
├── audit.log         # Audit trail (chmod 600)
├── ai_consent        # AI consent flag (chmod 600)
├── tars.log          # Application logs (chmod 600)
└── logs/             # Command logs (chmod 700)
```

**Secure permissions** prevent unauthorized access.

### No Cloud Storage

STARS does **not**:
- Store data in cloud services
- Sync data across devices
- Upload logs or metrics
- Use remote configuration

## Compliance Considerations

### Regulated Industries

If you work in regulated industries (healthcare, finance, government):

1. **Disable AI features** - Don't set `GEMINI_API_KEY`
2. **Use --no-ai flag** - Explicit per-command control
3. **Review audit logs** - Track all operations
4. **Air-gap deployment** - No external connectivity required

### GDPR Compliance

- No personal data collected
- No user tracking
- No cookies or identifiers
- Data minimization by design
- User consent required for external data

### Data Residency

- Google Gemini API location: Per Google's infrastructure
- No control over data residency when using AI features
- For strict data residency: Disable AI features

## Security

### Data in Transit

- HTTPS/TLS for all external API calls
- Kubernetes API uses cluster's TLS configuration
- No unencrypted data transmission

### Data at Rest

- Local files: chmod 600/700 (owner-only access)
- No encryption at rest (OS-level encryption recommended)
- Audit logs for compliance tracking

### Credential Management

- API keys via environment variables only
- No hardcoded credentials
- Secrets redacted before logging
- See SECURITY.md for details

## Transparency

### Open Source

STARS is open source. You can:

- Review all code: https://github.com/your-org/stars-cli
- Audit data handling: `src/tars/ai.py`, `src/tars/utils.py`
- Verify redaction patterns
- Build from source

### Audit Logging

All operations are logged locally:

```bash
# Review what data was sent
tail -f ~/.stars/audit.log

# Check AI API calls
grep "Gemini API" ~/.stars/tars.log
```

## Your Rights

You have the right to:

1. ✅ **Know what data is sent** - Documented above
2. ✅ **Opt-out** - Use `--no-ai` or revoke consent
3. ✅ **Access logs** - All stored in `~/.stars/`
4. ✅ **Delete data** - `rm -rf ~/.stars/`
5. ✅ **Audit code** - Open source, review anytime

## Questions?

- **Security issues**: See SECURITY.md for responsible disclosure
- **Privacy concerns**: Open an issue on GitHub
- **Feature requests**: Contribute or request enhancements

## Changes to This Policy

This privacy policy may be updated. Check the repository for the latest version.

**Last Updated**: 2026-02-20

---

**Summary**: STARS respects your privacy. Most features are local-only. AI features are optional, require consent, and send only anonymized data. You have full control.
