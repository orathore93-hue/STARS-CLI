"""Core monitoring commands"""
import logging
from typing import Optional
from .k8s_client import KubernetesClient
from .ai import analyzer
from .utils import (
    create_table, print_error, print_success, 
    print_info, format_pod_status, console
)
from .security import validate_namespace

logger = logging.getLogger(__name__)


class MonitoringCommands:
    """Kubernetes monitoring commands"""
    
    def __init__(self):
        try:
            self.k8s = KubernetesClient()
        except Exception as e:
            logger.error(f"Failed to initialize Kubernetes client: {e}")
            raise
    
    def health_check(self, namespace: Optional[str] = None):
        """Check cluster health"""
        try:
            print_info("Running health diagnostics...")
            
            # Get cluster data
            nodes = self.k8s.list_nodes()
            pods = self.k8s.list_pods(namespace)
            
            # Count statuses
            total_nodes = len(nodes)
            ready_nodes = sum(1 for n in nodes if self._is_node_ready(n))
            
            total_pods = len(pods)
            running_pods = sum(1 for p in pods if p.status.phase == "Running")
            failed_pods = sum(1 for p in pods if p.status.phase == "Failed")
            pending_pods = sum(1 for p in pods if p.status.phase == "Pending")
            
            # Create health table
            table = create_table("Cluster Health Report", ["Metric", "Value", "Status"])
            table.add_row("Nodes", f"{ready_nodes}/{total_nodes}", 
                         "✓" if ready_nodes == total_nodes else "⚠")
            table.add_row("Pods Running", f"{running_pods}/{total_pods}",
                         "✓" if running_pods == total_pods else "⚠")
            table.add_row("Failed Pods", str(failed_pods),
                         "✓" if failed_pods == 0 else "✗")
            table.add_row("Pending Pods", str(pending_pods),
                         "✓" if pending_pods == 0 else "⚠")
            
            console.print(table)
            
            # AI analysis
            if analyzer.is_available():
                health_data = {
                    "nodes": {"total": total_nodes, "ready": ready_nodes},
                    "pods": {"total": total_pods, "running": running_pods, 
                            "failed": failed_pods, "pending": pending_pods}
                }
                analysis = analyzer.analyze_cluster_health(health_data)
                print_info(f"AI Analysis: {analysis}")
            
        except Exception as e:
            print_error(f"Health check failed: {e}")
            logger.error(f"Health check error: {e}", exc_info=True)
    
    def list_pods(self, namespace: Optional[str] = None):
        """List pods with status"""
        try:
            if namespace and not validate_namespace(namespace):
                print_error(f"Invalid namespace: {namespace}")
                return
            
            pods = self.k8s.list_pods(namespace)
            
            table = create_table(
                f"Pods in {namespace or 'all namespaces'}", 
                ["Namespace", "Name", "Status", "Restarts", "Age"]
            )
            
            for pod in pods[:50]:  # Limit to 50 for performance
                restarts = sum(
                    c.restart_count for c in pod.status.container_statuses or []
                )
                age = self._calculate_age(pod.metadata.creation_timestamp)
                
                table.add_row(
                    pod.metadata.namespace,
                    pod.metadata.name,
                    format_pod_status(pod.status.phase),
                    str(restarts),
                    age
                )
            
            console.print(table)
            
            if len(pods) > 50:
                print_info(f"Showing 50 of {len(pods)} pods")
        
        except Exception as e:
            print_error(f"Failed to list pods: {e}")
            logger.error(f"List pods error: {e}", exc_info=True)
    
    def diagnose_pod(self, pod_name: str, namespace: str = "default"):
        """Diagnose pod issues"""
        try:
            if not validate_namespace(namespace):
                print_error(f"Invalid namespace: {namespace}")
                return
            
            print_info(f"Diagnosing {pod_name}...")
            
            pod = self.k8s.get_pod(pod_name, namespace)
            
            # Basic info
            console.print(f"\n[bold]Pod:[/bold] {pod.metadata.name}")
            console.print(f"[bold]Status:[/bold] {format_pod_status(pod.status.phase)}")
            console.print(f"[bold]Node:[/bold] {pod.spec.node_name}")
            
            # Container statuses
            if pod.status.container_statuses:
                console.print("\n[bold]Containers:[/bold]")
                for container in pod.status.container_statuses:
                    console.print(f"  • {container.name}: Ready={container.ready}, Restarts={container.restart_count}")
            
            # AI analysis
            if analyzer.is_available() and pod.status.phase != "Running":
                pod_data = {
                    "name": pod.metadata.name,
                    "status": pod.status.phase,
                    "containers": [
                        {"name": c.name, "ready": c.ready, "restarts": c.restart_count}
                        for c in (pod.status.container_statuses or [])
                    ]
                }
                analysis = analyzer.analyze_pod_issue(pod_data)
                console.print(f"\n[bold cyan]AI Analysis:[/bold cyan]\n{analysis}")
        
        except Exception as e:
            print_error(f"Diagnosis failed: {e}")
            logger.error(f"Diagnose error: {e}", exc_info=True)
    
    def _is_node_ready(self, node) -> bool:
        """Check if node is ready"""
        for condition in node.status.conditions or []:
            if condition.type == "Ready":
                return condition.status == "True"
        return False
    
    def _calculate_age(self, timestamp) -> str:
        """Calculate resource age"""
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        age = now - timestamp
        
        days = age.days
        hours = age.seconds // 3600
        minutes = (age.seconds % 3600) // 60
        
        if days > 0:
            return f"{days}d"
        elif hours > 0:
            return f"{hours}h"
        else:
            return f"{minutes}m"
