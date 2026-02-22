# 🚀 STARS CLI - Complete SRE Features Guide

## ✅ Implemented Features

### 📊 Real-Time Monitoring

```bash
# Live pod monitoring
stars watch

# Resource spike detection
stars spike

# Custom alerting with thresholds
stars alert --threshold-cpu 80 --threshold-memory 85 --interval 30

# Cluster health pulse
stars pulse

# Timeline of recent events
stars timeline

# Top resource consumers
stars top

# Heatmap visualization
stars heatmap
```

### 🔧 Auto-Remediation

```bash
# Auto-fix common issues (dry-run by default)
stars autofix

# AI-powered smart scaling
stars smart-scale <deployment>

# Quick restart
stars restart <pod-name>

# Fix crashloop issues
stars crashloop <pod-name>

# Clear evicted pods
stars clear-evicted
```

### 📸 Incident Documentation

```bash
# Take complete cluster snapshot
stars snapshot

# Generate runbook for any pod
stars runbook <pod-name>

# Create incident report with AI analysis
stars incident-report

# Show cluster story - what happened today?
stars story

# Incident management
stars incident start --title "Issue" --severity high
stars incident log "Action taken"
stars incident close "Resolved"
```

### 🔍 Advanced Analysis

```bash
# Blast radius analysis
stars blast <pod-name>

# Predict future issues
stars forecast

# Chaos engineering insights
stars chaos

# Compare two clusters
stars diff <context1> <context2>

# Diagnose pod issues
stars diagnose <pod-name>

# Analyze errors
stars errors

# Triage issues
stars triage

# Bottleneck detection
stars bottleneck
```

### 📈 SRE Metrics

```bash
# Service Level Objectives
stars slo

# Service Level Indicators
stars sli

# Resource usage comparison
stars compare

# Top resource consumers
stars top

# Cost analysis
stars cost

# Compliance checks
stars compliance
```

### 🔥 Prometheus Integration

```bash
# Check Prometheus connection
stars prom-check --url http://prometheus.example.com:9090

# View metrics dashboard
stars prom-dashboard --namespace production

# Check specific pod metrics
stars prom-metrics --namespace production --pod api-server-xyz

# Monitor active alerts
stars prom-alerts

# Run custom PromQL queries
stars prom-query 'rate(http_requests_total[5m])'
stars prom-query 'container_memory_usage_bytes{namespace="production"}'

# Compare metrics
stars prom-compare

# Export metrics
stars prom-export

# Record rules
stars prom-record
```

### 🎯 Core Operations

```bash
# Cluster health
stars health

# List resources
stars pods
stars nodes
stars deployments
stars services
stars namespaces

# Logs and events
stars logs <pod-name>
stars events
stars aggregate-logs

# Resource management
stars scale <deployment> --replicas 3
stars cordon <node>
stars uncordon <node>
stars drain <node>

# Execute commands
stars exec <pod-name> <command>
stars port-forward <pod-name> 8080:80

# Apply/Delete resources
stars apply -f manifest.yaml
stars delete -f manifest.yaml
```

### 🔒 Security & Compliance

```bash
# Security scanning
stars security-scan

# Audit logs
stars audit

# Privacy settings
stars privacy

# Network policies
stars network
```

### 📊 Advanced Features

```bash
# Multi-cluster management
stars multi-cluster

# Benchmarking
stars benchmark

# Cardinality analysis
stars cardinality
stars cardinality-labels

# OOM analysis
stars oom

# Pending pods
stars pending

# Resource quotas
stars quota

# Volume analysis
stars volumes

# Ingress status
stars ingress

# CRDs
stars crds

# ConfigMaps & Secrets
stars configmaps
stars secrets

# Trace analysis
stars trace

# Replay events
stars replay

# Profile pods
stars profile <pod-name>

# Export data
stars export
```

### 🎓 Utility Commands

