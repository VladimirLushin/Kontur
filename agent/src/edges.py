"""
Edges for the LangGraph agent workflow
"""
from .graph_state import GraphState


def route_after_clone(state: GraphState) -> str:
    """
    Route to next step after cloning repository
    
    Args:
        state: Current graph state
        
    Returns:
        Next node to execute
    """
    if state.get("error"):
        return "error"
    else:
        return "analyze_code"


def route_after_analysis(state: GraphState) -> str:
    """
    Route to next step after code analysis
    
    Args:
        state: Current graph state
        
    Returns:
        Next node to execute
    """
    if state.get("error"):
        return "error"
    else:
        return "generate_meta_description"


def route_after_generation(state: GraphState) -> str:
    """
    Route to next generation step or finish
    
    Args:
        state: Current graph state
        
    Returns:
        Next node to execute
    """
    if state.get("error"):
        return "error"
    
    completed = set(state.get("completed_tasks", []))
    
    # Check which generation tasks are left
    if "generate_meta_description" not in completed:
        return "generate_meta_description"
    elif "generate_component_diagram" not in completed:
        return "generate_component_diagram"
    elif "generate_behavior_diagram" not in completed:
        return "generate_behavior_diagram"
    elif "generate_openapi_spec" not in completed:
        return "generate_openapi_spec"
    else:
        # All generation tasks are complete
        return "finish"


def route_to_finish(state: GraphState) -> str:
    """
    Route to finish node
    
    Args:
        state: Current graph state
        
    Returns:
        Next node to execute
    """
    return "finish"