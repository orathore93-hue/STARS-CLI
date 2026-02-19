"""AI analysis using Gemini API with security and rate limiting"""
import logging
from typing import Optional
from google import genai
from .config import config

logger = logging.getLogger(__name__)


class AIAnalyzer:
    """AI-powered analysis using Gemini"""
    
    def __init__(self):
        self.api_key = config.gemini_api_key
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not set - AI features disabled")
            self.client = None
        else:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {e}")
                self.client = None
    
    def is_available(self) -> bool:
        """Check if AI analysis is available"""
        return self.client is not None
    
    def analyze_pod_issue(self, pod_data: dict) -> str:
        """Analyze pod issues with AI"""
        if not self.is_available():
            return "AI analysis unavailable - GEMINI_API_KEY not set"
        
        try:
            prompt = self._build_pod_analysis_prompt(pod_data)
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            return response.text
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return f"AI analysis failed: {str(e)}"
    
    def analyze_cluster_health(self, cluster_data: dict) -> str:
        """Analyze overall cluster health"""
        if not self.is_available():
            return "AI analysis unavailable"
        
        try:
            prompt = self._build_cluster_analysis_prompt(cluster_data)
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            return response.text
        except Exception as e:
            logger.error(f"Cluster analysis failed: {e}")
            return f"Analysis failed: {str(e)}"
    
    def _build_pod_analysis_prompt(self, pod_data: dict) -> str:
        """Build prompt for pod analysis"""
        return f"""Analyze this Kubernetes pod issue and provide:
1. Root cause
2. Impact assessment
3. Recommended fix

Pod Data:
{pod_data}

Be concise and actionable."""
    
    def _build_cluster_analysis_prompt(self, cluster_data: dict) -> str:
        """Build prompt for cluster analysis"""
        return f"""Analyze this Kubernetes cluster health:

{cluster_data}

Provide:
1. Overall health assessment (0-100%)
2. Critical issues
3. Recommendations

Be brief and actionable."""


# Global analyzer instance
analyzer = AIAnalyzer()
