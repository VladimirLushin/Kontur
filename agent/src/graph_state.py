"""
Graph state definition for the LangGraph agent
"""
from typing import Dict, Any, TypedDict


class GraphState(TypedDict):
    """
    Defines the state structure for the LangGraph agent
    """
    repo_url: str
    local_repo_path: str
    code_analysis: Dict[str, Any]
    meta_description: str
    component_diagram: str
    behavior_diagram: str
    openapi_spec: str
    error: str
    completed_tasks: list[str]