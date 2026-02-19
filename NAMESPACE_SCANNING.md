# Namespace Scanning Feature

## Overview
TARS CLI now scans **all namespaces** by default for comprehensive cluster monitoring. This enables SREs and on-call engineers to detect issues across the entire cluster without manually specifying each namespace.

## Changes Made

### 1. `tars spike` - Real-time Resource Spike Monitoring
**Before:** Monitored only the `default` namespace
**After:** Monitors all namespaces by default

```bash
# Monitor all namespaces (new default behavior)
tars spike

# Monitor specific namespace (optional)
tars spike --namespace production
```

**Key Changes:**
- Scans all namespaces for CPU/Memory spikes
- Shows pod names with namespace prefix: `namespace/pod-name`
- Detects resource spikes across entire cluster

---

### 2. `tars oncall` - On-Call Dashboard
**Before:** Showed issues only in `default` namespace
**After:** Shows critical issues across all namespaces

```bash
# View all namespaces (new default behavior)
tars oncall

# View specific namespace (optional)
tars oncall --namespace production
```

**Key Changes:**
- Aggregates critical issues (CrashLoopBackOff, OOMKilled, Pending, Failed) from all namespaces
- Displays deployments with namespace column
- Shows recent warning events from all namespaces with namespace context
- Limits display to top 10 deployments and 5 recent warnings for readability

---

### 3. `tars triage` - Incident Triage
**Before:** Triaged issues in `default` namespace only
**After:** Performs cluster-wide incident triage

```bash
# Triage all namespaces (new default behavior)
tars triage

# Triage specific namespace (optional)
tars triage --namespace production
```

**Key Changes:**
- Scans all namespaces for critical pod issues
- Shows pod names with namespace prefix: `namespace/pod-name`
- Provides comprehensive incident summary across entire cluster

---

### 4. `tars alert` - Real-time Alerting
**Before:** Monitored only `default` namespace
**After:** Monitors all namespaces for alerts

```bash
# Monitor all namespaces (new default behavior)
tars alert

# Monitor specific namespace (optional)
tars alert --namespace production
```

**Key Changes:**
- Monitors all namespaces for pod restarts, failures, and pending states
- Shows alerts with namespace prefix: `namespace/pod-name`
- Provides cluster-wide alerting capability

---

### 5. `tars watch` - Real-time Pod Monitoring Dashboard
**Before:** Watched only `default` namespace (required `--all-namespaces` flag)
**After:** Watches all namespaces by default

```bash
# Watch all namespaces (new default behavior)
tars watch

# Watch specific namespace (optional)
tars watch --namespace production

# Watch multiple specific namespaces
tars watch --namespaces "production,staging,dev"
```

**Key Changes:**
- Default behavior now watches all namespaces
- Shows namespace column automatically when monitoring multiple namespaces
- `--all-namespaces` flag deprecated (now default behavior)
- Backward compatible with `--namespace` for single namespace monitoring

---

## Benefits

1. **Complete Visibility**: No more blind spots - see issues across all namespaces
2. **Faster Incident Response**: Detect problems immediately without namespace guessing
3. **Backward Compatible**: Can still monitor specific namespaces with `--namespace` flag
4. **Production Ready**: Handles namespace access errors gracefully with try/except blocks
5. **Scalable**: Limits output (e.g., top 10 deployments) to prevent information overload

## Usage Examples

### Monitor entire cluster for spikes
```bash
tars spike --cpu-threshold 2.0 --memory-threshold 2000
```

### Quick cluster health check
```bash
tars oncall
```

### Triage all incidents cluster-wide
```bash
tars triage
```

### Set up cluster-wide alerting
```bash
tars alert --interval 60
```

### Watch all pods in real-time
```bash
tars watch
```

### Monitor specific namespace (legacy behavior)
```bash
tars spike --namespace production
tars oncall --namespace kube-system
tars triage --namespace default
tars watch --namespace production
```

## Technical Implementation

- Uses `v1.list_namespace()` to get all namespaces dynamically
- Iterates through namespaces with error handling for RBAC restrictions
- Displays namespace context in output (e.g., `namespace/pod-name`)
- Maintains backward compatibility with `--namespace` flag
- Default value changed from `"default"` to `None` to trigger all-namespace scanning

## Testing

Syntax validation passed:
```bash
python3 -m py_compile tars.py
# Exit status: 0 (success)
```

## Next Steps

Consider adding:
- Namespace filtering with regex patterns
- Exclude system namespaces option (e.g., `--exclude-system`)
- Export monitoring data to JSON/CSV for analysis
- Integration with Prometheus for historical metrics