```bash
# Setup and configuration
stars init
stars setup
stars set-api-key
stars delete-api-key

# Information
stars version
stars welcome
stars creator
stars quote
stars humor

# Context management
stars context

# Alert management
stars alert-history
stars alert-webhook

# Describe resources
stars describe <resource> <name>

# Create resources
stars create <resource>

# Dashboard
stars dashboard

# On-call dashboard
stars oncall
```

---

## 🎓 Real-World SRE Scenarios

### Scenario 1: 3 AM Page - Pod CrashLooping

```bash
# Quick triage
stars triage
# Shows: CrashLoopBackOff detected in payment-service

# Deep diagnosis
stars diagnose payment-service
# AI analysis: "OOMKilled - memory limit too low"

# Check blast radius
stars blast payment-service
# Shows: Affects checkout flow, 3 dependent services

# Auto-fix
stars autofix
# Recommendation: Increase memory limit to 512Mi

# Generate incident report
stars incident-report
```

### Scenario 2: Proactive Monitoring

```bash
# Start alert monitoring
stars alert --threshold-cpu 80 --threshold-memory 85

# In another terminal, watch for spikes
stars spike

# Check SLO compliance
stars slo

# Monitor cluster pulse
stars pulse
```

### Scenario 3: Capacity Planning

```bash
# Take snapshot for analysis
stars snapshot

# Compare production vs staging
stars diff prod-context staging-context

# Forecast future issues
stars forecast

# Analyze costs
stars cost

# Check resource quotas
stars quota
```

### Scenario 4: Multi-Cluster Management

```bash
# Compare clusters
stars diff us-east-1 us-west-2

# Switch context and check health
stars context
stars health

# Multi-cluster dashboard
stars multi-cluster
```

### Scenario 5: Prometheus Metrics Analysis

```bash
# Check Prometheus connection
stars prom-check --url http://prometheus.example.com:9090

# View metrics dashboard
stars prom-dashboard --namespace production

# Check specific pod metrics
stars prom-metrics --namespace production --pod api-server-xyz

# Monitor active alerts
stars prom-alerts

# Run custom PromQL queries
stars prom-query 'rate(http_requests_total[5m])'
stars prom-query 'container_memory_usage_bytes{namespace="production"}'

# Compare metrics between environments
stars prom-compare
```

### Scenario 6: Incident Management

```bash
# Start incident
stars incident start --title "API Gateway Down" --severity critical

# Log actions
stars incident log "Restarted api-gateway pods" --resource api-gateway
stars incident log "Checked database connections"
stars incident log "Scaled up to 5 replicas"

# Close incident
stars incident close "Issue resolved - increased memory limits"

# Generate report
stars incident-report
```

### Scenario 7: Security Audit

```bash
# Run security scan
stars security-scan

# Check compliance
stars compliance

# Review audit logs
stars audit

# Check network policies
stars network
```

### Scenario 8: Performance Optimization

```bash
# Identify bottlenecks
stars bottleneck

# Analyze top consumers
stars top

# Check OOM issues
stars oom

# Profile specific pod
stars profile api-server-xyz

# Benchmark performance
stars benchmark
```

---

## 📊 Command Summary

**Total Commands:** 100+

**Categories:**
- 📊 Monitoring: 15+ commands
- 🔧 Remediation: 10+ commands
- 📸 Documentation: 8+ commands
- 🔍 Analysis: 12+ commands
- 📈 Metrics: 10+ commands
- 🔥 Prometheus: 8+ commands
- 🎯 Core Ops: 20+ commands
- 🔒 Security: 5+ commands
- 📊 Advanced: 15+ commands
- 🎓 Utility: 10+ commands

---

## 🚀 Getting Started

```bash
# Install
curl -sSL https://raw.githubusercontent.com/orathore93-hue/STARS-CLI/main/install.sh | bash

# Setup
stars init

# Start monitoring
stars health
stars watch
stars oncall
```

---

**All features are production-ready and tested!** ✅
