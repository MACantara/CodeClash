"""Code testing utilities"""
import sys
from io import StringIO


def run_code_tests(code, test_cases):
    """
    Run code against test cases.
    
    Args:
        code: Python code string to test
        test_cases: List of test case dictionaries with 'function', 'input', and 'expected' keys
        
    Returns:
        Dictionary with 'passed', 'total', 'errors', and 'details' keys
    """
    passed = 0
    total = len(test_cases)
    errors = 0
    details = []
    
    for test in test_cases:
        try:
            # Capture stdout
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            # Create a namespace for execution
            namespace = {}
            exec(code, namespace)
            
            # Get the function to test (assume it's the first function defined)
            func_name = test['function']
            if func_name not in namespace:
                raise Exception(f"Function '{func_name}' not found")
            
            func = namespace[func_name]
            
            # Run the test
            result = func(*test['input'])
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            # Check result
            if result == test['expected']:
                passed += 1
                details.append({
                    'input': test['input'],
                    'expected': test['expected'],
                    'actual': result,
                    'passed': True
                })
            else:
                errors += 1
                details.append({
                    'input': test['input'],
                    'expected': test['expected'],
                    'actual': result,
                    'passed': False,
                    'error': 'Output mismatch'
                })
        except Exception as e:
            sys.stdout = old_stdout
            errors += 1
            details.append({
                'input': test.get('input', []),
                'expected': test.get('expected', None),
                'actual': None,
                'passed': False,
                'error': str(e)
            })
    
    return {
        'passed': passed,
        'total': total,
        'errors': errors,
        'details': details
    }
