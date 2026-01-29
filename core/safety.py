import ast


class SafetyChecker:
    FORBIDDEN_IMPORTS = {
        'os', 'subprocess', 'sys', 'socket', 
        'requests', 'random', 'secrets', 'shutil',
        'http', 'urllib', 'ftplib', 'telnetlib'
    }
    
    FORBIDDEN_CALLS = {
        'eval', 'exec', 'open', 'compile', 
        '__import__', 'getattr', 'setattr',
        'delattr', 'globals', 'locals'
    }
    
    def check(self, code: str) -> dict:
        """Check if generated code is safe to execute"""
        issues = []
        
        # Try to parse
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {'safe': False, 'issues': [f'Syntax error: {e}']}
        
        # Walk through all nodes
        for node in ast.walk(tree):
            # Check imports: import os
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in self.FORBIDDEN_IMPORTS:
                        issues.append(f'Forbidden import: {alias.name}')
            
            # Check from imports: from os import path
            if isinstance(node, ast.ImportFrom):
                if node.module:
                    root_module = node.module.split('.')[0]
                    if root_module in self.FORBIDDEN_IMPORTS:
                        issues.append(f'Forbidden import: {node.module}')
            
            # Check function calls: eval(), exec()
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in self.FORBIDDEN_CALLS:
                        issues.append(f'Forbidden call: {node.func.id}()')
        
        return {
            'safe': len(issues) == 0,
            'issues': issues
        }


# Test it
if __name__ == "__main__":
    checker = SafetyChecker()
    
    print("=== Testing Safety Checker ===\n")
    
    # Test 1: Safe code
    safe_code = """
def calculate(x):
    return x * 2

def main():
    return calculate(5)
"""
    result = checker.check(safe_code)
    print(f"1. Safe code: {result}")
    
    # Test 2: Forbidden import
    unsafe_import = """
import os
os.system("ls")
"""
    result = checker.check(unsafe_import)
    print(f"2. Unsafe import: {result}")
    
    # Test 3: Forbidden from import
    unsafe_from = """
from subprocess import call
call(["ls"])
"""
    result = checker.check(unsafe_from)
    print(f"3. Unsafe from import: {result}")
    
    # Test 4: Forbidden call
    unsafe_call = """
user_input = "2 + 2"
result = eval(user_input)
"""
    result = checker.check(unsafe_call)
    print(f"4. Unsafe call: {result}")
    
    # Test 5: Syntax error
    bad_syntax = """
def broken(
    return x
"""
    result = checker.check(bad_syntax)
    print(f"5. Syntax error: {result}")