"""
LangGraph workflow definition for the documentation generator agent
"""
from langgraph.graph import StateGraph
from .src.nodes import (
    clone_repository, 
    analyze_code, 
    generate_meta_description, 
    generate_component_diagram,
    generate_behavior_diagram,
    generate_openapi_spec
)
from .src.edges import (
    route_after_clone,
    route_after_analysis,
    route_after_generation,
    route_to_finish
)
from .src.graph_state import GraphState


def create_agent_workflow():
    """
    Create the LangGraph workflow for the documentation generator agent
    
    Returns:
        Compiled LangGraph workflow
    """
    # Create a stateful graph
    workflow = StateGraph(GraphState)
    
    # Add nodes to the graph
    workflow.add_node("clone_repository", clone_repository)
    workflow.add_node("analyze_code", analyze_code)
    workflow.add_node("generate_meta_description", generate_meta_description)
    workflow.add_node("generate_component_diagram", generate_component_diagram)
    workflow.add_node("generate_behavior_diagram", generate_behavior_diagram)
    workflow.add_node("generate_openapi_spec", generate_openapi_spec)
    workflow.add_node("finish", lambda x: x)  # Terminal node
    workflow.add_node("error", lambda x: x)   # Error node
    
    # Set the starting point
    workflow.set_entry_point("clone_repository")
    
    # Add edges to the graph
    workflow.add_conditional_edges(
        "clone_repository",
        route_after_clone,
        {
            "analyze_code": "analyze_code",
            "error": "error"
        }
    )
    
    workflow.add_conditional_edges(
        "analyze_code",
        route_after_analysis,
        {
            "generate_meta_description": "generate_meta_description",
            "error": "error"
        }
    )
    
    # After generating meta description, continue with other generation tasks
    workflow.add_edge("generate_meta_description", "generate_component_diagram")
    workflow.add_edge("generate_component_diagram", "generate_behavior_diagram")
    workflow.add_edge("generate_behavior_diagram", "generate_openapi_spec")
    
    # Add conditional edge from openapi generation back to handle remaining tasks
    workflow.add_conditional_edges(
        "generate_openapi_spec",
        route_after_generation,
        {
            "generate_meta_description": "generate_meta_description",
            "generate_component_diagram": "generate_component_diagram",
            "generate_behavior_diagram": "generate_behavior_diagram",
            "generate_openapi_spec": "generate_openapi_spec",
            "finish": "finish"
        }
    )
    
    # Add edges to terminal nodes
    workflow.add_edge("finish", "__end__")
    workflow.add_edge("error", "__end__")
    
    # Compile the workflow
    return workflow.compile()