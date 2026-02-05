"""
Main entry point for the LangGraph agent that coordinates the generation of:
- Component diagrams
- Behavioral diagrams
- Meta descriptions
- OpenAPI specifications
"""
import os
from dotenv import load_dotenv
from .workflow import create_agent_workflow
from .src.graph_state import GraphState


def main():
    print("Starting LangGraph agent for generating component diagrams, behavioral diagrams, meta descriptions, and OpenAPI specifications...")
    
    # Load environment variables
    load_dotenv()
    
    # Initialize the workflow
    workflow = create_agent_workflow()
    
    # Define the initial state
    initial_state: GraphState = {
        "repo_url": os.getenv("REPO_URL", "https://github.com/example/repo.git"),
        "local_repo_path": "",
        "code_analysis": {},
        "meta_description": "",
        "component_diagram": "",
        "behavior_diagram": "",
        "openapi_spec": "",
        "error": "",
        "completed_tasks": []
    }
    
    try:
        # Run the workflow
        final_state = workflow.invoke(initial_state)
        
        # Output results
        print("\n=== FINAL STATE ===")
        print(f"Repository URL: {final_state['repo_url']}")
        print(f"Local Repository Path: {final_state['local_repo_path']}")
        print(f"Code Analysis Summary: Found {len(final_state['code_analysis'].get('classes', {}))} classes, {len(final_state['code_analysis'].get('interfaces', {}))} interfaces, and {len(final_state['code_analysis'].get('packages', {}))} packages.")
        print(f"Completed Tasks: {final_state['completed_tasks']}")
        
        if final_state.get('error'):
            print(f"Error occurred: {final_state['error']}")
        else:
            print("\n=== META DESCRIPTION ===")
            print(final_state['meta_description'])
            print("\n=== COMPONENT DIAGRAM ===")
            print(final_state['component_diagram'])
            print("\n=== BEHAVIOR DIAGRAM ===")
            print(final_state['behavior_diagram'])
            print("\n=== OPENAPI SPECIFICATION ===")
            print(final_state['openapi_spec'])
        
    except Exception as e:
        print(f"Error during workflow execution: {str(e)}")


if __name__ == "__main__":
    main()