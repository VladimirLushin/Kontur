"""
Component diagram generator
"""
from typing import Dict, Any
from ...src.llm_client import LLMClient


class ComponentDiagramGenerator:
    """Generates component diagrams from code analysis"""
    
    def __init__(self):
        self.llm_client = LLMClient()
    
    def generate(self, code_analysis: Dict[str, Any]) -> str:
        """
        Generate component diagram from code analysis
        
        Args:
            code_analysis: Result from JavaAnalyzer
            
        Returns:
            Component diagram in Mermaid format
        """
        return self.llm_client.generate_component_diagram(code_analysis)