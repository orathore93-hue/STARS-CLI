# STARS CLI - Security Guide for Production Use

## ✅ Security Features

### 1. Secure Credential Storage

**STARS uses OS-native encrypted storage for sensitive credentials:**

| Platform | Storage Backend | Encryption | Access Control |
|----------|----------------|------------|----------------|
| **macOS** | Keychain | AES-256 | User authentication required |
| **Windows** | Credential Manager | DPAPI | Windows user account |
| **Linux** | Secret Service | Encrypted | Desktop session |

**How it works:**
```bash
# Store API key securely (one-time setup)
stars set-api-key
# Enter your API key when prompted (input hidden)

# STARS retrieves it automatically from keychain
stars init
```

**Security benefits:**
- ✅ Credentials encrypted at rest
- ✅ OS-level access control
- ✅ No plaintext files (`.env`, shell history)
- ✅ Automatic credential rotation support
- ✅ Audit trail of access attempts

**First-time keychain access:**

On first use, your OS will prompt for keychain access:
- **macOS**: "stars wants to access your keychain"
- **Windows**: User Account Control prompt
- **Linux**: "Authentication required" dialog

**This is standard behavior for secure CLI tools** (AWS CLI, Docker, kubectl). Click "Allow" or "Always Allow" to proceed. STARS will only access credentials it created.

**For CI/CD and headless servers:**
```bash
# Keychain unavailable - use environment variable
export GEMINI_API_KEY='your-key-here'

# STARS automatically falls back to env vars
stars init
```

### 2. Binary Integrity Verification

**Installation includes cryptographic verification:**

```bash
# One-line installer automatically verifies checksums
curl -sSL https://raw.githubusercontent.com/orathore93-hue/STARS-CLI/main/install.sh | bash
```

**What happens:**
1. Downloads binary from GitHub release
2. Downloads SHA-256 checksum file
3. **Verifies checksum before installation**
4. Installation fails if verification fails

**Manual verification:**
```bash
# Download binary and checksum
curl -LO https://github.com/orathore93-hue/STARS-CLI/releases/download/v5.0.0/stars-linux-amd64
curl -LO https://github.com/orathore93-hue/STARS-CLI/releases/download/v5.0.0/stars-linux-amd64.sha256

# Verify integrity
sha256sum -c stars-linux-amd64.sha256
# Output: stars-linux-amd64: OK

# Only install if verification passes
chmod +x stars-linux-amd64
sudo mv stars-linux-amd64 /usr/local/bin/stars
```

**Security benefits:**
- ✅ Detects tampered binaries
- ✅ Prevents man-in-the-middle attacks
- ✅ Ensures authentic releases
- ✅ Transparent build process

### 3. Human-in-the-Loop
- All destructive operations require explicit confirmation
- Shows exact commands before execution
- Displays current Kubernetes context
- Default answer is "No" for safety

### 4. Sensitive Data Protection
- Automatic redaction of passwords, tokens, API keys
- AWS access keys detection and redaction
- Bearer tokens and authorization headers protected
- Applied before sending data to AI services

### 5. Secure Local State
- All data stored in `~/.stars/` with chmod 700
- Log files with chmod 600 (owner read/write only)
- No usage of `/tmp/` or world-readable directories
- Audit log for all destructive operations

### 6. Audit Trail
- All destructive operations logged to `~/.stars/audit.log`
- Includes timestamp, user, action, resource, namespace
- Secure permissions (chmod 600)

## ⚠️ Production Considerations

### 1. RBAC Permissions
**Risk:** Commands require appropriate Kubernetes RBAC permissions

**Mitigation:**
- Pre-flight RBAC checks before all destructive operations
- Clear permission error messages with guidance
- Use service accounts with minimal required permissions
- Implement RBAC policies for your organization
- See docs/RBAC_REQUIREMENTS.md for detailed permission requirements
- Test in non-production first

### 2. Kubernetes Context
**Risk:** Commands run against current kubectl context

**Mitigation:**
- Always verify context before running commands: `tars context`
- Use context-specific kubeconfig files
- Destructive operations show context confirmation

### 3. Credential Management
**Risk:** API keys stored insecurely

**Mitigation:**
```bash
# Use OS keychain (recommended)
stars set-api-key
# Credentials encrypted and stored in OS keychain

# For CI/CD: Use secrets manager
export GEMINI_API_KEY=$(aws secretsmanager get-secret-value \
  --secret-id stars-gemini-key \
  --query SecretString \
  --output text)

# Or HashiCorp Vault
export GEMINI_API_KEY=$(vault kv get -field=api_key secret/stars)
```

