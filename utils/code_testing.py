"""Code testing utilities"""
import sys
from io import StringIO


# Global variables for loop tracking
_loop_count = 0
_loop_limit = 100000  # Maximum iterations allowed


def _trace_function(frame, event, arg):
    """
    Trace function to count loop iterations and detect infinite loops.
    This uses sys.settrace to monitor code execution.
    """
    global _loop_count
    
    if event == 'line':
        _loop_count += 1
        if _loop_count > _loop_limit:
            raise RuntimeError(f"Infinite loop detected: exceeded {_loop_limit} iterations")
    
    return _trace_function


def _reset_loop_counter():
    """Reset the global loop counter."""
    global _loop_count
    _loop_count = 0


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


def extract_function_name(code):
    """
    Extract the first function name from Python code.
    
    Args:
        code: Python code string
        
    Returns:
        Function name as string, or None if not found
    """
    import re
    match = re.search(r'def\s+(\w+)\s*\(', code)
    return match.group(1) if match else None


def run_code_tests(code, test_cases):
    """
    Run code against test cases.
    
    Args:
        code: Python code string to test
        test_cases: List of test case dictionaries with 'input' and 'expected' keys
                   (optionally with 'function' key; if missing, extracts from code)
        
    Returns:
        Dictionary with 'passed', 'total', 'errors', and 'details' keys
    """
    passed = 0
    total = len(test_cases)
    errors = 0
    details = []
    
    # Extract function name from code if not specified in test cases
    func_name = None
    if test_cases and 'function' not in test_cases[0]:
        func_name = extract_function_name(code)
    
    for test in test_cases:
        try:
            # Reset loop counter for each test
            _reset_loop_counter()
            
            # Capture stdout
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            old_trace = sys.gettrace()
            
            # Set up trace function to detect infinite loops
            sys.settrace(_trace_function)
            
            try:
                # Create a namespace for execution
                namespace = {}
                exec(code, namespace)
                
                # Get the function to test
                target_func_name = test.get('function', func_name)
                if target_func_name is None:
                    raise Exception("Could not determine function name from code")
                
                if target_func_name not in namespace:
                    raise Exception(f"Function '{target_func_name}' not found")
                
                func = namespace[target_func_name]
                
                # Run the test
                result = func(*test['input'])
                output = sys.stdout.getvalue()
                
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
            finally:
                # Restore trace function and stdout
                sys.settrace(old_trace)
                sys.stdout = old_stdout
                
        except RuntimeError as e:
            # Infinite loop or other runtime error
            if "Infinite loop" in str(e):
                sys.stdout = old_stdout
                errors += 1
                details.append({
                    'input': test.get('input', []),
                    'expected': test.get('expected', None),
                    'actual': None,
                    'passed': False,
                    'error': 'Infinite loop detected - code exceeded iteration limit'
                })
            else:
                sys.stdout = old_stdout
                errors += 1
                details.append({
                    'input': test.get('input', []),
                    'expected': test.get('expected', None),
                    'actual': None,
                    'passed': False,
                    'error': str(e)
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
