"""Kubernetes API client wrapper with security and error handling"""
from kubernetes import client, config as k8s_config
from kubernetes.client.rest import ApiException
import logging
from typing import Optional, List, Dict, Any
from functools import wraps
import time

logger = logging.getLogger(__name__)


def retry_on_failure(max_retries: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except ApiException as e:
                    if attempt == max_retries - 1:
                        raise
                    if e.status in [429, 500, 502, 503, 504]:
                        delay = backoff * (2 ** attempt)
                        logger.warning(f"API call failed, retrying in {delay}s...")
                        time.sleep(delay)
                    else:
                        raise
            return None
        return wrapper
    return decorator


class KubernetesClient:
    """Kubernetes API client with security and error handling"""
    
    def __init__(self):
        try:
            k8s_config.load_kube_config()
        except Exception as e:
            logger.error(f"Failed to load kubeconfig: {e}")
            raise
        
        self.core_v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
        self.auth_v1 = client.AuthorizationV1Api()
    
    @retry_on_failure()
    def list_pods(self, namespace: Optional[str] = None) -> List[Any]:
        """List pods in namespace or all namespaces"""
        try:
            if namespace:
                return self.core_v1.list_namespaced_pod(namespace).items
            return self.core_v1.list_pod_for_all_namespaces().items
        except ApiException as e:
            logger.error(f"Failed to list pods: {e}")
            raise
    
    @retry_on_failure()
    def get_pod(self, name: str, namespace: str = "default") -> Any:
        """Get specific pod"""
        try:
            return self.core_v1.read_namespaced_pod(name, namespace)
        except ApiException as e:
            logger.error(f"Failed to get pod {name}: {e}")
            raise
    
    @retry_on_failure()
    def list_nodes(self) -> List[Any]:
        """List all nodes"""
        try:
            return self.core_v1.list_node().items
        except ApiException as e:
            logger.error(f"Failed to list nodes: {e}")
            raise
    
    @retry_on_failure()
    def list_deployments(self, namespace: Optional[str] = None) -> List[Any]:
        """List deployments"""
        try:
            if namespace:
                return self.apps_v1.list_namespaced_deployment(namespace).items
            return self.apps_v1.list_deployment_for_all_namespaces().items
        except ApiException as e:
            logger.error(f"Failed to list deployments: {e}")
            raise
    
    @retry_on_failure()
    def list_namespaces(self) -> List[Any]:
        """List all namespaces"""
        try:
            return self.core_v1.list_namespace().items
        except ApiException as e:
            logger.error(f"Failed to list namespaces: {e}")
            raise
    
    @retry_on_failure()
    def get_pod_logs(self, name: str, namespace: str = "default", tail_lines: int = 100) -> str:
        """Get pod logs"""
        try:
            return self.core_v1.read_namespaced_pod_log(
                name, namespace, tail_lines=tail_lines
            )
        except ApiException as e:
            logger.error(f"Failed to get logs for {name}: {e}")
            raise
    
    @retry_on_failure()
    def delete_pod(self, name: str, namespace: str = "default"):
        """Delete a pod"""
        try:
            return self.core_v1.delete_namespaced_pod(name, namespace)
        except ApiException as e:
            logger.error(f"Failed to delete pod {name}: {e}")
            raise
    
    def check_rbac_permission(self, verb: str, resource: str, namespace: str = "") -> bool:
        """Check if user has RBAC permission"""
        try:
            review = client.V1SelfSubjectAccessReview(
                spec=client.V1SelfSubjectAccessReviewSpec(
                    resource_attributes=client.V1ResourceAttributes(
                        verb=verb,
                        resource=resource,
                        namespace=namespace
                    )
                )
            )
            result = self.auth_v1.create_self_subject_access_review(review)
            return result.status.allowed
        except Exception as e:
            logger.warning(f"RBAC check failed: {e}")
            return False
    
    @retry_on_failure()
    def get_pod_logs(self, name: str, namespace: str, tail: int = 50):
        """Get pod logs"""
        try:
            return self.core_v1.read_namespaced_pod_log(name, namespace, tail_lines=tail)
        except ApiException as e:
            logger.error(f"Failed to get logs for {name}: {e}")
            raise
    
    @retry_on_failure()
    def list_events(self, namespace: str = "default"):
        """List events in namespace"""
        try:
            events = self.core_v1.list_namespaced_event(namespace)
            return sorted(events.items, key=lambda x: x.last_timestamp or x.event_time, reverse=True)
        except ApiException as e:
            logger.error(f"Failed to list events: {e}")
            raise
    
    @retry_on_failure()
    def list_deployments(self, namespace: str = "default"):
        """List deployments"""
        try:
            return self.apps_v1.list_namespaced_deployment(namespace).items
        except ApiException as e:
            logger.error(f"Failed to list deployments: {e}")
            raise
    
    @retry_on_failure()
    def list_services(self, namespace: str = "default"):
        """List services"""
        try:
            return self.core_v1.list_namespaced_service(namespace).items
        except ApiException as e:
            logger.error(f"Failed to list services: {e}")
            raise
