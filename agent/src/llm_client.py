"""
LLM client for interacting with OpenRouter API
"""
import os
import openai
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    """Client for interacting with LLM via OpenRouter API"""
    
    def __init__(self):
        # Use OpenRouter API
        self.client = openai.OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )
        # Model identifier for Qwen Coder
        self.model = "qwen/qwen-2.5-coder-32b-instruct"
    
    def generate_response(self, prompt: str, max_tokens: int = 2048, temperature: float = 0.7) -> str:
        """
        Generate response from LLM
        
        Args:
            prompt: Input prompt for the model
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            
        Returns:
            Generated response text
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error calling LLM API: {str(e)}")
    
    def analyze_code_structure(self, code_analysis: Dict[str, Any]) -> Dict[str, str]:
        """
        Analyze code structure and generate documentation
        
        Args:
            code_analysis: Result from JavaAnalyzer
            
        Returns:
            Dictionary containing various documentation elements
        """
        # Generate meta description
        meta_description = self.generate_meta_description(code_analysis)
        
        # Generate component diagram
        component_diagram = self.generate_component_diagram(code_analysis)
        
        # Generate sequence diagram
        sequence_diagram = self.generate_sequence_diagram(code_analysis)
        
        # Generate OpenAPI spec if applicable
        openapi_spec = self.generate_openapi_spec(code_analysis)
        
        return {
            'meta_description': meta_description,
            'component_diagram': component_diagram,
            'sequence_diagram': sequence_diagram,
            'openapi_spec': openapi_spec
        }
    
    def generate_meta_description(self, code_analysis: Dict[str, Any]) -> str:
        """Generate meta description of the project"""
        prompt = f"""
        Analyze the following Java project structure and provide a meta description including:
        1. Technology stack
        2. Purpose of the project
        3. Main functionalities
        4. Architecture overview
        
        Project structure:
        {code_analysis}
        
        Provide a concise but comprehensive description.
        """
        return self.generate_response(prompt)
    
    def generate_component_diagram(self, code_analysis: Dict[str, Any]) -> str:
        """Generate Mermaid component diagram"""
        prompt = f"""
        Create a Mermaid component diagram for the following Java project structure.
        Show packages as containers and classes/interfaces inside them.
        Show dependencies between components with arrows.
        
        Project structure:
        {code_analysis}
        
        Format the response as a Mermaid diagram code block like:
        ```mermaid
        ...
        ```
        """
        response = self.generate_response(prompt)
        # Extract the mermaid code block
        if "```mermaid" in response and "```" in response:
            start_idx = response.find("```mermaid") + len("```mermaid")
            end_idx = response.find("```", start_idx)
            return response[start_idx:end_idx].strip()
        return response
    
    def generate_sequence_diagram(self, code_analysis: Dict[str, Any]) -> str:
        """Generate Mermaid sequence diagram"""
        prompt = f"""
        Create a Mermaid sequence diagram showing the main interactions in this Java project.
        Focus on the main entry points and how major components interact.
        
        Project structure:
        {code_analysis}
        
        Format the response as a Mermaid diagram code block like:
        ```mermaid
        ...
        ```
        """
        response = self.generate_response(prompt)
        # Extract the mermaid code block
        if "```mermaid" in response and "```" in response:
            start_idx = response.find("```mermaid") + len("```mermaid")
            end_idx = response.find("```", start_idx)
            return response[start_idx:end_idx].strip()
        return response
    
    def generate_openapi_spec(self, code_analysis: Dict[str, Any]) -> str:
        """Generate OpenAPI specification if the project contains APIs"""
        prompt = f"""
        Analyze the following Java project structure and generate an OpenAPI specification
        if it contains REST APIs or web services. Look for annotations like @RestController,
        @RequestMapping, @GetMapping, @PostMapping, etc.
        
        Project structure:
        {code_analysis}
        
        If the project does not appear to contain APIs, return an empty object.
        
        Format as a valid OpenAPI JSON specification.
        """
        return self.generate_response(prompt)