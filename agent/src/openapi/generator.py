"""
OpenAPI specification generator
"""
from typing import Dict, Any
from ...src.llm_client import LLMClient


class OpenAPISpecGenerator:
    """Generates OpenAPI specifications from code analysis"""
    
    def __init__(self):
        self.llm_client = LLMClient()
    
    def generate(self, code_analysis: Dict[str, Any]) -> str:
        """
        Generate OpenAPI specification from code analysis
        
        Args:
            code_analysis: Result from JavaAnalyzer
            
        Returns:
            OpenAPI specification in JSON format
        """
        return self.llm_client.generate_openapi_spec(code_analysis)