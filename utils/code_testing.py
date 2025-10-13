"""Code testing utilities"""
import sys
from io import StringIO


def test_code(code, test_input='', expected_output=''):
    """
    Test code with simple input/output comparison.
    
    Args:
        code: Python code string to execute
        test_input: Input string (for input() function)
        expected_output: Expected output string
        
    Returns:
        Dictionary with 'passed', 'output', and optional 'error' keys
    """
    try:
        # Capture stdout
        old_stdout = sys.stdout
        old_stdin = sys.stdin
        sys.stdout = StringIO()
        
        # Mock input if provided
        if test_input:
            sys.stdin = StringIO(test_input)
        
        # Execute the code
        namespace = {}
        exec(code, namespace)
        
        # Get output
        output = sys.stdout.getvalue().strip()
        sys.stdout = old_stdout
        sys.stdin = old_stdin
        
        # Compare output
        expected = expected_output.strip()
        passed = output == expected
        
        return {
            'passed': passed,
            'output': output,
            'expected': expected
        }
        
    except Exception as e:
        sys.stdout = old_stdout
        sys.stdin = old_stdin
        return {
            'passed': False,
            'output': '',
            'error': str(e)
        }


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
