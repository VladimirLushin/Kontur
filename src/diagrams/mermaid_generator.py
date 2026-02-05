"""Mermaid diagram generator for UML diagrams."""
from typing import Dict, List


class MermaidGenerator:
    """Generate Mermaid diagrams from parsed code structure."""
    
    def __init__(self):
        pass
    
    def generate_class_diagram(self, classes: List[Dict]) -> str:
        """Generate a Mermaid class diagram from class definitions."""
        diagram = "```mermaid\nclassDiagram\n"
        
        # Define classes and their relationships
        for cls in classes:
            class_name = cls.get('name', 'Unknown')
            
            # Add class definition
            diagram += f"    class {class_name} {{\n"
            
            # Add fields
            for field in cls.get('fields', []):
                field_name = field.get('name', '')
                field_type = field.get('type', 'unknown')
                diagram += f"        + {field_type} {field_name}\n"
            
            # Add methods
            for method in cls.get('methods', []):
                method_name = method.get('name', '')
                return_type = method.get('return_type', 'void')
                params = ", ".join([f"{param[0]} {param[1]}" for param in method.get('parameters', [])])
                diagram += f"        + {return_type} {method_name}({params})\n"
            
            diagram += "    }\n"
        
        # Add inheritance relationships
        for cls in classes:
            class_name = cls.get('name', 'Unknown')
            extends = cls.get('extends')
            if extends:
                diagram += f"    {extends} <|-- {class_name}\n"
            
            implements_list = cls.get('implements', [])
            for impl in implements_list:
                diagram += f"    {impl} <|.. {class_name}\n"
        
        diagram += "```"
        return diagram
    
    def generate_sequence_diagram(self, interactions: List[Dict]) -> str:
        """Generate a Mermaid sequence diagram from interaction data."""
        diagram = "```mermaid\nsequenceDiagram\n"
        
        # Extract participants from interactions
        participants = set()
        for interaction in interactions:
            participants.add(interaction.get('source', 'Unknown'))
            participants.add(interaction.get('target', 'Unknown'))
        
        # Add participants
        for participant in participants:
            diagram += f"    participant {participant}\n"
        
        # Add interactions
        for interaction in interactions:
            source = interaction.get('source', 'Unknown')
            target = interaction.get('target', 'Unknown')
            message = interaction.get('message', 'call')
            diagram += f"    {source}->>{target}: {message}\n"
        
        diagram += "```"
        return diagram