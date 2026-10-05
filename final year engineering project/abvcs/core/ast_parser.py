"""
Static AST parsing engine for detecting code structure changes.
"""

import ast
from typing import List, Dict, Set, Tuple, Optional


class ASTAnalyzer:
    """Analyzes Python code structural units and function definitions."""

    @staticmethod
    def extract_top_level_symbols(source_code: str) -> Dict[str, List[str]]:
        """Extracts top-level functions, classes, and async functions from source."""
        symbols = {
            "functions": [],
            "classes": [],
            "async_functions": []
        }
        try:
            tree = ast.parse(source_code)
            for node in tree.body:
                if isinstance(node, ast.FunctionDef):
                    symbols["functions"].append(node.name)
                elif isinstance(node, ast.AsyncFunctionDef):
                    symbols["async_functions"].append(node.name)
                elif isinstance(node, ast.ClassDef):
                    symbols["classes"].append(node.name)
        except SyntaxError:
            # Code is in mid-edit state with syntax issues
            pass
        return symbols

    @staticmethod
    def check_syntax(source_code: str) -> Tuple[bool, Optional[str]]:
        """Verifies if the code is syntactically valid."""
        try:
            ast.parse(source_code)
            return True, None
        except SyntaxError as e:
            return False, f"Line {e.lineno}: {e.msg}"
