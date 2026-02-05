"""
Meta description generator
"""
from typing import Dict, Any
from ...src.llm_client import LLMClient


class MetaDescriptionGenerator:
    """Generates meta descriptions from code analysis"""
    
    def __init__(self):
        self.llm_client = LLMClient()
    
    def generate(self, code_analysis: Dict[str, Any]) -> str:
        """
        Generate meta description from code analysis
        
        Args:
            code_analysis: Result from JavaAnalyzer
            
        Returns:
            Meta description text
        """
        return self.llm_client.generate_meta_description(code_analysis)