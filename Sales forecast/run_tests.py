"""
Test runner script - Voert alle unit tests uit en toont resultaten
"""
import unittest
import sys
import os

# Voeg parent directory toe aan path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


def run_all_tests():
    """Voer alle unit tests uit en toon samenvatting"""
    
    print("\n" + "=" * 70)
    print("  SALES FORECAST SIMULATIE - UNIT TEST RUNNER")
    print("=" * 70 + "\n")
    
    # Discover en run alle tests
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests met verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print samenvatting
    print("\n" + "=" * 70)
    print("  TEST SAMENVATTING")
    print("=" * 70)
    print(f"  Totaal tests uitgevoerd: {result.testsRun}")
    print(f"  ✓ Geslaagd: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  ✗ Gefaald: {len(result.failures)}")
    print(f"  ⚠ Errors: {len(result.errors)}")
    print("=" * 70 + "\n")
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit_code = run_all_tests()
    sys.exit(exit_code)
