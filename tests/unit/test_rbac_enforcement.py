"""
Test RBAC enforcement for destructive operations
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from tars.k8s_client import K8sClient


class TestRBACEnforcement:
    """Test RBAC permission checks before destructive operations"""
    
    @patch('tars.k8s_client.config')
    @patch('tars.k8s_client.client')
    def test_delete_pod_requires_permission(self, mock_client, mock_config):
        """Test that delete_pod checks RBAC permission"""
        k8s = K8sClient()
        k8s.check_rbac_permission = Mock(return_value=False)
        
        with pytest.raises(PermissionError, match="No permission to delete pods"):
            k8s.delete_pod("test-pod", "default")
    
    @patch('tars.k8s_client.config')
    @patch('tars.k8s_client.client')
    def test_delete_pod_with_permission(self, mock_client, mock_config):
        """Test that delete_pod succeeds with permission"""
        k8s = K8sClient()
        k8s.check_rbac_permission = Mock(return_value=True)
        k8s.core_v1.delete_namespaced_pod = Mock()
        
        k8s.delete_pod("test-pod", "default")
        k8s.core_v1.delete_namespaced_pod.assert_called_once_with("test-pod", "default")
    
    @patch('tars.k8s_client.config')
    @patch('tars.k8s_client.client')
    def test_restart_requires_permission(self, mock_client, mock_config):
        """Test that restart_resource checks RBAC permission"""
        k8s = K8sClient()
        k8s.check_rbac_permission = Mock(return_value=False)
        
        with pytest.raises(PermissionError, match="No permission to patch"):
            k8s.restart_resource("deployment", "test-deploy", "default")
    
    @patch('tars.k8s_client.config')
    @patch('tars.k8s_client.client')
    def test_scale_requires_permission(self, mock_client, mock_config):
        """Test that scale_resource checks RBAC permission"""
        k8s = K8sClient()
        k8s.check_rbac_permission = Mock(return_value=False)
        
        with pytest.raises(PermissionError, match="No permission to patch"):
            k8s.scale_resource("deployment", "test-deploy", 3, "default")
    
    @patch('tars.k8s_client.config')
    @patch('tars.k8s_client.client')
    def test_drain_requires_multiple_permissions(self, mock_client, mock_config):
        """Test that drain_node checks both node and pod permissions"""
        k8s = K8sClient()
        
        # Test missing node permission
        k8s.check_rbac_permission = Mock(side_effect=[False, True])
        with pytest.raises(PermissionError, match="No permission to patch nodes"):
            k8s.drain_node("test-node", False)
        
        # Test missing pod permission
        k8s.check_rbac_permission = Mock(side_effect=[True, False])
        with pytest.raises(PermissionError, match="No permission to delete pods"):
            k8s.drain_node("test-node", False)
    
    @patch('tars.k8s_client.config')
    @patch('tars.k8s_client.client')
    def test_delete_from_yaml_checks_each_resource(self, mock_client, mock_config):
        """Test that delete_from_yaml checks permission for each resource"""
        k8s = K8sClient()
        
        # Mock permission check to deny deployments but allow pods
        def permission_check(verb, resource, ns):
            return resource == "pods"
        
        k8s.check_rbac_permission = Mock(side_effect=permission_check)
        
        yaml_content = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-deploy
---
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
"""
        
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = yaml_content
            with patch('yaml.safe_load_all') as mock_yaml:
                mock_yaml.return_value = [
                    {'kind': 'Deployment', 'metadata': {'name': 'test-deploy'}},
                    {'kind': 'Pod', 'metadata': {'name': 'test-pod'}}
                ]
                
                k8s.core_v1.delete_namespaced_pod = Mock()
                results = k8s.delete_from_yaml('/tmp/test.yaml')
                
                # Should have permission_denied for deployment
                assert any(r['status'] == 'permission_denied' and r['kind'] == 'Deployment' 
                          for r in results)
                
                # Should successfully delete pod
                k8s.core_v1.delete_namespaced_pod.assert_called()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
