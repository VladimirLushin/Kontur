"""
Behavior diagram generator
"""
from typing import Dict, Any
from ...src.llm_client import LLMClient


class BehaviorDiagramGenerator:
    """Generates behavior diagrams from code analysis"""
    
    def __init__(self):
        self.llm_client = LLMClient()
    
    def generate(self, code_analysis: Dict[str, Any]) -> str:
        """
        Generate behavior diagram from code analysis
        
        Args:
            code_analysis: Result from JavaAnalyzer
            
        Returns:
            Behavior diagram in Mermaid format
        """
        return self.llm_client.generate_sequence_diagram(code_analysis)