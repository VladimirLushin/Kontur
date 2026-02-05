"""
Nodes for the LangGraph agent workflow
"""
import os
from typing import Dict, Any
from .graph_state import GraphState
from .git_handler import GitHandler
from .java_analyzer import JavaAnalyzer
from .components.generator import ComponentDiagramGenerator
from .behavior.generator import BehaviorDiagramGenerator
from .meta.generator import MetaDescriptionGenerator
from .openapi.generator import OpenAPISpecGenerator


def clone_repository(state: GraphState) -> Dict[str, Any]:
    """
    Node to clone the repository
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with local repository path
    """
    print("Cloning repository...")
    
    git_handler = GitHandler(
        username=os.getenv("GIT_USERNAME"), 
        password=os.getenv("GIT_PASSWORD")
    )
    
    try:
        local_path = git_handler.clone_repository(state["repo_url"])
        return {
            **state,
            "local_repo_path": local_path,
            "completed_tasks": state.get("completed_tasks", []) + ["clone_repository"]
        }
    except Exception as e:
        return {
            **state,
            "error": f"Error cloning repository: {str(e)}"
        }


def analyze_code(state: GraphState) -> Dict[str, Any]:
    """
    Node to analyze the Java code in the repository
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with code analysis
    """
    print("Analyzing code...")
    
    java_analyzer = JavaAnalyzer()
    
    try:
        code_analysis = java_analyzer.analyze_project(state["local_repo_path"])
        return {
            **state,
            "code_analysis": code_analysis,
            "completed_tasks": state.get("completed_tasks", []) + ["analyze_code"]
        }
    except Exception as e:
        return {
            **state,
            "error": f"Error analyzing code: {str(e)}"
        }


def generate_meta_description(state: GraphState) -> Dict[str, Any]:
    """
    Node to generate meta description
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with meta description
    """
    print("Generating meta description...")
    
    meta_generator = MetaDescriptionGenerator()
    
    try:
        meta_description = meta_generator.generate(state["code_analysis"])
        return {
            **state,
            "meta_description": meta_description,
            "completed_tasks": state.get("completed_tasks", []) + ["generate_meta_description"]
        }
    except Exception as e:
        return {
            **state,
            "error": f"Error generating meta description: {str(e)}"
        }


def generate_component_diagram(state: GraphState) -> Dict[str, Any]:
    """
    Node to generate component diagram
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with component diagram
    """
    print("Generating component diagram...")
    
    component_generator = ComponentDiagramGenerator()
    
    try:
        component_diagram = component_generator.generate(state["code_analysis"])
        return {
            **state,
            "component_diagram": component_diagram,
            "completed_tasks": state.get("completed_tasks", []) + ["generate_component_diagram"]
        }
    except Exception as e:
        return {
            **state,
            "error": f"Error generating component diagram: {str(e)}"
        }


def generate_behavior_diagram(state: GraphState) -> Dict[str, Any]:
    """
    Node to generate behavior diagram
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with behavior diagram
    """
    print("Generating behavior diagram...")
    
    behavior_generator = BehaviorDiagramGenerator()
    
    try:
        behavior_diagram = behavior_generator.generate(state["code_analysis"])
        return {
            **state,
            "behavior_diagram": behavior_diagram,
            "completed_tasks": state.get("completed_tasks", []) + ["generate_behavior_diagram"]
        }
    except Exception as e:
        return {
            **state,
            "error": f"Error generating behavior diagram: {str(e)}"
        }


def generate_openapi_spec(state: GraphState) -> Dict[str, Any]:
    """
    Node to generate OpenAPI specification
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with OpenAPI specification
    """
    print("Generating OpenAPI specification...")
    
    openapi_generator = OpenAPISpecGenerator()
    
    try:
        openapi_spec = openapi_generator.generate(state["code_analysis"])
        return {
            **state,
            "openapi_spec": openapi_spec,
            "completed_tasks": state.get("completed_tasks", []) + ["generate_openapi_spec"]
        }
    except Exception as e:
        return {
            **state,
            "error": f"Error generating OpenAPI spec: {str(e)}"
        }