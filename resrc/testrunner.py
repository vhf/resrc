"""Custom test runner for the project."""
from django_coverage.coverage_runner import CoverageRunner
from django_nose import NoseTestSuiteRunner

class NoseCoverageTestRunner(CoverageRunner, NoseTestSuiteRunner):
    """Custom test runner that uses nose and coverage"""
    pass
