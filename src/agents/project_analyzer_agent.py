from langgraph.graph import END, START, StateGraph
from typing import Dict, Any, List
from src.models.project_description import ProjectAnalysisResult, ProjectMetaDescription
from src.utils.java_analyzer import JavaAnalyzer
from src.diagrams.generator import DiagramGenerator
from src.utils.repo_loader import RepoLoader


class ProjectAnalyzerAgent:
    """
    Агент для анализа проектов с использованием LangGraph
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.java_analyzer = JavaAnalyzer()
        self.diagram_generator = DiagramGenerator()
        self.repo_loader = RepoLoader()
        
        # Инициализация LangGraph
        self.workflow = self._create_workflow()
    
    def _create_workflow(self):
        """
        Создает граф workflow для анализа проекта
        """
        # Определяем узлы графа
        def load_repository(state: Dict[str, Any]) -> Dict[str, Any]:
            """Загружает репозиторий"""
            repo_url = state.get("repo_url")
            username = state.get("username")
            password = state.get("password")
            
            loader = RepoLoader(username=username, password=password)
            repo_path = loader.clone_repo(repo_url)
            
            updated_state = state.copy()
            updated_state.update({
                "repo_path": repo_path, 
                "repo_info": loader.get_repo_info(repo_path)
            })
            return updated_state
        
        def analyze_codebase(state: Dict[str, Any]) -> Dict[str, Any]:
            """Анализирует кодовую базу"""
            repo_path = state.get("repo_path")
            analysis_result = self.java_analyzer.analyze_project_structure(repo_path)
            
            updated_state = state.copy()
            updated_state.update({"code_analysis": analysis_result})
            return updated_state
        
        def generate_meta_description(state: Dict[str, Any]) -> Dict[str, Any]:
            """Генерирует метаописание проекта"""
            code_analysis = state.get("code_analysis", {})
            repo_info = state.get("repo_info", {})
            
            # Извлекаем ключевые элементы для метаописания
            project_name = repo_info.get("name", "Unknown")
            technology_stack = ["Java"]
            
            # Добавляем обнаруженные пакеты и классы в стек технологий
            packages = code_analysis.get("all_packages", [])
            classes = code_analysis.get("all_classes", [])
            
            # Определяем назначение и функциональность на основе анализа
            purpose = "Java application"
            functionality = "Contains various Java classes and packages"
            
            # Определяем точки входа
            entry_points = [cls for cls in classes if "main" in cls.lower() or "controller" in cls.lower()]
            
            meta_description = ProjectMetaDescription(
                project_name=project_name,
                technology_stack=technology_stack + [pkg.replace('package ', '').replace(';', '') for pkg in packages],
                purpose=purpose,
                functionality=functionality,
                entry_points=entry_points
            )
            
            updated_state = state.copy()
            updated_state.update({"meta_description": meta_description})
            return updated_state
        
        def generate_diagrams(state: Dict[str, Any]) -> Dict[str, Any]:
            """Генерирует диаграммы"""
            code_analysis = state.get("code_analysis", {})
            
            component_diagram = self.diagram_generator.generate_component_diagram(code_analysis)
            sequence_diagram = self.diagram_generator.generate_sequence_diagram(code_analysis)
            
            updated_state = state.copy()
            updated_state.update({
                "component_diagram": component_diagram,
                "sequence_diagram": sequence_diagram
            })
            return updated_state
        
        def generate_openapi_spec(state: Dict[str, Any]) -> Dict[str, Any]:
            """Пытается сгенерировать OpenAPI спецификацию"""
            # В реальной реализации здесь будет логика поиска и анализа REST контроллеров
            # Пока возвращаем заглушку
            
            from src.models.project_description import OpenAPISpecification
            openapi_spec = OpenAPISpecification(
                description="No OpenAPI specification found or generated"
            )
            
            updated_state = state.copy()
            updated_state.update({"openapi_specification": openapi_spec})
            return updated_state
        
        def compile_result(state: Dict[str, Any]) -> Dict[str, Any]:
            """Собирает все результаты в единый объект"""
            meta_description = state.get("meta_description")
            component_diagram = state.get("component_diagram")
            sequence_diagram = state.get("sequence_diagram")
            openapi_specification = state.get("openapi_specification")
            
            result = ProjectAnalysisResult(
                meta_description=meta_description,
                component_diagram=component_diagram,
                sequence_diagram=sequence_diagram,
                openapi_specification=openapi_specification
            )
            
            updated_state = state.copy()
            updated_state.update({"final_result": result})
            return updated_state
        
        # Создаем граф
        workflow = StateGraph(dict)
        
        # Добавляем узлы
        workflow.add_node("load_repository", load_repository)
        workflow.add_node("analyze_codebase", analyze_codebase)
        workflow.add_node("generate_meta_description", generate_meta_description)
        workflow.add_node("generate_diagrams", generate_diagrams)
        workflow.add_node("generate_openapi_spec", generate_openapi_spec)
        workflow.add_node("compile_result", compile_result)
        
        # Добавляем ребра - последовательное выполнение для избежания конфликта состояний
        workflow.add_edge(START, "load_repository")
        workflow.add_edge("load_repository", "analyze_codebase")
        workflow.add_edge("analyze_codebase", "generate_meta_description")
        workflow.add_edge("generate_meta_description", "generate_diagrams")
        workflow.add_edge("generate_diagrams", "generate_openapi_spec")
        workflow.add_edge("generate_openapi_spec", "compile_result")
        workflow.add_edge("compile_result", END)
        
        return workflow.compile()
    
    async def analyze_project(self, repo_url: str, username: str = None, password: str = None) -> ProjectAnalysisResult:
        """
        Запускает анализ проекта
        """
        inputs = {
            "repo_url": repo_url,
            "username": username,
            "password": password
        }
        
        result = await self.workflow.ainvoke(inputs)
        
        return result["final_result"]