**Never:**
- ❌ Commit API keys to version control
- ❌ Store in plaintext `.env` files
- ❌ Share keys in chat/email
- ❌ Use production keys in development

### 4. Network Security
**Risk:** AI features send data to external API (Gemini)

**Mitigation:**
- **Explicit user consent required** on first use
- **Per-command opt-out** via `--no-ai` flag
- Data is redacted before sending
- Can disable AI features by not setting GEMINI_API_KEY
- Review data being sent in logs
- Use in air-gapped environments without AI features
- See docs/PRIVACY.md for complete data handling details

### 5. Audit and Compliance
**Risk:** Need to track who did what

**Mitigation:**
- Check audit log: `cat ~/.stars/audit.log`
- Integrate with your SIEM/logging system
- Regular audit log reviews

## 🔒 Best Practices

### 1. Secure Installation
```bash
# Always verify checksums (automatic with install.sh)
curl -sSL https://raw.githubusercontent.com/orathore93-hue/STARS-CLI/main/install.sh | bash

# Or manual verification
sha256sum -c stars-linux-amd64.sha256
```

### 2. Credential Management
```bash
# Use OS keychain (recommended)
stars set-api-key

# Verify keychain access
stars init  # Should not prompt for API key

# Rotate credentials regularly
stars delete-api-key
stars set-api-key  # Enter new key
```

### 3. Least Privilege
```bash
# Create service account with minimal permissions
kubectl create serviceaccount stars-user
kubectl create rolebinding stars-user-binding \
  --clusterrole=view \
  --serviceaccount=default:stars-user
```

### 4. Separate Contexts
```bash
# Use separate kubeconfig for production
export KUBECONFIG=~/.kube/config-prod
stars context  # Verify before any operation
```

### 5. Read-Only Mode
```bash
# For monitoring, use read-only commands:
stars health
stars pods
stars events
stars analyze

# Avoid destructive commands in production:
# stars restart
# stars scale
# stars autofix
```

### 6. Audit Log Monitoring
```bash
# Monitor audit log
tail -f ~/.stars/audit.log

# Export to central logging
cat ~/.stars/audit.log | logger -t stars-cli
```

## 🚨 Security Checklist

Before using in production:

- [ ] Install with checksum verification
- [ ] Store API keys in OS keychain (not plaintext)
- [ ] Verify RBAC permissions are appropriate
- [ ] Test in non-production environment first
- [ ] Set up audit log monitoring
- [ ] Review and understand all commands
- [ ] Train team on confirmation prompts
- [ ] Set up alerting for destructive operations
- [ ] Regular security audits of audit.log
- [ ] Keep STARS CLI updated
- [ ] Review data sent to AI services
- [ ] Rotate credentials regularly

## 🔐 Enterprise Security Features

### Supply Chain Security
- ✅ SHA-256 checksum verification
- ✅ Signed GitHub releases
- ✅ Transparent build process
- ✅ Dependency pinning with hashes
- ✅ Automated security scanning

### Credential Security
- ✅ OS-native encrypted storage
- ✅ No plaintext credentials
- ✅ Automatic keychain integration
- ✅ Environment variable fallback
- ✅ Credential rotation support

### Access Control
- ✅ RBAC enforcement
- ✅ Least privilege by default
- ✅ Audit logging
- ✅ User confirmation prompts
- ✅ Context verification

## 📋 Incident Response

If unauthorized action detected:

1. Check audit log: `cat ~/.stars/audit.log`
2. Identify user and action
3. Review Kubernetes audit logs
4. Revoke compromised credentials
5. Review RBAC permissions
6. Update security policies

## 🔐 Compliance

STARS CLI helps with:
- **SOC 2**: Audit logging, access controls, encrypted credential storage
- **HIPAA**: Data encryption at rest (chmod 600), OS keychain encryption
- **PCI DSS**: Sensitive data redaction, secure credential management
- **GDPR**: Data minimization, secure storage, user consent
- **ISO 27001**: Access control, audit trails, cryptographic verification

## 📞 Security Contact

For security issues:
- Email: orathore93@gmail.com
- GitHub: https://github.com/orathore93-hue/STARS-CLI/security

## 🔄 Updates

Keep STARS CLI updated for security patches:
```bash
# Via installer (recommended)
curl -sSL https://raw.githubusercontent.com/orathore93-hue/STARS-CLI/main/install.sh | bash

# Or via pip
pip install --upgrade stars-cli

# Verify version
stars --version
```

---

**Remember:** Security is a shared responsibility. STARS CLI provides enterprise-grade security tools, but you must use them according to your organization's security policies.
