import asyncio
import os
from dotenv import load_dotenv
from src.agents.project_analyzer_agent import ProjectAnalyzerAgent

# Загружаем переменные окружения
load_dotenv()

async def main():
    # Получаем API ключ из переменных окружения
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables")
    
    # Создаем экземпляр агента
    agent = ProjectAnalyzerAgent(api_key=api_key)
    
    # URL репозитория для анализа (замените на нужный вам репозиторий)
    repo_url = "https://github.com/spring-projects/spring-petclinic.git"  # Пример Java-проекта
    
    # Аутентификационные данные (если нужны)
    username = os.getenv("GITHUB_USERNAME")
    password = os.getenv("GITHUB_TOKEN")  # Используйте токен вместо пароля
    
    try:
        print(f"Starting analysis of repository: {repo_url}")
        result = await agent.analyze_project(repo_url, username, password)
        
        print("\n=== PROJECT ANALYSIS RESULT ===")
        print(f"Project Name: {result.meta_description.project_name}")
        print(f"Purpose: {result.meta_description.purpose}")
        print(f"Functionality: {result.meta_description.functionality}")
        print(f"Technology Stack: {', '.join(result.meta_description.technology_stack)}")
        print(f"Entry Points: {', '.join(result.meta_description.entry_points)}")
        
        print("\n=== COMPONENT DIAGRAM ===")
        print(result.component_diagram.mermaid_code)
        print(f"Description: {result.component_diagram.description}")
        
        print("\n=== SEQUENCE DIAGRAM ===")
        print(result.sequence_diagram.mermaid_code)
        print(f"Description: {result.sequence_diagram.description}")
        
        print("\n=== OPENAPI SPECIFICATION ===")
        print(f"Description: {result.openapi_specification.description}")
        
    except Exception as e:
        print(f"Error during analysis: {e}")

if __name__ == "__main__":
    asyncio.run(main())