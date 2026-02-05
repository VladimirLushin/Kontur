"""Java source code parser using javalang AST."""
import javalang
from typing import Dict, List, Optional


class JavaParser:
    """Parse Java source code to extract structural information."""
    
    def __init__(self):
        pass
    
    def parse_file(self, file_content: str) -> Optional[javalang.ast.Node]:
        """Parse a Java file content and return the AST."""
        try:
            tree = javalang.parse.parse(file_content)
            return tree
        except Exception as e:
            print(f"Error parsing Java file: {e}")
            return None
    
    def extract_classes_and_interfaces(self, tree: javalang.ast.Node) -> List[Dict]:
        """Extract class and interface definitions from the AST."""
        classes = []
        
        if tree:
            for path, node in tree.filter(javalang.tree.ClassDeclaration):
                class_info = {
                    'name': node.name,
                    'methods': [],
                    'fields': [],
                    'extends': node.extends.name if node.extends else None,
                    'implements': [imp.name for imp in node.implements] if node.implements else []
                }
                
                # Extract methods
                for item in node.body:
                    if isinstance(item, javalang.tree.MethodDeclaration):
                        method_info = {
                            'name': item.name,
                            'return_type': str(item.return_type) if item.return_type else 'void',
                            'parameters': [(param.type.name, param.name) for param in item.parameters],
                            'modifiers': list(item.modifiers)
                        }
                        class_info['methods'].append(method_info)
                    
                    # Extract fields
                    elif isinstance(item, javalang.tree.FieldDeclaration):
                        for decl in item.declarators:
                            field_info = {
                                'name': decl.name,
                                'type': str(item.type),
                                'modifiers': list(item.modifiers)
                            }
                            class_info['fields'].append(field_info)
                
                classes.append(class_info)
            
            # Extract interfaces
            for path, node in tree.filter(javalang.tree.InterfaceDeclaration):
                interface_info = {
                    'name': node.name,
                    'methods': [],
                    'extends': [ext.name for ext in node.extends] if node.extends else [],
                    'fields': []
                }
                
                for item in node.body:
                    if isinstance(item, javalang.tree.MethodDeclaration):
                        method_info = {
                            'name': item.name,
                            'return_type': str(item.return_type) if item.return_type else 'void',
                            'parameters': [(param.type.name, param.name) for param in item.parameters]
                        }
                        interface_info['methods'].append(method_info)
                        
                    elif isinstance(item, javalang.tree.FieldDeclaration):
                        for decl in item.declarators:
                            field_info = {
                                'name': decl.name,
                                'type': str(item.type),
                                'modifiers': list(item.modifiers)
                            }
                            interface_info['fields'].append(field_info)
                
                classes.append(interface_info)
        
        return classes
    
    def extract_packages_and_imports(self, tree: javalang.ast.Node) -> Dict:
        """Extract package declaration and imports from the AST."""
        package_name = None
        imports = []
        
        if tree:
            # Extract package
            if tree.package:
                package_name = str(tree.package.name)
            
            # Extract imports
            for imp in tree.imports:
                imports.append(str(imp.path))
        
        return {
            'package': package_name,
            'imports': imports
        }