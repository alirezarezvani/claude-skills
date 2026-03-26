#!/usr/bin/env python3
"""
Test Runner for skill-tester Package

Run all tests or specific test modules.

Usage:
    python run_tests.py              # Run all tests
    python run_tests.py validator    # Run only validator tests
    python run_tests.py tester       # Run only script tester tests
    python run_tests.py scorer       # Run only quality scorer tests
    python run_tests.py integration  # Run only integration tests
"""

import sys
import unittest
from pathlib import Path

# Test modules
TEST_MODULES = {
    "validator": "test_skill_validator",
    "tester": "test_script_tester", 
    "scorer": "test_quality_scorer",
    "integration": "test_integration"
}


def run_tests(modules=None):
    """Run the specified test modules."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    test_dir = Path(__file__).parent
    
    if modules:
        for module in modules:
            if module in TEST_MODULES:
                test_module = TEST_MODULES[module]
            elif module in TEST_MODULES.values():
                test_module = module
            else:
                print(f"Unknown test module: {module}")
                continue
                
            # Load tests from the module
            tests = loader.discover(test_dir, pattern=f"{test_module}.py")
            suite.addTests(tests)
    else:
        # Run all tests
        suite = loader.discover(test_dir, pattern="test_*.py")
    
    # Run with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        modules = sys.argv[1:]
    else:
        modules = None
        
    exit_code = run_tests(modules)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()