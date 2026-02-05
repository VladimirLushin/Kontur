"""
Java source code analyzer using AST parsing
"""
import os
import ast
import javalang
from typing import List, Dict, Any, Optional
from pathlib import Path


class JavaAnalyzer:
    """Analyzes Java source code to extract structure and relationships"""
    
    def __init__(self):
        pass
    
    def analyze_project(self, project_path: str) -> Dict[str, Any]:
        """
        Analyze an entire Java project
        
        Args:
            project_path: Path to the Java project directory
            
        Returns:
            Dictionary containing project analysis results
        """
        analysis_result = {
            'packages': {},
            'classes': {},
            'interfaces': {},
            'dependencies': [],
            'entry_points': []
        }
        
        java_files = self._find_java_files(project_path)
        
        for file_path in java_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = javalang.parse.parse(content)
                
                # Extract package information
                package_info = self._extract_package_info(tree)
                if package_info:
                    pkg_name = package_info['name']
                    if pkg_name not in analysis_result['packages']:
                        analysis_result['packages'][pkg_name] = {
                            'files': [],
                            'classes': [],
                            'interfaces': []
                        }
                    analysis_result['packages'][pkg_name]['files'].append(file_path)
                
                # Extract class and interface information
                classes, interfaces = self._extract_types(tree, file_path)
                
                for cls in classes:
                    class_key = f"{package_info['name']}.{cls['name']}" if package_info else cls['name']
                    analysis_result['classes'][class_key] = cls
                    if package_info:
                        analysis_result['packages'][package_info['name']]['classes'].append(cls['name'])
                
                for iface in interfaces:
                    iface_key = f"{package_info['name']}.{iface['name']}" if package_info else iface['name']
                    analysis_result['interfaces'][iface_key] = iface
                    if package_info:
                        analysis_result['packages'][package_info['name']]['interfaces'].append(iface['name'])
                
                # Extract dependencies
                file_deps = self._extract_dependencies(tree, package_info['name'] if package_info else '')
                analysis_result['dependencies'].extend(file_deps)
                
                # Find potential entry points
                entry_points = self._find_entry_points(tree, file_path)
                analysis_result['entry_points'].extend(entry_points)
                
            except Exception as e:
                print(f"Error analyzing file {file_path}: {str(e)}")
                continue
        
        return analysis_result
    
    def _find_java_files(self, directory: str) -> List[str]:
        """Find all Java files in a directory recursively"""
        java_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.java'):
                    java_files.append(os.path.join(root, file))
        return java_files
    
    def _extract_package_info(self, tree: javalang.ast.Node) -> Optional[Dict[str, str]]:
        """Extract package information from Java AST"""
        if hasattr(tree, 'package') and tree.package:
            return {
                'name': tree.package.name,
                'documentation': getattr(tree.package, 'documentation', None)
            }
        return None
    
    def _extract_types(self, tree: javalang.ast.Node, file_path: str) -> tuple[List[Dict], List[Dict]]:
        """Extract classes and interfaces from Java AST"""
        classes = []
        interfaces = []
        
        for path, node in tree.filter(javalang.tree.ClassDeclaration):
            class_info = {
                'name': node.name,
                'file_path': file_path,
                'modifiers': [m.value for m in node.modifiers] if hasattr(node, 'modifiers') else [],
                'extends': node.extends.name if node.extends else None,
                'implements': [imp.name for imp in node.implements] if node.implements else [],
                'methods': [],
                'fields': []
            }
            
            # Extract methods
            for item in node.body:
                if isinstance(item, javalang.tree.MethodDeclaration):
                    method_info = {
                        'name': item.name,
                        'return_type': str(item.return_type) if item.return_type else 'void',
                        'modifiers': [m.value for m in item.modifiers] if hasattr(item, 'modifiers') else [],
                        'parameters': [{'name': p.name, 'type': str(p.type)} for p in item.parameters]
                    }
                    class_info['methods'].append(method_info)
                
                elif isinstance(item, javalang.tree.FieldDeclaration):
                    field_info = {
                        'name': item.declarators[0].name if item.declarators else '',
                        'type': str(item.type),
                        'modifiers': [m.value for m in item.modifiers] if hasattr(item, 'modifiers') else []
                    }
                    class_info['fields'].append(field_info)
            
            classes.append(class_info)
        
        for path, node in tree.filter(javalang.tree.InterfaceDeclaration):
            interface_info = {
                'name': node.name,
                'file_path': file_path,
                'modifiers': [m.value for m in node.modifiers] if hasattr(node, 'modifiers') else [],
                'extends': [ext.name for ext in node.extends] if node.extends else [],
                'methods': []
            }
            
            # Extract methods from interface
            for item in node.body:
                if isinstance(item, javalang.tree.MethodDeclaration):
                    method_info = {
                        'name': item.name,
                        'return_type': str(item.return_type) if item.return_type else 'void',
                        'modifiers': [m.value for m in item.modifiers] if hasattr(item, 'modifiers') else []
                    }
                    interface_info['methods'].append(method_info)
            
            interfaces.append(interface_info)
        
        return classes, interfaces
    
    def _extract_dependencies(self, tree: javalang.ast.Node, current_package: str) -> List[Dict[str, str]]:
        """Extract dependencies from imports and type references"""
        dependencies = []
        
        # Extract import dependencies
        for imp in tree.imports:
            import_path = imp.path
            if not import_path.startswith('java.') and not import_path.startswith('javax.'):
                dependencies.append({
                    'type': 'import',
                    'from_package': current_package,
                    'to_package': '.'.join(import_path.split('.')[:-1]),
                    'target': import_path
                })
        
        # TODO: Extract type reference dependencies
        # This would involve traversing the AST to find type references that might indicate dependencies
        
        return dependencies
    
    def _find_entry_points(self, tree: javalang.ast.Node, file_path: str) -> List[Dict[str, Any]]:
        """Find potential entry points like main methods"""
        entry_points = []
        
        for path, node in tree.filter(javalang.tree.MethodDeclaration):
            if node.name == 'main' and 'public' in [m.value for m in node.modifiers] and 'static' in [m.value for m in node.modifiers]:
                # Check if it's a valid main method signature
                if len(node.parameters) == 1:
                    param = node.parameters[0]
                    if hasattr(param.type, 'name') and param.type.name == 'String' and param.type.dimensions:
                        class_path = file_path  # Simplified - in reality would need to extract class name
                        entry_points.append({
                            'type': 'main_method',
                            'class': self._get_class_containing_main(tree, node),
                            'file_path': file_path
                        })
        
        return entry_points
    
    def _get_class_containing_main(self, tree: javalang.ast.Node, main_node: javalang.tree.MethodDeclaration) -> Optional[str]:
        """Get the class name containing the main method"""
        # Find the parent class of the main method
        for path, node in tree.filter(javalang.tree.ClassDeclaration):
            for item in node.body:
                if item == main_node:
                    return node.name
        return None