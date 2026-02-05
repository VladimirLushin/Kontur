from typing import Dict, Any, List
from src.models.project_description import ComponentDiagram, SequenceDiagram


class DiagramGenerator:
    """
    Генератор диаграмм в формате Mermaid
    """
    
    def generate_component_diagram(self, project_structure: Dict[str, Any]) -> ComponentDiagram:
        """
        Генерирует компонентную диаграмму на основе структуры проекта
        """
        mermaid_code = "```mermaid\ncomponentDiagram\n"
        
        # Получаем уникальные пакеты и классы
        packages = project_structure.get('all_packages', [])
        classes = project_structure.get('all_classes', [])
        
        # Создаем компоненты для пакетов
        for pkg in packages:
            pkg_name = pkg.replace('package ', '').replace(';', '')
            mermaid_code += f"    component [{pkg_name}] as {pkg_name.replace('.', '_')}\n"
        
        # Создаем компоненты для основных классов
        for cls in classes[:10]:  # Ограничиваем количество классов для читаемости
            mermaid_code += f"    component [{cls}] as {cls}\n"
        
        # Добавляем связи между компонентами (упрощенно)
        if packages and classes:
            pkg_name = packages[0].replace('package ', '').replace(';', '').replace('.', '_')
            cls_name = classes[0] if classes else "MainClass"
            mermaid_code += f"    {pkg_name} -- {cls_name} : contains\n"
        
        mermaid_code += "```"
        
        description = f"Component diagram showing {len(packages)} packages and {len(classes)} classes"
        
        return ComponentDiagram(
            mermaid_code=mermaid_code,
            description=description
        )
    
    def generate_sequence_diagram(self, project_structure: Dict[str, Any]) -> SequenceDiagram:
        """
        Генерирует диаграмму последовательности на основе методов и вызовов
        """
        mermaid_code = "```mermaid\nsequenceDiagram\n"
        
        # Получаем уникальные методы
        methods = project_structure.get('all_methods', [])
        classes = project_structure.get('all_classes', [])[:5]  # Ограничиваем количество классов
        
        if not classes:
            classes = ['MainClass']
        
        # Создаем участников диаграммы (классы)
        for cls in classes:
            mermaid_code += f"    participant {cls}\n"
        
        # Добавляем простые вызовы между классами
        if len(classes) > 1:
            for i in range(len(classes)-1):
                mermaid_code += f"    {classes[i]}->>+{classes[i+1]}: callMethod()\n"
                mermaid_code += f"    {classes[i+1]}-->>-{classes[i]}: returnValue()\n"
        else:
            # Если только один класс, добавляем внутренние вызовы
            for i, method in enumerate(methods[:3]):
                mermaid_code += f"    {classes[0]}->>{classes[0]}: {method}()\n"
        
        mermaid_code += "```"
        
        description = f"Sequence diagram showing interactions between {len(classes)} classes"
        
        return SequenceDiagram(
            mermaid_code=mermaid_code,
            description=description
        )