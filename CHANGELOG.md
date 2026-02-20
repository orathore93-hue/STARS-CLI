# Changelog

All notable changes to STARS CLI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- OS keychain integration for secure API key storage
- Binary release automation with checksum verification
- DevSecOps pipeline with dependency hashing
- Comprehensive security documentation
- CLI test suite with 26 command validations

### Security
- SHA-256 checksum verification for binary downloads
- Pinned GitHub Actions to commit SHAs
- Hashed dependency requirements (pip --require-hashes)
- Secure credential storage (macOS Keychain, Windows Credential Manager, Linux Secret Service)

## [0.1.0] - 2026-02-21

### Added
- Initial release of STARS CLI
- Kubernetes cluster management commands
- AI-powered diagnostics with Gemini integration
- SRE incident management
- Health monitoring and analysis
- Pod, deployment, service, and node management
- Event monitoring and triage
- Crashloop detection and remediation
- Security scanning capabilities
- On-call reporting tools

### Security
- API key encryption in OS keychain
- Fallback to chmod 600 local file storage
- Environment variable support for CI/CD
- No hardcoded credentials in codebase

[Unreleased]: https://github.com/orathore93-hue/STARS-CLI/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/orathore93-hue/STARS-CLI/releases/tag/v0.1.0
