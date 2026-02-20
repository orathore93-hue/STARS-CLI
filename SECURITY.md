# TARS CLI - Security Guide for Production Use

## ✅ Security Features

### 1. Human-in-the-Loop
- All destructive operations require explicit confirmation
- Shows exact commands before execution
- Displays current Kubernetes context
- Default answer is "No" for safety

### 2. Sensitive Data Protection
- Automatic redaction of passwords, tokens, API keys
- AWS access keys detection and redaction
- Bearer tokens and authorization headers protected
- Applied before sending data to AI services

### 3. Secure Local State
- All data stored in `~/.tars/` with chmod 700
- Log files with chmod 600 (owner read/write only)
- No usage of `/tmp/` or world-readable directories
- Audit log for all destructive operations

### 4. Audit Trail
- All destructive operations logged to `~/.tars/audit.log`
- Includes timestamp, user, action, resource, namespace
- Secure permissions (chmod 600)

## ⚠️ Production Considerations

### 1. RBAC Permissions
**Risk:** Commands require appropriate Kubernetes RBAC permissions

**Mitigation:**
- Use service accounts with minimal required permissions
- Implement RBAC policies for your organization
- Test in non-production first

### 2. Kubernetes Context
**Risk:** Commands run against current kubectl context

**Mitigation:**
- Always verify context before running commands: `tars context`
- Use context-specific kubeconfig files
- Destructive operations show context confirmation

### 3. API Key Security
**Risk:** GEMINI_API_KEY in environment variables

**Mitigation:**
```bash
# Don't export globally
# Use per-session or secure secret management
export GEMINI_API_KEY='your-key'

# Or use a secrets manager
export GEMINI_API_KEY=$(aws secretsmanager get-secret-value --secret-id tars-api-key --query SecretString --output text)
```

### 4. Network Security
**Risk:** AI features send data to external API (Gemini)

**Mitigation:**
- Data is redacted before sending
- Can disable AI features by not setting GEMINI_API_KEY
- Review data being sent in logs
- Use in air-gapped environments without AI features

### 5. Audit and Compliance
**Risk:** Need to track who did what

**Mitigation:**
- Check audit log: `cat ~/.tars/audit.log`
- Integrate with your SIEM/logging system
- Regular audit log reviews

## 🔒 Best Practices

### 1. Least Privilege
```bash
# Create service account with minimal permissions
kubectl create serviceaccount tars-user
kubectl create rolebinding tars-user-binding \
  --clusterrole=view \
  --serviceaccount=default:tars-user
```

### 2. Separate Contexts
```bash
# Use separate kubeconfig for production
export KUBECONFIG=~/.kube/config-prod
tars context  # Verify before any operation
```

### 3. Read-Only Mode
```bash
# For monitoring, use read-only commands:
tars health
tars pods
tars events
tars analyze

# Avoid destructive commands in production:
# tars restart
# tars scale
# tars autofix
```

### 4. Audit Log Monitoring
```bash
# Monitor audit log
tail -f ~/.tars/audit.log

# Export to central logging
cat ~/.tars/audit.log | logger -t tars-cli
```

### 5. Secure API Keys
```bash
# Use AWS Secrets Manager
export GEMINI_API_KEY=$(aws secretsmanager get-secret-value \
  --secret-id tars-gemini-key \
  --query SecretString \
  --output text)

# Or HashiCorp Vault
export GEMINI_API_KEY=$(vault kv get -field=api_key secret/tars)
```

## 🚨 Security Checklist

Before using in production:

- [ ] Verify RBAC permissions are appropriate
- [ ] Test in non-production environment first
- [ ] Set up audit log monitoring
- [ ] Secure API key storage (not in shell history)
- [ ] Review and understand all commands
- [ ] Train team on confirmation prompts
- [ ] Set up alerting for destructive operations
- [ ] Regular security audits of audit.log
- [ ] Keep TARS CLI updated
- [ ] Review data sent to AI services

## 📋 Incident Response

If unauthorized action detected:

1. Check audit log: `cat ~/.tars/audit.log`
2. Identify user and action
3. Review Kubernetes audit logs
4. Revoke compromised credentials
5. Review RBAC permissions
6. Update security policies

## 🔐 Compliance

TARS CLI helps with:
- **SOC 2**: Audit logging, access controls
- **HIPAA**: Data encryption at rest (chmod 600)
- **PCI DSS**: Sensitive data redaction
- **GDPR**: Data minimization, secure storage

## 📞 Security Contact

For security issues:
- Email: orathore93@gmail.com
- GitHub: https://github.com/orathore93-hue/tars-cli/security

## 🔄 Updates

Keep TARS CLI updated for security patches:
```bash
pip install --upgrade tars-cli
tars version
```

---

**Remember:** Security is a shared responsibility. TARS CLI provides tools, but you must use them wisely.
