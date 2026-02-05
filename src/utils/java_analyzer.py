import ast
import os
from typing import List, Dict, Any, Optional
from pathlib import Path


class JavaAnalyzer:
    """
    Анализатор Java-кода с использованием AST-деревьев
    """
    
    def __init__(self):
        pass
    
    def find_java_files(self, project_path: str) -> List[str]:
        """
        Находит все Java файлы в проекте
        """
        java_files = []
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith('.java'):
                    java_files.append(os.path.join(root, file))
        return java_files
    
    def extract_class_info(self, java_file_path: str) -> Dict[str, Any]:
        """
        Извлекает информацию о классе из Java файла
        Пока заглушка, так как Python не может напрямую разбирать Java AST
        """
        # TODO: Реализовать полноценный парсер Java с помощью ANTLR или другого инструмента
        class_info = {
            'file_path': java_file_path,
            'classes': [],
            'methods': [],
            'imports': [],
            'interfaces': [],
            'packages': []
        }
        
        # Простое извлечение базовой информации через регулярные выражения
        try:
            with open(java_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Извлечение импортов
                import_lines = [line.strip() for line in content.split('\n') if line.strip().startswith('import ')]
                class_info['imports'] = import_lines
                
                # Извлечение пакета
                package_lines = [line.strip() for line in content.split('\n') if line.strip().startswith('package ')]
                if package_lines:
                    class_info['packages'] = package_lines
                
                # Извлечение классов и методов (простая эвристика)
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if ' class ' in line and '{' in line:
                        class_name = line.split(' class ')[1].split('{')[0].strip().split()[0]
                        class_info['classes'].append(class_name)
                    elif ('public ' in line or 'private ' in line or 'protected ' in line) and '(' in line and ')' in line:
                        method_parts = line.split('(')[0].split()
                        if len(method_parts) >= 2:
                            method_name = method_parts[-1]
                            class_info['methods'].append(method_name)
                            
        except Exception as e:
            print(f"Error analyzing {java_file_path}: {e}")
            
        return class_info
    
    def analyze_project_structure(self, project_path: str) -> Dict[str, Any]:
        """
        Анализирует структуру всего Java-проекта
        """
        structure = {
            'project_path': project_path,
            'java_files': [],
            'all_classes': [],
            'all_methods': [],
            'all_imports': [],
            'all_packages': [],
            'directory_structure': {}
        }
        
        java_files = self.find_java_files(project_path)
        structure['java_files'] = java_files
        
        for java_file in java_files:
            class_info = self.extract_class_info(java_file)
            structure['all_classes'].extend(class_info['classes'])
            structure['all_methods'].extend(class_info['methods'])
            structure['all_imports'].extend(class_info['imports'])
            structure['all_packages'].extend(class_info['packages'])
            
        # Уникальные значения
        structure['all_classes'] = list(set(structure['all_classes']))
        structure['all_methods'] = list(set(structure['all_methods']))
        structure['all_imports'] = list(set(structure['all_imports']))
        structure['all_packages'] = list(set(structure['all_packages']))
        
        # Получение директорией структуры
        for root, dirs, files in os.walk(project_path):
            rel_path = os.path.relpath(root, project_path)
            structure['directory_structure'][rel_path] = {
                'dirs': dirs,
                'files': [f for f in files if f.endswith('.java')]
            }
        
        return structure