# RBAC Requirements for TARS CLI

## Overview
TARS CLI requires specific Kubernetes RBAC permissions to function. This document outlines the minimum required permissions for each command.

## Minimum Required Permissions

### Read-Only Operations
Commands: `status`, `health`, `logs`, `describe`, `top`, `events`

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: tars-readonly
rules:
- apiGroups: [""]
  resources:
    - pods
    - pods/log
    - nodes
    - events
    - namespaces
    - services
    - configmaps
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources:
    - deployments
    - replicasets
    - statefulsets
    - daemonsets
  verbs: ["get", "list", "watch"]
- apiGroups: ["metrics.k8s.io"]
  resources:
    - pods
    - nodes
  verbs: ["get", "list"]
```

### Write Operations
Commands: `restart`, `scale`, `apply`, `delete`, `drain`

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: tars-operator
rules:
- apiGroups: [""]
  resources:
    - pods
    - pods/eviction
  verbs: ["get", "list", "delete", "create"]
- apiGroups: ["apps"]
  resources:
    - deployments
    - replicasets
    - statefulsets
  verbs: ["get", "list", "patch", "update"]
- apiGroups: [""]
  resources:
    - nodes
  verbs: ["get", "list", "patch", "update"]
```

### Full Access (Recommended for Admins)
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: tars-admin
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["*"]
```

## Permission Checks by Command

| Command | Required Verbs | Resources |
|---------|---------------|-----------|
| `tars status` | get, list | pods, deployments |
| `tars health` | get, list | pods, nodes |
| `tars logs` | get, list | pods, pods/log |
| `tars restart` | get, delete | pods |
| `tars scale` | get, patch | deployments |
| `tars delete` | get, delete | pods, deployments, services |
| `tars apply` | create, patch | * |
| `tars drain` | get, patch, delete | nodes, pods |

## Setup Instructions

### 1. Create Service Account
```bash
kubectl create serviceaccount tars-user -n default
```

### 2. Bind Role
```bash
# For read-only access
kubectl create clusterrolebinding tars-readonly-binding \
  --clusterrole=tars-readonly \
  --serviceaccount=default:tars-user

# For operator access
kubectl create clusterrolebinding tars-operator-binding \
  --clusterrole=tars-operator \
  --serviceaccount=default:tars-user
```

### 3. Get Token
```bash
kubectl create token tars-user -n default
```

### 4. Configure kubeconfig
```bash
kubectl config set-credentials tars-user --token=<token>
kubectl config set-context tars-context \
  --cluster=<cluster-name> \
  --user=tars-user
kubectl config use-context tars-context
```

## Permission Validation

TARS CLI automatically checks permissions before destructive operations. To manually verify:

```bash
# Check if you can delete pods
kubectl auth can-i delete pods

# Check specific namespace
kubectl auth can-i delete pods -n production

# Check all permissions
kubectl auth can-i --list
```

## Troubleshooting

### "Forbidden" Errors
```
Error: pods "my-pod" is forbidden: User cannot delete resource "pods"
```

**Solution:** Request additional RBAC permissions from your cluster administrator.

### Missing Metrics
```
Warning: Unable to fetch metrics - permission denied
```

**Solution:** Ensure metrics-server is installed and you have `get` permissions on `metrics.k8s.io` resources.

## Security Best Practices

1. **Principle of Least Privilege**: Grant only the minimum required permissions
2. **Namespace Scoping**: Use `Role` instead of `ClusterRole` when possible
3. **Regular Audits**: Review and rotate service account tokens
4. **Separate Accounts**: Use different service accounts for different environments (dev/staging/prod)

## Example: Production Setup

```yaml
# Read-only for developers
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: tars-dev
  namespace: production
rules:
- apiGroups: ["", "apps"]
  resources: ["pods", "deployments", "pods/log"]
  verbs: ["get", "list", "watch"]
---
# Operator access for SRE team
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: tars-sre
  namespace: production
rules:
- apiGroups: ["", "apps"]
  resources: ["pods", "deployments"]
  verbs: ["get", "list", "delete", "patch"]
```
