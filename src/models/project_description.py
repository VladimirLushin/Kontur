from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class ComponentDiagram(BaseModel):
    """Компонентная диаграмма в формате Mermaid"""
    mermaid_code: str
    description: str


class SequenceDiagram(BaseModel):
    """Диаграмма последовательности в формате Mermaid"""
    mermaid_code: str
    description: str


class OpenAPISpecification(BaseModel):
    """OpenAPI спецификация"""
    specification: Optional[Dict[str, Any]] = None
    endpoints: Optional[List[Dict[str, str]]] = None
    description: Optional[str] = None


class ProjectMetaDescription(BaseModel):
    """Метаописание проекта"""
    project_name: str
    technology_stack: List[str]
    purpose: str
    functionality: str
    entry_points: List[str]


class ProjectAnalysisResult(BaseModel):
    """Результат анализа проекта"""
    meta_description: ProjectMetaDescription
    component_diagram: Optional[ComponentDiagram] = None
    sequence_diagram: Optional[SequenceDiagram] = None
    openapi_specification: Optional[OpenAPISpecification] = None